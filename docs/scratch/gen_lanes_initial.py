# -*- coding: utf-8 -*-
"""Sinh 9 thư mục lanes/<lane>/ lần đầu. Chạy 1 lần; sau đó sửa tay, KHÔNG regenerate."""
import json
from pathlib import Path
import yaml

ROOT = Path(r"E:\CLAUDE\YOUTUBE\TRENDING-RESEARCH\lanes")

SENIOR_AUD = {"age_range": "60+", "gender": "mixed", "interests": ["老後", "年金", "人間関係", "家族", "孤独", "健康", "人生の教訓"]}
NARR_FORMATS = ["narration", "stock_story", "ai_image_story", "slideshow_story", "manga_story"]
EXCL_FORMATS = ["vlog", "podcast", "interview", "talk_show", "news", "tv_clip", "livestream", "reaction", "music_video", "sports_highlight"]
EXCL_SUBJ_COMMON = ["celebrity gossip", "idol scandal", "US police bodycam", "gaming", "politics", "food/cooking vlog", "travel vlog", "music", "sports"]

COMMON_NEG = [
    {"pattern": "アイドル/芸能人スキャンダル (idol or celebrity scandal news)", "reason": "celebrity news, not lane content", "count": 1},
    {"pattern": "グルメ/料理動画 (food, cooking, restaurant)", "reason": "wrong topic — matched loose keyword only", "count": 1},
    {"pattern": "ミュージックビデオ/歌ってみた (music video, cover song)", "reason": "MV matched 1 word (サイエンス) — not content", "count": 1},
    {"pattern": "ライブカメラ/生配信 (live camera, live stream)", "reason": "live view count is not comparable", "count": 1},
    {"pattern": "中国語/英語の動画 (Chinese or English language video)", "reason": "wrong market language", "count": 2},
    {"pattern": "アメリカ警察の取材/トークショー (US police guest talk show, bodycam)", "reason": "wrong format (host/interview, real person) + wrong content identity", "count": 1},
    {"pattern": "スポーツハイライト転載/TVクリップ (sports highlight reup, TV clip)", "reason": "REUP — footage not owned, not replicable", "count": 1},
    {"pattern": "顔出しVlog/対談 (person on camera vlog, two-person podcast)", "reason": "faceless pipeline cannot reproduce", "count": 2},
]

