# -*- coding: utf-8 -*-
"""Dựng báo cáo audit hook/tiêu đề/thumbnail cho các lane từ data/hook_audit_laneEFG/<X>/{videos_part*.json, lane_summary.json}.
Xuất 1 HTML (có ảnh, cho anh xem) + 1 Markdown (cho agent h2dev đọc).

    py -3.13 -X utf8 src/report_lane_audit.py --base data/hook_audit_laneEFG --lanes E_kenko F_real G_tano --out docs/HOOK_AUDIT_LANE_EFG
"""
from __future__ import annotations

import argparse, base64, glob, html, io, json, re
from pathlib import Path

from PIL import Image

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from md2html_lite import md2html  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
NAMES = {"E_kenko": "Lane E · kenko-chiebukuro", "F_real": "Lane F · teinengo-real", "G_tano": "Lane G · teinengo-tanoshimi"}


def S(x) -> str:
    if x is None:
        return ""
    if isinstance(x, (list, tuple)):
        return "; ".join(S(i) for i in x if i not in (None, ""))
    if isinstance(x, dict):
        return "; ".join(f"{k}: {S(v)}" for k, v in x.items() if v not in (None, "", []))
    return str(x)


E = lambda x: html.escape(S(x))


def chip(v):
    if isinstance(v, dict):
        v = [v.get("rating") or v.get("r") or v.get("score") or "", v.get("why") or v.get("reason") or ""]
    r = S(v[0] if isinstance(v, (list, tuple)) and v else v).strip()[:1].upper()
    c, t = {"K": ("ok", "Khớp"), "P": ("part", "Một phần"), "L": ("bad", "Lệch")}.get(r, ("na", "—"))
    why = v[1] if isinstance(v, (list, tuple)) and len(v) > 1 else ""
    return f'<span class="chip {c}">{t}</span> {E(why)}'


