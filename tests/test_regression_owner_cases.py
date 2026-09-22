# -*- coding: utf-8 -*-
"""Guide §40/§41 — chạy toàn bộ chuỗi gate (không discovery/enrich/API) trên fixture cố định
với LLM stub. Mọi lỗi owner đã bắt được phải bị chặn ở ĐÚNG gate — vĩnh viễn.

Chạy thật với model (tốn tiền, cần key): py -3.13 -X utf8 -m pytest tests -m live
"""
import pytest

from hunt_v2 import final_qc, hard_filter, opportunity_gate, ranker, semantic_format_gate, viral_engine

FLAGS = {"semantic_gate": True, "format_gate": True, "opportunity_gate": True, "final_qc": True}


def _canned(cases):
    sf, op, qc = {}, {}, {}
    for c in cases["cases"]:
        st = c.get("stub") or {}
        vid = c["row"]["video_id"]
        if "semantic" in st:
            sf[vid] = {"semantic": st["semantic"], "format": st["format"]}
        if "opportunity" in st:
            op[vid] = st["opportunity"]
        if "final_qc" in st:
            qc[vid] = st["final_qc"]
    return {"semantic_format": sf, "opportunity": op, "final_qc": qc}


def run_pipeline(cases, lane, rules, client):
    rows = [dict(c["row"]) for c in cases["cases"]]
    kept, rejected = hard_filter.apply(rows, lane, rules, set(), [], lane.all_queries["core_tags"])
    semantic_format_gate.run(kept, lane, client, rules, FLAGS)
    alive = [c for c in kept if c["semantic_pass"] and c["format_pass"]]
    baselines = {c["row"]["channel_id"]: c.get("baseline") for c in cases["cases"]}
    viral_engine.score(alive, baselines, rules)
    short = sorted([c for c in alive if c["viral"]["viral_pass"]],
                   key=lambda c: c["viral"]["viral_score"], reverse=True)[: rules["opportunity"]["shortlist_n"]]
    opportunity_gate.run(short, lane, client, rules, True)
    qc_short = [c for c in short if c["opportunity"].get("decision") in ("PASS", "UNCERTAIN")]
    final_qc.run(qc_short, lane, client, True)
    selected, shadow = ranker.rank(alive, rules, lane.lane_id)
    return {"rejected": {r["video_id"]: r["reason"] for r in rejected},
            "kept": {c["video_id"]: c for c in kept}, "selected": [c["video_id"] for c in selected],
            "shadow": shadow}


@pytest.fixture
def result(cases, lane_satori, rules, stub_client_factory):
    return run_pipeline(cases, lane_satori, rules, stub_client_factory(_canned(cases)))


def test_every_pass_case_is_selectable(cases, result):
    expected_pass = {c["row"]["video_id"] for c in cases["cases"] if c["expected"] == "PASS"}
    # pick_per_lane=2 nên không phải tất cả vào selected, nhưng tất cả phải đủ 4 cờ và không bị chặn
    for vid in expected_pass:
        c = result["kept"][vid]
        assert c["semantic_pass"] and c["format_pass"] and c["viral"]["viral_pass"], vid
        assert c.get("final_qc_pass"), vid
    assert set(result["selected"]) <= expected_pass and len(result["selected"]) == 2


@pytest.mark.parametrize("gate", ["hard_filter", "semantic", "format", "opportunity", "viral_or_qc"])
def test_reject_cases_blocked_at_expected_gate(cases, result, gate):
    for c in cases["cases"]:
        if c["expected"] != "REJECT" or c["expected_gate"] != gate:
            continue
        vid = c["row"]["video_id"]
        assert vid not in result["selected"], c["id"]
        if gate == "hard_filter":
            assert vid in result["rejected"], c["id"]
            continue
        k = result["kept"][vid]
        if gate == "semantic":
            assert k["semantic"]["decision"] == "REJECT", c["id"]
        elif gate == "format":
            assert k["format"]["decision"] == "REJECT", c["id"]
        elif gate == "opportunity":
            assert k["opportunity"]["decision"] == "REJECT", c["id"]
            assert "NEWS_DEPENDENCY" in k["opportunity"]["fatal_flags"]
        elif gate == "viral_or_qc":
            assert (not k["viral"]["viral_pass"]) or (not k.get("final_qc_pass")), c["id"]


def test_owner_cases_are_present(cases):
    """Case owner bắt được phải luôn còn trong fixture — xoá là test fail."""
    owner = {c["id"] for c in cases["cases"] if c.get("owner_case")}
    assert {"police_bodycam_talkshow", "wrong_niche_tag_match", "celebrity", "disney_la_placename",
            "chinese_language", "live_camera"} <= owner


def test_gate_error_never_passes(cases, lane_satori, rules, stub_client_factory):
    """LLM lỗi (không canned) → decision ERROR → không PASS (guide §33)."""
    client = stub_client_factory({"semantic_format": {}, "opportunity": {}, "final_qc": {}})
    r = run_pipeline(cases, lane_satori, rules, client)
    assert r["selected"] == []
    assert all(c["semantic"]["decision"] == "ERROR" for c in r["kept"].values())


def test_final_qc_disabled_blocks_selection(cases, lane_satori, rules, stub_client_factory):
    client = stub_client_factory(_canned(cases))
    rows = [dict(c["row"]) for c in cases["cases"] if c["expected"] == "PASS"]
    kept, _ = hard_filter.apply(rows, lane_satori, rules, set(), [], [])
    semantic_format_gate.run(kept, lane_satori, client, rules, FLAGS)
    viral_engine.score(kept, {c["row"]["channel_id"]: c.get("baseline") for c in cases["cases"]}, rules)
    opportunity_gate.run(kept, lane_satori, client, rules, True)
    final_qc.run(kept, lane_satori, client, enabled=False)
    selected, shadow = ranker.rank(kept, rules, "L")
    assert selected == [] and len(shadow) == len(rows)


def test_gapfill_rescues_videos_dropped_by_model(cases, lane_satori, rules, stub_client_factory):
    """Model trả JSON hợp lệ nhưng BỎ BỚT video trong lô → phải hỏi lại, không để thành ERROR.
    Đo thật 2026-09-22: 39/200 (20%) bị bỏ im lặng."""
    canned = _canned(cases)
    dropped = "OK000000001"
    state = {"first": True}

    class DroppingClient(type(stub_client_factory({}))):
        def call(self, gate, prompt, ids, schema_name, expect_list=False, system=None, use_cache=True):
            if gate == "semantic_format" and state["first"]:
                state["first"] = False
                ids = [v for v in ids if v != dropped]      # lô đầu: nuốt mất 1 video
            return super().call(gate, prompt, ids, schema_name, expect_list, system, use_cache)

    client = DroppingClient(stub_client_factory({}).cfg, canned)
    rows = [dict(c["row"]) for c in cases["cases"]]
    kept, _ = hard_filter.apply(rows, lane_satori, rules, set(), [], [])
    semantic_format_gate.run(kept, lane_satori, client, rules, FLAGS)
    c = next(c for c in kept if c["video_id"] == dropped)
    assert c["semantic"]["decision"] != "ERROR", "video bị bỏ sót phải được hỏi lại"
    assert "GAPFILL_RETRIED" in c["flags"]