LANES = {
 "shinya_shiryoshitsu": dict(
   label="Lane A — 都市伝説/宇宙/未解決ミステリー (narrated mystery)",
   audience={"age_range": "40+", "gender": "mixed", "interests": ["都市伝説", "UFO", "宇宙", "未解決事件", "陰謀論", "オカルト", "ミステリー"]},
   identity=["narrated_mystery", "documentary_style_story", "investigation_narration"],
   topics=["UFO事件", "宇宙の謎", "未解決失踪事件", "政府の隠蔽", "エリア51", "古代文明の謎", "深海・未知の生物", "NASA/宇宙開発の裏側", "人類滅亡シナリオ", "超常現象の実話"],
   formats=["narration", "stock_footage_story", "documentary_narration", "slideshow_story"],
   excl_subj=EXCL_SUBJ_COMMON + ["horror fiction / creepypasta pure fiction", "ghost prank", "anime/game lore"],
   dur=(8, 60),
   expansion={"core_tags": ["宇宙 謎", "宇宙 都市伝説", "UFO 日本", "NASA 隠蔽", "未解決 ミステリー"],
              "concept_queries": ["消えた 飛行機 真相", "失踪事件 未解決", "政府 隠蔽 宇宙", "地球外生命 証拠", "深海 未知 生物", "古代文明 謎", "月 裏側 秘密", "人類 滅亡 予言"],
              "format_queries": ["都市伝説 解説", "ミステリー 考察", "闇 真実 解説"],
              "audience_queries": ["怖い 都市伝説 2026", "ゾッとする 話 宇宙"],
              "story_queries": ["エリア51 内部告発", "アブダクション 実話", "UFO 遭遇 証言"]},
   watch=[],
   pos=[{"title": "セスナ上空の光はUFOか金星か…父が語る息子の恐怖【都市伝説 ミステリー 怖い話】", "why": "narrated real unsolved case, mystery framing"},
        {"title": "「地下に9機の円盤」エリア51の男を公文書で追うと…", "why": "document-driven investigation narration"}],
   neg=COMMON_NEG + [{"pattern": "ホラー創作/怪談朗読 (fictional horror story reading)", "reason": "fiction, not investigation of real case", "count": 1}],
   draft=False),
 "Lopezzapa68": dict(
   label="Lane satori — 老後の人間関係・感動実話 (senior narrated emotional story)",
   audience=SENIOR_AUD,
   identity=["narrated_story", "emotional_story", "senior_story"],
   topics=["老後の人間関係", "友情の崩壊", "親子関係", "孤独", "後悔", "老老介護", "老後のお金", "年金", "特殊詐欺", "熟年離婚", "遺産相続"],
   formats=NARR_FORMATS,
   excl_subj=EXCL_SUBJ_COMMON + ["medical advice / health tips", "finance how-to"],
   dur=(8, 60),
   expansion={"core_tags": ["老後 実話", "高齢者 感動 話", "年金 生活 実話", "老老介護 実話", "特殊詐欺 実話"],
              "concept_queries": ["友達 絶縁 老後", "親友 裏切り 60代", "孤独死 実話", "後悔 人生 70代", "親の介護 限界", "遺産 争い 兄弟", "年金 月 万円 生活", "熟年離婚 その後"],
              "format_queries": ["朗読 感動する話", "人生の教訓 物語", "シニア 実話 泣ける"],
              "audience_queries": ["60代 人生", "70代 一人暮らし", "高齢者 本音"],
              "story_queries": ["LINE 誤送信 友人", "同窓会 その後", "妻 に 言えなかった"]},
   watch=[{"channel_id": "UCvA0jwPl5qjhsHQOWuZYe-g", "channel_name": "他人の人生【タニジン】", "confidence": 0.95, "note": "Lane C kênh mẫu đã duyệt 2026-09-10"}],
   pos=[{"title": "年金「月25万」を漏らした73歳…40年の仲間の会が解散、LINE誤送信の一行", "why": "senior relationship story, emotional twist"},
        {"title": "【老老介護】手帳の最後に鉛筆で「たすけて」…倒れたのは80歳の母ではなく娘", "why": "caregiving story with emotional contradiction"}],
   neg=COMMON_NEG,
   draft=False),
 "irogatatarukioku": dict(
   label="Lane D — 色でたどる戦争の記録 (WW2 real photos AI-colorized, narrated)",
   audience={"age_range": "50+", "gender": "mostly_male", "interests": ["太平洋戦争", "日本軍", "戦史", "昭和史", "沖縄戦", "硫黄島"]},
   identity=["historical_photo_narration", "war_history_documentary", "colorized_archive_story"],
   topics=["太平洋戦争の戦い", "日本軍将校の最期", "玉砕・特攻", "沖縄戦", "硫黄島", "戦争写真の裏側", "戦後の引き揚げ", "戦時中の生活", "軍艦・航空機の記録"],
   formats=["narration", "archive_photo_story", "documentary_narration", "slideshow_story"],
   excl_subj=EXCL_SUBJ_COMMON + ["modern travel to war sites vlog", "modern US city life", "military hardware news today", "war game footage"],
   dur=(8, 60),
   expansion={"core_tags": ["太平洋戦争 カラー化", "戦争 写真 カラー", "日本軍 将校 最期", "玉砕 真実", "沖縄戦 実話"],
              "concept_queries": ["硫黄島 栗林 最期", "特攻隊 遺書", "引き揚げ 満州 実話", "戦艦大和 最後", "ガダルカナル 飢餓", "戦争 一枚の写真", "終戦 玉音放送 その日", "捕虜 収容所 日本兵"],
              "format_queries": ["戦争 記録 ドキュメンタリー", "戦争 写真 解説", "昭和 戦争 実話"],
              "audience_queries": ["日本軍 真実", "太平洋戦争 知られざる"],
              "story_queries": ["最後の総攻撃 手紙", "残存日本兵 洞窟", "将校 家族 写真"]},
   watch=[{"channel_id": "UCaj1dslbibbHEnOAOh0tyYw", "channel_name": "色でたどる戦争の記録", "confidence": 0.95, "note": "Lane D kênh mẫu đã duyệt 2026-09-10"}],
   pos=[{"title": "【沖縄戦】首里城地下の壕でランタンを囲む4人の将校——撮影から2か月3週間後…", "why": "one real photo → narrated fate of people in it"},
        {"title": "【硫黄島】正面を見据えるこの司令官は万歳突撃を禁じた——", "why": "archive photo, officer story"}],
   neg=COMMON_NEG + [{"pattern": "ディズニー/ロサンゼルス 旅行 (Disney, LA travel, modern US life)", "reason": "matched place-name tag only; not history", "count": 1}],
   draft=False),
 "70dai-kenko": dict(
   label="Lane E — 70代の健康・長寿 (senior health & longevity tips)",
   audience={"age_range": "65+", "gender": "mixed", "interests": ["健康", "長生き", "食事", "転倒予防", "筋肉", "血流", "認知症予防"]},
   identity=["health_tips_list", "senior_health_explainer", "narrated_health_story"],
   topics=["転倒・骨折予防", "サルコペニア", "高齢者の食事", "長生きの習慣", "血流・足のむくみ", "認知症予防", "睡眠", "朝の習慣", "食べてはいけない食品"],
   formats=["narration", "slideshow_story", "ai_image_story", "manga_story", "explainer"],
   excl_subj=EXCL_SUBJ_COMMON + ["doctor on camera lecture", "fitness influencer workout", "product sales / supplement ads", "hospital news"],
   dur=(6, 40),
   expansion={"core_tags": ["70代 健康", "高齢者 食べ物", "転倒 予防", "筋肉 減る 高齢者", "長生き 習慣", "血流 改善 足"],
              "concept_queries": ["サルコペニア サイン", "骨折 防ぐ 食品", "認知症 予防 食事", "夜 トイレ 高齢者", "足 むくみ 解消 70代", "ふくらはぎ 血流", "長寿 の 秘訣 100歳"],
              "format_queries": ["高齢者 健康 5選", "シニア 食べてはいけない", "70代 やめるべき"],
              "audience_queries": ["70代 体 変化", "65歳 から 健康"],
              "story_queries": []},
   watch=[], pos=[], neg=COMMON_NEG + [{"pattern": "医師 顔出し 解説 (doctor speaking on camera)", "reason": "real person host format", "count": 1}],
   draft=True),
 "teinengo-real": dict(
   label="Lane F — 定年後リアル漫画 (retirement manga, money regret, 2 contrasting characters)",
   audience=SENIOR_AUD,
   identity=["manga_story", "retirement_money_drama", "contrast_two_characters"],
   topics=["定年後のお金", "年金繰り上げの後悔", "再雇用と給料", "退職金の失敗", "夫婦の収入差", "老後破産", "住宅ローン 老後", "退職後の人間関係"],
   formats=["manga_story", "ai_image_story", "narration", "slideshow_story"],
   excl_subj=EXCL_SUBJ_COMMON + ["FP on camera lecture", "investment product promotion", "news about pension law"],
   dur=(8, 40),
   expansion={"core_tags": ["定年後 漫画", "年金 繰り上げ 後悔", "再雇用 給料 半分", "退職 後悔 漫画", "老後 お金 失敗"],
              "concept_queries": ["退職金 溶けた", "老後破産 漫画", "60歳 退職 その後", "年金 月 差 夫婦", "定年 再雇用 屈辱", "住宅ローン 定年 残り"],
              "format_queries": ["漫画 定年 実話", "漫画動画 老後", "アニメ 老後 お金"],
              "audience_queries": ["60代 お金 現実", "定年後 リアル"],
              "story_queries": ["元部下 上司 再雇用", "妻 働き続けた 差"]},
   watch=[], pos=[{"title": "【漫画】60歳で退職した俺と働き続けた妻…5年後、夫婦の月収に8万円の差が出た理由", "why": "manga drama, money contrast between 2 characters"}],
   neg=COMMON_NEG, draft=True),
 "teinengo-tanoshimi": dict(
   label="Lane G — 定年後の楽しみ漫画 N選 (retirement lifestyle list manga)",
   audience=SENIOR_AUD,
   identity=["manga_story", "list_video_n_sen", "retirement_lifestyle"],
   topics=["定年後の趣味", "朝の習慣", "一人旅", "節約生活", "60代の楽しみ", "小さな幸せ", "定年後の生きがい"],
   formats=["manga_story", "ai_image_story", "narration", "slideshow_story"],
   excl_subj=EXCL_SUBJ_COMMON + ["travel vlog with person on camera", "hobby product review"],
   dur=(6, 40),
   expansion={"core_tags": ["定年後 趣味 5選", "60代 朝の習慣", "定年後 一人旅", "老後 楽しみ 漫画", "シニア 節約 生活"],
              "concept_queries": ["定年後 生きがい 見つけた", "60代 幸せ 習慣", "老後 楽しい 毎日", "年金 で 楽しむ", "定年後 やってよかった"],
              "format_queries": ["漫画 定年後 5選", "老後 習慣 7選", "シニア おすすめ 選"],
              "audience_queries": ["60代 から 楽しみ", "定年 した ら"],
              "story_queries": []},
   watch=[], pos=[{"title": "【漫画】60代から始める「朝の習慣」5選…1年後、体と気持ちが驚くほど軽くなる理由", "why": "list N選 in manga format, positive lifestyle"}],
   neg=COMMON_NEG, draft=True),
 "kokoro-kazoku": dict(
   label="Lane H — 老後の家族心理 (senior family psychology: parent-child, couple)",
   audience=SENIOR_AUD,
   identity=["family_psychology_story", "narrated_story", "senior_relationship"],
   topics=["老後の夫婦関係", "親子関係の心理", "高齢の親の本音", "定年後の夫婦", "孫との距離", "嫁姑", "家族との断絶", "心理学 老後"],
   formats=NARR_FORMATS + ["explainer"],
   excl_subj=EXCL_SUBJ_COMMON + ["psychologist on camera lecture", "parenting of small children"],
   dur=(8, 45),
   expansion={"core_tags": ["老後 夫婦 心理", "親子 関係 老後", "高齢の親 心", "定年後 夫婦 関係", "家族 心理 高齢者"],
              "concept_queries": ["息子 疎遠 理由", "娘 帰ってこない 老後", "夫 定年 妻 ストレス", "親 の 本音 老後", "孫 会えない 心理", "実家 帰らない 子供"],
              "format_queries": ["心理学 老後 家族", "家族 心理 解説 シニア"],
              "audience_queries": ["60代 家族 悩み", "70代 親子"],
              "story_queries": []},
   watch=[], pos=[], neg=COMMON_NEG, draft=True),
 "sengoku-uragawa": dict(
   label="Lane I — 戦国の裏側 (Sengoku history, chibi manga + narration, myth-busting)",
   audience={"age_range": "40+", "gender": "mostly_male", "interests": ["戦国時代", "武将", "日本史", "歴史の真実", "通説の嘘"]},
   identity=["history_explainer_manga", "myth_busting_narration", "sengoku_story"],
   topics=["戦国武将の真実", "通説の嘘", "織田信長・豊臣秀吉・徳川家康の裏話", "合戦の真相", "戦国の生活", "裏切りと謀略", "最期の真実"],
   formats=["manga_story", "ai_image_story", "narration", "slideshow_story", "explainer"],
   excl_subj=EXCL_SUBJ_COMMON + ["taiga drama clips", "castle travel vlog", "game (Nobunaga's Ambition) footage", "history teacher on camera"],
   dur=(8, 45),
   expansion={"core_tags": ["戦国時代 真実", "戦国武将 裏話", "織田信長 真相", "戦国 通説 嘘", "戦国 漫画 解説"],
              "concept_queries": ["本能寺の変 真相", "関ヶ原 裏切り 理由", "秀吉 最期 真実", "家康 の 嘘", "戦国 農民 生活", "武将 死因 意外"],
              "format_queries": ["戦国 解説 アニメ", "歴史 漫画 解説", "日本史 ゆっくり 戦国"],
              "audience_queries": ["戦国 知られざる", "武将 知らない 真実"],
              "story_queries": []},
   watch=[], pos=[], neg=COMMON_NEG + [{"pattern": "大河ドラマ 切り抜き (taiga drama TV clip)", "reason": "TV_CLIP reup", "count": 1}], draft=True),
 "teinengo-fuufu": dict(
   label="Lane J — 定年後の夫婦 漫画 (retired couple emotional manga, big decisions)",
   audience=SENIOR_AUD,
   identity=["manga_story", "couple_emotional_drama", "retirement_decision"],
   topics=["定年後の夫婦", "熟年離婚", "老後の二人暮らし", "妻の本音", "夫婦の決断", "家を売る", "田舎移住", "介護と夫婦"],
   formats=["manga_story", "ai_image_story", "narration", "slideshow_story"],
   excl_subj=EXCL_SUBJ_COMMON + ["couple vlog on camera", "divorce lawyer lecture"],
   dur=(8, 40),
   expansion={"core_tags": ["定年後 夫婦 漫画", "熟年離婚 漫画", "老後 夫婦 決断", "定年 妻 本音", "老後 二人暮らし"],
              "concept_queries": ["定年 夫 邪魔 妻", "熟年離婚 切り出した", "夫婦 家 売る 老後", "移住 夫婦 後悔", "妻 突然 別居", "夫 定年 うつ"],
              "format_queries": ["漫画 夫婦 定年", "漫画動画 熟年", "アニメ 老後 夫婦"],
              "audience_queries": ["60代 夫婦 本音", "定年後 二人"],
              "story_queries": []},
   watch=[], pos=[], neg=COMMON_NEG, draft=True),
}


