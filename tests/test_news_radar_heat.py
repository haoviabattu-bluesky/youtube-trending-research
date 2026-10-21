# -*- coding: utf-8 -*-
"""Điểm nóng NEWS RADAR: các bất biến phải giữ khi chỉnh ngưỡng."""
from news_radar import heat as H

CFG = {"source_weight": {"google_trends": 1.0, "google_news": 0.6, "yahoo_ranking": 1.0,
                         "x_trends24": 0.8, "x_getdaytrends": 0.6},
       "multi_source_bonus": {2: 1.5, 3: 2.0, 4: 2.5},
       "velocity_cap": 3.0, "supply_view_unit": 10000, "sensational_floor": 0.6}


def test_google_trends_log_scale():
    assert H.source_score("google_trends", [{"rank": 1, "traffic": 100}]) == 1.0
    assert abs(H.source_score("google_trends", [{"rank": 1, "traffic": 10000}]) - 3.0) < 1e-9


def test_multi_source_beats_single_source():
    one = H.heat_of({"google_trends": [{"rank": 1, "traffic": 5000}]}, CFG)[0]
    two = H.heat_of({"google_trends": [{"rank": 1, "traffic": 5000}],
                     "yahoo_ranking": [{"rank": 30}]}, CFG)[0]
    assert two > one * 1.5


def test_new_event_gets_fresh_velocity_and_cap():
    assert H.velocity_of(5.0, None, 3.0) == 1.5
    assert H.velocity_of(9.0, 1.0, 3.0) == 3.0
    assert H.velocity_of(2.0, 4.0, 3.0) == 0.5


def test_gap_shrinks_when_supply_grows():
    g0 = H.gap_of(0, 0, 10000)
    g1 = H.gap_of(3, 50_000, 10000)
    g2 = H.gap_of(40, 2_000_000, 10000)
    assert g0 == 1.5 and g0 > g1 > g2 >= 0.5
    assert H.gap_of(28, 1_900_000, 10000) == 0.5     # 片山さつき 17/10: bão hoà nhưng không dưới 0.5


def test_final_penalises_non_news_and_rewards_sensational():
    base = dict(heat=4.0, velocity=1.5, gap=1.0, cfg=CFG)
    assert H.final_of(sensational=5, is_news=True, **base) > H.final_of(sensational=1, is_news=True, **base)
    assert H.final_of(sensational=3, is_news=False, **base) == H.final_of(sensational=3, is_news=True, **base) / 2


def test_trends24_persistence_bonus():
    short = H.source_score("x_trends24", [{"rank": 5, "extra": {"hours": 1, "of": 8}}])
    long_ = H.source_score("x_trends24", [{"rank": 5, "extra": {"hours": 8, "of": 8}}])
    assert long_ - short > 0.8
