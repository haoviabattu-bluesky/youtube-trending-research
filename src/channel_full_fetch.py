# -*- coding: utf-8 -*-
"""Tải TOÀN BỘ video của 1 kênh cho audit hook/tiêu đề: metadata (API) + thumbnail + transcript ĐẦY ĐỦ theo mốc giây.

Khác hook_fetch.py (chỉ giữ 0–120s vào HOOK_LIBRARY\\raw): ở đây giữ cả transcript để đọc "hook của cả video"
(lời hứa được trả ở đâu, mục 1 nằm ở giây mấy). Chạy TUẦN TỰ 1 tiến trình — 3 tiến trình song song đã bị chặn IP
(2026-09-23). Chạy lại được: video đã có transcript thì bỏ qua.

    py -3.13 -X utf8 src/channel_full_fetch.py UCxxxx --out data/hook_audit_laneE --lang ja [--min-sec 60]
"""
from __future__ import annotations

import argparse, json, os, sys, time
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
import hook_fetch  # noqa: E402  (dùng lại 4 đường lấy transcript chống IpBlocked)
import deepdive  # noqa: E402  (fetch_comments — insight khán giả, thấy thiếu 2026-09-26)

API = "https://www.googleapis.com/youtube/v3"


def _key() -> str:
    from dotenv import load_dotenv
    load_dotenv(ROOT / "config" / ".env")
    return os.environ["YOUTUBE_API_KEY"]


def _dur(s: str) -> int:
    import re
    m = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", s or "")
    return int(m[1] or 0) * 3600 + int(m[2] or 0) * 60 + int(m[3] or 0) if m else 0


def list_videos(channel_id: str) -> list[dict]:
    k = _key()
    ch = requests.get(f"{API}/channels", params=dict(part="contentDetails,snippet,statistics", id=channel_id, key=k),
                      timeout=30).json()["items"][0]
    up = ch["contentDetails"]["relatedPlaylists"]["uploads"]
    ids, tok = [], None
    while True:
        r = requests.get(f"{API}/playlistItems", params=dict(part="contentDetails", playlistId=up, maxResults=50,
                                                            pageToken=tok, key=k), timeout=30).json()
        ids += [i["contentDetails"]["videoId"] for i in r.get("items", [])]
        tok = r.get("nextPageToken")
        if not tok:
            break
    out = []
    for i in range(0, len(ids), 50):
        r = requests.get(f"{API}/videos", params=dict(part="snippet,statistics,contentDetails", id=",".join(ids[i:i + 50]),
                                                     key=k), timeout=30).json()
        for v in r.get("items", []):
            sn, st = v["snippet"], v["statistics"]
            out.append(dict(id=v["id"], title=sn["title"], published=sn["publishedAt"], description=sn.get("description", ""),
                            tags=sn.get("tags", []), views=int(st.get("viewCount", 0)), likes=int(st.get("likeCount", 0)),
                            comments=int(st.get("commentCount", 0)), dur=_dur(v["contentDetails"]["duration"])))
    meta = dict(channel_id=channel_id, name=ch["snippet"]["title"], subs=ch["statistics"].get("subscriberCount"),
                total_views=ch["statistics"].get("viewCount"), video_count=len(out))
    return meta, out


def thumb(vid: str, d: Path) -> str:
    p = d / f"{vid}.jpg"
    if p.exists():
        return str(p)
    for q in ("maxresdefault", "hqdefault"):
        r = requests.get(f"https://i.ytimg.com/vi/{vid}/{q}.jpg", timeout=20)
        if r.status_code == 200 and len(r.content) > 5000:
            p.write_bytes(r.content)
            return str(p)
    return ""


def fetch_all_comments(vs: list[dict], out: Path, limit: int, gap: float) -> None:
    """Ghi/nối out/comments.json — dict {video_id: [{text,votes,is_reply,author}]}.
    Resume-safe: video đã có trong file (kể cả file cũ từ lượt chạy khác) thì bỏ qua,
    không gọi lại (comment downloader không dùng API key nhưng vẫn tốn thời gian/dễ bị chặn)."""
    p = out / "comments.json"
    store = json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}
    ok = miss = 0
    for v in vs:
        if v["id"] in store and store[v["id"]]:
            ok += 1
            continue
        try:
            cs = deepdive.fetch_comments(v["id"], limit=limit)
        except Exception as e:
            print(f"  ✗ comments {v['id']}: {type(e).__name__} {str(e)[:100]}", flush=True)
            miss += 1
            continue
        store[v["id"]] = cs
        ok += 1
        print(f"  comments {v['id']}: {len(cs)} bình luận", flush=True)
        p.write_text(json.dumps(store, ensure_ascii=False, indent=1), encoding="utf-8")
        time.sleep(gap)
    print(f"COMMENTS xong ok={ok} miss={miss} -> {p}", flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("channel_id")
    ap.add_argument("--out", required=True)
    ap.add_argument("--lang", default="ja")
    ap.add_argument("--min-sec", type=int, default=60, help="bỏ Shorts ngắn hơn ngưỡng này khỏi bước tải transcript")
    ap.add_argument("--gap", type=float, default=4.0, help="nghỉ giữa 2 video (giây)")
    ap.add_argument("--no-comments", action="store_true", help="tắt bước tải bình luận (bật mặc định từ 2026-09-26)")
    ap.add_argument("--comment-limit", type=int, default=80, help="số bình luận tối đa/video, sort theo lượt thích")
    a = ap.parse_args()
    out = ROOT / a.out if not os.path.isabs(a.out) else Path(a.out)
    (out / "thumbs").mkdir(parents=True, exist_ok=True)
    (out / "transcripts").mkdir(exist_ok=True)
    meta, vs = list_videos(a.channel_id)
    (out / "channel.json").write_text(json.dumps(dict(meta=meta, videos=vs), ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{meta['name']}: {len(vs)} video", flush=True)
    ok = miss = 0
    for v in vs:
        v["thumb"] = thumb(v["id"], out / "thumbs")
        tp = out / "transcripts" / f"{v['id']}.json"
        if v["dur"] < a.min_sec:
            continue
        if tp.exists() and json.loads(tp.read_text(encoding="utf-8")).get("segments"):
            ok += 1
            continue
        segs, way = hook_fetch.transcript(v["id"], a.lang)
        tp.write_text(json.dumps(dict(id=v["id"], via=way, segments=segs), ensure_ascii=False), encoding="utf-8")
        ok, miss = (ok + 1, miss) if segs else (ok, miss + 1)
        print(f"  {v['id']} {way} {len(segs)} seg | ok {ok} miss {miss}", flush=True)
        time.sleep(a.gap)
    (out / "channel.json").write_text(json.dumps(dict(meta=meta, videos=vs), ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"XONG ok={ok} miss={miss}", flush=True)

    if not a.no_comments:
        print("Tải bình luận (sort theo lượt thích)...", flush=True)
        fetch_all_comments(vs, out, a.comment_limit, a.gap)


if __name__ == "__main__":
    main()
