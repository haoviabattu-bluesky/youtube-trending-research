# -*- coding: utf-8 -*-
"""Quét RỘNG một nhóm đề tài (danh sách từ khoá) để chấm đề tài: ai thắng, ai thua, vì sao.

Khác run_probe/run_video_hunt (quét ngách theo kênh): ở đây đơn vị là ĐỀ TÀI. Mỗi từ khoá được tìm 3 kiểu
(year=12 tháng theo view, month=30 ngày theo view, rel=liên quan) để thấy cả video thắng lẫn video thua
cùng đề tài. Sau đó enrich bằng Data API + baseline kênh (median 12 video ≥7 ngày) → breakout.

    py -3.13 -X utf8 src/topic_scan.py --kw data/<dir>/keywords.txt --out data/<dir> [--min-dur 180]
Ra: <out>/raw_search.json, <out>/videos.json (đã enrich, có breakout).
"""
from __future__ import annotations

import argparse, datetime as dt, json, os, statistics as st, sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
import innertube  # noqa: E402
from ytapi import YouTubeAPI  # noqa: E402

# 2026-10-17: thêm cửa sổ 'year' (upload_date=5) và 'rel' (không sort, chỉ lọc video)
innertube.WINDOW_PARAMS.update({"year": "CAMSBAgFEAE", "rel": "EgIQAQ=="})


def _key() -> str:
    from dotenv import load_dotenv
    load_dotenv(ROOT / "config" / ".env")
    return os.environ["YOUTUBE_API_KEY"]


def search_all(kws: list[str], out: Path) -> dict[str, dict]:
    p = out / "raw_search.json"
    found: dict[str, dict] = json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}
    done = {k for v in found.values() for k in v.get("kws", [])}
    cli = innertube.InnerTube()
    for i, kw in enumerate(kws):
        if kw in done:
            continue
        for win, pages in (("year", 2), ("month", 1), ("rel", 1)):
            try:
                rows = cli.search(kw, window=win, pages=pages)
            except Exception as e:  # noqa: BLE001 — 1 từ khoá lỗi không làm hỏng cả lượt
                print(f"  ✗ {kw} {win}: {type(e).__name__} {str(e)[:80]}", flush=True)
                continue
            for r in rows:
                cur = found.setdefault(r["video_id"], dict(r, kws=[], wins=[]))
                if kw not in cur["kws"]:
                    cur["kws"].append(kw)
                if win not in cur["wins"]:
                    cur["wins"].append(win)
        print(f"[{i + 1}/{len(kws)}] {kw}: tổng {len(found)} video", flush=True)
        p.write_text(json.dumps(found, ensure_ascii=False), encoding="utf-8")
    return found


def enrich(found: dict[str, dict], out: Path, min_dur: int) -> list[dict]:
    api = YouTubeAPI(_key(), safety_limit=9000)
    vids = api.videos_batch(list(found))
    rows = []
    for vid, v in vids.items():
        if v["duration_s"] < min_dur or v["live_broadcast_content"] != "none":
            continue
        rows.append(dict(found[vid], **v))
    chans = api.channels_batch(sorted({r["channel_id_api"] for r in rows}))
    cache_p = out / "baseline_cache.json"
    cache = json.loads(cache_p.read_text(encoding="utf-8")) if cache_p.exists() else {}
    now = dt.datetime.now(dt.timezone.utc)
    for i, (cid, c) in enumerate(chans.items()):
        if cid in cache or not c["uploads_playlist"]:
            continue
        try:
            base = api.baseline_videos(c["uploads_playlist"], want=12)
            cache[cid] = [b["views"] for b in base if b["duration_s"] >= min_dur] or [b["views"] for b in base]
        except Exception as e:  # noqa: BLE001
            print(f"  ✗ baseline {cid}: {e}", flush=True)
            cache[cid] = []
        if i % 50 == 0:
            cache_p.write_text(json.dumps(cache), encoding="utf-8")
            print(f"  baseline {i}/{len(chans)} quota {api.used}", flush=True)
    cache_p.write_text(json.dumps(cache), encoding="utf-8")
    for r in rows:
        c = chans.get(r["channel_id_api"], {})
        r.update({k: c.get(k) for k in ("channel_title", "subs", "ch_age_days", "ch_video_count")})
        b = cache.get(r["channel_id_api"]) or []
        r["ch_median"] = st.median(b) if b else None
        r["breakout"] = round(r["views"] / r["ch_median"], 2) if r.get("ch_median") else None
        born = dt.datetime.fromisoformat(r["published_at"].replace("Z", "+00:00"))
        r["age_days"] = max(1, (now - born).days)
        r["vpd"] = round(r["views"] / r["age_days"])
        r.pop("description", None)
    (out / "videos.json").write_text(json.dumps(rows, ensure_ascii=False, indent=0), encoding="utf-8")
    print(f"XONG {len(rows)} video dài · {len(chans)} kênh · quota {api.used}", flush=True)
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kw", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--min-dur", type=int, default=180)
    a = ap.parse_args()
    out = Path(a.out) if os.path.isabs(a.out) else ROOT / a.out
    out.mkdir(parents=True, exist_ok=True)
    kws = [k.strip() for k in Path(a.kw).read_text(encoding="utf-8").splitlines() if k.strip() and not k.startswith("#")]
    found = search_all(kws, out)
    enrich(found, out, a.min_dur)


if __name__ == "__main__":
    main()
