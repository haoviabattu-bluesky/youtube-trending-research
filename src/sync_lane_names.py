# -*- coding: utf-8 -*-
"""Tự đổi tên file data/title_intel/<lane>.json khi h2dev gán HANDLE chính thức trên tab NOTE.

Đọc-CHỈ-ĐỌC tab NOTE (không ghi gì vào Sheet) làm nguồn chân lý: cột B = link kênh (khớp channel_id
trong export_title_intel.CHDIR), cột G = NHẬN KÊNH, cột I = HANDLE. Khi HANDLE khác lane hiện tại
trong CHDIR và NHẬN KÊNH đã có giá trị (h2dev đã chính thức nhận kênh), xoá file JSON cũ (chỉ file
local do chính script này sinh ra, KHÔNG đụng Sheet) và sinh lại dưới tên mới.

Việc đổi tên là thao tác THUẦN CƠ HỌC (khớp chuỗi + ghi file) — không cần gọi Claude/LLM.

    py -3.13 -X utf8 src/sync_lane_names.py            # chạy 1 lần, in ra những gì đã đổi
    py -3.13 -X utf8 src/sync_lane_names.py --dry-run   # chỉ xem sẽ đổi gì, không ghi
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import gspread
from dotenv import load_dotenv
from google.oauth2.service_account import Credentials
import os

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from export_title_intel import CHDIR, OUT, from_channel_dna, save_chdir  # noqa: E402

SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
NOTE_RANGE = "A2:L200"


def read_note_rows() -> list[list[str]]:
    load_dotenv(ROOT / "config" / ".env")
    creds = Credentials.from_service_account_file(os.environ["GOOGLE_SHEETS_KEY"], scopes=SCOPES)
    sh = gspread.authorize(creds).open_by_key(os.environ["SHEET_ID"])
    return sh.worksheet("NOTE").get(NOTE_RANGE)


def find_handle(rows: list[list[str]], channel_id: str) -> tuple[str, str] | None:
    """Trả (handle, nhan_kenh) của dòng NOTE có channel_id khớp cột B, hoặc None."""
    for row in rows:
        b = row[1] if len(row) > 1 else ""
        if channel_id in b:
            g = row[6] if len(row) > 6 else ""
            i = row[8] if len(row) > 8 else ""
            return (i.strip(), g.strip())
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    rows = read_note_rows()
    changed = 0
    for key, (lane, data_rel, channel_ja, dna_rel, channel_id) in list(CHDIR.items()):
        found = find_handle(rows, channel_id)
        if not found:
            print(f"  [{key}] không thấy dòng NOTE khớp channel_id {channel_id} — bỏ qua")
            continue
        handle, nhan_kenh = found
        handle = re.sub(r"^@", "", handle)  # cột L ghi @handle, cột I có thể ghi trần — chấp nhận cả 2
        if not handle or not nhan_kenh:
            print(f"  [{key}] chưa có HANDLE hoặc chưa 'Đã nhận kênh' trên NOTE — giữ nguyên '{lane}'")
            continue
        if handle == lane:
            print(f"  [{key}] '{lane}' đã khớp HANDLE trên NOTE — không đổi")
            continue

        print(f"  [{key}] ĐỔI TÊN: '{lane}.json' -> '{handle}.json' (theo HANDLE tab NOTE)")
        if args.dry_run:
            changed += 1
            continue

        old_path = OUT / f"{lane}.json"
        if old_path.exists():
            old_path.unlink()
        CHDIR[key] = (handle, data_rel, channel_ja, dna_rel, channel_id)
        rec = from_channel_dna(key)
        rec["lane"] = handle
        rec["key"] = key
        import json
        (OUT / f"{handle}.json").write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
        save_chdir()
        changed += 1

    print(f"\n{'(dry-run) ' if args.dry_run else ''}{changed} lane đã đổi tên." if changed
          else "\nKhông có lane nào cần đổi tên.")


if __name__ == "__main__":
    main()
