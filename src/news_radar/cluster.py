# -*- coding: utf-8 -*-
"""Gộp keyword 24h của 5 nguồn thành CỤM SỰ KIỆN bằng LLM (gate `news_cluster` trong config/models.yaml).
Đầu vào: signal gần nhất → bảng keyword (nguồn, hạng, traffic). Đầu ra: list cụm
{label_ja, label_vi, keywords[], category, sensational 1–5, is_news, q_fit, summary_vi}.
Keyword nóng mà model bỏ sót (Google Trends ≥1000 hoặc có ở ≥2 nguồn) → cụm đơn, không để mất."""
from __future__ import annotations

import hashlib
import json
import re
from collections import defaultdict

from hunt_v2.llm_client import LlmClient

CATEGORIES = ("政治", "事件", "災害", "経済", "芸能", "スポーツ", "社会", "国際", "その他")

PROMPT = """あなたは日本のニュース編集者です。以下は直近24時間に Google Trends / Google News / Yahoo!ニュース
アクセスランキング / X トレンドで観測されたキーワードです。これらを「同じ出来事・話題」ごとにグループ化してください。

ルール:
- 同じ人物・事件・発表・試合を指すキーワードは1つのクラスタにまとめる。
- keywords には与えられた文字列を一字一句そのまま入れる（創作しない）。1つのキーワードは1クラスタにだけ入れる。
- is_news=false: アニメ放送・誕生祭・商品販促・定期イベントのハッシュタグなど、ニュース性のないもの。
- category は次のいずれか: {cats}
- sensational (1–5): 一般視聴者が「衝撃・怒り・驚き」を感じる度合い。事件・不祥事・急死・炎上=4–5、普通の発表=2、日常ネタ=1。
- q_fit=true: 中国（政府・企業・世論）や海外が日本に対して何かをした／日本の対応が話題、という「日中・海外×日本」の構図があるもの。
- summary_vi: 1 câu tiếng Việt ≤25 từ nói rõ chuyện gì xảy ra (ai, làm gì, ở đâu). label_vi: tên cụm tiếng Việt ngắn.
- query_ja: YouTube検索用の短い語（1–3語、固有名詞中心、12文字以内。見出し全文は不可）。
- ニュース性のあるキーワードは漏れなくどこかのクラスタに入れること。出力は簡潔に（説明や重複を書かない）。
- ニュース性のないキーワード（アニメ放送・誕生祭・販促・定期番組）は出力に含めない。「雑多」「その他まとめ」のような
  寄せ集めクラスタを作らない（作ると最上位に来てしまう）。1クラスタ = 1つの出来事。

出力は JSON 配列のみ（説明文なし）。各要素:
{{"label_ja": "...", "label_vi": "...", "query_ja": "...", "keywords": ["..."], "category": "...", "sensational": 3,
  "is_news": true, "q_fit": false, "summary_vi": "..."}}

キーワード一覧（nguồn | hạng | traffic | keyword）:
{rows}
"""


SOURCE_CAP = {"x_trends24": 40, "x_getdaytrends": 15, "google_news": 30, "yahoo_ranking": 45, "google_trends": 25}


def keyword_table(signals: list, max_keywords: int) -> list[dict]:
    """Gom signal theo keyword (nhiều snapshot/nguồn) → 1 dòng/keyword, sắp theo điểm thô giảm dần.
    Mỗi nguồn chỉ lấy top SOURCE_CAP theo hạng (trends24 140 hashtag anime làm model ngập, output cụt — đo 17/10)."""
    agg: dict[str, dict] = {}
    for s in signals:
        d = dict(s)
        if int(d.get("rank") or 999) > SOURCE_CAP.get(d["source"], 999):
            continue
        try:
            d["extra"] = json.loads(d.get("extra") or "{}")
        except (TypeError, ValueError):
            d["extra"] = {}
        a = agg.setdefault(d["keyword"], {"keyword": d["keyword"], "sources": set(), "best_rank": 999,
                                          "traffic": 0, "signals": []})
        a["sources"].add(d["source"])
        a["best_rank"] = min(a["best_rank"], int(d.get("rank") or 999))
        a["traffic"] = max(a["traffic"], int(d.get("traffic") or 0))
        a["signals"].append(d)
    rows = list(agg.values())
    for r in rows:
        r["raw"] = len(r["sources"]) * 2 + (3 if r["traffic"] >= 1000 else 0) + max(0, 1 - r["best_rank"] / 50)
    rows.sort(key=lambda r: -r["raw"])
    return rows[:max_keywords]


