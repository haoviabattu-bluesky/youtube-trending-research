# -*- coding: utf-8 -*-
import pytest

from hunt_v2 import schemas
from hunt_v2.lane_profile import load_lane
from conftest import ROOT

LANES = ["shinya_shiryoshitsu", "Lopezzapa68", "irogatatarukioku", "70dai-kenko", "teinengo-real",
         "teinengo-tanoshimi", "kokoro-kazoku", "sengoku-uragawa", "teinengo-fuufu"]


def test_rules_weights_sum_to_one(rules):
    assert abs(sum(rules["viral"]["weights"].values()) - 1.0) < 1e-9
    assert abs(sum(rules["ranking"]["weights"].values()) - 1.0) < 1e-9
    for k in ("hard_filter", "keyword_match", "semantic", "format", "baseline", "viral",
              "opportunity", "final_qc", "ranking", "discovery"):
        assert k in rules


def test_models_every_gate_has_chain(models):
    for gate, g in models["gates"].items():
        assert g["chain"], gate
        for prov, _model in g["chain"]:
            assert prov in models["providers"], (gate, prov)
        assert g["prompt_version"]


@pytest.mark.parametrize("lane_id", LANES)
def test_lane_profiles_load(lane_id):
    lane = load_lane(ROOT / "lanes", lane_id)
    assert lane is not None
    assert lane.profile["lane_id"] == lane_id
    assert lane.all_queries["core_tags"]
    assert lane.duration_min_s < lane.duration_max_s
    assert len(lane.fingerprint()) == 16


def test_lane_missing_returns_none():
    assert load_lane(ROOT / "lanes", "khong_ton_tai") is None


def test_fingerprint_changes_with_content(tmp_path):
    d = tmp_path / "x"
    d.mkdir()
    (d / "lane_profile.yaml").write_text("lane_id: x\n", encoding="utf-8")
    a = load_lane(tmp_path, "x").fingerprint()
    (d / "lane_profile.yaml").write_text("lane_id: x\nnotes: y\n", encoding="utf-8")
    assert load_lane(tmp_path, "x").fingerprint() != a


def test_schema_valid_semantic_coerces():
    obj = {"topic_match": "87", "audience_match": 70.0, "content_identity_match": 66,
           "market_language_match": 100, "semantic_confidence": 80, "decision": "pass",
           "reasons": None, "matched_topics": [], "mismatch_flags": []}
    assert schemas.validate("semantic", obj) == []
    assert obj["topic_match"] == 87 and obj["decision"] == "PASS" and obj["reasons"] == []


def test_schema_rejects_bad_enum_and_range():
    obj = {"format_class": "MOVIE", "real_person_present": "no", "host_driven": False,
           "interview_style": False, "news_style": False, "format_confidence": 140,
           "decision": "MAYBE", "reason": ""}
    errs = schemas.validate("format", obj)
    assert any("format_class" in e for e in errs)
    assert any("format_confidence" in e for e in errs)
    assert any("decision" in e for e in errs)


def test_missing_critical():
    assert "final_score" in schemas.missing_critical({"video_id": "x"})
