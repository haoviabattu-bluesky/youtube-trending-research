# -*- coding: utf-8 -*-
"""Quét rộng tìm kênh GIỐNG 1 lane đã có (mặc định Lane F 老後の暮らし研究所) —
manga story ngôi 1, nhân vật có tên/tuổi/nghề, biến cố tài chính sau nghỉ hưu.

Chiến lược: quét ~70 từ khoá JP qua InnerTube (today/week/month, sort viewCount, pages=2)
để tối đa hoá số video/kênh chạm được (mục tiêu người dùng: 300-500 lượt kênh), gom
channel_id duy nhất, lọc subs < --max-subs qua Data API, tính `ch_mult` = median view
12 video gần nhất (bỏ <7 ngày) / subs — đúng chỉ số "kênh có công thức" đã dùng ở
explore_niches.py, không phải mult đơn (views/subs) dễ nhiễu.

    py -3.13 -X utf8 src/find_lane_similar.py --out data/lane_f_similar --max-subs 30000
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import time
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from innertube import BotCheckError, InnerTube, ProxyError  # noqa: E402
from proxy_pool import ProxyPool, load_proxies                # noqa: E402
from ytapi import QuotaExhausted, YouTubeAPI                  # noqa: E402

KEYWORDS = [
    # lõi định dạng manga + biến cố tài chính hưu trí (đúng khuôn Lane F)
    "漫画 定年 退職金", "漫画 老後 貯金", "漫画 年金 生活", "漫画 熟年離婚",
    "漫画 定年後 現実", "漫画 老後 破産", "漫画 退職金 使い方", "漫画 老後 絶望",
    "漫画 60歳 定年", "漫画 65歳 退職", "漫画 定年 後悔", "漫画 老後 一人暮らし",
    "漫画 年金 いくら", "漫画 独身 老後", "漫画 夫婦 年金", "漫画 老後 資金",
    "漫画 定年 妻", "漫画 老後 末路", "漫画 退職 末路", "漫画 定年 衝撃",
    "漫画 老後 現実", "漫画 貯金 消えた", "漫画 熟年 夫婦", "漫画 年金 現実",
    "漫画 定年退職 妻", "漫画 老後 生活", "漫画 定年 資産", "漫画 退職金 老後",
    "漫画 老後 後悔", "漫画 定年 転職",
    # biến thể tuổi cụ thể (đúng "tuổi + số tiền thật" của công thức)
    "60歳で定年 漫画", "65歳 退職 漫画", "70歳 年金 漫画", "55歳 早期退職 漫画",
    "62歳 年金 漫画", "63歳 定年 漫画",
    # kênh cùng dòng tương tự đã biết → mở rộng bằng tên kênh/format gần giống
    "老後の暮らし 漫画", "老後のお金 漫画", "定年後の暮らし 漫画", "人生 漫画 老後",
    "シニア 漫画 ストーリー", "漫画 老後 教訓", "漫画 老後 実話",
    # góc "so sánh 2 số phận" đúng công thức lane F
    "漫画 同僚 差 老後", "漫画 退職 差 5年後", "漫画 定年 明暗",
    "漫画 老後 勝ち組 負け組", "漫画 老後 格差",
    # góc cô đơn/lo âu tuổi già (1 phần công thức)
    "漫画 孤独死 老後", "漫画 老後 孤独", "漫画 定年 孤独",
    # nhóm dùng ẩn dụ 末路/衝撃/真実 phổ biến ngách nhật bứt phá
    "老後 末路 漫画動画", "定年 末路 漫画動画", "年金 現実 漫画動画",
    "退職金 現実 漫画動画", "老後 衝撃の理由 漫画",
    # mở rộng nhẹ sang nghề nghiệp cụ thể hay dùng làm nhân vật
    "漫画 元教師 老後", "漫画 元公務員 老後", "漫画 元銀行員 老後",
    "漫画 元サラリーマン 老後", "漫画 中小企業 社長 老後",
    # vòng 2 (2026-09-27) — học từ kết quả vòng 1: nhiều kênh dùng マンガ (katakana) hoặc
    # không có 漫画/マンガ trong tên mà chỉ có 物語/シニア/朗読/逆襲/知恵/ラボ
    "マンガ 老後", "マンガ シニア", "マンガ 定年", "マンガ 人生 老後", "マンガ 熟年",
    "シニア 物語", "老後 物語", "定年 物語", "熟年 物語", "人生 物語 老後",
    "シニア 朗読", "老後 朗読", "熟年 朗読劇", "シニア 逆襲", "シニアの逆襲",
    "シニア 知恵", "老後 教訓 物語", "シニア 幸福", "老後の分かれ道", "人生 ラボ",
    "老後 ラジオ", "老後 お役立ち情報", "シニア お役立ち", "偉人の遺言", "賢者のしおり",
    "老後 自営", "60歳から お金", "定年 お金 マンガ", "老後 スカッと", "シニア スカッと",
    "私を甘く見るな 漫画", "人生の果実 漫画", "老後 相談室 漫画", "老後の知恵袋 漫画",
    "定年 漫画 実話", "老後 漫画 実話", "熟年離婚 漫画", "老後 女性 一人 漫画",
    "夫婦 老後 マンガ", "老後 貧困 マンガ", "定年 貧困 マンガ", "退職 貧困 マンガ",
]

CH_MULT_MIN = 2.0
MIN_SUBS = 300


def dedup_channels(it: InnerTube, pool: ProxyPool, out_dir: Path) -> dict[str, dict]:
    raw_p = out_dir / "all_channels_raw.json"
    done_p = out_dir / "scanned_keywords.json"
    seen: dict[str, dict] = json.loads(raw_p.read_text(encoding="utf-8")) if raw_p.exists() else {}
    done = set(json.loads(done_p.read_text(encoding="utf-8"))) if done_p.exists() else set()
    todo = [kw for kw in KEYWORDS if kw not in done]
    print(f"resume: {len(seen)} kênh đã có từ trước, {len(done)}/{len(KEYWORDS)} từ khoá đã quét, "
          f"còn {len(todo)} từ khoá mới")
    log = (out_dir / "scan.log").open("a", encoding="utf-8")
    for i, kw in enumerate(todo):
        for window in ("month", "week"):
            for attempt in range(3):
                try:
                    rows = it.search(kw, window=window, pages=2)
                    break
                except (BotCheckError, ProxyError) as e:
                    msg = f"  [{kw}/{window}] {type(e).__name__}, đổi proxy"
                    print(msg); log.write(msg + "\n")
                    it.set_proxy(pool.next())
                    time.sleep(3)
            else:
                continue
            for r in rows:
                cid = r["channel_id"]
                if cid not in seen:
                    seen[cid] = {"channel_id": cid, "channel": r["channel"], "sample_video": r["title"],
                                "sample_views_it": r["views_it"], "found_kw": kw}
            msg = f"[{i+1}/{len(todo)}] {kw}/{window}: +{len(rows)} video, {len(seen)} kênh duy nhất tính tới giờ"
            print(msg); log.write(msg + "\n"); log.flush()
        done.add(kw)
        raw_p.write_text(json.dumps(seen, ensure_ascii=False, indent=1), encoding="utf-8")
        done_p.write_text(json.dumps(sorted(done), ensure_ascii=False, indent=1), encoding="utf-8")
    log.close()
    return seen


def enrich_and_filter(seen: dict[str, dict], api: YouTubeAPI, max_subs: int) -> list[dict]:
    ids = list(seen.keys())
    out = []
    for i in range(0, len(ids), 50):
        chunk = ids[i:i + 50]
        try:
            info = api.channels_batch(chunk)
        except QuotaExhausted:
            print("  ✗ hết quota Data API, dừng enrich sớm")
            break
        for cid, meta in info.items():
            subs = meta["subs"]
            if not (MIN_SUBS <= subs < max_subs):
                continue
            row = {**seen[cid], **meta}
            try:
                base = api.baseline_videos(meta["uploads_playlist"], want=12, min_age_days=7, fetch=24)
            except Exception as e:
                print(f"  ✗ {cid} baseline lỗi: {type(e).__name__}")
                continue
            if not base:
                continue
            views = sorted(v["views"] for v in base)
            median = views[len(views) // 2]
            ch_mult = round(median / max(subs, 1), 3)
            top_view = max((v["views"] for v in base), default=0)
            row.update(median_view=median, ch_mult=ch_mult, n_baseline=len(base), top_baseline_view=top_view)
            out.append(row)
        print(f"  enrich {min(i+50,len(ids))}/{len(ids)} kênh, giữ lại {len(out)} qua lọc subs")
    out.sort(key=lambda r: -r["ch_mult"])
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--max-subs", type=int, default=30000)
    a = ap.parse_args()
    out_dir = ROOT / a.out
    out_dir.mkdir(parents=True, exist_ok=True)

    load_dotenv(ROOT / "config" / ".env")
    pool = ProxyPool(load_proxies(ROOT / "config" / "proxies.txt"))
    it = InnerTube(hl="ja", gl="JP", proxy_url=pool.next())
    api = YouTubeAPI(os.environ["YOUTUBE_API_KEY"], safety_limit=9000)

    print(f"=== QUÉT {len(KEYWORDS)} từ khoá x 2 window x 2 trang ===")
    seen = dedup_channels(it, pool, out_dir)
    (out_dir / "all_channels_raw.json").write_text(json.dumps(seen, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\n=== TỔNG {len(seen)} kênh duy nhất chạm được, giờ enrich + lọc subs<{a.max_subs} ===")

    kept = enrich_and_filter(seen, api, a.max_subs)
    (out_dir / "candidates.json").write_text(json.dumps(kept, ensure_ascii=False, indent=1), encoding="utf-8")
    with (out_dir / "candidates.csv").open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["channel_id", "channel_title", "subs", "ch_age_days", "ch_video_count", "median_view",
                    "ch_mult", "top_baseline_view", "found_kw", "url"])
        for r in kept:
            w.writerow([r["channel_id"], r.get("channel_title") or r.get("channel"), r["subs"], r.get("ch_age_days"),
                       r.get("ch_video_count"), r["median_view"], r["ch_mult"], r["top_baseline_view"],
                       r["found_kw"], f"https://www.youtube.com/channel/{r['channel_id']}"])
    good = [r for r in kept if r["ch_mult"] >= CH_MULT_MIN]
    print(f"\n=== XONG: {len(seen)} kênh chạm · {len(kept)} qua lọc subs<{a.max_subs} · "
          f"{len(good)} đạt ch_mult>={CH_MULT_MIN} (đáng xem trước) ===")
    print(f"-> {out_dir}\\candidates.csv (đủ), lọc ch_mult>={CH_MULT_MIN} để xem nhanh")


if __name__ == "__main__":
    main()
