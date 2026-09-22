# -*- coding: utf-8 -*-
import json
import sqlite3
import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from hunt_v2 import llm_client as lc  # noqa: E402
from hunt_v2.lane_profile import load_lane  # noqa: E402


@pytest.fixture
def rules():
    with open(ROOT / "config" / "hunt_rules.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f)


@pytest.fixture
def models():
    with open(ROOT / "config" / "models.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f)


@pytest.fixture
def lane_satori():
    return load_lane(ROOT / "lanes", "Lopezzapa68")


@pytest.fixture
def cases():
    with open(ROOT / "tests" / "fixtures" / "video_hunt_cases.json", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture
def mem_con():
    import store
    con = sqlite3.connect(":memory:")
    con.row_factory = sqlite3.Row
    con.executescript(store.SCHEMA)
    return con


class StubClient(lc.LlmClient):
    """LlmClient giả: trả response ghi sẵn theo gate/video_id — offline, 0 tiền."""

    def __init__(self, models_cfg, canned: dict, con=None, tmp_path=None):
        super().__init__(models_cfg, con, tmp_path or (ROOT / "logs" / "_test"), "fp-test")
        self.canned = canned      # {gate: {video_id: parsed}} ; gate "semantic_format" -> list items
        self.calls = []

    def call(self, gate, prompt, ids, schema_name, expect_list=False, system=None, use_cache=True):
        self.calls.append((gate, tuple(ids)))
        res = lc.LlmResult(gate=gate, model="stub", provider="stub", attempt=1)
        table = self.canned.get(gate, {})
        if expect_list:
            items = [dict(table[v], video_id=v) for v in ids if v in table]
            if not items:
                res.error = "stub: không có canned"
                return res
            res.parsed_response = items
            return res
        v = ids[0]
        if v not in table:
            res.error = "stub: không có canned"
            return res
        res.parsed_response = json.loads(json.dumps(table[v]))
        if schema_name:
            res.schema_errors = lc._validate(schema_name, res.parsed_response, False)
        return res


@pytest.fixture
def stub_client_factory(models, mem_con, tmp_path):
    def make(canned):
        return StubClient(models, canned, mem_con, tmp_path)
    return make
