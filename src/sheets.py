# -*- coding: utf-8 -*-
"""Ghi Google Sheet — CHỈ append/update, TUYỆT ĐỐI không xoá.

Sheet đích chứa dữ liệu thật của user ở tab GMAIL/NOTE. Mọi hàm đi qua
`_assert_allowed()`; module này KHÔNG gọi API xoá nào của gspread.
"""
from __future__ import annotations

import hashlib

import gspread
from google.oauth2.service_account import Credentials

from gapi import retry_api
from sheet_schema import (HEADERS, MAIN_TAB, TAB_PREFIX, SheetGuardError,
                          ShrinkGuard, _assert_allowed)

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

class SheetReporter:
    def __init__(self, sheet_id: str, key_path: str):
        creds = Credentials.from_service_account_file(key_path, scopes=SCOPES)
        self.sh = gspread.authorize(creds).open_by_key(sheet_id)

    # ---------- an toàn ----------
    def guard_snapshot(self) -> dict[str, str]:
        """Dấu vân tay của MỌI tab — gọi trước & sau để chứng minh không mất gì.

        Tab NGOÀI whitelist (dữ liệu thật của user) đọc TOÀN BỘ ô rồi băm: đếm cột A
        thôi là sót — GMAIL có 12 dòng trống cột A nhưng có dữ liệu ở cột khác, hai cách
        đếm ra 89 vs 101. Tab của tool thì chỉ cần đếm dòng.
        Vẫn 1 request nhờ values_batch_get.
        """
        titles = [ws.title for ws in retry_api(self.sh.worksheets)]
        ranges = [f"'{x}'!A:A" if (x == MAIN_TAB or x.startswith(TAB_PREFIX))
                  else f"'{x}'!A:Z" for x in titles]
        res = retry_api(self.sh.values_batch_get, ranges)
        out = {}
        for title, vr in zip(titles, res.get("valueRanges", [])):
            vals = vr.get("values", [])
            if title == MAIN_TAB or title.startswith(TAB_PREFIX):
                out[title] = f"{len(vals)} dòng"
            else:
                digest = hashlib.sha1(
                    repr(vals).encode("utf-8", "replace")).hexdigest()[:10]
                out[title] = f"{len(vals)} dòng/{digest}"
        return out

    def ensure_tab(self, tab: str, cols: int | None = None) -> gspread.Worksheet:
        _assert_allowed(tab)
        try:
            ws = retry_api(self.sh.worksheet, tab)
        except gspread.WorksheetNotFound:
            ws = retry_api(self.sh.add_worksheet, tab, rows=1000,
                           cols=cols or len(HEADERS[tab]) + 2)
        header = HEADERS[tab]
        first = retry_api(ws.get_values, "A1:1")
        cur = first[0] if first else []
        if not any(cur):
            retry_api(ws.update, values=[header], range_name="A1", value_input_option="RAW")
        elif [c.strip() for c in cur] == header[:len(cur)] and len(cur) < len(header):
            # phiên bản sau thêm cột ở CUỐI → cập nhật ô header, dữ liệu cũ giữ nguyên
            retry_api(ws.update, values=[header], range_name="A1", value_input_option="RAW")
        elif [c.strip() for c in cur[:len(header)]] != header:
            raise SheetGuardError(
                f"Tab '{tab}' có header khác mong đợi → từ chối ghi để bảo vệ dữ liệu.\n"
                f"  đang có : {cur[:len(header)]}\n  mong đợi: {header}")
        return ws

    # ---------- ghi ----------
    def append(self, tab: str, rows: list[list]) -> int:
        """Nối thêm vào cuối. Không bao giờ đụng dòng đã có."""
        if not rows:
            return 0
        ws = self.ensure_tab(tab)
        need = len(retry_api(ws.get_all_values)) + len(rows) + 10
        if need > ws.row_count:
            retry_api(ws.add_rows, need - ws.row_count)
        retry_api(ws.append_rows, rows, value_input_option="USER_ENTERED",
                  insert_data_option="INSERT_ROWS", table_range="A1")
        return len(rows)

    def upsert_by_key(self, tab: str, rows: list[list], key_col: int = 0) -> tuple[int, int]:
        """Cập nhật dòng đã có theo khoá, nối thêm dòng mới. KHÔNG xoá dòng nào.

        Dòng cũ không còn trong `rows` vẫn được giữ nguyên tại chỗ.
        """
        if not rows:
            return 0, 0
        ws = self.ensure_tab(tab)
        existing = retry_api(ws.get_all_values)
        index = {r[key_col]: i for i, r in enumerate(existing[1:], start=2)
                 if len(r) > key_col and r[key_col]}
        updates, appends = [], []
        width = len(HEADERS[tab])
        for r in rows:
            r = [("" if v is None else v) for v in r][:width]
            r += [""] * (width - len(r))
            pos = index.get(str(r[key_col]))
            if pos:
                updates.append({"range": f"A{pos}:{chr(64 + width)}{pos}", "values": [r]})
            else:
                appends.append(r)
        if updates:
            retry_api(ws.batch_update, updates, value_input_option="USER_ENTERED")
        if appends:
            need = len(existing) + len(appends) + 10
            if need > ws.row_count:
                retry_api(ws.add_rows, need - ws.row_count)
            retry_api(ws.append_rows, appends, value_input_option="USER_ENTERED",
                          insert_data_option="INSERT_ROWS", table_range="A1")
        return len(updates), len(appends)

    def write_daily_block(self, tab: str, rows: list[list], snap: str,
                          force: bool = False, expect: int | None = None) -> tuple[int, int]:
        """Ghi khối báo cáo của MỘT ngày. Chạy lại trong ngày thì GHI ĐÈ TẠI CHỖ khối cũ,
        không nhân đôi và cũng không xoá dòng nào.

        Nếu lượt chạy sau ra ít dòng hơn lượt trước, phần dư của khối cũ được GIỮ NGUYÊN
        (không xoá được theo quy tắc) — hàm trả về số dòng dư để caller cảnh báo.
        """
        if not rows:
            return 0, 0
        ws = self.ensure_tab(tab)
        existing = retry_api(ws.get_all_values)
        width = len(HEADERS[tab])
        mine = [i for i, r in enumerate(existing[1:], start=2) if r and r[0] == snap]
        # Một lượt chạy NHỎ (test vài keyword) không được phép đè mất báo cáo ĐẦY ĐỦ đã
        # ghi trước đó trong ngày. Đã dính thật: chạy thử 3 keyword xoá sạch top 28 dòng.
        # So với SỐ DÒNG MONG ĐỢI của cấu hình, không so với khối cũ: báo cáo cố tình
        # chắt lọc còn 10 dòng thì so với khối 150 dòng hôm trước sẽ chặn oan.
        bar = expect if expect is not None else len(mine)
        if mine and len(rows) < bar * 0.7 and not force:
            raise ShrinkGuard(len(rows), bar, tab)
        norm = []
        for r in rows:
            r = [("" if v is None else v) for v in r][:width]
            norm.append(r + [""] * (width - len(r)))

        updates = []
        for r, pos in zip(norm, mine):
            updates.append({"range": f"A{pos}:{chr(64 + width)}{pos}", "values": [r]})
        if updates:
            retry_api(ws.batch_update, updates, value_input_option="USER_ENTERED")
        rest = norm[len(mine):]
        if rest:
            need = len(existing) + len(rest) + 10
            if need > ws.row_count:
                retry_api(ws.add_rows, need - ws.row_count)
            retry_api(ws.append_rows, rest, value_input_option="USER_ENTERED",
                          insert_data_option="INSERT_ROWS", table_range="A1")
        leftover = mine[len(norm):]
        if leftover:
            self._mark_superseded(ws, leftover, snap)
        return len(rest), len(leftover)

    @staticmethod
    def _mark_superseded(ws, rows: list[int], snap: str) -> None:
        """Đánh dấu dòng thừa của khối cũ thay vì xoá (quy tắc cấm xoá).

        Chỉ sửa ô ngày ở cột A thành '<ngày> ⏹cũ' — KHÔNG xoá nội dung dòng. Nhờ vậy
        dòng vẫn đọc được, nhìn là biết đã bị thay thế, và lượt sau không còn nhận nhầm
        nó là khối của hôm nay.
        """
        retry_api(ws.batch_update,
                  [{"range": f"A{i}", "values": [[f"{snap} ⏹cũ"]]} for i in rows],
                  value_input_option="RAW")

    # ---------- đọc config ----------
    def read_config(self) -> dict:
        """Đọc tab TRD_CONFIG → {niche: {hl, gl, keywords[]}}. Trống thì trả {}."""
        ws = self.ensure_tab("TRD_CONFIG")
        rows = retry_api(ws.get_all_values)[1:]
        out: dict[str, dict] = {}
        for r in rows:
            r = (r + [""] * 6)[:6]
            niche, enabled, kw, hl, gl, _ = (c.strip() for c in r)
            if not niche or not kw or enabled.upper() in ("0", "FALSE", "NO", "OFF"):
                continue
            d = out.setdefault(niche, {"hl": hl or "ja", "gl": gl or "JP", "keywords": []})
            if kw not in d["keywords"]:
                d["keywords"].append(kw)
        return out

    def bootstrap_config(self, niches: dict) -> int:
        """Đổ config từ niches.yaml lên Sheet lần đầu (chỉ khi tab đang trống)."""
        ws = self.ensure_tab("TRD_CONFIG")
        if len(retry_api(ws.get_all_values)) > 1:
            return 0
        rows = [[name, "TRUE", kw, n.get("hl", "ja"), n.get("gl", "JP"), n.get("label", "")]
                for name, n in niches.items() for kw in n["keywords"]]
        return self.append("TRD_CONFIG", rows)
