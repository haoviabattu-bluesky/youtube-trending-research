# -*- coding: utf-8 -*-
"""Brief ngày: LLM (gate `news_brief`) viết cho từng cụm top N: tiêu đề JP+VI, vì sao nóng, góc kể,
rủi ro, còn nóng bao lâu → markdown 1 file/ngày cho MG_STUDIO lane Q + JSON cùng tên.
Mọi tiêu đề/trích dẫn tiếng Nhật PHẢI kèm nghĩa Việt (luật dich-tieng-viet-bat-buoc)."""
from __future__ import annotations

import datetime as dt
import hashlib
import json
from pathlib import Path

PROMPT = """Bạn là biên tập viên chọn đề tài cho kênh YouTube tiếng Nhật dạng TIN TỨC (faceless, 8–12 phút, motion
graphics + ảnh báo). Kênh làm 3–5 video/ngày nên chỉ chọn đề tài THẬT nóng. Dưới đây là 1 cụm sự kiện đang viral
ở Nhật kèm tín hiệu đo được, video YouTube đã có trong 24–48h (CUNG), và trích đoạn bài báo gốc.

Cụm: {label_ja} ({label_vi}) · thể loại {category} · giật gân {sensational}/5 · q_fit={q_fit}
Tóm tắt: {summary_vi}
Tín hiệu: {signals}
Cung YouTube 24–48h: {supply_n} video, tổng {supply_views} view. Top: {supply_top}
Trích bài gốc:
{evidence}

Trả JSON duy nhất (không giải thích):
{{"title_ja": "tiêu đề YouTube tiếng Nhật ≤40 ký tự, có số/đối lập nếu có thật",
  "title_vi": "nghĩa tiếng Việt của title_ja",
  "why_hot_vi": "2 câu tiếng Việt: vì sao đang nóng, nguồn nào đẩy (Yahoo/X/Google), dân thường quan tâm gì",
  "angle_vi": "góc kể đề xuất 2–3 câu: mở bằng chi tiết nào, mạch 3 chặng, câu chốt",
  "facts": ["3–6 dữ kiện CÓ TRONG trích đoạn (số, tên, mốc giờ) kèm tên báo — không bịa, không có thì ghi ít"],
  "risk_vi": "rủi ro: người thật tên thật/đang điều tra/bản quyền ảnh/chính trị nhạy cảm — 1–2 câu",
  "freshness_h": 24,
  "verdict": "LÀM NGAY | LÀM NẾU CÒN SLOT | BỎ",
  "verdict_vi": "1 câu lý do"}}
freshness_h = số giờ ước tính đề tài còn nóng (6 / 24 / 72 / 168).
Khán giả: dân thường Nhật 40–70 tuổi xem tin giật gân, vụ án, chính trị gây tranh cãi, scandal, tiền bạc đời sống.
Luật verdict:
- LÀM NGAY: tin lớn nhất ngày hoặc giật gân ≥4, còn nóng ≥24h, có ≥3 dữ kiện trong trích đoạn. Cung bão hoà (>20 video,
  >1 triệu view) KHÔNG phải lý do BỎ — đó là bằng chứng cầu rất lớn; khi đó angle_vi PHẢI nêu góc KHÁC các video đã có
  (ví dụ: bối cảnh ít ai nói, con số, phản ứng nước ngoài, "chuyện gì xảy ra tiếp").
- LÀM NẾU CÒN SLOT: tin thật nhưng tầm trung, hoặc còn thiếu dữ kiện.
- BỎ: không phải tin (lịch phát sóng/khuyến mãi/clip đời sống cá nhân), chỉ 1 nguồn mỏng không có gì để kể 8 phút,
  hoặc rủi ro pháp lý cao (nạn nhân vị thành niên, người thường không phải nhân vật công chúng).
- q_fit=True → trong angle_vi nêu rõ góc "nước ngoài/TQ × Nhật" vì kênh đích (lane Q) kể theo khung đó."""


def _signals_text(cluster: dict) -> str:
    parts = []
    for src, sigs in cluster.get("by_source", {}).items():
        best = min(int(s.get("rank") or 999) for s in sigs)
        tr = max(int(s.get("traffic") or 0) for s in sigs)
        parts.append(f"{src}: {len(sigs)} tín hiệu, hạng tốt nhất {best}" + (f", traffic {tr}+" if tr else ""))
    return "; ".join(parts) or "(không có)"


