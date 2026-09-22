# -*- coding: utf-8 -*-
"""H0 — hồ sơ lane cố định (guide §5, §6, §22). Đọc lanes/<lane_id>/*, KHÔNG regenerate mỗi run.

`fingerprint()` băm toàn bộ nội dung → đổi 1 ký tự là cache LLM cũ không dùng lại (guide §26).
Lane không có thư mục → trả None, runner bỏ qua lane đó (không lỗi).
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from pathlib import Path

import yaml

FILES = ("lane_profile.yaml", "query_expansion.json", "watch_channels.json",
         "positive_examples.json", "negative_examples.json", "blacklist.json")


@dataclass
class LaneProfile:
    lane_id: str
    profile: dict
    expansion: dict = field(default_factory=dict)
    watch_channels: list = field(default_factory=list)
    positives: list = field(default_factory=list)
    negatives: list = field(default_factory=list)
    blacklist: dict = field(default_factory=dict)
    _fp: str = ""

    # --- tiện ích cho gate ---
    @property
    def duration_min_s(self) -> int:
        return int(self.profile.get("duration", {}).get("min_minutes", 3)) * 60

    @property
    def duration_max_s(self) -> int:
        return int(self.profile.get("duration", {}).get("max_minutes", 60)) * 60

    @property
    def allowed_formats(self) -> list[str]:
        return [f.upper() for f in self.profile.get("allowed_formats", [])]

    @property
    def excluded_formats(self) -> list[str]:
        return [f.upper() for f in self.profile.get("excluded_formats", [])]

    @property
    def blacklist_channels(self) -> set[str]:
        return {c.get("channel_id") for c in self.blacklist.get("channels", []) if c.get("channel_id")}

    @property
    def all_queries(self) -> dict[str, list[str]]:
        """Nhóm query cho discovery (guide §7) — bỏ trùng, giữ thứ tự ưu tiên."""
        seen, out = set(), {}
        for grp in ("core_tags", "concept_queries", "format_queries", "audience_queries",
                    "story_queries"):
            qs = []
            for q in self.expansion.get(grp, []):
                q = q.strip()
                if q and q not in seen:
                    seen.add(q)
                    qs.append(q)
            out[grp] = qs
        return out

    def fingerprint(self) -> str:
        return self._fp

    def prompt_block(self) -> str:
        """Khối LANE_PROFILE dán vào prompt — YAML gọn, bỏ field kỹ thuật."""
        p = {k: v for k, v in self.profile.items() if k not in ("draft", "notes")}
        return yaml.safe_dump(p, allow_unicode=True, sort_keys=False).strip()

    def examples_block(self, n: int) -> str:
        pos = self.positives[:n]
        neg = self.negatives[:n]
        lines = ["POSITIVE EXAMPLES (videos that DO belong to this lane):"]
        lines += [f"- {e.get('title', '')} — {e.get('why', '')}" for e in pos] or ["- (none yet)"]
        lines.append("NEGATIVE EXAMPLES (videos that must be REJECTED even if keywords match):")
        lines += [f"- {e.get('pattern') or e.get('title', '')} — {e.get('reason', '')}"
                  for e in neg] or ["- (none yet)"]
        return "\n".join(lines)


def _read_json(p: Path, default):
    if not p.exists():
        return default
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def load_lane(lanes_dir: str | Path, lane_id: str) -> LaneProfile | None:
    d = Path(lanes_dir) / lane_id
    yml = d / "lane_profile.yaml"
    if not yml.exists():
        return None
    with open(yml, encoding="utf-8") as f:
        profile = yaml.safe_load(f) or {}
    h = hashlib.sha256()
    for name in FILES:
        p = d / name
        if p.exists():
            h.update(name.encode() + p.read_bytes())
    neg = _read_json(d / "negative_examples.json", {})
    pos = _read_json(d / "positive_examples.json", {})
    return LaneProfile(
        lane_id=lane_id, profile=profile,
        expansion=_read_json(d / "query_expansion.json", {}),
        watch_channels=_read_json(d / "watch_channels.json", []),
        positives=pos.get("positive_examples", pos) if isinstance(pos, dict) else pos,
        negatives=neg.get("negative_patterns", neg) if isinstance(neg, dict) else neg,
        blacklist=_read_json(d / "blacklist.json", {}),
        _fp=h.hexdigest()[:16],
    )