def _rows_text(rows: list[dict]) -> str:
    return "\n".join(f"{'/'.join(sorted(r['sources']))} | {r['best_rank']} | {r['traffic'] or '-'} | {r['keyword']}"
                     for r in rows)


def _cluster_id(snap_date: str, label_ja: str) -> str:
    return snap_date + "-" + hashlib.sha1(label_ja.encode("utf-8")).hexdigest()[:8]


def _valid(c) -> bool:
    return (isinstance(c, dict) and isinstance(c.get("keywords"), list) and c.get("label_ja")
            and c.get("category") in CATEGORIES)


def cluster_keywords(client: LlmClient, rows: list[dict], snap_date: str, log=print) -> list[dict]:
    """Trả list cụm đã gắn cluster_id + signals của từng keyword. Lỗi LLM → mọi keyword nóng thành cụm đơn."""
    by_kw = {r["keyword"]: r for r in rows}
    prompt = PROMPT.format(cats="/".join(CATEGORIES), rows=_rows_text(rows))
    ids = [hashlib.sha1("|".join(sorted(by_kw)).encode()).hexdigest()[:12],
           hashlib.sha1(PROMPT.encode()).hexdigest()[:8]]  # cache key của LlmClient không chứa prompt → tự gắn hash
    res = client.call("news_cluster", prompt, ids, schema_name=None, expect_list=True)
    raw = res.parsed_response if res.ok else None
    if isinstance(raw, dict):  # model bọc {"clusters":[...]} → lấy list đầu tiên
        raw = next((v for v in raw.values() if isinstance(v, list)), None)
    raw = raw if isinstance(raw, list) else []
    if not raw:
        log(f"  ✗ LLM gộp cụm thất bại ({res.error}); dùng cụm đơn cho keyword nóng")
    clusters, used = [], set()
    for c in raw:
        if not _valid(c) or not c.get("is_news", True) or len(c["keywords"]) > 12:
            continue  # cụm "rác gom" (model vẫn hay tạo dù đã cấm) ăn 4 nguồn → heat 15 đứng đầu (đo 17/10)
        kws = [k for k in c["keywords"] if isinstance(k, str) and k in by_kw and k not in used]
        if not kws:
            continue
        used.update(kws)
        clusters.append(_build(c, kws, by_kw, snap_date))
    for r in rows:  # keyword nóng model bỏ sót → cụm đơn (giữ luật "không mất im lặng")
        k = r["keyword"]
        hot = r["traffic"] >= 1000 or len(r["sources"]) >= 2  # Yahoo top-10 đơn lẻ model đã thấy và bỏ = không phải tin
        if k in used or not hot:
            continue
        used.add(k)
        clusters.append(_build({"label_ja": k, "label_vi": k, "category": "その他", "sensational": 2,
                                "is_news": True, "q_fit": False, "summary_vi": "(model bỏ sót — cụm đơn)"},
                               [k], by_kw, snap_date))
    log(f"  ✓ {len(clusters)} cụm từ {len(rows)} keyword (model gộp {len(raw)}, cụm đơn {len(clusters) - len(raw)})")
    return clusters


def _build(c: dict, kws: list[str], by_kw: dict, snap_date: str) -> dict:
    by_source: dict[str, list[dict]] = defaultdict(list)
    for k in kws:
        for s in by_kw[k]["signals"]:
            by_source[s["source"]].append(s)
    return {"cluster_id": _cluster_id(snap_date, c["label_ja"]), "snap_date": snap_date,
            "label_ja": c["label_ja"], "label_vi": c.get("label_vi") or c["label_ja"],
            "category": c["category"], "sensational": int(c.get("sensational") or 3),
            "is_news": bool(c.get("is_news", True)), "q_fit": bool(c.get("q_fit", False)),
            "summary_vi": c.get("summary_vi") or "", "query_ja": short_query(c.get("query_ja") or c["label_ja"]),
            "keywords": kws, "by_source": dict(by_source)}


def short_query(label: str, max_len: int = 14) -> str:
    """Tiêu đề Yahoo dài → truy vấn YouTube ngắn: cắt ở dấu câu/ngoặc/khoảng trắng đầu tiên sau 4 ký tự.
    Đo 17/10: InnerTube trả 0 video với tiêu đề 40 ký tự, 8–19 video với tên riêng 5–8 ký tự."""
    s = re.sub(r"^[「」『』【】“”\"#\s　]+", "", label.strip())
    m = re.search(r"[、。「」『』【】（）()・:：,…！!？?\s　]", s[4:])
    if m:
        s = s[: 4 + m.start()]
    return s[:max_len].strip() or label[:max_len]
