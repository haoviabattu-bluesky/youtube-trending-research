# -*- coding: utf-8 -*-
"""Xoay proxy cho InnerTube khi quét dồn dập dính 403/bot-check.

File `config/proxies.txt` (gitignored) — 1 dòng/proxy, `scheme://user:pass@host:port`,
dòng `#` là comment. Không có file/rỗng → `ProxyPool` trả None (chạy trực tiếp, không proxy).
"""
from __future__ import annotations

import time
from pathlib import Path


def load_proxies(path: str | Path) -> list[str]:
    p = Path(path)
    if not p.exists():
        return []
    out = []
    for line in p.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            out.append(line)
    return out


class ProxyPool:
    """Round-robin, đưa proxy lỗi vào "nghỉ" tạm thời thay vì loại vĩnh viễn
    (residential proxy có thể chỉ lỗi tạm do phiên hết hạn, không phải chết hẳn)."""

    def __init__(self, urls: list[str], cooldown_s: int = 120):
        self.urls = urls
        self.cooldown_s = cooldown_s
        self._i = 0
        self._resting: dict[str, float] = {}

    def __bool__(self) -> bool:
        return bool(self.urls)

    def mark_bad(self, url: str) -> None:
        self._resting[url] = time.time() + self.cooldown_s

    def next(self) -> str | None:
        if not self.urls:
            return None
        now = time.time()
        for _ in range(len(self.urls)):
            url = self.urls[self._i % len(self.urls)]
            self._i += 1
            if self._resting.get(url, 0) <= now:
                return url
        return self.urls[self._i % len(self.urls)]  # mọi proxy đều đang nghỉ — vẫn thử

    @staticmethod
    def to_requests_proxies(url: str) -> dict[str, str]:
        return {"http": url, "https": url}
