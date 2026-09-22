# -*- coding: utf-8 -*-
"""hard_filter / baseline / viral_engine / ranker — thuần số, không LLM."""
import datetime as dt

from hunt_v2 import baseline, hard_filter, ranker, viral_engine
from hunt_v2.semantic_format_gate import code_decision_format, code_decision_semantic


def _row(**kw):
    base = {"video_id": "v", "title": "老後の人間関係で後悔した70代の実話【朗読】", "channel": "c",
            "channel_id": "UC1", "views": 50000, "likes": 500, "comments": 50, "duration_s": 1200,
            "age_hours": 100, "subs": 1000, "live_broadcast_content": "none"}
    base.update(kw)
    return base


# ---------- hard filter ----------
def test_keyword_match_is_feature_not_reject(lane_satori, rules):
    kws = ["老後 人間関係", "特殊詐欺 実話"]
    kept, rej = hard_filter.apply([_row(title="七十歳の夜に鳴った電話の話")], lane_satori, rules, set(), [], kws)
    assert len(kept) == 1 and kept[0]["keyword_match_score"] == 0.0
    kept, _ = hard_filter.apply([_row()], lane_satori, rules, set(), [], kws)
    assert 0 < kept[0]["keyword_match_score"] <= 1 and "人間関係" in kept[0]["matched_tags"]


def test_hard_filter_reasons(lane_satori, rules):
    rows = [_row(video_id="a", live_broadcast_content="live"),
            _row(video_id="b", title="🔴 ライブカメラ 老後"),
            _row(video_id="c", age_hours=24 * 40),
            _row(video_id="d", views=100),
            _row(video_id="e", duration_s=60),
            _row(video_id="f", title="退休後最後悔的三件事"),
            _row(video_id="g"),
            _row(video_id="h", channel_id="UCBLACK")]
    lane_satori.blacklist = {"channels": [{"channel_id": "UCBLACK"}]}
    kept, rej = hard_filter.apply(rows, lane_satori, rules, {"g"}, [], [])
    reasons = {r["video_id"]: r["reason"] for r in rej}
    assert reasons == {"a": "LIVE_OR_PREMIERE", "b": "LIVE_OR_PREMIERE", "c": "AGE_GT_MAX",
                       "d": "VIEWS_LT_MIN", "e": "DURATION_TOO_SHORT", "f": "NON_TARGET_LANGUAGE",
                       "g": "ALREADY_SELECTED", "h": "CHANNEL_BLACKLIST"}
    assert kept == []


# ---------- baseline ----------
def test_baseline_skips_shorts_and_floors_vph():
    now = dt.datetime.now(dt.timezone.utc)
    vids = [{"published_at": (now - dt.timedelta(days=10)).isoformat(), "views": 240, "duration_s": 1200},
            {"published_at": (now - dt.timedelta(days=20)).isoformat(), "views": 480, "duration_s": 1200},
            {"published_at": (now - dt.timedelta(days=5)).isoformat(), "views": 999999, "duration_s": 30}]
    b = baseline.baseline_from_videos(vids, min_vph_floor=2.0)
    assert b["n_videos"] == 2 and b["median_recent_views"] == 360
    assert b["median_recent_vph"] == 2.0  # 1 vph thật → floor 2.0


def test_baseline_cache_hit_no_api(mem_con, rules):
    class Api:
        def baseline_videos(self, *a, **k):
            raise AssertionError("không được gọi")
    from hunt_v2 import store_v2
    store_v2.save_hunt_baseline(mem_con, "UCx", {"median_recent_views": 10, "median_recent_vph": 3.0, "n_videos": 5})
    st = {}
    out = baseline.channel_baselines(Api(), mem_con, {"UCx": "UUx"}, rules, st)
    assert out["UCx"]["cached"] and st["cache_hit"] == 1


