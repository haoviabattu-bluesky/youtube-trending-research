# -*- coding: utf-8 -*-
"""Parser THUẦN (không mạng) cho 5 nguồn trend → list signal {source, keyword, rank, traffic, url, extra}.
Mẫu thật lưu ở tests/fixtures/news_radar/ (tải 17/10/2026) — đổi parser thì chạy pytest trước.

- google_trends : RSS trends.google.com/trending/rss?geo=JP — keyword + approx_traffic + ≤3 bài báo kèm
- google_news   : RSS news.google.com — tiêu đề "headline - 媒体"; link là redirect của Google
- yahoo_ranking : HTML news.yahoo.co.jp/ranking/access/news — thứ hạng truy cập + 媒体 + giờ
- x_trends24    : HTML trends24.in/japan — ~25 snapshot/giờ, mỗi snapshot 1 <ol class=trend-card__list>
- x_getdaytrends: HTML getdaytrends.com/japan — bảng top hiện tại (pos + tên)"""
from __future__ import annotations

import html
import re
import xml.etree.ElementTree as ET

HT = "{https://trends.google.com/trending/rss}"


def _traffic(s: str | None) -> int:
    m = re.search(r"([\d,.]+)\s*([KkMm]?)", s or "")
    if not m:
        return 0
    n = float(m.group(1).replace(",", ""))
    return int(n * {"k": 1_000, "m": 1_000_000}.get(m.group(2).lower(), 1))


def parse_google_trends(xml_text: str) -> list[dict]:
    root = ET.fromstring(xml_text)
    out = []
    for i, item in enumerate(root.iter("item"), 1):
        kw = (item.findtext("title") or "").strip()
        if not kw:
            continue
        news = []
        for n in item.findall(f"{HT}news_item"):
            news.append({"title": (n.findtext(f"{HT}news_item_title") or "").strip(),
                         "url": (n.findtext(f"{HT}news_item_url") or "").strip(),
                         "source": (n.findtext(f"{HT}news_item_source") or "").strip()})
        out.append({"source": "google_trends", "keyword": kw, "rank": i,
                    "traffic": _traffic(item.findtext(f"{HT}approx_traffic")),
                    "url": news[0]["url"] if news else None,
                    "extra": {"news": news, "pub": item.findtext("pubDate")}})
    return out


def parse_google_news(xml_text: str) -> list[dict]:
    root = ET.fromstring(xml_text)
    out = []
    for i, item in enumerate(root.iter("item"), 1):
        title = html.unescape((item.findtext("title") or "").strip())
        if not title:
            continue
        head, _, medium = title.rpartition(" - ")
        if not head:
            head, medium = title, ""
        out.append({"source": "google_news", "keyword": head.strip(), "rank": i, "traffic": None,
                    "url": (item.findtext("link") or "").strip(),
                    "extra": {"medium": medium.strip(), "pub": item.findtext("pubDate")}})
    return out


_YA_A = re.compile(r'<a href="(https://news\.yahoo\.co\.jp/articles/[^"]+)"[^>]*_cl_position:(\d+)[^>]*>(.*?)</a>', re.S)
_YA_TXT = re.compile(r"^(\d+)\s+(.+?)\s{2,}(\S+)\s+(\d+/\d+\(.\)\s*\d+:\d+)\s*$")


def parse_yahoo_ranking(html_text: str, category: str = "news") -> list[dict]:
    out, seen = [], set()
    for m in _YA_A.finditer(html_text):
        url, pos, inner = m.group(1), int(m.group(2)), m.group(3)
        txt = html.unescape(re.sub(r"<[^>]+>", "  ", inner))
        txt = re.sub(r"[ \t\r\n　]+", lambda mm: "  " if len(mm.group(0)) > 1 else " ", txt).strip()
        t = _YA_TXT.match(txt)
        if t:
            title, medium, when = t.group(2).strip(), t.group(3), t.group(4)
        else:
            parts = [p for p in re.split(r"\s{2,}", txt) if p]
            title = parts[1] if len(parts) > 1 and parts[0].isdigit() else (parts[0] if parts else "")
            medium, when = (parts[2] if len(parts) > 2 else ""), (parts[3] if len(parts) > 3 else "")
        if not title or url in seen:
            continue
        seen.add(url)
        out.append({"source": "yahoo_ranking", "keyword": title, "rank": pos, "traffic": None, "url": url,
                    "extra": {"medium": medium, "when": when, "category": category}})
    return out


_T24_CARD = re.compile(r"<h3 class=title data-timestamp=([\d.]+)>.*?<ol class=trend-card__list>(.*?)</ol>", re.S)
_T24_LI = re.compile(r'class=trend-link>(.*?)</a><span class=tweet-count data-count="([^"]*)"', re.S)


def parse_trends24(html_text: str, max_cards: int = 8) -> list[dict]:
    """Gộp các snapshot theo giờ: keyword nào xuất hiện ở nhiều snapshot = bền. rank = hạng tốt nhất,
    traffic = số tweet (nếu có), extra.hours = số snapshot có mặt trong `max_cards` gần nhất."""
    agg: dict[str, dict] = {}
    cards = _T24_CARD.findall(html_text)[:max_cards]
    for ts, body in cards:
        for pos, (name, cnt) in enumerate(_T24_LI.findall(body), 1):
            name = html.unescape(name).strip()
            if not name:
                continue
            a = agg.setdefault(name, {"rank": pos, "hours": 0, "count": 0, "first_ts": float(ts)})
            a["rank"] = min(a["rank"], pos)
            a["hours"] += 1
            a["count"] = max(a["count"], _traffic(cnt))
            a["first_ts"] = min(a["first_ts"], float(ts))
    return [{"source": "x_trends24", "keyword": k, "rank": a["rank"], "traffic": a["count"] or None,
             "url": "https://x.com/search?q=" + k,
             "extra": {"hours": a["hours"], "of": len(cards)}} for k, a in agg.items()]


_GDT_ROW = re.compile(r'<th scope="row" class="pos">(\d+)</th><td class="main"><a href="[^"]*">(.*?)</a>', re.S)


def parse_getdaytrends(html_text: str) -> list[dict]:
    out, seen = [], set()
    for pos, name in _GDT_ROW.findall(html_text):
        name = html.unescape(re.sub(r"<[^>]+>", "", name)).strip()
        if not name or name in seen:
            continue
        seen.add(name)
        out.append({"source": "x_getdaytrends", "keyword": name, "rank": int(pos), "traffic": None,
                    "url": "https://x.com/search?q=" + name, "extra": {}})
    return out
