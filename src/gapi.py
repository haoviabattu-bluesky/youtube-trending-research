# -*- coding: utf-8 -*-
"""Retry cho Google Sheets API."""
from __future__ import annotations

import random
import time

from gspread.exceptions import APIError

RETRY_CODES = (429, 500, 502, 503)


def retry_api(fn, *a, tries: int = 6, base: float = 2.0, **kw):
    """Sheets API giới hạn 60 read/phút/user — chạy liên tiếp là ăn 429 ngay.

    gspread KHÔNG tự retry. Đã dính thật 2026-09-09: lượt chạy đầy đủ chết giữa chừng
    vì 429 sau vài lượt liên tiếp. Backoff luỹ thừa + jitter, 6 lần ≈ chờ tối đa ~60s.
    """
    for i in range(tries):
        try:
            return fn(*a, **kw)
        except APIError as e:
            code = getattr(getattr(e, "response", None), "status_code", None)
            if code not in RETRY_CODES or i == tries - 1:
                raise
            time.sleep(base ** i + random.uniform(0, 1))
    raise RuntimeError("unreachable")