# ---------- viral engine ----------
def test_small_channel_breakout_vs_big_channel_normal(rules):
    cands = [_row(video_id="small", channel_id="S", views=2000, age_hours=48, likes=20, comments=2),
             _row(video_id="big", channel_id="B", views=300000, age_hours=48, likes=3000, comments=300),
             _row(video_id="mid", channel_id="M", views=40000, age_hours=48)]
    for c in cands:
        c["age_days"] = c["age_hours"] / 24
        c["flags"] = []
    bl = {"S": {"median_recent_vph": 2.0}, "B": {"median_recent_vph": 8000.0}, "M": None}
    viral_engine.score(cands, bl, rules)
    by = {c["video_id"]: c["viral"] for c in cands}
    assert by["small"]["breakout_ratio"] > rules["viral"]["breakout_extreme"]
    assert by["small"]["viral_type"] == "CHANNEL_BREAKOUT"
    assert by["big"]["breakout_ratio"] < 1 and by["big"]["viral_type"] in ("MARKET_TREND", "NORMAL")
    assert "BASELINE_MISSING" in cands[2]["flags"] and by["mid"]["breakout_score"] == 50.0
    # video 2k view không được đứng trên video 300k chỉ vì kênh nhỏ (absolute traction)
    assert by["big"]["absolute_view_score"] > by["small"]["absolute_view_score"]


def test_freshness_buckets(rules):
    vr = rules["viral"]
    assert viral_engine.freshness(1, vr) == (100.0, "0-3")
    assert viral_engine.freshness(20, vr) == (0.0, "15-30")
    s8, b8 = viral_engine.freshness(10, vr)
    assert b8 == "8-14" and 0 < s8 < 100


# ---------- decision mapping ----------
def test_semantic_decision_thresholds(rules):
    assert code_decision_semantic({"topic_match": 80, "audience_match": 70, "content_identity_match": 70}, rules) == "PASS"
    assert code_decision_semantic({"topic_match": 60, "audience_match": 90, "content_identity_match": 90}, rules) == "UNCERTAIN"
    assert code_decision_semantic({"topic_match": 90, "audience_match": 90, "content_identity_match": 40}, rules) == "REJECT"


def test_format_decision(lane_satori, rules):
    ok = {"format_class": "NARRATED_STORY", "format_confidence": 90, "host_driven": False, "interview_style": False}
    assert code_decision_format(ok, lane_satori, rules) == "PASS"
    assert code_decision_format(dict(ok, format_class="TALK_SHOW"), lane_satori, rules) == "REJECT"
    assert code_decision_format(dict(ok, host_driven=True), lane_satori, rules) == "REJECT"
    assert code_decision_format(dict(ok, format_confidence=30), lane_satori, rules) == "UNCERTAIN"


# ---------- ranker ----------
def _alive(vid, ch, title, viral=80, qc=True):
    return {"video_id": vid, "channel_id": ch, "title": title, "flags": [],
            "semantic_pass": True, "format_pass": True, "final_qc_pass": qc,
            "viral": {"viral_pass": True, "viral_score": viral, "freshness_score": 50,
                      "viral_type": "BOTH", "breakout_ratio": 3.0},
            "semantic": {"topic_match": 90, "audience_match": 90, "content_identity_match": 90},
            "format": {"format_class": "NARRATED_STORY"},
            "opportunity": {"decision": "PASS", "opportunity_score": 80, "why_viral": ["TOPIC"], "reason": "r"},
            "final_qc": {"decision": "PASS" if qc else "REJECT", "learning_value": 80}}


def test_ranker_requires_final_qc_and_distinct_channels(rules):
    cands = [_alive("a", "C1", "老後の友情の話 その一", 90),
             _alive("b", "C1", "老後の友情の話 その二", 88),
             _alive("c", "C2", "年金と孤独の夜", 70),
             _alive("d", "C3", "介護の実話", 95, qc=False)]
    selected, shadow = ranker.rank(cands, rules, "L")
    ids = [c["video_id"] for c in selected]
    assert ids == ["a", "c"]                      # b cùng kênh, d thiếu final_qc_pass
    # shadow_ranked vẫn xếp d (viral cao nhất) đầu — để audit thấy V2 "muốn" gì dù chưa đủ cờ
    assert shadow[0]["video_id"] == "d" and shadow[0]["shadow_rank"] == 1
    assert any(c["video_id"] == "b" and c["diversity_penalty"] >= 25 for c in shadow)
    assert selected[0]["selected_record"]["final_qc_pass"] is True


def test_ranker_opportunity_reject_blocks(rules):
    c = _alive("a", "C1", "x")
    c["opportunity"]["decision"] = "REJECT"
    assert ranker.rank([c], rules, "L")[0] == []
