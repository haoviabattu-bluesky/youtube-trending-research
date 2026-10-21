# -*- coding: utf-8 -*-
"""Tiết kiệm quota (21/10/2026): gate ext_* không dùng Claude, cổng chống bịa của source_extract/draft_writer,
comment_topics cộng like bằng Python. Offline, 0 tiền."""
import json

import comment_topics as ct
import draft_writer as dw
import ext_llm
import source_extract as se
import title_classify as tc
from hunt_v2.llm_client import LlmResult

PAGE = "厚生労働省の調査によると、\n再雇用後に賃金が下がった人は 44.2％ だった。\n一方、変わらない人は28.0%。"


def test_ext_gates_claude_only_lite_full_name(models):
    """21/10 phương án 4: gate ext_* được dùng Claude, nhưng chỉ qua provider gọn (lite) + tên model đầy đủ."""
    ext = {g: v for g, v in models["gates"].items() if g.startswith("ext_")}
    assert set(ext) == {"ext_classify", "ext_hook", "ext_comments", "ext_extract", "ext_draft"}
    for g, v in ext.items():
        for p, m in v["chain"]:
            prov = models["providers"][p]
            assert prov["kind"] in ("openai_http", "claude_cli"), g
            if prov["kind"] == "claude_cli":
                assert prov.get("lite"), f"{g}: {p} không phải đường gọn"
                assert m.startswith("claude-") and m.count("-") >= 3, f"{g}: model {m} không đầy đủ tên"
        assert any(models["providers"][p]["kind"] == "openai_http" for p, _ in v["chain"]), f"{g}: thiếu dự phòng ns24"


def test_claude_lite_cmd_has_flags(models):
    from hunt_v2.llm_transport import claude_cli_cmd
    cmd = claude_cli_cmd(models["providers"]["claude_lite"], "claude-haiku-5-5", "low", "sp.txt")
    i = cmd.index("--tools")
    assert cmd[i + 1] == "" and "--strict-mcp-config" in cmd
    assert cmd[cmd.index("--system-prompt-file") + 1] == "sp.txt"
    assert cmd[cmd.index("--effort") + 1] == "low" and cmd[cmd.index("--model") + 1] == "claude-haiku-5-5"
    plain = claude_cli_cmd(models["providers"]["claude_cli"], "sonnet", None, "sp.txt")
    assert "--tools" not in plain and "--effort" not in plain


def test_cli_usage_reads_real_tokens():
    from hunt_v2.llm_transport import _cli_usage
    u = _cli_usage({"modelUsage": {"claude-haiku-5-5": {"inputTokens": 2, "cacheCreationInputTokens": 790,
                                                        "cacheReadInputTokens": 8, "outputTokens": 8}}})
    assert u["prompt_tokens"] == 800 and u["completion_tokens"] == 8


def test_verify_accepts_exact_quote_with_spacing_and_fullwidth():
    f = {"so_lieu": "44.2%", "nguyen_van": "再雇用後に賃金が下がった人は44.2%だった"}
    assert se.verify(f, PAGE) is None


def test_verify_rejects_invented_quote_and_wrong_number():
    assert "KHÔNG có" in se.verify({"so_lieu": "50%", "nguyen_van": "再雇用後に賃金が下がった人は50%だった"}, PAGE)
    assert "không nằm" in se.verify({"so_lieu": "28.0%", "nguyen_van": "再雇用後に賃金が下がった人は44.2%だった"}, PAGE)


def test_run_keeps_only_verified(tmp_path, monkeypatch):
    monkeypatch.setattr(se, "load_page", lambda u: ("調査", PAGE * 10, u))
    facts = {"facts": [{"so_lieu": "44.2%", "nguyen_van": "賃金が下がった人は 44.2％ だった", "y_nghia_vi": "x"},
                       {"so_lieu": "61%", "nguyen_van": "賃金が下がった人は61%", "y_nghia_vi": "bịa"}]}
    monkeypatch.setattr(se, "ask_json", lambda *a, **k: LlmResult(gate="ext_extract", model="m", parsed_response=facts))
    r = se.run("q", ["https://a.jp/x"], [], tmp_path, 5)
    assert [f["id"] for f in r["db"]["tu_lieu"]] == ["D5"]
    assert len(r["db"]["bi_loai"]) == 1 and (tmp_path / "nguon").exists()


def test_comment_aggregate_counts_likes_once():
    cm = [{"text": "a", "likes": 100}, {"text": "b", "likes": 10}, {"text": "c", "likes": 1}]
    topics = [{"chu_de": "T1", "idx": [0, 1, 99], "trich": [{"idx": 0, "vi": "A"}]},
              {"chu_de": "T2", "idx": [1, 2], "trich": []}]
    out = ct.aggregate(cm, topics)
    assert out[0]["chu_de"] == "T1" and out[0]["like_tong"] == 110 and out[0]["trich"][0]["likes"] == 100
    assert out[1]["like_tong"] == 1 and out[1]["so_cmt"] == 1


def test_draft_check_flags_unknown_code_number_and_bare_japanese():
    data = json.dumps({"tu_lieu": [{"id": "D1", "so_lieu": "44.2%"}]}, ensure_ascii=False)
    draft = "Tỉ lệ giảm lương là 44.2% [D1], còn 61.5% [D9].\n再雇用の現実\nVì sao (再雇用)"
    w = dw.check(draft, data)
    assert any("D9" in x for x in w) and any("61.5" in x for x in w)
    assert sum("chỉ có tiếng Nhật" in x for x in w) == 1


def test_classify_marks_missing_without_inventing(monkeypatch):
    rows = [{"id": "v1", "vi": "dịch", "hop": 8}]
    monkeypatch.setattr(tc, "ask_json", lambda *a, **k: LlmResult(gate="ext_classify", model="m", parsed_response=rows))
    vids, errs = tc.classify([{"video_id": "v1", "title": "t"}, {"video_id": "v2", "title": "u"}], "lane")
    assert vids[0]["llm"]["hop"] == 8 and vids[1]["llm"] == {} and "bỏ sót 1/2" in errs[0]


def test_ask_json_adds_prompt_hash_to_cache_ids(monkeypatch, tmp_path):
    seen = []

    class Fake:
        def call(self, gate, prompt, ids, schema, system=None, use_cache=True):
            seen.append(ids)
            return LlmResult(gate=gate, model="m", parsed_response={})

    monkeypatch.setattr(ext_llm, "client", lambda: Fake())
    monkeypatch.setattr(ext_llm, "LOGS", tmp_path)
    ext_llm.ask_json("ext_hook", "prompt A", ["v"])
    ext_llm.ask_json("ext_hook", "prompt B", ["v"])
    assert seen[0][-1] != seen[1][-1] and seen[0][0] == "v"


def test_draft_check_accepts_vietnamese_number_format():
    """21/10: số viết kiểu Việt (18.995 · 1,0%) cùng giá trị với nguồn kiểu Nhật (18,995 · 1.0％) không phải số lạ."""
    data = '{"id": "D1", "nguyen_van": "18,995人減少（1.0％減）、被保護実人員1,969,502人、４４．２％"}'
    draft = "Giảm 18.995 người, tức 1,0% [D1]; còn 1.969.502 người, 44,2% [D1]. File E:\\data\\lane_20261021\\a.md"
    assert dw.check(draft, data) == []
    warns = dw.check("Giảm 50.123 người, 77,7% [D1]", data)
    assert warns == ["số 50.123 không thấy trong dữ liệu", "số 77,7 không thấy trong dữ liệu"]
