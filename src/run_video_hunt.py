# -*- coding: utf-8 -*-
"""Video Hunt — mỗi ngày chọn đúng 2 video xuất sắc nhất/lane, ghi tab RESEARCH.

Khác run_daily.py (quét theo KÊNH): ở đây gom video của MỌI kênh theo tag chủ đề
1 lane, không quan tâm kênh đã biết hay chưa. Chấm điểm view/ngày, ưu tiên video mới.

  py -3.13 -X utf8 src/run_video_hunt.py --dry-run                 # xem, không ghi Sheet
  py -3.13 -X utf8 src/run_video_hunt.py --lane shinya_shiryoshitsu --dry-run
  py -3.13 -X utf8 src/run_video_hunt.py                           # chạy đủ, ghi RESEARCH
"""
from __future__ import annotations

import argparse
import os
import sys
import time
from pathlib import Path

import yaml
from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).parent))
import hunt_score as hs                                    # noqa: E402
import store                                                # noqa: E402
from enrich import Enricher                                 # noqa: E402
from gapi import retry_api                                   # noqa: E402
from hunt_tags import lane_done_titles, lane_keywords        # noqa: E402
from innertube import BotCheckError, InnerTube, ProxyError   # noqa: E402
from lockfile import RunLock                                 # noqa: E402
from proxy_pool import ProxyPool, load_proxies                # noqa: E402
import reup_filter                                            # noqa: E402
from sheet_schema import HEADERS                              # noqa: E402
from sheets import SheetReporter                             # noqa: E402
from ytapi import YouTubeAPI                                 # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / "config" / ".env")
LOG = lambda *a: print(*a, file=sys.stderr, flush=True)  # noqa: E731