def img(p, w=420):
    try:
        im = Image.open(p).convert("RGB"); im.thumbnail((w, w * 9 // 16))
        b = io.BytesIO(); im.save(b, "JPEG", quality=70)
        return f'<img alt="" loading="lazy" src="data:image/jpeg;base64,{base64.b64encode(b.getvalue()).decode()}">'
    except Exception:
        return '<div class="noimg">không có ảnh</div>'


def tsec(x):
    if x in (None, "", "null"):
        return "—"
    try:
        s = float(x); return f"{int(s)//60}:{int(s)%60:02d}"
    except Exception:
        return E(x)


def load(d: Path):
    vids = []
    for f in sorted(d.glob("videos_part*.json")):
        vids += json.loads(f.read_text(encoding="utf-8"))
    ch = json.loads((d / "channel.json").read_text(encoding="utf-8"))
    summ = json.loads((d / "lane_summary.json").read_text(encoding="utf-8")) if (d / "lane_summary.json").exists() else {}
    by = {v["id"]: v for v in ch["videos"]}
    for v in vids:
        vid = v.get("video_id") or v.get("id")
        v["_vid"] = vid; v["_meta"] = by.get(vid, {})
    vids.sort(key=lambda v: -(float(v.get("view_per_day") or 0)))
    return ch, vids, summ


def thumb_txt(v):
    tl = v.get("thumb_lines") or []
    if isinstance(tl, list):
        return " ｜ ".join((f"[{x[0]}] {x[1]}" if isinstance(x, (list, tuple)) and len(x) > 1 else
                           (f"[{x.get('color', x.get('mau', ''))}] {x.get('text', x.get('chu', ''))}" if isinstance(x, dict) else S(x))) for x in tl)
    return S(tl)


def loops_html(v):
    L = v.get("open_loops") or []
    if not isinstance(L, list):
        return E(L)
    rows = "".join(f"<li><span lang=ja>{E(o.get('line_ja', o) if isinstance(o, dict) else o)}</span> — mở {tsec(o.get('t_open') if isinstance(o, dict) else None)} → trả {tsec(o.get('t_paid') if isinstance(o, dict) else None)} {E(o.get('note') if isinstance(o, dict) else '')}</li>" for o in L)
    return f"<ul>{rows}</ul>"


def video_card(v, d):
    vid = v["_vid"]; m = v["_meta"]
    tw = v.get("title_why")
    tw_html = ("<ul>" + "".join(f"<li>{E(x)}</li>" for x in tw) + "</ul>") if isinstance(tw, list) else f"<p>{E(tw)}</p>"
    return f'''<details class="v"><summary><span class="tier {E(v.get("tier"))}">{E(v.get("tier"))}</span> {float(v.get("view_per_day") or 0):,.0f}/ngày · {int(m.get("views") or v.get("views") or 0):,} view · <span lang=ja>{E(m.get("title") or v.get("title"))}</span></summary>
<div class="vg"><figure>{img(d / "thumbs" / f"{vid}.jpg")}<figcaption lang=ja>{E(thumb_txt(v))}</figcaption><p class="meta">{E(v.get("thumb_visual"))}</p></figure>
<div class="col"><p><a href="https://www.youtube.com/watch?v={vid}" target="_blank" rel="noopener">{vid}</a> · {E(m.get("published", "")[:10])} · {int(m.get("dur") or 0)//60} phút · mốc giây: {E(v.get("timing_source") or "thật")}</p>
<p class="lab">Tiêu đề gốc</p><p lang=ja class="big">{E(m.get("title") or v.get("title"))}</p>
<p class="lab">Vì sao tiêu đề ghi như vậy</p>{tw_html}<p class="meta">Khuôn: <span lang=ja>{E(v.get("title_formula"))}</span></p>
<p class="lab">Mô tả (đầu)</p><p lang=ja>{E(v.get("desc_first"))}</p>
<p>Thumbnail ↔ tiêu đề: {E(v.get("title_vs_thumb"))}</p><p>Hook ↔ tiêu đề: {chip(v.get("title_hook_link"))}</p><p>Thumbnail ↔ hook: {chip(v.get("thumb_hook_link"))}</p>
<p class="lab">Hook đầu — 30 giây đầu</p><blockquote lang=ja>{E(v.get("open_0_30_ja"))}</blockquote>
<p class="nums">câu chốt {tsec(v.get("key_t"))} · câu khoá {tsec(v.get("lock_t"))} · tự giới thiệu {tsec(v.get("intro_t"))} · lời hứa {tsec(v.get("promise_t"))} · {E(v.get("kind"))} {E(v.get("patterns"))} {E(v.get("closers"))} · {E(v.get("score_0_12"))}/12</p>
<p>Câu chốt: <span lang=ja>「{E(v.get("key_line_ja"))}」</span></p><p>Câu khoá: <span lang=ja>「{E(v.get("lock_line_ja"))}」</span></p>
<p class="lab">Hook của cả video</p><p><b>Lời hứa:</b> {E(v.get("video_promise"))}</p>
<p><b>Trả lời hứa:</b> {tsec(v.get("payoff_t"))} <span lang=ja>{E(v.get("payoff_ja"))}</span></p>
<p><b>Vòng mở:</b></p>{loops_html(v)}
<p><b>Cấu trúc:</b> {E(v.get("structure"))}</p><p><b>Giữ người giữa video:</b> {E(v.get("retention_devices"))}</p><p><b>Kết:</b> {E(v.get("ending_hook"))}</p>
<p><b>Vì sao giữ người:</b> {E(v.get("why"))}</p><p><b>Điểm yếu:</b> {E(v.get("weak"))}</p></div></div></details>'''


def lane_html(key, d):
    ch, vids, s = load(d)
    meta = ch["meta"]
    rows = "".join(f'<tr><td><span class="tier {E(v.get("tier"))}">{E(v.get("tier"))}</span></td><td class=num>{float(v.get("view_per_day") or 0):,.0f}</td>'
                   f'<td class=num>{int(v["_meta"].get("views") or 0):,}</td><td lang=ja>{E(v["_meta"].get("title"))}</td><td lang=ja>{E(thumb_txt(v))}</td>'
                   f'<td class=num>{tsec(v.get("key_t"))}</td><td>{E(v.get("video_promise"))}</td></tr>' for v in vids)
    f = s.get("title_formulas") or []
    ff = "".join(f'<div class="box f"><h4>{E(x.get("id"))} · {E(x.get("name"))}</h4><p>{E(x.get("mechanism"))}</p>'
                 f'<p class="tpl" lang=ja>{E(x.get("template_ja"))}</p><p class="meta">Dùng khi: {E(x.get("when"))}</p>'
                 f'<ul>{"".join(f"<li lang=ja>{E(e.get("title"))} — {E(e.get("vpd"))}/ngày</li>" for e in (x.get("examples") or []) if isinstance(e, dict))}</ul></div>' for x in f)
    pairs = "".join(f'<tr><td>{E(p.get("topic"))}</td><td lang=ja>{E((p.get("win") or {}).get("title"))} — <b>{E((p.get("win") or {}).get("vpd"))}</b></td>'
                    f'<td lang=ja>{E((p.get("lose") or {}).get("title"))} — {E((p.get("lose") or {}).get("vpd"))}</td><td>{E(p.get("why"))}</td></tr>' for p in s.get("title_pairs") or [])
    losers = "".join(f'<li><b>{E(x.get("pattern"))}</b> — {E(x.get("why"))} <span class=meta lang=ja>{E(x.get("examples"))}</span></li>' for x in s.get("title_losers") or [])
    hb = "".join(f'<div class="step"><span class="tm">{E(b.get("t"))}</span><h4>{E(b.get("name"))}</h4><p>{E(b.get("desc"))}</p><q lang=ja>{E(b.get("example_ja"))}</q></div>' for b in (s.get("hook_open") or {}).get("beats") or [])
    eps = ""
    for e in s.get("our_eps") or []:
        tp = "".join(f'<li lang=ja>{E(t.get("title_ja"))} <span class=meta>({E(t.get("formula"))}; {E(t.get("checked_in_script"))})</span></li>' for t in e.get("title_proposals") or [] if isinstance(t, dict))
        eps += f'''<article class="ep"><h4><span class="epno">{E(e.get("ep"))}</span> <span lang=ja>{E(e.get("title_now"))}</span></h4>
<p class="meta">{E(e.get("status"))} · mốc: {E(e.get("timing_source"))} · câu chốt {tsec(e.get("key_t"))} · lời hứa {tsec(e.get("promise_t"))} · ưu tiên {E(e.get("priority"))}</p>
<blockquote lang=ja>{E(S(e.get("hook_now_ja"))[:300])}</blockquote><p><b>Lời hứa cả video có giữ không:</b> {E(e.get("whole_video_promise_kept"))}</p>
<p class="lab">Vấn đề</p><ul>{"".join(f"<li>{E(x)}</li>" for x in e.get("problems") or [])}</ul>
<p class="lab good">Tiêu đề đề xuất</p><ul>{tp}</ul><p class="lab good">Sửa hook</p><ul>{"".join(f"<li>{E(x)}</li>" for x in e.get("hook_fix") or [])}</ul>
<p class="path">{E(e.get("dir"))}</p></article>'''
    pr = "".join(f'<li><b>{E(p.get("claim"))}</b><br><span class=k>Cơ chế:</span> {E(p.get("cause"))}<br><span class=k>Bằng chứng:</span> {E(p.get("evidence"))}<br><span class=k>Áp dụng:</span> {E(p.get("how"))}</li>' for p in s.get("principles") or [])
    th = s.get("thumbnail") or {}; hw = s.get("hook_whole") or {}; ho = s.get("hook_open") or {}
    cards = "".join(video_card(v, d) for v in vids)
    return f'''<section class="lane" id="{key}"><p class="eyebrow">{E(NAMES.get(key, key))}</p>
<h2><a href="https://www.youtube.com/channel/{E(meta.get("channel_id"))}" target="_blank" rel="noopener">{E(meta.get("name"))}</a> · {E(meta.get("subs"))} sub · {len(vids)} video đã phân tích</h2>
<h3>Công thức tiêu đề</h3><div class="grid">{ff or "<p class=meta>chưa có tổng hợp</p>"}</div>
<h3>Cặp cùng chủ đề: thắng vs thua</h3><div class="tablebox"><table><thead><tr><th>Chủ đề</th><th>Thắng</th><th>Thua</th><th>Vì sao</th></tr></thead><tbody>{pairs}</tbody></table></div>
<h3>Thứ làm tiêu đề thua</h3><ul>{losers}</ul><p class="meta">{E(s.get("title_over_time"))}</p>
<h3>Thumbnail</h3><div class="box"><p>{E(th.get("formula"))}</p><p><b>So với tiêu đề:</b> {E(th.get("vs_title"))}</p><p><b>Thắng vs thua:</b> {E(th.get("win_vs_lose"))}</p></div>
<h3>Hook đầu — khung theo giây</h3><div class="formula">{hb}</div><p>{E(ho.get("win_vs_lose"))}</p><p class="meta">{E(ho.get("counts"))}</p>
<h3>Hook của cả video</h3><div class="box"><p><b>Lời hứa:</b> {E(hw.get("promise"))}</p><p><b>Vòng mở:</b> {E(hw.get("open_loops"))}</p><p><b>Giữ người:</b> {E(hw.get("retention"))}</p><p><b>Kết:</b> {E(hw.get("ending"))}</p><p class="meta">{E(hw.get("counts"))}</p></div>
<h3>Tất cả video (xếp theo view/ngày)</h3><div class="tablebox"><table><thead><tr><th>Nhóm</th><th>View/ngày</th><th>View</th><th>Tiêu đề gốc</th><th>Chữ thumbnail</th><th>Câu chốt</th><th>Lời hứa cả video</th></tr></thead><tbody>{rows}</tbody></table></div>
<h3>Chi tiết từng video</h3>{cards}
<h3>Các tập của mình</h3>{eps or "<p class=meta>chưa có</p>"}
<h3>Nguyên tắc cho lane</h3><ol class="pr">{pr}</ol>
<p class="meta">Sửa lại so với phần video: {E(s.get("corrections"))}</p><p class="meta">Lưu ý dữ liệu: {E(s.get("caveats"))}</p></section>'''


def lane_md(key, d):
    ch, vids, s = load(d)
    L = [f"## {NAMES.get(key, key)} — {ch['meta'].get('name')} (https://www.youtube.com/channel/{ch['meta'].get('channel_id')})", ""]
    for x in s.get("title_formulas") or []:
        L.append(f"- **Công thức {S(x.get('id'))} {S(x.get('name'))}** — {S(x.get('mechanism'))} Khuôn: 「{S(x.get('template_ja'))}」 Dùng khi: {S(x.get('when'))}")
    for p in s.get("title_pairs") or []:
        L.append(f"- Cặp {S(p.get('topic'))}: THẮNG 「{S((p.get('win') or {}).get('title'))}」 {S((p.get('win') or {}).get('vpd'))}/ngày vs THUA 「{S((p.get('lose') or {}).get('title'))}」 {S((p.get('lose') or {}).get('vpd'))}/ngày — {S(p.get('why'))}")
    for x in s.get("title_losers") or []:
        L.append(f"- Thua: {S(x.get('pattern'))} — {S(x.get('why'))}")
    L += ["", f"Thumbnail: {S(s.get('thumbnail'))}", "", f"Hook đầu: {S(s.get('hook_open'))}", "", f"Hook cả video: {S(s.get('hook_whole'))}", "", "### Từng video", ""]
    for v in vids:
        m = v["_meta"]
        L += [f"#### {S(m.get('title'))} — https://www.youtube.com/watch?v={v['_vid']}",
              f"- {S(v.get('tier'))} · {float(v.get('view_per_day') or 0):,.0f} view/ngày · {int(m.get('views') or 0):,} view · đăng {S(m.get('published'))[:10]} · mốc giây {S(v.get('timing_source') or 'thật')}",
              f"- Chữ thumbnail: {thumb_txt(v)} · hình: {S(v.get('thumb_visual'))}",
              f"- Vì sao tiêu đề ghi như vậy: {S(v.get('title_why'))} · khuôn: {S(v.get('title_formula'))}",
              f"- Hook đầu: 「{S(v.get('open_0_30_ja'))}」 · chốt {S(v.get('key_t'))}s 「{S(v.get('key_line_ja'))}」 · khoá {S(v.get('lock_t'))}s 「{S(v.get('lock_line_ja'))}」",
              f"- Hook cả video: {S(v.get('video_promise'))} · trả ở {S(v.get('payoff_t'))}s · vòng mở: {S(v.get('open_loops'))}",
              f"- Hook↔tiêu đề {S(v.get('title_hook_link'))} · Thumb↔hook {S(v.get('thumb_hook_link'))} · Vì sao giữ người: {S(v.get('why'))} · Yếu: {S(v.get('weak'))}", ""]
    L += ["### Các tập của mình", ""]
    for e in s.get("our_eps") or []:
        L += [f"#### {S(e.get('ep'))} — {S(e.get('title_now'))}", f"- `{S(e.get('dir'))}` · {S(e.get('status'))} · ưu tiên {S(e.get('priority'))}",
              f"- Hook hiện tại: 「{S(e.get('hook_now_ja'))[:300]}」 · chốt {S(e.get('key_t'))} · hứa {S(e.get('promise_t'))} ({S(e.get('timing_source'))})",
              f"- Lời hứa cả video: {S(e.get('whole_video_promise_kept'))}"]
        L += [f"- Vấn đề: {S(x)}" for x in e.get("problems") or []]
        L += [f"- **Tiêu đề đề xuất:** 「{S(t.get('title_ja'))}」 ({S(t.get('formula'))}; {S(t.get('checked_in_script'))})" for t in e.get("title_proposals") or [] if isinstance(t, dict)]
        L += [f"- **Sửa hook:** {S(x)}" for x in e.get("hook_fix") or []]
        L.append("")
    L += ["### Nguyên tắc", ""] + [f"- **{S(p.get('claim'))}** — {S(p.get('cause'))} · bằng chứng: {S(p.get('evidence'))} · áp dụng: {S(p.get('how'))}" for p in s.get("principles") or []]
    L += ["", f"Lưu ý dữ liệu: {S(s.get('caveats'))}"]
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default="data/hook_audit_laneEFG")
    ap.add_argument("--lanes", nargs="+", default=["E_kenko", "F_real", "G_tano"])
    ap.add_argument("--out", default="docs/HOOK_AUDIT_LANE_EFG")
    a = ap.parse_args()
    base = ROOT / a.base; out = ROOT / a.out
    lanes = [k for k in a.lanes if (base / k / "channel.json").exists() and list((base / k).glob("videos_part*.json"))]
    tpl = (ROOT / "src" / "report_lane_audit_tpl.html").read_text(encoding="utf-8")
    head = (base / "HEAD.md").read_text(encoding="utf-8") if (base / "HEAD.md").exists() else ""
    nav = "".join(f'<a href="#{k}">{E(NAMES.get(k, k))}</a>' for k in lanes)
    Path(str(out) + ".html").write_text(tpl.replace("{{NAV}}", nav).replace("{{HEAD}}", md2html(head)).replace("{{LANES}}", "\n".join(lane_html(k, base / k) for k in lanes)), encoding="utf-8")
    Path(str(out) + ".md").write_text(head + "\n\n" + "\n\n---\n\n".join(lane_md(k, base / k) for k in lanes), encoding="utf-8")
    print(out, lanes)


if __name__ == "__main__":
    main()