def write_one(client, cluster: dict, supply: list[dict], evidence: list[dict], log=print) -> dict:
    ev = "\n".join(f"[{i}] {e.get('source','')} 「{e.get('title','')[:60]}」 {e['url']}\n{(e.get('excerpt') or '')[:1200]}"
                   for i, e in enumerate(evidence, 1) if e.get("status") == "ok") or "(chưa đọc được bài nào)"
    top = "; ".join(f"「{v.get('title','')[:40]}」{v.get('channel','')} {int(v.get('views') or 0):,}v"
                    for v in supply[:3]) or "(chưa có video)"
    prompt = PROMPT.format(label_ja=cluster["label_ja"], label_vi=cluster["label_vi"], category=cluster["category"],
                           sensational=cluster["sensational"], q_fit=cluster["q_fit"], summary_vi=cluster["summary_vi"],
                           signals=_signals_text(cluster), supply_n=len(supply),
                           supply_views=sum(int(v.get("views") or 0) for v in supply), supply_top=top, evidence=ev)
    ids = [cluster["cluster_id"], str(len(evidence)), str(len(supply)), hashlib.sha1(PROMPT.encode()).hexdigest()[:8]]
    res = client.call("news_brief", prompt, ids, schema_name=None)
    if res.ok and isinstance(res.parsed_response, dict):
        return res.parsed_response
    log(f"  ✗ brief LLM lỗi {cluster['label_ja'][:20]}: {res.error}")
    return {"title_ja": cluster["label_ja"], "title_vi": cluster["label_vi"], "why_hot_vi": cluster["summary_vi"],
            "angle_vi": "", "facts": [], "risk_vi": "", "freshness_h": 24, "verdict": "LÀM NẾU CÒN SLOT",
            "verdict_vi": "(LLM lỗi — chưa thẩm định)"}


def _fmt_views(n) -> str:
    return f"{int(n or 0):,}"


def render_markdown(snap_date: str, clusters: list[dict], packs: dict[str, dict], notes: list[str]) -> str:
    now = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
    L = [f"# NEWS RADAR — {snap_date} (sinh {now})",
         "", "Người đọc: Claude MG_STUDIO lane Q. Mỗi đề tài: tiêu đề JP (nghĩa VI) · vì sao nóng · góc kể · dữ kiện có nguồn · rủi ro.",
         "Điểm `final` = nóng × tốc độ × khoảng trống cung–cầu × giật gân. `q_fit` = có góc Nhật–Trung/nước ngoài (khung lane Q).",
         "Gói tư liệu JSON từng đề tài ở thư mục `packs/` cùng cấp. Chọn 3–5 đề tài `LÀM NGAY` đầu bảng.", ""]
    if notes:
        L += ["> " + n for n in notes] + [""]
    L += ["| # | final | verdict | Tiêu đề JP (VI) | thể loại | nguồn | cung 24–48h | q_fit |", "|---|---|---|---|---|---|---|---|"]
    for i, c in enumerate(clusters, 1):
        b = c.get("brief") or {}
        L.append(f"| {i} | {c['final']:.2f} | {b.get('verdict','?')} | {b.get('title_ja', c['label_ja'])} ({b.get('title_vi', c['label_vi'])}) "
                 f"| {c['category']} | {'/'.join(c.get('sources') or [])} | {c.get('supply_videos',0)} video · {_fmt_views(c.get('supply_views'))} view "
                 f"| {'✔' if c.get('q_fit') else ''} |")
    L.append("")
    for i, c in enumerate(clusters, 1):
        b = c.get("brief") or {}
        L += [f"## {i}. {b.get('title_ja', c['label_ja'])}", f"**VI:** {b.get('title_vi', c['label_vi'])}  ",
              f"**Điểm:** final {c['final']:.2f} · heat {c['heat']:.2f} · velocity {c['velocity']:.2f} · gap {c['gap']:.2f} · "
              f"giật gân {c['sensational']}/5 · còn nóng ~{b.get('freshness_h','?')}h · **{b.get('verdict','?')}** — {b.get('verdict_vi','')}",
              f"**Keyword:** {', '.join(c.get('keywords') or [])}", f"**Vì sao nóng:** {b.get('why_hot_vi','')}",
              f"**Góc kể:** {b.get('angle_vi','')}", f"**Rủi ro:** {b.get('risk_vi','')}"]
        facts = b.get("facts") or []
        if facts:
            L += ["**Dữ kiện có nguồn:**"] + [f"- [D{j}] {f}" for j, f in enumerate(facts, 1)]
        pk = packs.get(c["cluster_id"]) or {}
        ev = [e for e in pk.get("evidence", []) if e.get("status") == "ok"]
        if ev:
            L += ["**Bài gốc đã đọc:**"] + [f"- {e.get('source','')} 「{e.get('title','')[:70]}」 {e['url']}" for e in ev]
        sup = pk.get("supply", [])
        if sup:
            L += ["**Video đối thủ 24–48h (cung):**"] + [
                f"- {_fmt_views(v.get('views'))} view · {v.get('channel','')} · 「{v.get('title','')[:60]}」 https://youtu.be/{v['video_id']}"
                for v in sup[:5]]
        for h in pk.get("hooks", []):
            L.append(f"- hook {h['video_id']} ({h.get('via')}): {h.get('text','')[:300]}")
        L.append("")
    return "\n".join(L)


def write_files(snap_date: str, md: str, clusters: list[dict], run_dir: Path, lane_dir: Path | None) -> list[Path]:
    run_dir.mkdir(parents=True, exist_ok=True)
    out = [run_dir / f"{snap_date}.md"]
    out[0].write_text(md, encoding="utf-8")
    (run_dir / f"{snap_date}.json").write_text(
        json.dumps([{k: v for k, v in c.items() if k != "by_source"} for c in clusters], ensure_ascii=False, indent=1),
        encoding="utf-8")
    if lane_dir:
        lane_dir.mkdir(parents=True, exist_ok=True)
        p = lane_dir / f"{snap_date}.md"
        p.write_text(md, encoding="utf-8")
        out.append(p)
    return out
