# -*- coding: utf-8 -*-
"""Lấy dữ liệu HOOK của 1 hay nhiều video → E:\\CLAUDE\\YOUTUBE\\HOOK_LIBRARY\\raw\\<id>.json.

Bước ĐẦU TIÊN mỗi khi research ra video mới (user chốt 2026-09-23): phải đọc hook trước.
Tool chỉ lấy dữ liệu (tiêu đề, view, 0–120s transcript theo mốc giây, thumbnail) và in ra
để Claude đọc + phân loại; phân tích do Claude viết vào hooks.jsonl qua hook_library.py.

Transcript có 4 đường vì YouTube hay chặn IP nhà (IpBlocked/429, dính thật 2026-09-23):
  api trực tiếp → api qua proxy → yt-dlp qua proxy → yt-dlp trực tiếp.

    py -3.13 -X utf8 src/hook_fetch.py VIDEO_ID [VIDEO_ID ...] [--lang ja] [--sec 90]
"""
from __future__ import annotations

import argparse, glob, json, os, re, subprocess, sys, tempfile, time
from pathlib import Path

import requests

LIB = Path(r"E:\CLAUDE\YOUTUBE\HOOK_LIBRARY")
ROOT = Path(__file__).resolve().parents[1]
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/131 Safari/537.36"}


def _proxies() -> list[str]:
    p = ROOT / "config" / "proxies.txt"
    if not p.exists():
        return []
    return [l.strip() for l in p.read_text(encoding="utf-8").splitlines() if l.strip() and not l.startswith("#")]


def vid_of(s: str) -> str:
    m = re.search(r"(?:v=|youtu\.be/|shorts/)([\w-]{11})", s)
    return m.group(1) if m else s.strip()


def _api(vid, lang, proxy=None):
    from youtube_transcript_api import YouTubeTranscriptApi
    kw = {}
    if proxy:
        from youtube_transcript_api.proxies import GenericProxyConfig
        kw["proxy_config"] = GenericProxyConfig(http_url=proxy, https_url=proxy)
    return YouTubeTranscriptApi(**kw).fetch(vid, languages=[lang]).to_raw_data()


def _ytdlp(vid, lang, proxy=None):
    with tempfile.TemporaryDirectory() as d:
        cmd = [sys.executable, "-m", "yt_dlp", "--skip-download", "--write-auto-subs", "--write-subs",
               "--sub-langs", lang, "--sub-format", "json3", "-o", f"{d}/%(id)s.%(ext)s",
               f"https://www.youtube.com/watch?v={vid}"]
        if proxy:
            cmd[3:3] = ["--proxy", proxy]
        subprocess.run(cmd, capture_output=True, timeout=120)
        files = glob.glob(f"{d}/*.json3")
        if not files:
            raise RuntimeError("yt-dlp không ra phụ đề")
        ev = json.load(open(files[0], encoding="utf-8")).get("events", [])
        return [{"start": e.get("tStartMs", 0) / 1000, "duration": e.get("dDurationMs", 0) / 1000,
                 "text": "".join(s.get("utf8", "") for s in e["segs"]).replace("\n", "")}
                for e in ev if "segs" in e]


def transcript(vid, lang):
    px = _proxies()
    ways = [("api", lambda: _api(vid, lang))]
    ways += [(f"api+proxy{i}", (lambda p=p: _api(vid, lang, p))) for i, p in enumerate(px, 1)]
    ways += [(f"ytdlp+proxy{i}", (lambda p=p: _ytdlp(vid, lang, p))) for i, p in enumerate(px, 1)]
    ways += [("ytdlp", lambda: _ytdlp(vid, lang))]
    # 2026-10-11: phụ đề bị chặn hết (cả timedtext trong Chrome thật) nhưng luồng audio vẫn tải được → ASR whisper
    from transcript_asr import fetch as _asr
    ways += [("asr", lambda: _asr(vid, lang))]
    for name, fn in ways:
        try:
            segs = fn()
            if segs:
                return segs, name
        except Exception as e:  # thử đường kế tiếp — lỗi chặn IP là tạm thời, không phải video hỏng
            print(f"    · {name}: {type(e).__name__}", file=sys.stderr)
            time.sleep(2)
    return [], "none"


def meta(vid):
    sys.path.insert(0, str(ROOT / "src"))
    from dotenv import load_dotenv
    from ytapi import YouTubeAPI
    load_dotenv(ROOT / "config" / ".env")
    d = YouTubeAPI(os.environ["YOUTUBE_API_KEY"]).videos_batch([vid]).get(vid, {})
    return {k: d.get(k) for k in ("title_api", "channel_id_api", "published_at", "views", "likes",
                                  "comments", "duration_s", "description")}


def fetch(vid, lang="ja", sec=120, force=False):
    out = LIB / "raw" / f"{vid}.json"
    if out.exists() and not force:
        old = json.loads(out.read_text(encoding="utf-8"))
        if old.get("transcript_via") != "none":      # bản lỗi (bị chặn) thì tải lại, đừng trả cache rỗng
            return old
    m = meta(vid)
    segs, way = transcript(vid, lang)
    ch = ""
    try:
        t = requests.get(f"https://www.youtube.com/watch?v={vid}", headers=UA, timeout=30).text
        mm = re.search(r'"ownerChannelName":"([^"]+)"', t)
        ch = mm.group(1) if mm else ""
    except Exception:
        pass
    thumb = LIB / "thumbs" / f"{vid}.jpg"
    for q in ("maxresdefault", "hqdefault"):
        r = requests.get(f"https://i.ytimg.com/vi/{vid}/{q}.jpg", timeout=20)
        if r.status_code == 200 and len(r.content) > 5000:
            thumb.write_bytes(r.content)
            break
    rec = {"video_id": vid, "channel": ch, **m, "transcript_via": way,
           "hook_segments": [s for s in segs if s["start"] < sec],
           "full_chars": len("".join(s["text"] for s in segs)), "thumb": str(thumb)}
    out.write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
    return rec


def show(rec, sec=90):
    print(f"\n=== {rec['video_id']} | {rec.get('channel')} | {rec.get('views') or 0:,} view | "
          f"{(rec.get('duration_s') or 0)//60}m | via {rec['transcript_via']}")
    print(f"TITLE: {rec.get('title_api')}")
    for s in rec["hook_segments"]:
        if s["start"] < sec:
            print(f"  [{int(s['start'])//60}:{int(s['start'])%60:02d}] {s['text'].replace('[音楽]', '').strip()}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ids", nargs="+")
    ap.add_argument("--lang", default="ja")
    ap.add_argument("--sec", type=int, default=90)
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    for s in a.ids:
        show(fetch(vid_of(s), a.lang, max(a.sec, 120), a.force), a.sec)


if __name__ == "__main__":
    main()
