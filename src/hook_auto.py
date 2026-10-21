# -*- coding: utf-8 -*-
"""Phân tích HOOK bằng model NGOÀI (deepseek/Sol qua ns24) thay vì Claude đọc transcript.

Đo 21/10/2026: các bước đọc transcript/tài liệu in thẳng vào chat là chỗ tốn quota Claude
nhiều nhất — mỗi video 0–120s ≈ 2–4k token nằm lại trong ngữ cảnh tới hết phiên.
Tool này: hook_fetch.fetch (cache raw/) → gửi 0–120s + danh mục patterns.json cho model ngoài
→ kiểm đúng schema hook_library (REQ, mã H/K có thật, kind A–E) → ghi hooks.jsonl.
Claude chỉ thấy 1 dòng/video. Bản ghi gắn `analyzed_by` để biết không phải Claude viết.

    py -3.13 -X utf8 src/hook_auto.py ID [ID ...] [--lane "shakai-no-naze"]   (đổi model: config/models.yaml gate ext_hook)
"""
from __future__ import annotations

import argparse, json, sys, tempfile
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
load_dotenv(ROOT / "config" / ".env")
from hook_fetch import fetch, vid_of                              # noqa: E402
from hook_library import KINDS, REQ, add, load_pat                # noqa: E402
from ext_llm import ask_json                                      # noqa: E402

GATE = "ext_hook"   # chain model ở config/models.yaml

PROMPT = """Bạn là biên tập viên phân tích HOOK video YouTube Nhật (0–30s mở đầu + câu khoá 30–90s).
Viết MỌI phần giải thích bằng tiếng Việt. Không bịa: chỉ dựa vào transcript bên dưới.
Danh mục kiểu hook (patterns, mã H..) và thiết bị khoá (closers, mã K..) — CHỈ dùng mã có trong danh mục:
{catalog}
Loại hook kind ∈ {kinds}.
Trả về DUY NHẤT 1 object JSON:
{{"video_id":"{vid}","channel":"{ch}","title":"{title}","views":{views},
 "hook_0_30s":"nguyên văn tiếng Nhật 0–30s, nối câu bằng ／",
 "hook_0_30s_vi":"dịch tiếng Việt đoạn trên",
 "beats":["m:ss mô tả nhịp bằng tiếng Việt", "... 3–6 nhịp"],
 "kind":"A|B|C|D|E|none","patterns":["H.."],"closers":["K.."],
 "score_0_12":0-12,"why":"2–4 câu tiếng Việt: vì sao giữ/không giữ người xem",
 "lanes_fit":["{lane}"]}}
TIÊU ĐỀ: {title}
TRANSCRIPT 0–120s ({via}):
{segs}"""


def catalog() -> str:
    p = load_pat()
    rows = [f'{x["id"]} {x["name"]}' for x in p["patterns"]] + [f'{x["id"]} {x["name"]}' for x in p["closers"]]
    return "\n".join(rows)


def analyze(vid: str, lane: str) -> tuple[dict | None, str]:
    raw = fetch(vid)
    if raw.get("transcript_via") == "none" or not raw.get("hook_segments"):
        return None, "không có transcript"
    segs = "\n".join(f'[{int(s["start"]) // 60}:{int(s["start"]) % 60:02d}] {s["text"]}' for s in raw["hook_segments"])
    msg = PROMPT.format(catalog=catalog(), kinds=list(KINDS), vid=vid, ch=raw.get("channel", ""),
                        title=(raw.get("title_api") or "").replace('"', "'"), views=raw.get("views") or 0,
                        lane=lane, via=raw["transcript_via"], segs=segs)
    known = {x["id"] for x in load_pat()["patterns"]} | {x["id"] for x in load_pat()["closers"]}
    err = ""
    for lan in range(2):   # lần 2: bỏ cache + nhắc lại luật mã, vì JSON hợp lệ nhưng sai schema không tự sang model kế
        res = ask_json(GATE, msg + ("" if lan == 0 else "\nLƯU Ý: chỉ dùng mã H../K.. có trong danh mục, đủ mọi trường."),
                       ids=[vid], use_cache=lan == 0)
        rec = res.parsed_response
        if not res.ok or not isinstance(rec, dict):
            err = res.error or "JSON không phải object"; continue
        rec["patterns"] = [p for p in rec.get("patterns", []) if p in known]
        rec["closers"] = [k for k in rec.get("closers", []) if k in known]
        if any(k not in rec for k in REQ) or rec.get("kind") not in KINDS or not rec["patterns"]:
            err = f"{res.model}: thiếu trường/mã lạ"; continue
        rec.update({"video_id": vid, "url": f"https://www.youtube.com/watch?v={vid}",
                    "analyzed_by": f"{res.provider}/{res.model}", "transcript_via": raw["transcript_via"]})
        return rec, res.model
    return None, err


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ids", nargs="+")
    ap.add_argument("--lane", default="")
    a = ap.parse_args()
    ok = []
    for s in a.ids:
        vid = vid_of(s)
        rec, info = analyze(vid, a.lane)
        if not rec:
            print(f"✗ {vid}: {info}"); continue
        ok.append(rec)
        print(f'✓ {vid} {rec["kind"]} {"+".join(rec["patterns"] + rec["closers"])} {rec["score_0_12"]}/12 '
              f'[{info}] {rec.get("hook_0_30s_vi", "")[:90]}')
    if ok:
        f = Path(tempfile.gettempdir()) / "hook_auto_batch.json"
        f.write_text(json.dumps(ok, ensure_ascii=False), encoding="utf-8")
        add([str(f)])


if __name__ == "__main__":
    main()
