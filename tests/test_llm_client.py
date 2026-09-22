# -*- coding: utf-8 -*-
"""llm_client: parse/repair, không nuốt lỗi, cache theo prompt_version, fallback chain."""
import json

from hunt_v2 import llm_client as lc
from hunt_v2 import llm_transport as tr

GOOD = {"semantic_fit": 80, "format_fit": 80, "viral_validity": 70, "learning_value": 75,
        "independent_confidence": 80, "fatal_issue": None, "disagreements": [], "decision": "PASS",
        "reason": "ok"}


def _client(models, con, tmp_path):
    return lc.LlmClient(models, con, tmp_path / "logs", "fp")


def test_repair_json_fence_and_prose():
    assert tr.repair_json("```json\n{\"a\": 1}\n```") == {"a": 1}
    assert tr.repair_json("Sure! Here: [{\"x\":1}] thanks") == [{"x": 1}]
    assert tr.repair_json("no json here") is None


def test_parse_ok_and_cached(models, mem_con, tmp_path, monkeypatch):
    calls = []

    def fake(prov, model, messages, timeout, max_tokens, temperature):
        calls.append(model)
        return "```json\n" + json.dumps(GOOD) + "\n```", {"prompt_tokens": 10, "completion_tokens": 5}

    monkeypatch.setattr(tr, "chat_http", fake)
    c = _client(models, mem_con, tmp_path)
    r1 = c.call("final_qc", "p", ["v1"], "final_qc")
    assert r1.ok and not r1.schema_errors and r1.parsed_response["decision"] == "PASS"
    r2 = c.call("final_qc", "p", ["v1"], "final_qc")
    assert r2.cached and len(calls) == 1
    assert c.stats["prompt_tokens"] == 10


def test_bad_json_sets_error_not_exception(models, mem_con, tmp_path, monkeypatch):
    monkeypatch.setattr(tr, "chat_http", lambda *a, **k: ("hoàn toàn không phải json", {}))
    c = _client(models, mem_con, tmp_path)
    r = c.call("final_qc", "p", ["v2"], "final_qc")
    assert not r.ok and r.error and "JSON" in r.error
    assert c.stats["errors"] == 1


def test_cache_miss_when_prompt_version_changes(models, mem_con, tmp_path, monkeypatch):
    monkeypatch.setattr(tr, "chat_http", lambda *a, **k: (json.dumps(GOOD), {}))
    c = _client(models, mem_con, tmp_path)
    k1 = c.cache_key("final_qc", "m", ["v"])
    models["gates"]["final_qc"]["prompt_version"] = "finalqc_v2"
    assert c.cache_key("final_qc", "m", ["v"]) != k1


def test_fallback_to_second_provider(models, mem_con, tmp_path, monkeypatch):
    seen = []

    def fake(prov, model, messages, timeout, max_tokens, temperature):
        seen.append(prov["base_url"])
        if "ramclouds" in prov["base_url"]:
            raise tr.TransportError("HTTP 503")
        return json.dumps({"video_id": "x"}), {}

    monkeypatch.setattr(tr, "chat_http", fake)
    monkeypatch.setattr(lc.time, "sleep", lambda s: None)
    c = _client(models, mem_con, tmp_path)
    r = c.call("semantic_format", "p", ["x"], None)
    assert r.ok and r.fallback_used and r.provider == "ns24"
    assert seen.count("https://ramclouds.me/v1") == 2  # 2 attempt rồi mới đổi


def test_schema_error_recorded_not_cached(models, mem_con, tmp_path, monkeypatch):
    bad = dict(GOOD, decision="UNCERTAIN")  # final_qc chỉ PASS|REJECT
    monkeypatch.setattr(tr, "chat_http", lambda *a, **k: (json.dumps(bad), {}))
    c = _client(models, mem_con, tmp_path)
    r = c.call("final_qc", "p", ["v3"], "final_qc")
    assert r.schema_errors
    assert c._cache_get(c.cache_key("final_qc", "gpt-5.6-sol", ["v3"])) is None
