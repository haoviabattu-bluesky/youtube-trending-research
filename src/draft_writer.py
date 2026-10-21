# -*- coding: utf-8 -*-
"""Viết NHÁP file dài (hồ sơ tập, MAU_*.md, báo cáo) bằng model ngoài (gate ext_draft, mặc định gpt-5.6-sol).

Đo 07–21/10: Claude tự viết file dài = 12% quota. Giờ Claude chỉ soạn yêu cầu + dữ liệu JSON, Sol viết,
Python soát rồi Claude đọc phần cảnh báo (không đọc lại cả file nếu không cần):
  - mọi [Dn] trong nháp phải có trong dữ liệu
  - số ≥2 chữ số trong nháp không thấy ở dữ liệu → cảnh báo (nghi bịa)
  - dòng có chữ Nhật mà không có chữ Việt → cảnh báo (luật dịch tiếng Việt bắt buộc)

    py -3.13 -X utf8 src/draft_writer.py --task "Viết HO_SO đề tài 生活保護 theo khung …" \
        --instr docs/KHUNG_HO_SO.md --data data/x/tu_lieu/tu_lieu.json data/x/cands.json --out data/x/HO_SO.md
"""
from __future__ import annotations

import argparse, json, re, sys, unicodedata
from decimal import Decimal, InvalidOperation
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ext_llm import ask_text  # noqa: E402

GATE, MAXDATA = "ext_draft", 90000
SYSTEM = ("Bạn là biên tập viên nghiên cứu cho kênh YouTube tiếng Nhật, viết bằng tiếng Việt. "
          "CHỈ dùng số liệu/sự kiện có trong DỮ LIỆU, mỗi số kèm mã [Dn] đúng như dữ liệu. Không có thì ghi "
          "'(chưa có nguồn)', không tự thêm số. Mọi tiêu đề/trích dẫn tiếng Nhật phải có bản dịch tiếng Việt đi trước, "
          "nguyên văn để trong ngoặc. Đường dẫn file ghi tuyệt đối. Trả về Markdown thuần, không bọc ```.")
JP = re.compile(r"[\u3040-\u30ff\u4e00-\u9fff]")
VI = re.compile(r"[a-zA-Zàáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđ]{2,}")
NUM = re.compile(r"\d[\d,.]*\d")


def _readings(n: str) -> set[str]:
    """Mọi cách đọc 1 số: kiểu Nhật/Anh (18,995 · 44.2) và kiểu Việt (18.995 · 44,2) → giá trị chuẩn.
    Model viết số kiểu Việt trong khi nguồn ghi kiểu Nhật → trước đây báo "số lạ" nhầm (đo 21/10: 10/10 giả)."""
    out = set()
    for t in (n.replace(",", ""), n.replace(".", "").replace(",", ".")):
        try:
            out.add(format(Decimal(t).normalize(), "f"))
        except InvalidOperation:
            pass
    return out


def check(draft: str, data_text: str) -> list[str]:
    warns = []
    d_ids = set(re.findall(r"\[(D\d+)\]", data_text)) | set(re.findall(r'"id":\s*"(D\d+)"', data_text))
    for d in sorted(set(re.findall(r"\[(D\d+)\]", draft)) - d_ids):
        warns.append(f"mã {d} không có trong dữ liệu")
    data_text = unicodedata.normalize("NFKC", data_text)
    known = {v for n in NUM.findall(data_text) for v in _readings(n)}
    plain = data_text.replace(",", "")
    no_paths = re.sub(r"[A-Za-z]:\\\S+|https?://\S+", " ", draft)  # số trong đường dẫn/URL không phải số liệu
    for n in dict.fromkeys(NUM.findall(no_paths)):
        if re.fullmatch(r"20\d\d", n) or _readings(n) & known:
            continue
        if n.replace(",", "") not in plain and n.replace(".", "").replace(",", ".") not in plain:
            warns.append(f"số {n} không thấy trong dữ liệu")
    for i, line in enumerate(draft.splitlines(), 1):
        if JP.search(line) and not VI.search(JP.sub("", line)):
            warns.append(f"dòng {i} chỉ có tiếng Nhật: {line.strip()[:60]}")
    return warns


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--task", required=True)
    ap.add_argument("--instr", default="")
    ap.add_argument("--data", nargs="*", default=[])
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    instr = Path(a.instr).read_text(encoding="utf-8") if a.instr else ""
    data = "\n\n".join(f"### {p}\n{Path(p).read_text(encoding='utf-8')}" for p in a.data)
    if len(data) > MAXDATA:
        sys.exit(f"dữ liệu {len(data):,} ký tự > {MAXDATA:,}: lọc bớt (vd chỉ tu_lieu, bỏ bi_loai) rồi chạy lại")
    prompt = f"NHIỆM VỤ:\n{a.task}\n\nKHUNG / HƯỚNG DẪN:\n{instr or '(không có)'}\n\nDỮ LIỆU:\n{data}"
    text, model = ask_text(GATE, prompt, system=SYSTEM)
    text = re.sub(r"^```(?:markdown|md)?\n|\n```\s*$", "", text.strip())
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text + f"\n\n<!-- nháp: {model} · Claude soát trước khi giao -->\n", encoding="utf-8")
    warns = check(text, data)
    print(f"→ {out} · {len(text):,} ký tự · {model} · {len(warns)} cảnh báo")
    for w in warns[:15]:
        print("  ⚠", w)


if __name__ == "__main__":
    main()
