# -*- coding: utf-8 -*-
"""Lấp transcript thiếu (YouTube chặn) bằng transcripts.json của channel_dna h2dev — văn bản KHÔNG có mốc giây,
nên chia câu và ƯỚC TÍNH start = vị trí ký tự ÷ (len/duration). Ghi via="dna_text_est" để báo cáo nói rõ là ước tính.

    py -3.13 -X utf8 src/fill_missing_transcripts.py data/hook_audit_laneEFG/E_kenko <dna_transcripts.json> [...]
"""
import json, re, sys
from pathlib import Path

d = Path(sys.argv[1]); ch = json.loads((d / "channel.json").read_text(encoding="utf-8"))
dur = {v["id"]: v["dur"] for v in ch["videos"]}
src = {}
for f in sys.argv[2:]:
    for r in json.loads(Path(f).read_text(encoding="utf-8")):
        if r.get("transcript"):
            src[r["id"]] = r["transcript"]
n = 0
for vid, sec in dur.items():
    p = d / "transcripts" / f"{vid}.json"
    have = p.exists() and json.loads(p.read_text(encoding="utf-8")).get("segments")
    if have or vid not in src or sec < 60:
        continue
    t = re.sub(r"\s+", " ", src[vid]); rate = len(t) / sec
    parts = [x for x in re.split(r"(?<=[。？！?!])", t) if x.strip()]
    segs, pos = [], 0
    for x in parts:
        segs.append({"start": round(pos / rate, 1), "duration": round(len(x) / rate, 1), "text": x.strip()}); pos += len(x)
    p.write_text(json.dumps(dict(id=vid, via="dna_text_est", segments=segs), ensure_ascii=False), encoding="utf-8"); n += 1
    print("filled", vid, len(segs))
print("filled", n)
