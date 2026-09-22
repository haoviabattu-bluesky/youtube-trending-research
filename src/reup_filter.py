# -*- coding: utf-8 -*-
"""Phân loại ORIGINAL / REUP / VLOG_PERSON cho kết quả trend_hunter.py.

Phát hiện thật 2026-09-11: phần lớn kênh khớp tiêu chí "sub<1000 + 3-5 video + view
đột biến" là kênh REUP cưỡi trên 1 khoảnh khắc viral có sẵn (clip TV danh hài, meme
battle, highlight thể thao ghép nhạc hot) — không phải kênh có công thức nội dung
mới. Tách riêng khỏi trend_hunter.py vì đây là bước LLM TUỲ CHỌN (không có
LLM_API_KEY vẫn chạy được, chỉ là không gắn nhãn).
"""
from __future__ import annotations

import json

import requests

PROMPT = """Bạn là chuyên gia phân loại kênh YouTube tiếng Nhật cho mục đích tìm kênh CÓ THỂ
NHÂN BẢN (clone) để sản xuất video mới. Với mỗi video dưới đây, phân loại kênh thành:
- ORIGINAL: kênh tự dựng nội dung (kể chuyện/giải thích/phân tích/animation/hình ảnh AI...),
  có công thức/format riêng lặp lại được, KHÔNG phụ thuộc tư liệu người khác đã làm sẵn
- REUP: dựa trên tư liệu có sẵn không do kênh tạo ra (clip cắt từ TV/chương trình, meme
  viral có sẵn, highlight thể thao, MV/bài hát người khác, lyric video, cover nhạc)
- VLOG_PERSON: người thật xuất hiện/tự quay, không phải kênh faceless

Trả về DUY NHẤT JSON list, không thêm chữ nào khác, không dùng markdown fence:
[{{"video_id": "...", "type": "ORIGINAL|REUP|VLOG_PERSON", "why": "lý do ngắn 1 câu"}}]

Danh sách video:
{items}"""


def _strip_fence(text: str) -> str:
    t = text.strip()
    if t.startswith("```"):
        t = t.split("\n", 1)[1] if "\n" in t else t[3:]
        if t.rstrip().endswith("```"):
            t = t.rstrip()[:-3]
    return t.strip()


def classify(rows: list[dict], base_url: str, api_key: str, model: str,
             timeout: int = 120) -> dict[str, dict]:
    """Gọi 1 lượt LLM phân loại cả lô (rẻ hơn gọi từng video). Không key → trả rỗng."""
    if not api_key or not rows:
        return {}
    items = "\n".join(
        f"- video_id={r['video_id']} | kênh={r.get('channel', '')} | "
        f"tiêu đề={r.get('title_api') or r.get('title', '')}"
        for r in rows)
    try:
        r = requests.post(
            f"{base_url}/chat/completions",
            headers={"Authorization": f"Bearer {api_key}"},
            json={"model": model,
                  "messages": [{"role": "user", "content": PROMPT.format(items=items)}],
                  "max_tokens": 1500, "temperature": 0.2}, timeout=timeout)
        if r.status_code != 200:
            return {}
        content = _strip_fence(r.json()["choices"][0]["message"]["content"])
        data = json.loads(content)
        return {d["video_id"]: d for d in data if "video_id" in d}
    except Exception:
        return {}
