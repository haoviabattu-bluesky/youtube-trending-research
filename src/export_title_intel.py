# -*- coding: utf-8 -*-
"""Gom dữ liệu tiêu đề / thumbnail / hook của kênh mẫu từng lane thành 1 file JSON mỗi lane cho dự án YT-TITLE-RESEARCH.

Nguồn: data/hook_audit_2026-09-23/analysis_<key>.json (9 kênh, mẫu 9–15 video) và
data/hook_audit_laneEFG/<X>/{channel.json, videos_part*.json, lane_summary.json} (Lane E/F/G, TẤT CẢ video).
Ra: data/title_intel/<lane>.json + data/title_intel/README.md

    py -3.13 -X utf8 src/export_title_intel.py
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / "data" / "hook_audit_2026-09-23"
EFG = ROOT / "data" / "hook_audit_laneEFG"
HOOKS_JSONL = Path(r"E:\CLAUDE\YOUTUBE\HOOK_LIBRARY\hooks.jsonl")
OUT = ROOT / "data" / "title_intel"
LANE = {"simbot2": "satori-jp-obaa", "toshi": "toshi-densetsu-jp", "iro": "irogatatarukioku", "kenko": "kenko-chiebukuro",
        "real": "teinengo-real", "tano": "teinengo-tanoshimi", "fuufu": "teinengo-fuufu", "kokoro": "kokoro-kazoku",
        "sengoku": "sengoku-uragawa"}
EFG_DIR = {"kenko": "E_kenko", "real": "F_real", "tano": "G_tano"}

# Lane K1dev 24/09: iyaku_labo (Lane K, handle yakkyoku-sukatto) + shakai_no_uragawa (ứng viên, chưa gán lane).
# Nguồn khác hẳn A/EFG ở trên: đọc thẳng data/<slug>/channel.json (channel_full_fetch.py) + hooks.jsonl
# (đã nạp qua hook_library.py add) thay vì file analysis_*.json/lane_summary.json cũ.
# CHDIR["<key>"] = (lane_hien_tai, data_rel, channel_ja, dna_rel, channel_id). `lane_hien_tai` là
# phần DUY NHẤT đổi được — qua sync_lane_names.py khi h2dev chính thức gán HANDLE trên tab NOTE.
# Sống ở file JSON riêng (KHÔNG hard-code trong .py) để sync_lane_names.py ghi lại được mà không
# phải sửa source code mỗi lần đổi lane.
CH_MAP_PATH = ROOT / "data" / "title_intel" / "_channel_map.json"
_DEFAULT_CHDIR = {
    "iyaku": ["yakkyoku-sukatto", "data/iyaku_labo", "千種テンカ", "docs/channel_dna/iyaku_labo", "UCEBA1RFfkXQtqgiDVLh4bcw"],
    "shakai": ["shakai_no_uragawa", "data/shakai_no_uragawa", "社会のウラガワ", "docs/channel_dna/shakai_no_uragawa", "UCFWFKb3Yr_1SrAT0kcvwFdw"],
}
if not CH_MAP_PATH.exists():
    CH_MAP_PATH.parent.mkdir(parents=True, exist_ok=True)
    CH_MAP_PATH.write_text(json.dumps(_DEFAULT_CHDIR, ensure_ascii=False, indent=1), encoding="utf-8")
CHDIR = {k: tuple(v) for k, v in json.loads(CH_MAP_PATH.read_text(encoding="utf-8")).items()}


def save_chdir() -> None:
    CH_MAP_PATH.write_text(json.dumps({k: list(v) for k, v in CHDIR.items()}, ensure_ascii=False, indent=1),
                           encoding="utf-8")


def rd(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


def from_analysis(key: str) -> dict:
    a = rd(A / f"analysis_{key}.json")
    f = a.get("formula", {})
    vids = [{k: v.get(k) for k in ("video_id", "tag", "views", "title", "desc_first", "thumb_text", "key_line_ja", "key_t",
                                   "promise_t", "title_hook", "thumb_title", "thumb_hook", "why", "weak")} for v in a.get("videos", [])]
    return dict(source="analysis_sample", channel=a.get("channel"), title_rule=f.get("title"), thumbnail_rule=f.get("thumbnail"),
                description_rule=f.get("description"), link_4_parts=f.get("link_4_parts"), hook_beats=f.get("hook_beats"),
                first_episode_template=f.get("khuon_tap_dau"), principles=a.get("principles"), videos=vids,
                our_eps=[{k: e.get(k) for k in ("ep", "title", "thumb_text", "title_hook", "thumb_title", "broken_promises", "fix")}
                         for e in a.get("our_eps", [])])


def from_efg(key: str) -> dict:
    d = EFG / EFG_DIR[key]
    ch = rd(d / "channel.json"); s = rd(d / "lane_summary.json")
    meta = {v["id"]: v for v in ch["videos"]}
    vids = []
    for f in sorted(d.glob("videos_part*.json")):
        for v in rd(f):
            vid = v.get("video_id") or v.get("id"); m = meta.get(vid, {})
            vids.append(dict(video_id=vid, title=m.get("title"), published=m.get("published"), views=m.get("views"),
                             view_per_day=v.get("view_per_day"), tier=v.get("tier"), desc_first=v.get("desc_first"),
                             thumb_lines=v.get("thumb_lines"), thumb_visual=v.get("thumb_visual"), title_why=v.get("title_why"),
                             title_formula=v.get("title_formula"), title_vs_thumb=v.get("title_vs_thumb"),
                             title_hook_link=v.get("title_hook_link"), thumb_hook_link=v.get("thumb_hook_link"),
                             video_promise=v.get("video_promise"), key_line_ja=v.get("key_line_ja"), key_t=v.get("key_t"),
                             payoff_t=v.get("payoff_t"), timing_source=v.get("timing_source")))
    vids.sort(key=lambda x: -(float(x.get("view_per_day") or 0)))
    return dict(source="all_videos", channel=s.get("channel") or ch["meta"], median_view_per_day=s.get("median_vpd"),
                title_formulas=s.get("title_formulas"), title_pairs=s.get("title_pairs"), title_losers=s.get("title_losers"),
                title_over_time=s.get("title_over_time"), thumbnail=s.get("thumbnail"), hook_open=s.get("hook_open"),
                hook_whole=s.get("hook_whole"), principles=s.get("principles"), videos=vids,
                our_eps=[{k: e.get(k) for k in ("ep", "title_now", "problems", "title_proposals", "priority")} for e in s.get("our_eps", [])])


RULES = {
    "iyaku": dict(
        title_rule="【漫画】「[câu cửa miệng toxic, trong 「」]」が口ぐせの/だった薬剤師が、[hành động sai lầm/mốc đếm]結果…"
                   " (hoặc 行き着く先…) — 33–46 ký tự, LUÔN trích nguyên văn câu cửa miệng trong ngoặc kép.",
        thumbnail_rule="Chữ thumbnail = CHÉP NGUYÊN tiêu đề video (không viết lại), không có ảnh người — chỉ chữ trên nền màu.",
        description_rule="L1 trích câu cửa miệng 1 dòng → L2 câu mở cố định 'Đó là câu cửa miệng của 1 dược sĩ' → "
                          "L3 2-4 câu hành vi cụ thể → L4 câu nhử không lộ kết quả → 3 dòng miễn trừ trách nhiệm (hư cấu, "
                          "không phải lời khuyên y tế) → もくじ mốc phút:giây → credit giọng VOICEVOX → 4 hashtag cố định.",
        principles=["Không có CTA sub/like.", "Không có cảnh trả thù — hậu quả tới từ hệ thống/số liệu (log giờ, hợp đồng).",
                    "Cấu trúc 6 giai đoạn: ảo tưởng → góc khuất bị bao che → giọt nước tràn ly → phản tác dụng → nếm mùi đời → kết đối lập.",
                    "Câu kết luôn lặp lại đúng câu cửa miệng, khẳng định nó đã biến mất."],
    ),
    "shakai": dict(
        title_rule="なぜ〜のか？【漫画】 / 〜の理由【漫画】 / 〜の末路とは【漫画】 / 『[phát ngôn cực đoan]』なぜ〜なのか【漫画】"
                   " — 20–42 ký tự, luôn 【漫画】 cuối câu, KHÔNG có tên nhân vật/câu cửa miệng riêng như yakkyoku-sukatto.",
        thumbnail_rule="Băng đen 3 màu trên cùng (vàng=chủ ngữ, đỏ=từ khoá sốc, trắng=phần còn lại) + 2 khung minh hoạ AI "
                       "phong cách anime + 2 ô chữ vàng viền đen. ⚠ CHỮ THUMBNAIL VIẾT LẠI ngắn gọn hơn, KHÔNG chép nguyên tiêu đề.",
        description_rule="2 câu chào cố định ('cảm ơn đã xem, kênh giải thích なぜ của xã hội qua manga') → 1-3 số liệu thật "
                          "→ câu hỏi なぜ lặp tiêu đề → hé nguyên nhân → hashtag đổi theo từng video.",
        principles=["Nhân vật xuyên suốt さくら (Sakura) ở CẢ 8 video, luôn hỏi thay khán giả kiểu Socratic.",
                    "CTA sub/like cố định ở 6/7 video — KHÁC yakkyoku-sukatto không có CTA.",
                    "Nhịp twist mỗi 60-90 giây, câu chuyển cảnh cố định 'câu trả lời ẩn trong câu chuyện của...'",
                    "3 công thức hook: đảo ngược định kiến / tái hiện oan ức in medias res / câu hỏi trải nghiệm thường nhật."],
    ),
    "otona": dict(
        title_rule="【漫画】+ [đối tượng 60代 / 60代以降 / 定年後] + [trạng thái/nỗi sợ/mục tiêu cụ thể] + [N]選 ｜ "
                   "[vế sau sau dấu ｜ = nhân vật cụ thể hoặc lời hứa giải pháp] — 47–58 ký tự (trung vị 51), "
                   "KHÔNG dùng ？ trừ dạng なぜ〜のか. Từ khoá bắt buộc: 【漫画】· 60代/定年後 · アルバイト・パート hoặc 趣味/口癖 · ○選 (hoặc ○つの理由). "
                   "Video hit 92k đặt tuổi+giới người tìm được việc ở vế sau (64歳男性が見つけた“無理なく続く仕事”) và bọc lời hứa trong “”.",
        thumbnail_rule="Khuôn 5/6 ảnh: BĂNG ĐEN TRÊN 1 dòng (「60代」VÀNG + từ khoá ĐỎ + phần còn lại TRẮNG) → 4 khung xếp hạng "
                       "第5位→第2位 (nhãn màu) → BĂNG ĐEN DƯỚI 「N選」ĐỎ. 第1位 LUÔN BỊ GIẤU (khoảng trống tò mò). "
                       "Ngoại lệ chính là video hit 92k: chỉ 2 khung TO (第3位/第2位 nền vàng), cột chữ DỌC giữa nền đen "
                       "(「60代」đỏ「穴場」vàng「バイト」đỏ) + ô chữ dọc TRẮNG ghi LỢI ÍCH cụ thể (「午後は自由」「座れて快適」). "
                       "⚠ Chữ thumbnail KHÔNG chép tiêu đề — viết lại ≤12 ký tự, cảm xúc mạnh hơn. Nhân vật cố định 高瀬 chibi đầu to, "
                       "áo polo navy, kính; ảnh hit là nhân vật CƯỜI TƯƠI (92k) — ảnh nhăn nhó/đổ mồ hôi chỉ 10k.",
        description_rule="Khuôn 6/6 video: (1) 1 câu hỏi lặp lại tiêu đề (…どんなアルバイト・パートを選べばよいのでしょうか) → "
                         "(2) 2–3 câu so sánh CÓ SỐ THẬT đối nghịch (時給1300円でもぐったり vs 時給1100円でも動ける) + tên+tuổi nhân vật "
                         "(64歳の高瀬健一) + 5 trục đo (時給・通勤時間・拘束時間・体への負担・勤務日数) → (3) 1 câu chốt ngược "
                         "(時給が高い仕事ほど得とは限りません) → (4) đoạn kể 3–4 thất bại cụ thể → (5) 【こんな方におすすめです】 6 dấu ・ "
                         "→ (6) 【チャプター】mốc mm:ss 第N章 → (7) hashtag. KHÔNG spoil 第1位.",
        principles=["Nhân vật CỐ ĐỊNH xuyên kênh (kênh mẫu 高瀬健一 64歳 cựu 信用金庫 + vợ 恵子 làm mỏ neo thực tế); lane mình dùng người RIÊNG 田島誠 63歳 cựu 総務 + vợ 春江.",
                    "Câu chốt cuối video của kênh mẫu 「盲点だった。」 xuất hiện 6/6 — lane mình KHÔNG chép câu này.",
                    "Mọi mục xếp hạng phải có 1 ưu điểm + 1 'độc dược ngầm' (毒/落とし穴) đo bằng SỐ (kg, số phòng/giờ, phút đi lại, giờ hồi phục).",
                    "Trắc nghiệm A/B/C giữa video (35–50% thời lượng) để kéo bình luận — 6/6 video đều có.",
                    "Kết luôn là thoả hiệp thực tế (3–5 vạn yên, giúp vợ việc nhà), không kết màu hồng.",
                    "So với đối thủ cùng ngách: video >180k (人生の知らせ 1,14M / 人生の果実 422k / 老後のお金ストーリー 186k) đều gắn móc TIẾT KIỆM (0円 / 1円もかからない) hoặc 最強/神 mà kênh mẫu chưa dùng → móc giá-0-đồng là khoảng trống bỏ ngỏ.",
                    "Mục xếp hạng đầu tiên của video hit xuất hiện rất muộn (9:14/31 phút) và bị bình luận chê 「出てくるの遅すぎない？」 nhưng vẫn hit → drama mở đầu không giết video, nhưng mô tả/Timestamps phải cho người xem nhảy tới danh sách."],
        extra=dict(
            thumb_rows_measured=[
                {"video_id": "wG4fI9voims", "views": 92034, "top": "(không có băng trên) — 2 khung 「第３位」「第2位」nền vàng",
                 "mid": "cột dọc giữa nền đen: 「60代」đỏ 「穴場」vàng 「バイト」đỏ; ô chữ dọc trắng 「午後は自由」「座れて快適」",
                 "bottom": "(không có)", "face": "高瀬 CƯỜI TƯƠI ở cả 2 khung — lợi ích tích cực"},
                {"video_id": "do0n9Wirigs", "views": 26982, "top": "「60代」vàng 「ひとりが」trắng 「楽しい」đỏ",
                 "mid": "4 khung 5位→2位 (nhãn trắng)", "bottom": "「一生遊べる趣味7選」đỏ", "face": "高瀬 cười ở cả 4 khung"},
                {"video_id": "vritvBsvYjc", "views": 11145, "top": "「60代」vàng 「この」trắng 「一言」đỏ 「が言える人」trắng",
                 "mid": "4 khung 「言葉⑤④③②」nhãn xanh lá/đỏ/vàng/xanh dương", "bottom": "「なぜか好かれます」đỏ",
                 "face": "4 ông già KHÁC NHAU, không phải 高瀬"},
                {"video_id": "TIoRmIZKkAg", "views": 10442, "top": "「60代で始めて」vàng 「後悔」đỏ", "mid": "4 khung 5位→2位",
                 "bottom": "「つらすぎるバイト13選」đỏ", "face": "高瀬 đổ mồ hôi, nhăn nhó (tiêu cực)"},
                {"video_id": "SN2VjauDlJA", "views": 6634, "top": "「60代」vàng 「なぜ」trắng 「辞めない？」đỏ",
                 "mid": "4 khung 「理由⑤④③②」nhãn màu", "bottom": "「働き続ける」trắng 「7つの理由」đỏ", "face": "高瀬 lẫn lộn cảm xúc"},
                {"video_id": "HvLbO2pqUcI", "views": 1005, "top": "「60代」vàng 「月5万稼ぐ」đỏ 「なら…」trắng",
                 "mid": "4 khung 「第5位→第2位」nhãn màu", "bottom": "「続けやすいバイト11選」đỏ", "face": "nhiều người khác nhau"},
            ],
            title_lengths={"wG4fI9voims": 53, "do0n9Wirigs": 48, "vritvBsvYjc": 47, "TIoRmIZKkAg": 51,
                           "SN2VjauDlJA": 58, "HvLbO2pqUcI": 51, "median": 51},
            competitor_thumbs=[
                {"channel": "人生の知らせ", "views": 1141270, "thumb_text": "定年後、安く楽しむ / 最高の趣味5選"},
                {"channel": "人生の果実", "views": 422663, "thumb_text": "定年後..最強の趣味 / ※ぜんぶ0円です！"},
                {"channel": "老後のお金ストーリー", "views": 186807, "thumb_text": "定年後、最強の暇つぶし / ※1円もかからない"},
                {"channel": "シニアの人生これから", "views": 224354, "thumb_text": "老後のおすすめ神バイト (lưới 2×2 CÓ hiện 1位)"},
            ],
            title_hook_match="Khớp hoàn toàn 5/6 · khớp một phần 1/6 (SN2VjauDlJA: tiêu đề vĩ mô なぜ…増えたのか nhưng hook lại là chuột rút bắp chân 6h sáng) · lệch 0/6.",
            our_eps=[],
        ),
    ),
}


def load_hooks_for(channel_ja: str) -> dict[str, dict]:
    out = {}
    if not HOOKS_JSONL.exists():
        return out
    for line in HOOKS_JSONL.read_text(encoding="utf-8").splitlines():
        r = json.loads(line)
        if channel_ja in r.get("channel", ""):
            out[r["video_id"]] = r
    return out


def from_channel_dna(key: str) -> dict:
    lane, data_rel, channel_ja, dna_rel, _channel_id = CHDIR[key]
    ch = rd(ROOT / data_rel / "channel.json")
    hooks = load_hooks_for(channel_ja)
    vids = []
    for v in sorted(ch["videos"], key=lambda x: -(x.get("views") or 0)):
        h = hooks.get(v["id"])
        vids.append(dict(video_id=v["id"], title=v.get("title"), published=v.get("published"), views=v.get("views"),
                         duration_s=v.get("dur"), hook_0_30s=h.get("hook_0_30s") if h else None,
                         hook_kind=h.get("kind") if h else None, hook_patterns=h.get("patterns") if h else None,
                         hook_why=h.get("why") if h else None))
    r = RULES[key]
    rec = dict(source="channel_report", channel=ch.get("meta"), title_rule=r["title_rule"], thumbnail_rule=r["thumbnail_rule"],
                description_rule=r["description_rule"], principles=r["principles"], videos=vids,
                channel_report_html=str(ROOT / "docs" / f"{Path(data_rel).name.upper()}_CHANNEL_REPORT.html"),
                channel_dna_md=str(ROOT / dna_rel / "CHANNEL_DNA.md"))
    rec.update(r.get("extra") or {})
    return rec


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for key, lane in LANE.items():
        rec = from_efg(key) if key in EFG_DIR and (EFG / EFG_DIR[key] / "lane_summary.json").exists() else from_analysis(key)
        if key == "simbot2":
            p = ROOT / "data" / "hook_audit_2026-09-23" / "tools" / "simbot2_all.json"
            if p.exists():
                rec["all_titles_26"] = rd(p)
            rec["title_formula_report"] = r"E:\CLAUDE\YOUTUBE\TRENDING-RESEARCH\docs\SIMBOT2_CONG_THUC_TIEU_DE.html"
            rec["thumb_vs_title_report"] = r"E:\CLAUDE\YOUTUBE\TRENDING-RESEARCH\docs\SIMBOT2_TIEU_DE_THUMBNAIL.html"
        rec["lane"] = lane; rec["key"] = key
        (OUT / f"{lane}.json").write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
        print(lane, rec["source"], len(rec.get("videos") or []))

    for key in CHDIR:
        lane = CHDIR[key][0]
        rec = from_channel_dna(key)
        rec["lane"] = lane; rec["key"] = key
        (OUT / f"{lane}.json").write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
        print(lane, rec["source"], len(rec.get("videos") or []))


if __name__ == "__main__":
    main()
