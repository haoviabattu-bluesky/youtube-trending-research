# -*- coding: utf-8 -*-
"""Kho HOOK dùng chung mọi dự án YouTube — E:\\CLAUDE\\YOUTUBE\\HOOK_LIBRARY\\.

Hai nguồn chân lý (sửa 2 file này, KHÔNG sửa tay HOOK_LIBRARY.md vì file đó sinh lại):
  patterns.json  — danh mục kiểu hook (H..) + thiết bị khoá hook (K..), mỗi kiểu có công thức + lane hợp
  hooks.jsonl    — 1 dòng / 1 video đã phân tích (nguyên văn 0–30s, 4 nhịp, loại A–E, điểm /12)

    py -3.13 -X utf8 src/hook_library.py add  rec.json [rec2.json ...]   # thêm/ghi đè theo video_id
    py -3.13 -X utf8 src/hook_library.py build                          # sinh lại HOOK_LIBRARY.md
    py -3.13 -X utf8 src/hook_library.py lane teinengo-real             # kiểu hook hợp 1 kênh của mình
"""
from __future__ import annotations

import datetime as dt, json, sys
from collections import defaultdict
from pathlib import Path

LIB = Path(r"E:\CLAUDE\YOUTUBE\HOOK_LIBRARY")
PAT, HOOKS, MD = LIB / "patterns.json", LIB / "hooks.jsonl", LIB / "HOOK_LIBRARY.md"
KINDS = {"A": "Biến cố bất thường", "B": "Câu nói sốc", "C": "Mâu thuẫn",
         "D": "Hậu quả chưa rõ nguyên nhân", "E": "Hé reveal 20–40%", "none": "Không có hook (vào thẳng nội dung)"}
REQ = ("video_id", "channel", "title", "views", "hook_0_30s", "beats", "kind", "patterns",
       "score_0_12", "why", "lanes_fit")


def load_hooks() -> dict[str, dict]:
    out = {}
    if HOOKS.exists():
        for line in HOOKS.read_text(encoding="utf-8").splitlines():
            if line.strip():
                r = json.loads(line)
                out[r["video_id"]] = r
    return out


def load_pat() -> dict:
    return json.loads(PAT.read_text(encoding="utf-8"))


def add(files):
    hooks, pat = load_hooks(), load_pat()
    known = {p["id"] for p in pat["patterns"]} | {k["id"] for k in pat["closers"]}
    for f in files:
        data = json.loads(Path(f).read_text(encoding="utf-8"))
        for r in data if isinstance(data, list) else [data]:
            miss = [k for k in REQ if k not in r]
            bad = [p for p in r["patterns"] + r.get("closers", []) if p not in known]
            if miss or bad or r["kind"] not in KINDS:
                sys.exit(f"✗ {r.get('video_id')}: thiếu {miss} · mã lạ {bad} · kind {r.get('kind')}")
            r.setdefault("analyzed_at", dt.date.today().isoformat())
            r.setdefault("url", f"https://www.youtube.com/watch?v={r['video_id']}")
            hooks[r["video_id"]] = r
            print(f"✓ {r['video_id']} {r['kind']} {r['patterns']} {r['score_0_12']}/12")
    HOOKS.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in hooks.values()),
                     encoding="utf-8")
    build()


def _ex(r):
    return (f"  - {r['views']:,} view · [{r['channel']}]({r['url']}) · 「{r['title'][:48]}」\n"
            f"    > {r['hook_0_30s'][:170]}")


def build():
    pat, hooks = load_pat(), load_hooks()
    by = defaultdict(list)
    for r in hooks.values():
        for p in r["patterns"] + r.get("closers", []):
            by[p].append(r)
    L = ["# HOOK LIBRARY — kho kiểu mở đầu video (sinh tự động, đừng sửa tay)", "",
         f"Cập nhật: {dt.date.today().isoformat()} · {len(hooks)} video đã phân tích · "
         f"{len(pat['patterns'])} kiểu hook · {len(pat['closers'])} thiết bị khoá hook.",
         "Sửa nội dung ở `patterns.json` / `hooks.jsonl` rồi chạy "
         "`py -3.13 -X utf8 E:\\CLAUDE\\YOUTUBE\\TRENDING-RESEARCH\\src\\hook_library.py build`.", "",
         "## Loại gốc A–E (khớp `hook_stage.py` của h2dev)", ""]
    L += [f"- **{k}** {v}" for k, v in KINDS.items()]
    L += ["", "## Bảng tra nhanh: kênh của mình → kiểu hook nên dùng", ""]
    lanes = defaultdict(list)
    for p in pat["patterns"]:
        for ln in p.get("lanes_fit", []):
            lanes[ln].append(p["id"])
    L += ["| Kênh (h2dev) | Kiểu hook hợp |", "|---|---|"]
    L += [f"| {ln} | {', '.join(ids)} |" for ln, ids in sorted(lanes.items())]
    for sec, key in (("Kiểu hook (mở đầu 0–30s)", "patterns"), ("Thiết bị khoá hook (30–90s)", "closers")):
        L += ["", f"## {sec}", ""]
        for p in pat[key]:
            ex = sorted(by.get(p["id"], []), key=lambda r: -r["views"])
            L += [f"### {p['id']} — {p['name']}" + (f"  · loại {p['kind']}" if p.get("kind") else ""),
                  "", f"**Cơ chế:** {p['mechanism']}", "", f"**Khuôn:** `{p['template']}`", ""]
            if p.get("when"):
                L += [f"**Dùng khi:** {p['when']}", ""]
            if p.get("avoid"):
                L += [f"**Tránh:** {p['avoid']}", ""]
            if p.get("lanes_fit"):
                L += [f"**Hợp kênh:** {', '.join(p['lanes_fit'])}", ""]
            L += [f"**Ví dụ thật ({len(ex)}):**"] + ([_ex(r) for r in ex[:6]] or ["  - (chưa có)"]) + [""]
    L += ["## Toàn bộ video đã phân tích (view giảm dần)", "",
          "| View | Kênh | Loại | Kiểu | Điểm | Tiêu đề |", "|--:|---|---|---|--:|---|"]
    for r in sorted(hooks.values(), key=lambda r: -r["views"]):
        L.append(f"| {r['views']:,} | {r['channel']} | {r['kind']} | {' '.join(r['patterns'] + r.get('closers', []))}"
                 f" | {r['score_0_12']} | [{r['title'][:40]}]({r['url']}) |")
    MD.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"→ {MD} ({len(hooks)} video)")


def lane(name):
    pat, hooks = load_pat(), load_hooks()
    for p in pat["patterns"]:
        if name in p.get("lanes_fit", []):
            n = sum(p["id"] in r["patterns"] for r in hooks.values())
            print(f"{p['id']} {p['name']} ({n} ví dụ)\n   khuôn: {p['template']}")


if __name__ == "__main__":
    cmd, *rest = sys.argv[1:] or ["build"]
    {"add": lambda: add(rest), "build": build, "lane": lambda: lane(rest[0])}[cmd]()
