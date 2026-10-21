# -*- coding: utf-8 -*-
"""Lấy transcript qua Chrome NỀN RIÊNG của dự án (pw_search, cổng 9461) khi IP bị YouTube đòi đăng nhập với yt-dlp/api.

Mở 1 TAB MỚI trong Chrome đó (không mở/tắt Chrome), đọc ytInitialPlayerResponse → captionTracks → tải json3
từ ngữ cảnh trang; hỏng thì bấm bảng 「文字起こしを表示」 và đọc DOM. Xong thì chỉ đóng tab đã mở.
Ghi ra HOOK_LIBRARY\\raw\\<id>.json cùng khuôn với hook_fetch (transcript_via = 'cdp').

    py -3.13 -X utf8 src/cdp_transcript.py <id> [<id> ...] [--sec 120]
"""
import json, os, re, sys, time
from pathlib import Path
from playwright.sync_api import sync_playwright

PORT = int(os.environ.get("PW_PORT", "9461"))
RAW = Path(r"E:\CLAUDE\YOUTUBE\HOOK_LIBRARY\raw")

JS_TRACKS = """() => { const p = window.ytInitialPlayerResponse || {};
  const t = ((p.captions||{}).playerCaptionsTracklistRenderer||{}).captionTracks || [];
  return {title: (p.videoDetails||{}).title || '', tracks: t.map(x => ({url: x.baseUrl, lang: x.languageCode, kind: x.kind||''}))}; }"""
JS_FETCH = """async (u) => { const r = await fetch(u + '&fmt=json3'); return r.ok ? await r.text() : 'HTTP' + r.status; }"""


def _ts(s):
    p = [int(x) for x in s.strip().split(":")]
    return p[0] * 60 + p[1] if len(p) == 2 else p[0] * 3600 + p[1] * 60 + p[2]


def grab(page, vid, sec):
    page.goto(f"https://www.youtube.com/watch?v={vid}", wait_until="domcontentloaded", timeout=60000)
    page.wait_for_timeout(3500)
    info = page.evaluate(JS_TRACKS)
    tracks = sorted(info["tracks"], key=lambda t: (t["lang"] != "ja", t["kind"] == "asr"))
    for t in tracks:
        txt = page.evaluate(JS_FETCH, t["url"])
        if txt.startswith("{"):
            ev = json.loads(txt).get("events", [])
            segs = [{"start": round(e["tStartMs"] / 1000, 2), "duration": round(e.get("dDurationMs", 0) / 1000, 2),
                     "text": "".join(s.get("utf8", "") for s in e.get("segs", [])).strip()} for e in ev if e.get("segs")]
            segs = [s for s in segs if s["text"] and s["start"] <= sec]
            if segs:
                return info["title"], segs, "cdp-json3"
    # đường 2: bảng 文字起こし
    try:
        page.evaluate("() => { const b=[...document.querySelectorAll('button')].find(x=>/文字起こし|transcript/i.test(x.innerText||x.ariaLabel||'')); if(b) b.click(); }")
        page.locator("#description-inline-expander, tp-yt-paper-button#expand").first.click(timeout=3000)
        page.wait_for_timeout(800)
        page.get_by_role("button", name=re.compile("文字起こし|transcript", re.I)).first.click(timeout=5000)
        page.wait_for_selector("ytd-transcript-segment-renderer", timeout=15000)
        rows = page.evaluate("() => [...document.querySelectorAll('ytd-transcript-segment-renderer')].map(r => [r.querySelector('.segment-timestamp')?.innerText||'', r.querySelector('.segment-text')?.innerText||''])")
        segs = [{"start": _ts(a), "duration": 0, "text": b.strip()} for a, b in rows if a.strip()]
        segs = [s for s in segs if s["start"] <= sec]
        if segs:
            return info["title"], segs, "cdp-panel"
    except Exception as e:  # noqa: BLE001
        print(f"  panel ✗ {type(e).__name__}", flush=True)
    return info["title"], [], "none"


def main():
    sec = int(sys.argv[sys.argv.index("--sec") + 1]) if "--sec" in sys.argv else 120
    ids = [a for a in sys.argv[1:] if not a.startswith("--") and not a.isdigit()]
    with sync_playwright() as p:
        br = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
        ctx = br.contexts[0]
        page = ctx.new_page()
        try:
            for vid in ids:
                title, segs, via = grab(page, vid, sec)
                f = RAW / f"{vid}.json"
                rec = json.loads(f.read_text(encoding="utf-8")) if f.exists() else {"video_id": vid}
                if segs:
                    rec.update(segments=segs, transcript_via=via)
                    rec.setdefault("title", title)
                    f.write_text(json.dumps(rec, ensure_ascii=False), encoding="utf-8")
                print(f"{vid} {via} {len(segs)} seg | {title[:50]}", flush=True)
                time.sleep(2)
        finally:
            page.close()


if __name__ == "__main__":
    main()
