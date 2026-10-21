# -*- coding: utf-8 -*-
"""Parser NEWS RADAR chạy trên mẫu thật tải 17/10/2026 (tests/fixtures/news_radar/)."""
from pathlib import Path

from news_radar import parsers as P

FX = Path(__file__).resolve().parent / "fixtures" / "news_radar"


def _read(name):
    return (FX / name).read_text(encoding="utf-8")


def test_google_trends_has_keywords_traffic_and_news():
    rows = P.parse_google_trends(_read("gtrends.xml"))
    assert len(rows) >= 10
    r = rows[0]
    assert r["source"] == "google_trends" and r["keyword"] and r["rank"] == 1
    assert any(x["traffic"] >= 5000 for x in rows)          # "5000+" → 5000
    assert any(x["extra"]["news"] for x in rows)
    assert all(n["url"].startswith("http") for x in rows for n in x["extra"]["news"])


def test_google_news_splits_headline_and_medium():
    rows = P.parse_google_news(_read("gnews.xml"))
    assert len(rows) >= 20
    assert all(r["url"].startswith("https://news.google.com/") for r in rows)
    assert any(r["extra"]["medium"] for r in rows)
    assert all(" - " not in r["keyword"][-12:] for r in rows)


def test_yahoo_ranking_title_medium_time():
    rows = P.parse_yahoo_ranking(_read("yahoo_access.html"))
    assert len(rows) >= 40
    assert rows[0]["rank"] == 1 and rows[0]["url"].startswith("https://news.yahoo.co.jp/articles/")
    assert not rows[0]["keyword"][0].isdigit()               # rank đã tách khỏi tiêu đề
    assert sum(1 for r in rows if r["extra"]["medium"]) >= 35
    assert sum(1 for r in rows if "/" in r["extra"]["when"]) >= 35


def test_trends24_aggregates_hours():
    rows = P.parse_trends24(_read("trends24.html"), max_cards=8)
    assert len(rows) >= 30
    assert max(r["extra"]["hours"] for r in rows) >= 2       # có keyword bền qua nhiều snapshot
    assert all(r["extra"]["of"] == 8 for r in rows)
    assert min(r["rank"] for r in rows) == 1


def test_getdaytrends_rows():
    rows = P.parse_getdaytrends(_read("getdaytrends.html"))
    assert len(rows) >= 10 and rows[0]["rank"] == 1   # trang có nhiều bảng trùng tên, sau dedupe còn ~15
    assert all(r["keyword"] for r in rows)


def test_traffic_parse():
    assert P._traffic("5000+") == 5000 and P._traffic("1,000+") == 1000
    assert P._traffic("12K") == 12000 and P._traffic("") == 0
