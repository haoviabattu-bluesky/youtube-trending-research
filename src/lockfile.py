# -*- coding: utf-8 -*-
"""Chống 2 lượt chạy chồng nhau — chạy được cả Windows (Task Scheduler) lẫn Linux (systemd).

Lượt trước treo mà lượt sau vẫn nổ = 2 tiến trình cùng nện YouTube, dễ ăn bot-check.
`fcntl.flock` chỉ có trên Linux nên ở đây dùng lock file có PID + hạn tuổi, chạy mọi nơi.
"""
from __future__ import annotations

import os
import time
from pathlib import Path


def _alive(pid: int) -> bool:
    if pid <= 0:
        return False
    if os.name == "nt":
        import subprocess
        out = subprocess.run(["tasklist", "/FI", f"PID eq {pid}", "/NH"],
                             capture_output=True, text=True).stdout
        return str(pid) in out
    try:
        os.kill(pid, 0)
        return True
    except (ProcessLookupError, PermissionError) as e:
        return isinstance(e, PermissionError)


class RunLock:
    """`with RunLock(path) as ok:` — `ok is False` nghĩa là có lượt khác đang chạy."""

    def __init__(self, path: str | Path, max_age_s: int = 7200):
        self.path, self.max_age_s, self.held = Path(path), max_age_s, False

    def __enter__(self) -> bool:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if self.path.exists():
            try:
                pid, ts = self.path.read_text(encoding="utf-8").split(",")
                pid, ts = int(pid), float(ts)
            except Exception:
                pid, ts = -1, 0.0
            fresh = (time.time() - ts) < self.max_age_s
            if fresh and _alive(pid):
                return False
            # lock mồ côi (tiến trình chết / quá hạn) → chiếm lại
        self.path.write_text(f"{os.getpid()},{time.time()}", encoding="utf-8")
        self.held = True
        return True

    def __exit__(self, *exc) -> None:
        if self.held:
            try:
                self.path.unlink()
            except OSError:
                pass
        return None
