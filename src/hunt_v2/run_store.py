# -*- coding: utf-8 -*-
"""Lưu output từng gate vào runs/<ngày>/<lane>/NN_<tên>.json + report.md (guide §4, §28, §29).

Không overwrite: chạy lại trong ngày thì file mới mang hậu tố giờ, file cũ giữ nguyên
để so được 2 lượt. `report.md` thì ghi đè (là bản tổng hợp của lượt mới nhất).
"""
from __future__ import annotations

import datetime as dt
import json
from pathlib import Path


class RunStore:
    def __init__(self, root: str | Path, snap_date: str, lane: str):
        self.dir = Path(root) / snap_date / lane
        self.dir.mkdir(parents=True, exist_ok=True)
        self.run_id = f"{snap_date}_{dt.datetime.now().strftime('%H%M%S')}"
        self.counts: dict[str, int] = {}
        self.notes: list[str] = []
        self.errors: list[str] = []

    def save(self, step_no: int, name: str, obj) -> Path:
        base = self.dir / f"{step_no:02d}_{name}.json"
        path = base
        if base.exists():
            path = self.dir / f"{step_no:02d}_{name}.{dt.datetime.now().strftime('%H%M%S')}.json"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(obj, f, ensure_ascii=False, indent=1, default=str)
        if isinstance(obj, list):
            self.counts[name] = len(obj)
        elif isinstance(obj, dict) and "kept" in obj and isinstance(obj["kept"], list):
            self.counts[name] = len(obj["kept"])
        return path

    def count(self, name: str, n: int) -> None:
        self.counts[name] = n

    def note(self, msg: str) -> None:
        self.notes.append(msg)

    def error(self, msg: str) -> None:
        self.errors.append(msg)

    def write_report(self, lane_label: str, top: list[dict], rejections: dict[str, int],
                     llm_stats: dict | None = None, shadow: list[dict] | None = None) -> Path:
        lines = [f"# Video Hunt V2 — {lane_label}", f"run_id: {self.run_id}", ""]
        lines.append("## Phễu")
        for k, v in self.counts.items():
            lines.append(f"- {k}: {v}")
        lines += ["", "## Lý do loại nhiều nhất"]
        for k, v in sorted(rejections.items(), key=lambda x: -x[1])[:12]:
            lines.append(f"- {k}: {v}")
        if llm_stats:
            lines += ["", "## LLM"]
            for k, v in llm_stats.items():
                lines.append(f"- {k}: {v}")
        if self.errors:
            lines += ["", "## Lỗi"] + [f"- {e}" for e in self.errors]
        if self.notes:
            lines += ["", "## Ghi chú"] + [f"- {n}" for n in self.notes]
        lines += ["", "## Top ứng viên V2"]
        for i, c in enumerate(top, 1):
            lines.append(f"{i}. https://youtu.be/{c['video_id']} — {c.get('title', '')[:70]}")
            lines.append(f"   final={c.get('final_score')} viral={c.get('viral', {}).get('viral_score')} "
                         f"type={c.get('viral', {}).get('viral_type')} "
                         f"topic={c.get('semantic', {}).get('topic_match')} "
                         f"fmt={c.get('format', {}).get('format_class')} "
                         f"opp={c.get('opportunity', {}).get('opportunity_score')} "
                         f"qc={c.get('final_qc', {}).get('decision')} "
                         f"flags={c.get('flags')}")
            why = c.get("opportunity", {}).get("why_viral") or []
            if why:
                lines.append(f"   why_viral: {', '.join(map(str, why))[:200]}")
        if shadow:
            lines += ["", "## So sánh OLD vs V2 (guide §31)", "| video | old | v2 | human |", "|---|---|---|---|"]
            for s in shadow:
                lines.append(f"| {s['video_id']} | {s['old']} | {s['v2']} | {s.get('human', '')} |")
        path = self.dir / "report.md"
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return path