def w(p: Path, obj, is_yaml=False):
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        if is_yaml:
            yaml.safe_dump(obj, f, allow_unicode=True, sort_keys=False, width=100)
        else:
            json.dump(obj, f, ensure_ascii=False, indent=2)


for lane, s in LANES.items():
    d = ROOT / lane
    if (d / "lane_profile.yaml").exists():
        print("skip (đã có):", lane); continue
    prof = {
        "lane_id": lane, "label": s["label"], "draft": s["draft"],
        "market": {"country": "Japan", "language": "Japanese"},
        "audience": s["audience"],
        "content_identity": {"primary": s["identity"]},
        "wanted_topics": s["topics"],
        "allowed_formats": s["formats"],
        "excluded_formats": EXCL_FORMATS,
        "excluded_subjects": s["excl_subj"],
        "duration": {"min_minutes": s["dur"][0], "max_minutes": s["dur"][1]},
        "notes": "draft=true: soạn từ seed_tags + ô B1 tab, chưa có handoff — user duyệt sau lượt shadow đầu" if s["draft"] else "soạn từ docs/LANE_*_HANDOFF.md",
    }
    w(d / "lane_profile.yaml", prof, True)
    w(d / "query_expansion.json", s["expansion"])
    w(d / "watch_channels.json", s["watch"])
    w(d / "positive_examples.json", {"positive_examples": s["pos"]})
    w(d / "negative_examples.json", {"negative_patterns": s["neg"]})
    w(d / "blacklist.json", {"channels": [], "note": "channel_id + reason; hard filter loại thẳng"})
    print("ok:", lane)
