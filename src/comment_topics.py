# -*- coding: utf-8 -*-
"""Bình luận → CHỦ ĐỀ người xem tâm đắc, xếp theo TỔNG LIKE (luật anh 17/10 "người xem thích nghe gì").

Model ngoài (gate ext_comments) chỉ GÁN từng bình luận vào chủ đề + dịch vài câu tiêu biểu;
tổng like / số bình luận do Python cộng (không tin model làm toán). Claude chỉ đọc bảng chủ đề.
Lấy bình luận: Data API commentThreads (ổn định, 1 quota/100 cmt) → youtube-comment-downloader dự phòng.

    py -3.13 -X utf8 src/comment_topics.py VIDEO_ID [VIDEO_ID ...] --out data/x/comments_topics.json [--max 400]
"""
from __future__ import annotations

import argparse, json, os, sys
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ext_llm import ask_json  # noqa: E402

GATE, LOT = "ext_comments", 120
PROMPT = """Dưới đây là bình luận YouTube (thường tiếng Nhật) của video: {title}
Gom chúng thành 4–10 CHỦ ĐỀ mà người xem tâm đắc / tranh cãi / kể chuyện bản thân. Mỗi bình luận thuộc tối đa 1 chủ đề
(bình luận vô nghĩa thì bỏ). Viết bằng tiếng Việt. Trả DUY NHẤT JSON:
{{"topics":[{{"chu_de":"≤10 chữ","mo_ta":"1 câu: người xem nói gì","idx":[số thứ tự bình luận],
  "trich":[{{"idx":số,"vi":"dịch nguyên ý bình luận đó"}}]}}]}}
"trich" = 2 bình luận tiêu biểu nhất của chủ đề. Không bịa bình luận không có trong danh sách.
BÌNH LUẬN (số | like | nội dung):
{body}"""


def fetch_api(vid: str, mx: int) -> list[dict]:
    key, out, tok = os.environ.get("YOUTUBE_API_KEY", ""), [], None
    while key and len(out) < mx:
        r = requests.get("https://www.googleapis.com/youtube/v3/commentThreads", timeout=30, params=dict(
            part="snippet", videoId=vid, maxResults=100, order="relevance", textFormat="plainText",
            pageToken=tok, key=key)).json()
        for it in r.get("items", []):
            s = it["snippet"]["topLevelComment"]["snippet"]
            out.append({"text": s.get("textDisplay", ""), "likes": int(s.get("likeCount", 0)),
                        "replies": int(it["snippet"].get("totalReplyCount", 0))})
        tok = r.get("nextPageToken")
        if not tok or "error" in r:
            break
    return out[:mx]


def fetch(vid: str, mx: int) -> list[dict]:
    cm = fetch_api(vid, mx)
    if not cm:
        from deepdive import fetch_comments
        cm = [{"text": c["text"], "likes": c["votes"], "replies": 0} for c in fetch_comments(vid, mx) if not c["is_reply"]]
    return cm


def aggregate(comments: list[dict], topics: list[dict]) -> list[dict]:
    """Cộng like/số bình luận theo idx model gán; idx lạ hoặc trùng chủ đề bị bỏ (đếm 1 lần)."""
    seen, out = set(), []
    for t in topics:
        idx = [i for i in t.get("idx", []) if isinstance(i, int) and 0 <= i < len(comments) and i not in seen]
        seen.update(idx)
        if not idx:
            continue
        trich = [x for x in t.get("trich", []) if isinstance(x, dict) and x.get("idx") in idx]
        for x in trich:
            x["goc"], x["likes"] = comments[x["idx"]]["text"][:300], comments[x["idx"]]["likes"]
        out.append({"chu_de": t.get("chu_de", ""), "mo_ta": t.get("mo_ta", ""), "so_cmt": len(idx),
                    "like_tong": sum(comments[i]["likes"] for i in idx), "trich": trich})
    tot = sum(t["like_tong"] for t in out) or 1
    for t in out:
        t["ty_le_like"] = round(t["like_tong"] / tot * 100, 1)
    return sorted(out, key=lambda t: -t["like_tong"])


def analyze(vid: str, title: str, mx: int) -> dict:
    cm = sorted(fetch(vid, mx), key=lambda c: -c["likes"])
    topics, errs = [], []
    for i in range(0, len(cm), LOT):
        body = "\n".join(f'{j} | {c["likes"]} | {c["text"][:220]!r}' for j, c in enumerate(cm[i:i + LOT], start=i))
        res = ask_json(GATE, PROMPT.format(title=title, body=body), ids=[vid, f"lot{i}"])
        got = (res.parsed_response or {}).get("topics") if res.ok and isinstance(res.parsed_response, dict) else None
        if got is None:
            errs.append(res.error or "không có topics")
        topics += got or []
    return {"video_id": vid, "title": title, "n_comments": len(cm), "topics": aggregate(cm, topics), "errors": errs}


def main():
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).resolve().parents[1] / "config" / ".env")
    ap = argparse.ArgumentParser()
    ap.add_argument("ids", nargs="+")
    ap.add_argument("--out", required=True)
    ap.add_argument("--max", type=int, default=400)
    ap.add_argument("--title", default="")
    a = ap.parse_args()
    res = []
    for vid in a.ids:
        r = analyze(vid, a.title, a.max)
        res.append(r)
        print(f"\n{vid}: {r['n_comments']} bình luận" + (f" · ⚠ {r['errors']}" if r["errors"] else ""))
        for t in r["topics"][:6]:
            q = t["trich"][0]["vi"][:80] if t["trich"] else ""
            print(f'  {t["ty_le_like"]:5.1f}% like · {t["so_cmt"]:3d} cmt · {t["chu_de"]} — {q}')
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"→ {a.out}")


if __name__ == "__main__":
    main()
