# -*- coding: utf-8 -*-
"""Phân loại + DỊCH tiêu đề video hàng loạt bằng model ngoài (gate ext_classify) — Claude không đọc bảng thô.

Đầu vào: file JSON list video có `video_id` + (`title_api` | `title`) [+ `channel_title`, `description`].
Mô tả lane: --lane-file (txt/md) hoặc --lane "chuỗi". Mỗi video được gắn khoá `llm`:
  {"vi": dịch tiêu đề, "de_tai", "kieu", "hop": 0–10, "ly_do"}
Ghi đè lại file (hoặc --out), in tối đa --top dòng gọn để Claude đọc.

    py -3.13 -X utf8 src/title_classify.py data/x/cands.json --lane-file lanes/shakai-no-naze/MO_TA.txt --top 30
Dùng như module: classify(videos, lane_desc) → videos (đã gắn llm).
"""
from __future__ import annotations

import argparse, json, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ext_llm import ask_json  # noqa: E402

GATE, LOT = "ext_classify", 20
PROMPT = """Bạn phân loại video YouTube (thường là tiếng Nhật) cho một kênh của mình.
MÔ TẢ LANE / KHUÔN CẦN TÌM:
{lane}
Với MỖI video trả 1 phần tử trong JSON list:
{{"id":"video_id","vi":"dịch nghĩa tiêu đề sang tiếng Việt, đủ ý, giữ số","de_tai":"đề tài 3–8 chữ tiếng Việt",
"kieu":"{kieu}","hop":0-10,"ly_do":"≤15 chữ tiếng Việt"}}
Tên riêng Nhật: phiên âm/dịch, không bỏ. Chỉ trả JSON list, không giải thích.
VIDEO (id | tiêu đề | kênh | mô tả):
{body}"""
KIEU = "nao_xa_hoi|truyen_drama|sukatto|tin_tuc|huong_dan|khac"


def _title(v: dict) -> str:
    return v.get("title_api") or v.get("title") or ""


def classify(videos: list[dict], lane: str, kieu: str = KIEU) -> tuple[list[dict], list[str]]:
    """Gắn v['llm'] cho từng video. Trả (videos, lỗi theo lô). Video model bỏ sót → llm = {} (không bịa)."""
    errs = []
    for i in range(0, len(videos), LOT):
        lot = videos[i:i + LOT]
        body = "\n".join(f'{v["video_id"]} | {_title(v)} | {v.get("channel_title") or v.get("channel", "")} | '
                         f'{(v.get("description") or "")[:150]!r}' for v in lot)
        res = ask_json(GATE, PROMPT.format(lane=lane, kieu=kieu, body=body), ids=[v["video_id"] for v in lot])
        rows = res.parsed_response if res.ok else None
        if isinstance(rows, dict):
            rows = next((x for x in rows.values() if isinstance(x, list)), None)
        if not isinstance(rows, list):
            errs.append(f"lô {i // LOT + 1}: {res.error or 'không phải list'}")
            rows = []
        by = {r.get("id"): r for r in rows if isinstance(r, dict)}
        for v in lot:
            v["llm"] = by.get(v["video_id"], {})
            v["llm_model"] = res.model
        miss = sum(1 for v in lot if not v["llm"])
        if miss:
            errs.append(f"lô {i // LOT + 1}: model bỏ sót {miss}/{len(lot)} video")
    return videos, errs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--lane", default="")
    ap.add_argument("--lane-file", default="")
    ap.add_argument("--out", default="")
    ap.add_argument("--top", type=int, default=30)
    a = ap.parse_args()
    lane = Path(a.lane_file).read_text(encoding="utf-8") if a.lane_file else a.lane
    if not lane.strip():
        sys.exit("cần --lane hoặc --lane-file")
    vids = json.loads(Path(a.file).read_text(encoding="utf-8"))
    vids, errs = classify(vids, lane)
    Path(a.out or a.file).write_text(json.dumps(vids, ensure_ascii=False, indent=1), encoding="utf-8")
    for e in errs:
        print("⚠", e)
    vids.sort(key=lambda v: -(v["llm"].get("hop") or 0))
    for v in vids[:a.top]:
        l = v["llm"]
        print(f'{l.get("hop", "?")}|{l.get("kieu", "?")}|{v["video_id"]}|{v.get("views", "")}|{l.get("vi", "")}|{l.get("ly_do", "")}')
    print(f"→ {a.out or a.file} ({len(vids)} video)")


if __name__ == "__main__":
    main()