def load_cfg() -> dict:
    with open(ROOT / "config" / "video_hunt.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f)


def discover_lane(it: InnerTube, kws: list[str], windows: list[str], pages: int,
                  name: str, pool: ProxyPool | None = None) -> dict[str, dict]:
    """Bot-check/lỗi proxy KHÔNG còn làm hỏng cả lane — nếu có pool thì đổi proxy
    và thử lại đúng lát đó 1 lần; hết proxy để đổi (hoặc không có pool) mới bỏ qua lát đó.
    """
    found: dict[str, dict] = {}
    for i, kw in enumerate(kws, 1):
        for w in windows:
            try:
                for row in it.search(kw, w, pages=pages):
                    found.setdefault(row["video_id"], row)
            except (BotCheckError, ProxyError) as e:
                cur = getattr(it._s, "proxies", {}).get("https")
                if pool:
                    if cur:
                        pool.mark_bad(cur)
                    nxt = pool.next()
                    if nxt:
                        LOG(f"  ! {kw}[{w}]: {type(e).__name__} → đổi proxy, thử lại 1 lần")
                        it.set_proxy(nxt)
                        try:
                            for row in it.search(kw, w, pages=pages):
                                found.setdefault(row["video_id"], row)
                            continue
                        except Exception as e2:
                            LOG(f"  ! {kw}[{w}] (sau đổi proxy): {type(e2).__name__} — bỏ qua lát này")
                            continue
                LOG(f"  ! {kw}[{w}]: {type(e).__name__} — không có proxy dự phòng, bỏ qua lát này")
            except Exception as e:
                LOG(f"  ! {kw}[{w}]: {type(e).__name__}")
        if i % 10 == 0:
            LOG(f"  [{name}] {i}/{len(kws)} tag → {len(found)} video")
    return found


def match_tags(title: str, kws: list[str]) -> list[str]:
    return [k for k in kws if k.replace(" ", "") in title.replace(" ", "")]


def video_cell(p: dict) -> str:
    """Ô chỉ chứa ĐÚNG link video — user chốt 2026-09-22 (bản trước nhét cả tiêu đề/số
    liệu/kênh vào ô, thừa; số liệu vẫn còn đủ trong `hunt_pick`/log nếu cần tra lại)."""
    return f"https://youtu.be/{p['video_id']}"


def run_lane(name: str, lcfg: dict, cfg: dict, api: YouTubeAPI | None,
            rep: SheetReporter, con, pool: ProxyPool | None = None) -> list[dict]:
    hl, gl = cfg.get("hl", "ja"), cfg.get("gl", "JP")
    kws = lane_keywords(rep, lcfg, cfg.get("stop_tags", []))
    LOG(f"[{name}] {len(kws)} từ khoá (tag cột F + seed)")
    if not kws:
        return []

    it = InnerTube(hl=hl, gl=gl, proxy_url=pool.next() if pool else None)
    found = discover_lane(it, kws, cfg["windows"], cfg["pages_per_kw"], name, pool)
    LOG(f"[{name}] {len(found)} video thô, parse_ok={it.parse_ok} parse_fail={it.parse_fail}")

    # sơ loại keyless trước khi tốn quota Data API
    rough = [r for r in found.values() if r["views_it"] >= cfg["min_views"]]
    LOG(f"[{name}] {len(rough)} video ≥{cfg['min_views']:,} view (thô)")
    if not rough:
        return []

    enr = Enricher(api, it)
    rows = enr.build_rows(rough, name)  # build_rows đã gắn sẵn niche=name, keyword khớp
    store.save_snapshot(con, rows)

    scored = hs.score_rows(rows, cfg)
    already = store.picked_video_ids(con, name)
    done_titles = lane_done_titles(rep, lcfg)
    non_jp = sum(1 for r in scored if not hs.is_japanese_title(r["title"]))
    live = sum(1 for r in scored if hs.is_live_stream(r["title"]))
    mismatch = sum(1 for r in scored if not hs.title_matches_pool(r["title"], kws))
    usable = hs.filter_rows(scored, cfg, already, done_titles, kws)
    LOG(f"[{name}] {len(usable)} video qua hết sàng lọc (loại: {non_jp} không có chữ Nhật, "
        f"{live} live-stream, {mismatch} tiêu đề không khớp từ khoá thật, "
        f"+ trùng lane/quá 30d/<10k/Shorts/trùng đề tài đã làm)")

    # Kiểm tra ĐỊNH DẠNG kênh — bước 3 của RESEARCH_PLAYBOOK ("loại kênh không clone
    # được") đã bị BỎ SÓT ở bản đầu, dẫn tới chọn nhầm kênh talk-show/phỏng vấn có
    # người thật xuất hiện (không dùng được cho kênh faceless). Chỉ gọi LLM cho nhóm
    # điểm cao nhất (rẻ, đủ dùng vì chỉ cần đúng top `pick_per_lane`).
    usable.sort(key=lambda r: r["score"], reverse=True)
    check_n = min(30, len(usable))
    to_check, rest = usable[:check_n], usable[check_n:]
    tags = reup_filter.classify(to_check, os.getenv("LLM_BASE_URL", ""),
                                os.getenv("LLM_API_KEY", ""), os.getenv("LLM_MODEL", ""))
    if tags:
        bad = {vid for vid, t in tags.items() if t.get("type") in ("VLOG_PERSON", "REUP")}
        good = [r for r in to_check if r["video_id"] not in bad]
        LOG(f"[{name}] LLM loại {len(bad)}/{len(to_check)} video (người thật xuất hiện/"
            f"dùng tư liệu có sẵn — không clone được cho kênh faceless)")
        usable = good + rest
    else:
        LOG(f"[{name}] bỏ qua bước kiểm định dạng kênh (thiếu LLM_API_KEY hoặc lỗi gọi model)")

    picks = hs.pick_top(usable, cfg["pick_per_lane"], cfg["distinct_channels"])
    for p in picks:
        p["reason"] = hs.reason_text(p, match_tags(p["title"], kws))
    return picks


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default="", help="mặc định: tất cả lane trong config")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--no-api", action="store_true")
    ap.add_argument("--no-proxy", action="store_true", help="bỏ qua config/proxies.txt, chạy IP thật")
    args = ap.parse_args()

    t0 = time.time()
    cfg = load_cfg()
    d = cfg["defaults"]
    key = os.getenv("YOUTUBE_API_KEY", "")
    api = None if (args.no_api or not key) else YouTubeAPI(key)
    proxy_urls = [] if args.no_proxy else load_proxies(ROOT / "config" / "proxies.txt")
    pool = ProxyPool(proxy_urls) if proxy_urls else None
    LOG(f"[proxy] {len(proxy_urls)} proxy trong pool" if pool else "[proxy] không dùng proxy (IP thật)")
    con = store.connect(ROOT / "data" / "trending.db")
    snap = store.today()

    rep = SheetReporter(d["sheet_id"], os.getenv("GOOGLE_SHEETS_KEY"))
    lane_tabs = [lc["tab"] for lc in cfg["lanes"].values()]
    before = rep.guard_snapshot()
    LOG(f"[guard] trước khi chạy: { {k: before[k] for k in before if k in lane_tabs or k in ('GMAIL', 'NOTE')} }")

    names = [n.strip() for n in args.lane.split(",") if n.strip()] or list(cfg["lanes"])
    n_ranks = d["pick_per_lane"]
    all_picks: dict[str, list[dict]] = {}
    for name in names:
        lcfg = cfg["lanes"][name]
        LOG(f"\n=== {name} — {lcfg.get('label', '')} ===")
        try:
            picks = run_lane(name, lcfg, d, api, rep, con, pool)
        except BotCheckError as e:
            LOG(f"!! BOT-CHECK ở lane {name}: {e} — bỏ qua lane này, giữ nguyên các lane khác")
            picks = []
        all_picks[name] = picks

    if args.dry_run:
        LOG("\n[dry-run] KHÔNG ghi Sheet. Kết quả từng lane:")
        for name in names:
            picks = all_picks[name]
            if not picks:
                LOG(f"\n--- {name} --- (không có video ≥10k/30d hôm nay)")
            for i, p in enumerate(picks, 1):
                LOG(f"\n--- {name} #{i} ---\n{video_cell(p)}")
    else:
        header = HEADERS[d["research_tab"]]
        # Chạy từng lane riêng lẻ (để publish ngay khi 1 lane xong) sẽ GHI ĐÈ MẤT các
        # lane/hạng KHÁC nếu chỉ đẩy dữ liệu của lane vừa chạy — phải đọc các dòng
        # (DATE, RANK) hôm nay đã có trên Sheet trước, giữ nguyên cột lane KHÁC.
        ws = rep.ensure_tab(d["research_tab"])
        existing = retry_api(ws.get_all_values)
        by_key: dict[tuple[str, str], list] = {}
        row_pos: dict[tuple[str, str], int] = {}
        for i, r in enumerate(existing[1:], start=2):
            if len(r) >= 2 and r[0] == snap:
                key = (r[0], r[1])
                by_key[key] = r
                row_pos[key] = i

        for rank in range(1, n_ranks + 1):
            key = (snap, str(rank))
            width = len(header)
            existing_row = by_key.get(key, [])
            merged = [("" if j >= len(existing_row) else existing_row[j]) for j in range(width)]
            merged[0], merged[1] = snap, str(rank)
            for name in names:
                col_idx = header.index(cfg["lanes"][name]["col"])
                picks = all_picks[name]
                if rank == 1 and not picks:
                    merged[col_idx] = "(không có video ≥10k/30d hôm nay)"
                elif rank <= len(picks):
                    merged[col_idx] = video_cell(picks[rank - 1])
                elif rank > 1:
                    merged[col_idx] = ""  # lane không đủ pick_per_lane video hôm nay
            by_key[key] = merged

        updates, appends = [], []
        for rank in range(1, n_ranks + 1):
            key = (snap, str(rank))
            row_vals = by_key[key]
            pos = row_pos.get(key)
            if pos:
                updates.append({"range": f"A{pos}:{chr(64 + len(header))}{pos}", "values": [row_vals]})
            else:
                appends.append(row_vals)
        if updates:
            retry_api(ws.batch_update, updates, value_input_option="USER_ENTERED")
        if appends:
            need = len(existing) + len(appends) + 5
            if need > ws.row_count:
                retry_api(ws.add_rows, need - ws.row_count)
            retry_api(ws.append_rows, appends, value_input_option="USER_ENTERED",
                      insert_data_option="INSERT_ROWS", table_range="A1")

        for name in names:
            if all_picks[name]:
                store.save_hunt_picks(con, name, all_picks[name], snap)
        LOG(f"\n[sheet] đã ghi {n_ranks} dòng ({snap} #1..#{n_ranks}) vào tab {d['research_tab']}")

        after = rep.guard_snapshot()
        bad = [t for t in lane_tabs + ["GMAIL", "NOTE"]
              if t in before and before[t] != after.get(t)]
        if bad:
            LOG(f"!! CẢNH BÁO: tab bị đổi ngoài dự kiến: {bad}")
            return 3

    if api:
        LOG(f"[quota] {api.used} / 10000")
    LOG(f"[done] {time.time() - t0:.0f}s")
    return 0


if __name__ == "__main__":
    with RunLock(Path(__file__).resolve().parent.parent / "data" / "hunt.lock") as acquired:
        if not acquired:
            LOG("[lock] đã có lượt Video Hunt khác đang chạy — thoát")
            raise SystemExit(0)
        raise SystemExit(main())
