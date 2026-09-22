# IMPLEMENTATION_PLAN.md — VIDEO HUNT V2

> Thư mục gốc: `E:\CLAUDE\YOUTUBE\TRENDING-RESEARCH`
> Nguồn yêu cầu: `E:\CLAUDE\YOUTUBE\TRENDING-RESEARCH\VIDEO_HUNT_V2_CLAUDE_IMPLEMENTATION_GUIDE.md` (mục 37–41)
> Trạng thái: **KẾ HOẠCH — chưa sửa dòng code nào.** Chờ user review.
> Ngày lập: 2026-09-22

**Mục tiêu:** Đưa Video Hunt từ "search theo tag → lọc chuỗi → 1 call LLM → view/ngày" sang kiến trúc 11 gate của V2, **không phá lượt chạy hiện tại**, chạy `shadow_mode=true` song song cho tới khi Top 2 của V2 được owner accept ≥ 80%.

**Kiến trúc:** Giữ nguyên `src/run_video_hunt.py` làm đường OLD. Thêm gói `src/hunt_v2/` chứa từng gate là 1 file ≤ 200 dòng, mỗi gate ghi JSON riêng vào `runs/<ngày>/<lane>/`. Runner V2 chạy SAU đường OLD trong cùng tiến trình, đọc chung pool discovery + enrich, và ghi kết quả so sánh vào tab audit `TRD_HUNT_AUDIT`. Tab `RESEARCH` vẫn nhận pick OLD chừng nào `shadow_mode=true`.

**Stack:** Python 3.13 (`py -3.13 -X utf8`), InnerTube keyless, YouTube Data API v3, SQLite `data/trending.db`, gspread, ramclouds `https://ramclouds.me/v1` (OpenAI-compatible), PyYAML, pytest (thêm mới).

## Ràng buộc toàn cục (không được vi phạm ở bất kỳ task nào)

- Sheet `1xu4iNudIPanWrUxlTODqIySGf9YxLy7rpTq9OtXDMOU`: **chỉ** ghi tab `TRENDING`, prefix `TRD_`, và `RESEARCH`. **Cấm mọi thao tác xoá/clear/ghi đè hàng loạt.** Tab audit mới phải tên `TRD_HUNT_AUDIT` (nằm trong whitelist sẵn, không nới `_assert_allowed`).
- Cột `HUMAN_DECISION` / `REJECT_REASON` trên `TRD_HUNT_AUDIT` là của user gõ — tool **chỉ đọc**, không bao giờ ghi đè.
- File code ≤ 200 dòng. Không hard-code model string ngoài `config/models.yaml`. Không hard-code threshold ngoài `config/hunt_rules.yaml`.
- Mọi call LLM phải lưu `raw_response` + `parsed_response` + `latency_ms` + `attempt`; lỗi parse **không được nuốt im lặng** (khác `reup_filter.classify` hiện tại trả `{}`).
- Rule "title match ≥ 2 tag" → **feature `keyword_match_score`**, không còn là hard reject (guide §10).
- Thiếu 1 trong 4 cờ `SEMANTIC_PASS / FORMAT_PASS / VIRAL_PASS / FINAL_QC_PASS` → không được production-select. Sol lỗi → `FINAL_QC_STATUS=ERROR`, không coi là PASS (guide §33).
- Không dùng Google Trends (pytrends chết). Không thử lại retention heatmap đối thủ.
- Dự án **không phải git repo** → không có bước commit; rollback bằng feature flag + giữ nguyên file OLD. Khuyến nghị `git init` trước khi bắt đầu P0 (xem mục 8).

---

## 1. DATA FLOW HIỆN TẠI (đã đọc code thật, không suy diễn)

Entry: `src/run_video_hunt.py::main()` → `run_lane()` cho từng lane trong `config/video_hunt.yaml`.

```text
[H0] config/video_hunt.yaml (lanes: tab/col/label/seed_tags)   ← không có lane_profile
       + Google Sheet tab lane, cột F = tag (hunt_tags.lane_keywords)
       + stop_tags (defaults.stop_tags)
         │
[H1] innertube.InnerTube.search(kw, window∈{week,month}, pages=2)   ← 1 nguồn duy nhất (tag)
       ProxyPool đổi proxy khi BotCheckError/ProxyError
       → dict video_id → {title, channel, channel_id, views_it, age_hours_it, duration_s_it, keyword, window}
         │
     sơ loại views_it ≥ min_views (10.000)
         │
[H2] enrich.Enricher.build_rows()  → ytapi.videos_batch + channels_batch (+ scrape /about fallback)
       → rows (ROW_FIELDS: views/likes/comments/duration_s/published_at/age_hours/subs/ch_*/uploads_playlist/src)
       store.save_snapshot() → SQLite video/video_snapshot/channel/channel_snapshot
       ← KHÔNG có description, tags, baseline kênh
         │
[H6-cũ] hunt_score.score_rows(): vpd = views/age_days ; score = vpd × (1 + (14-age)/14)  ← boost tới 2×
         │
[H3] hunt_score.filter_rows(): already_picked · is_japanese_title(kana) · is_live_stream ·
       title_matches_pool(≥2 tag, min_len 4)  ← HARD REJECT cần bỏ · views ≥ 10k · age ≤ 30d ·
       duration ≥ 180s · _is_dup_topic(difflib ≥0.6 với cột B/E tab lane)
         │
[H4/H5-cũ] reup_filter.classify(top 30 theo score) → 1 call ramclouds gemini-3.5-flash-low
       prompt ORIGINAL/REUP/VLOG_PERSON, JSON list, KHÔNG schema check, KHÔNG cache,
       KHÔNG log raw, lỗi → {} → pipeline CHẠY TIẾP KHÔNG GATE (fail-open)
         │
[H9-cũ] hunt_score.pick_top(n=2, distinct_channels) ; reason_text()
         │
[H10] Sheet tab RESEARCH: dòng (DATE, RANK) × cột lane, ô = https://youtu.be/<id>
       store.save_hunt_picks() → SQLite hunt_pick (chống chọn lại)
       guard_snapshot() trước/sau
[H11] không có (chỉ có lane_done_titles đọc cột B/E làm chống trùng đề tài)
```

**Sheet input:** tab lane (`shinya_shiryoshitsu`, `Lopezzapa68`, `irogatatarukioku`, `70dai-kenko`, `teinengo-real`, `teinengo-tanoshimi`, `kokoro-kazoku`, `sengoku-uragawa`, `teinengo-fuufu`) — cột F tag, cột B mô tả đề tài, cột E tiêu đề đã đăng. **Chỉ đọc.**
**Sheet output:** tab `RESEARCH` header `DATE, RANK, <9 cột lane>` — mỗi ô = 1 link. SQLite `hunt_pick` đã có 18 pick ngày 2026-09-22 (4 lane).

**LLM đang gọi thế nào:** `config/.env` → `LLM_BASE_URL=https://ramclouds.me/v1`, `LLM_MODEL=gemini-3.5-flash-low`, `LLM_API_KEY`. Gọi `requests.post(f"{base}/chat/completions")` kiểu OpenAI, `temperature 0.2`, `max_tokens 1500`, timeout 120. Duy nhất 1 chỗ gọi: `src/reup_filter.py::classify()`.

---

## 2. MAPPING KIẾN TRÚC CŨ ↔ V2

| Gate V2 | Module cũ | Quyết định | Ghi chú |
|---|---|---|---|
| H0 Lane profile | `config/video_hunt.yaml` (lanes) + tag cột F Sheet | **SỬA + TẠO MỚI** | Giữ yaml làm nguồn `tab/col/label`; thêm `lanes/<lane>/lane_profile.yaml`. Lane chưa có profile → V2 skip lane đó (không lỗi). |
| Query expansion | `seed_tags` + `stop_tags` | **TẠO MỚI** | `lanes/<lane>/query_expansion.json`; `seed_tags` = `core_tags` ban đầu. |
| H1 Discovery | `src/innertube.py`, `src/proxy_pool.py`, `run_video_hunt.discover_lane()` | **GIỮ** (tái dùng nguyên) + **TẠO** `discovery.py` bọc ngoài | Thêm nguồn B/C/D. Window `today` đã có trong `WINDOW_PARAMS` nhưng chưa dùng. |
| H2 Enrich | `src/enrich.py`, `src/ytapi.py` | **SỬA nhỏ** | `videos_batch` thêm `description`, `tags`, `live_broadcast_content`. Baseline: tái dùng `ytapi.baseline_videos()` (đã bỏ video <7 ngày). |
| H3 Hard filter | `src/hunt_score.py::filter_rows/title_matches_pool/is_japanese_title/is_live_stream` | **GIỮ hàm, TẠO** `hard_filter.py` gọi lại | `title_matches_pool` → đổi thành `keyword_match_score()` trả 0–1. Hàm cũ giữ nguyên cho đường OLD. |
| H4 Semantic gate | không có | **TẠO MỚI** | `semantic_gate.py` |
| H5 Format gate | `src/reup_filter.py` (ORIGINAL/REUP/VLOG_PERSON) | **GIỮ cho OLD, TẠO** `format_gate.py` | Gộp chung 1 call với H4 (guide §12 cho phép). `reup_filter` → BỎ ở P2 sau khi V2 lên production. |
| H6 Viral engine | `hunt_score.score_rows` (vpd × fresh ≤2×) | **GIỮ cho OLD, TẠO** `viral_engine.py` | Tái dùng `score.channel_baseline_from_videos()` + bảng `channel_baseline` (thêm cột `median_vph`). |
| H7 Opportunity | không có | **TẠO MỚI** | `opportunity_gate.py` |
| H8 Final QC | không có | **TẠO MỚI** | `final_qc.py` |
| H9 Ranking | `hunt_score.pick_top` | **GIỮ cho OLD, TẠO** `ranker.py` | Diversity: đã có `distinct_channels`; thêm penalty same-topic. |
| H10 Sheet | `run_video_hunt.main()` khối ghi RESEARCH, `src/sheets.py`, `src/sheet_schema.py` | **GIỮ + SỬA nhỏ** | Thêm `HEADERS["TRD_HUNT_AUDIT"]`. Khối ghi RESEARCH giữ nguyên, chỉ đổi nguồn `all_picks` khi `shadow_mode=false`. |
| H11 Feedback | `hunt_tags.lane_done_titles` (chống trùng) | **GIỮ + TẠO** `feedback.py` | Đọc `HUMAN_DECISION` từ `TRD_HUNT_AUDIT`. |
| LLM client | `reup_filter.classify` (requests thô) | **TẠO MỚI** `llm_client.py` | Retry/schema/cache/log. `reup_filter` không đổi. |
| Store | `src/store.py` | **SỬA nhỏ** | Thêm bảng `llm_cache`, `hunt_v2_pick`, cột baseline. Không đổi bảng cũ. |
| Run log | không có | **TẠO** `run_store.py` | `runs/YYYY-MM-DD/<lane>/NN_*.json` + `report.md`. |

### 2.1 Bảng GIỮ / SỬA / TẠO MỚI / BỎ

**GIỮ NGUYÊN (0 dòng thay đổi):** `src/innertube.py`, `src/proxy_pool.py`, `src/lockfile.py`, `src/gapi.py`, `src/hunt_tags.py`, `src/reup_filter.py` (tới P2), `src/hunt_score.py` (đường OLD vẫn import), `src/sheets.py`, `src/score.py`, toàn bộ `run_daily.py / trend_hunter.py / explore_niches.py / deepdive.py / …` (luồng khác, không liên quan).

**SỬA (backward-compatible, thêm không bớt):**
| File | Sửa gì |
|---|---|
| `src/ytapi.py` | `videos_batch` thêm field `description`, `tags`, `live_broadcast_content`, `default_language` (cùng request `part=snippet`, **0 quota thêm**). Thêm `baseline_vph_rows()` tái dùng `baseline_videos` trả kèm `age_hours`. |
| `src/enrich.py` | `ROW_FIELDS` thêm `description`, `tags`, `live_broadcast_content`; `build_rows` copy các field này (default rỗng khi không có API). |
| `src/store.py` | `SCHEMA` thêm `CREATE TABLE IF NOT EXISTS llm_cache`, `hunt_v2_pick`, `human_feedback`; `ALTER TABLE channel_baseline ADD COLUMN median_vph` (bọc try/except vì ALTER không có IF NOT EXISTS). |
| `src/sheet_schema.py` | `HEADERS["TRD_HUNT_AUDIT"] = [...]` (24 cột guide §19 + `OLD_SELECTED`, `V2_SELECTED`, `RUN_MODE`). |
| `src/run_video_hunt.py` | Sau khi có `picks` OLD: nếu `cfg["video_hunt_v2"]["enabled"]` → gọi `hunt_v2.runner.run_lane_v2(...)` với cùng `found`/`rows`; `shadow_mode` quyết định nguồn ghi RESEARCH. Thêm flag `--v2-only-lane`, `--no-v2`. ≤ 25 dòng thêm. |
| `config/video_hunt.yaml` | Thêm khối `video_hunt_v2:` (feature flags). |
| `requirements.txt` | Thêm `pytest`, `jsonschema`. |
| `.gitignore` | Thêm `runs/`, `logs/`. |

**TẠO MỚI:**
```text
config/models.yaml
config/hunt_rules.yaml
lanes/<lane_id>/{lane_profile.yaml, query_expansion.json, watch_channels.json,
                 positive_examples.json, negative_examples.json, blacklist.json}   × 9 lane
src/hunt_v2/__init__.py
src/hunt_v2/schemas.py
src/hunt_v2/llm_client.py
src/hunt_v2/run_store.py
src/hunt_v2/lane_profile.py
src/hunt_v2/discovery.py
src/hunt_v2/baseline.py
src/hunt_v2/hard_filter.py
src/hunt_v2/semantic_format_gate.py     (H4+H5 chung 1 call; tên file gộp để không tạo 2 file mỏng)
src/hunt_v2/viral_engine.py
src/hunt_v2/opportunity_gate.py
src/hunt_v2/final_qc.py
src/hunt_v2/ranker.py
src/hunt_v2/audit_writer.py
src/hunt_v2/feedback.py
src/hunt_v2/runner.py
src/hunt_v2/prompts/{semantic_format_v1.txt, opportunity_v1.txt, finalqc_v1.txt}
tests/conftest.py
tests/fixtures/video_hunt_cases.json
tests/test_hard_filter.py, test_viral_engine.py, test_llm_client.py, test_ranker.py,
tests/test_regression_owner_cases.py, test_sheet_guard_audit.py
```

**BỎ (chỉ sau khi V2 lên production ≥ 2 tuần, P2):** `src/reup_filter.py` (thay bằng format gate), hàm `title_matches_pool` hard-reject trong đường OLD, `fresh_mult` 2× trong `hunt_score.score_rows`.

### 2.2 Phần code hiện tại TÁI SỬ DỤNG được (không viết lại)

| Thứ tái dùng | Ở đâu | Dùng cho |
|---|---|---|
| `InnerTube.search(kw, window, pages)` + `WINDOW_PARAMS["today"]` | `src/innertube.py:153` | H1 mọi nguồn query; thêm window `today` cho bucket 0–3 ngày |
| `discover_lane()` (đổi proxy khi bot-check) | `src/run_video_hunt.py:45` | H1 — gọi lại với list query mở rộng |
| `ProxyPool`, `RunLock`, `retry_api` | `proxy_pool.py`, `lockfile.py`, `gapi.py` | nguyên xi |
| `Enricher.build_rows`, `channels()` cache | `src/enrich.py` | H2 |
| `YouTubeAPI.baseline_videos(uploads_playlist, want=12, min_age_days=7)` | `src/ytapi.py:114` | H2 baseline kênh — đã lọc video <7 ngày (bẫy đã trả giá) |
| `score.channel_baseline_from_videos()` + `store.channel_baseline` | `src/score.py:138`, `store.py` | median/p90/trend kênh → H6 breakout |
| `is_japanese_title`, `is_live_stream`, `_is_dup_topic`, `age_days_of` | `src/hunt_score.py` | H3 |
| `title_matches_pool` (logic đếm hit) | `src/hunt_score.py:36` | đổi thành `keyword_match_score` = hits / max(2, min(len(checkable), 4)) clamp 0–1 |
| `pick_top` distinct-channel | `src/hunt_score.py` | H9 diversity rule |
| `_strip_fence()` | `src/reup_filter.py` | `llm_client` JSON repair bước 1 |
| `SheetReporter.ensure_tab / append / guard_snapshot` | `src/sheets.py` | H10 audit tab |
| Khối ghi RESEARCH merge theo (DATE, RANK) | `run_video_hunt.py:164-205` | giữ nguyên, chỉ đổi nguồn picks |
| `store.save_hunt_picks / picked_video_ids` | `src/store.py` | chống chọn lại — V2 dùng bảng riêng `hunt_v2_pick` để không làm nhiễu OLD |
| Các comment "đã dính thật" trong `hunt_score.py`, `video_hunt.yaml` | — | seed cho `tests/fixtures/video_hunt_cases.json` (mục 41 guide) |

---

## 3. FEATURE FLAGS (thêm vào `config/video_hunt.yaml`)

```yaml
video_hunt_v2:
  enabled: true            # false → run_video_hunt.py chạy y hệt hôm nay, không import hunt_v2
  shadow_mode: true        # true → RESEARCH nhận pick OLD; V2 chỉ ghi TRD_HUNT_AUDIT + runs/
  discovery_expansion: false   # P1
  semantic_gate: true
  format_gate: true
  viral_engine_v2: true
  opportunity_gate: false  # P1
  final_qc: false          # P1
  feedback_learning: false # P2
  write_audit_tab: true    # false → chỉ ghi runs/ local
```

Quy tắc: gate tắt → candidate được gắn `<gate>_status = "SKIPPED"` và **không** được coi là PASS → với `final_qc=false` thì V2 không bao giờ production-select (đúng guide §33/§34.7). Đây là lý do P0 buộc phải shadow.

---

## 4. P0 — DATA FOUNDATION + GEMINI GATES + SHADOW (guide Phase 1–2)

Điều kiện xong P0: chạy `py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\TRENDING-RESEARCH\src\run_video_hunt.py --dry-run` ra đủ `runs/<ngày>/<lane>/01..06_*.json + 09_ranked.json + report.md` cho 9 lane; chạy thật ghi RESEARCH **giống hệt** hôm nay + thêm tab `TRD_HUNT_AUDIT`; `pytest` xanh; guard_snapshot GMAIL/NOTE không đổi.

| ID | Task | File | Current behavior | New behavior | Risk | Test | Rollback |
|---|---|---|---|---|---|---|---|
| P0-01 | Feature flags + rules + models config | `config/video_hunt.yaml`, `config/hunt_rules.yaml` (mới), `config/models.yaml` (mới) | Threshold rải trong `defaults`; model trong `.env` | Khối `video_hunt_v2` (mục 3); `hunt_rules.yaml` chứa threshold semantic (75/65/65, 55/50), viral weights (.30/.30/.20/.10/.10), freshness (1.35/1.25/1.15/1.00), `MIN_BASELINE_VPH`, breakout 2/5/10, ranking weights (.40/.25/.20/.10/.05), diversity_penalty 25; `models.yaml` map gate→{provider, model, timeout, max_tokens}. `.env` vẫn giữ key. | Sai key YAML làm crash lúc load | `tests/test_config.py`: load 3 file, assert mọi key bắt buộc có, weights cộng = 1.0 | Xoá khối `video_hunt_v2` hoặc `enabled: false` |
| P0-02 | `schemas.py` | `src/hunt_v2/schemas.py` | Không có validate JSON | Dataclass/dict schema cho: Candidate (H2), SemanticResult, FormatResult, ViralResult, OpportunityResult, FinalQcResult, SelectedRecord (guide §36). Hàm `validate(name, obj) -> list[str]` trả lỗi, `require_critical(record)` ném khi thiếu field critical. Dùng `jsonschema`. | Schema quá chặt làm reject output hợp lệ của model | Unit test: mẫu hợp lệ pass, thiếu `decision` fail, `decision="MAYBE"` fail | Không dùng ở đâu nếu gate tắt |
| P0-03 | `llm_client.py` | `src/hunt_v2/llm_client.py` | `reup_filter.classify`: 1 request, lỗi → `{}` | `class LlmClient(models_cfg, con)`: `call(gate, prompt_version, messages, schema_name, cache_key_parts) -> LlmResult{model, provider, latency_ms, attempt, raw_response, parsed_response, cached, error}`. Provider routing đọc `models.yaml` + env key theo provider (`LLM_API_KEY` cho ramcloud; `ANTHROPIC_API_KEY`, `OPENAI_API_KEY` P1). Retry 3 lần backoff; JSON repair = `_strip_fence` → tìm `{...}`/`[...]` ngoài cùng → parse; validate schema; fail → `error` field, **không** ném nuốt. Cache SQLite `llm_cache(key sha256(video_id+lane_hash+gate+prompt_version+model), payload, created)`. Fallback provider từ `models.yaml.fallback` khi 5xx/timeout. Log 1 dòng/call vào `logs/llm_YYYYMMDD.jsonl`. | ramclouds 524 Cloudflare ~100s (skill `proxy-llm-api-gotchas`) → timeout phải ≤ 90s và batch nhỏ; model name trên ramclouds phải probe `/v1/models` trước — **`gemini-flash-3.8` trong guide chưa verify tồn tại, hiện đang chạy `gemini-3.5-flash-low`** | `tests/test_llm_client.py` với `requests.post` monkeypatch: (a) JSON có fence → parse OK, (b) JSON hỏng → `error` set, không exception, (c) cache hit không gọi network, (d) đổi `prompt_version` → cache miss, (e) 503 → fallback provider | Gate tắt → không gọi |
| P0-04 | `run_store.py` | `src/hunt_v2/run_store.py` | Không lưu trung gian | `RunStore(root, snap_date, lane)`: `save(step_no, name, obj)` → `runs/<ngày>/<lane>/NN_name.json` (không overwrite: nếu file có thì ghi `NN_name.<HHMMSS>.json`), `report(counts, reasons, errors)` → `report.md`. | Đầy đĩa nếu chạy nhiều lượt/ngày (mỗi lane ~1–3 MB) | Test ghi 2 lần cùng step → 2 file | Xoá `runs/` |
| P0-05 | Lane profile loader + 9 hồ sơ lane | `src/hunt_v2/lane_profile.py`, `lanes/<lane>/lane_profile.yaml`, `query_expansion.json`, `watch_channels.json`, `positive_examples.json`, `negative_examples.json`, `blacklist.json` | Lane = `tab/col/label/seed_tags` | `load_lane(lane_id) -> LaneProfile` (dataclass, `fingerprint()` = sha256 nội dung yaml + examples). Thiếu profile → `None` và runner log "lane bỏ qua V2". Soạn 9 profile từ `label` + `seed_tags` + `docs/LANE_*_HANDOFF.md` (lane A/C/D có tài liệu đầy đủ; 6 lane còn lại soạn từ seed + ô B1 tab, đánh dấu `draft: true` để user duyệt). `query_expansion.json`: `core_tags` = seed_tags; các nhóm khác Claude soạn. `watch_channels.json`: lane A/C/D điền kênh mẫu đã duyệt (`UCvA0jwPl5qjhsHQOWuZYe-g`, `UCaj1dslbibbHEnOAOh0tyYw`…), lane khác `[]`. `negative_examples.json` seed từ lỗi đã ghi trong code: idol scandal, ẩm thực, MV「サイエンス」, Disney/LA lọt lane D, tiếng Trung, tiếng Anh, live-cam sân bay, talk-show cảnh sát Mỹ. | Profile soạn sai chủ đề → semantic gate reject nhầm hàng loạt (chỉ ảnh hưởng shadow) | `tests/test_lane_profile.py`: load 9 lane không lỗi, `fingerprint` đổi khi sửa 1 ký tự, lane không tồn tại → None | Xoá thư mục `lanes/<lane>` → lane đó tự rơi về OLD |
| P0-06 | Enrich thêm description/tags + baseline kênh | `src/ytapi.py`, `src/enrich.py`, `src/hunt_v2/baseline.py`, `src/store.py` | `videos_batch` bỏ qua `description/tags`; không có baseline cho Video Hunt | `videos_batch` trả thêm `description`, `tags`, `live_broadcast_content`, `default_language` (cùng `part=snippet`, 0 quota thêm). `baseline.py::channel_baseline(api, con, channel_id, uploads_playlist, max_age_days=7)`: đọc `channel_baseline` nếu `updated` ≤ 7 ngày; không thì gọi `api.baseline_videos(want=10)` → `recent_video_views/age_hours/vph`, `median_recent_views`, `median_recent_vph` → lưu. **Chỉ gọi cho candidate đã qua H3+H4/H5** (không phải toàn pool) để tiết kiệm quota: 2 quota/kênh × ~30 kênh/lane × 9 lane ≈ 540 quota/ngày. | Quota 10k/ngày: nếu pool sau semantic > 100 kênh/lane sẽ vượt → có `max_baseline_channels_per_lane: 40` trong rules, ưu tiên theo vpd. `QuotaExhausted` → baseline `None` → breakout_score = 50 (trung tính) + flag `BASELINE_MISSING` | Test `baseline.py` với API giả: 12 video (3 video <7d) → median tính trên 9; cache hit không gọi API; `median_recent_vph` floor `MIN_BASELINE_VPH` | Field mới default rỗng; OLD không đọc |
| P0-07 | `hard_filter.py` + `keyword_match_score` | `src/hunt_v2/hard_filter.py` (tái dùng hàm `hunt_score`) | `filter_rows` hard-reject khi <2 tag khớp | `apply(rows, lane, rules, already_picked, done_titles, kws) -> (kept, rejected[{video_id, reason}])`. Loại: age>30d, views<min, live (`is_live_stream` + `live_broadcast_content!="none"`), duration ngoài `lane.duration`, `blacklist.json`, already picked (bảng `hunt_v2_pick`), không có kana (giữ, vì lane JP), dup topic. **Không** loại theo tag; gắn `keyword_match_score` 0–1 và `matched_tags`. | Pool lớn hơn ~2–3× → tăng số call semantic gate (ước 150–300 candidate/lane → batch 20 = 8–15 call/lane ≈ 100 call/ngày gemini, chấp nhận) | `tests/test_hard_filter.py`: video khớp 1 tag vẫn kept với score 0.25–0.5; live → rejected reason `LIVE`; fixture cases mục 40 | OLD vẫn dùng `filter_rows` |
| P0-08 | Semantic + Format gate (1 call) | `src/hunt_v2/semantic_format_gate.py`, `src/hunt_v2/prompts/semantic_format_v1.txt` | `reup_filter`: 3 nhãn, top 30, fail-open | `run(cands, lane, client, rules) -> list[cand + semantic{} + format{}]`. Batch 15 video/call (nhỏ để né 524), input gồm LANE_PROFILE, title, description (cắt 600 ký tự), channel_title, tags, keyword_match_score, 5 positive + 5 negative examples. Output per video = schema §11 + §12. Decision theo threshold `hunt_rules.yaml`. `UNCERTAIN` → retry 1 lần đơn lẻ (không batch); vẫn UNCERTAIN → giữ, gắn cờ. Model lỗi/parse lỗi → `status=ERROR`, candidate **không** PASS. Phân biệt `real_person_present` vs `host_driven` (guide §12). | Gemini chấm lệch nhẹ → điều chỉnh threshold sau shadow; cost ~100 call/ngày | `tests/test_semantic_format_gate.py` (client giả): decision map đúng ngưỡng; ERROR không thành PASS; UNCERTAIN retry đúng 1 lần. Regression: fixture "US police talk show" → format REJECT | `semantic_gate: false` / `format_gate: false` |
| P0-09 | `viral_engine.py` | `src/hunt_v2/viral_engine.py` | `score = vpd × fresh(≤2×)` | `score(cands, baselines, rules) -> cands + viral{vph, vpd, breakout_ratio, absolute_view_score, velocity_score, breakout_score, engagement_score, freshness_score, viral_score, viral_type, viral_pass}`. Chuẩn hoá percentile **trong pool của lane cùng lượt** (log10 cho absolute). Freshness bucket 0–3/4–7/8–14/15–30 → 1.35/1.25/1.15/1.00 quy về 0–100. `viral_type` theo ngưỡng rules. `viral_pass = viral_score ≥ rules.viral.min_score` (mặc định 40). Baseline thiếu → breakout_score 50 + flag. Không AI. | Pool nhỏ (<5 video) → percentile vô nghĩa → rules `min_pool_for_percentile: 8`, dưới đó dùng log-scale tuyệt đối | `tests/test_viral_engine.py`: kênh 50 view thường + video 2k → breakout cao nhưng absolute thấp → không đứng top; kênh lớn view bình thường → `NORMAL`; floor baseline tránh chia 0; weights từ rules | `viral_engine_v2: false` → V2 dùng `hunt_score.score_rows` |
| P0-10 | `ranker.py` (bản P0: không có opportunity/QC) | `src/hunt_v2/ranker.py` | `pick_top` theo score | `rank(cands, rules, n, require_flags) -> ranked`. `final_score` theo §17 (sub-score thiếu → dùng weight còn lại chuẩn hoá lại, ghi `score_components`). Diversity: same channel +25 penalty, `_is_dup_topic` ≥0.6 với rank trên +15. `require_flags` P0 = `{semantic, format, viral}`; P1 thêm `final_qc`. Trả `shadow_rank` cho mọi candidate PASS kể cả khi chưa đủ cờ production. | Ở P0 thiếu `final_qc_pass` nên **không** bao giờ đủ điều kiện production — cố ý | `tests/test_ranker.py`: cùng kênh bị phạt; thiếu cờ → không vào `selected`, có trong `shadow_ranked` | `shadow_mode` giữ RESEARCH = OLD |
| P0-11 | Audit tab + so sánh OLD/V2 | `src/sheet_schema.py`, `src/hunt_v2/audit_writer.py`, `src/store.py` | Sheet chỉ có link | `HEADERS["TRD_HUNT_AUDIT"]` = 24 cột §19 + `OLD_SELECTED`, `V2_SELECTED`, `RUN_MODE`, `RUN_ID`. `write(rep, rows)`: `ensure_tab` + `append` (chỉ append). Ghi cho: mọi pick OLD (2/lane) + top 5 shadow V2/lane; cột `HUMAN_DECISION`, `REJECT_REASON` để trống. `store.hunt_v2_pick` lưu bản đầy đủ (JSON payload) để không phụ thuộc Sheet. Trước/sau vẫn `guard_snapshot`. | Thêm ~60 dòng/ngày; chạy lại trong ngày sẽ append trùng → khoá idempotent: đọc cột `RUN_ID`+`VIDEO_URL` hôm nay trước, bỏ dòng đã có | `tests/test_sheet_guard_audit.py`: `_assert_allowed("TRD_HUNT_AUDIT")` OK, `HUNT_AUDIT` (không prefix) bị chặn; writer không gọi hàm nào ngoài `append/ensure_tab` (grep) | `write_audit_tab: false` |
| P0-12 | `runner.py` + nối vào `run_video_hunt.py` | `src/hunt_v2/runner.py`, `src/run_video_hunt.py` | 1 đường | `run_lane_v2(lane_id, lcfg, cfg, found, rows, api, client, con, rep, run_store) -> V2Result{shadow_ranked, selected, counts}`; gọi H3→H4/5→baseline→H6→H9, mỗi bước `run_store.save`. `run_video_hunt.run_lane` trả thêm `found`+`rows` (đóng gói vào dict, chữ ký cũ giữ qua wrapper) → `main` gọi V2 **sau** OLD, bọc `try/except Exception` log lỗi + `report.md` — lỗi V2 **không** làm hỏng ghi RESEARCH OLD. `--no-v2` bỏ qua V2; `--dry-run` vẫn chạy V2 nhưng chỉ ghi `runs/`. Cuối `main` in bảng so sánh: `lane | OLD top2 | V2 top2 | trùng?`. | Thời gian chạy +2–5 phút/lane (LLM). Scheduled task đang tạm dừng nên không ảnh hưởng lịch. | Chạy `--dry-run` thật với `--lane shinya_shiryoshitsu`; kiểm `runs/` có 7 file; ép lỗi (`LLM_API_KEY` sai) → OLD vẫn ra pick, V2 report ghi ERROR | `enabled: false` hoặc `--no-v2` → không import `hunt_v2` |
| P0-13 | Test dataset + regression owner | `tests/fixtures/video_hunt_cases.json`, `tests/test_regression_owner_cases.py`, `tests/conftest.py` | Không có `tests/` | ≥ 14 case theo mục 40 + 41: đúng ngách/view cao; đúng ngách/breakout; sai ngách nhưng tag match (MV「サイエンス」); police bodycam; interview; podcast; vlog; celebrity (idol scandal); news; kênh lớn view bình thường; kênh nhỏ breakout; title không tag nhưng semantic đúng; Disney/LA lọt lane D; tiếng Trung phồn thể; live-cam sân bay; reup highlight thể thao. Mỗi case có `expected: PASS/REJECT` + `expected_gate` (gate nào phải chặn). Test chạy pipeline với `LlmClient` giả trả response ghi sẵn trong fixture (`llm_stub`), nên **offline, 0 tiền**; thêm marker `@pytest.mark.live` để chạy thật khi muốn. | Fixture LLM stub không phản ánh model thật → bổ sung `--live` run tay 1 lần trước khi chốt threshold | `py -3.13 -X utf8 -m pytest E:\CLAUDE\YOUTUBE\TRENDING-RESEARCH\tests -q` xanh | — |

**Thứ tự làm P0:** 01 → 02 → 03 → 04 → 05 → 06 → 07 → 09 → 10 → 08 → 11 → 12 → 13 (viết test song song từng task theo TDD; 13 là tổng hợp).

---

## 5. P1 — DISCOVERY MỞ RỘNG + CLAUDE + SOL + CHUYỂN RANKING (guide Phase 3–5)

Điều kiện vào P1: P0 chạy shadow ≥ 5 lượt, có `HUMAN_DECISION` cho ≥ 20 dòng audit.
Điều kiện xong P1: `shadow_mode=false` được bật, Human Acceptance Rate Top 2 ≥ 80% trên ≥ 3 lượt liên tiếp.

| ID | Task | File | Current behavior | New behavior | Risk | Test | Rollback |
|---|---|---|---|---|---|---|---|
| P1-01 | Discovery 4 nguồn + window `today` | `src/hunt_v2/discovery.py` | Chỉ tag cột F + seed, window week/month | `discover(it, lane, sheet_tags, cfg, pool) -> found{video_id: row + discovery_sources[]}`: A tag (cũ), B `concept_queries`, C `format_queries`+`audience_queries`, D watch channels (Data API `playlistItems` 1 quota/kênh, lấy video ≤30 ngày). Thêm window `today` cho mọi query (bucket 0–3 ngày). Gắn `discovery_sources` để trace "vì sao được search" (§28). Tái dùng `discover_lane` + `ProxyPool`. | Số request InnerTube ×2–3 → bot-check nhiều hơn; giới hạn `max_queries_per_lane: 60` trong rules, ưu tiên core → concept → format | Test dedup nhiều nguồn cùng video → `discovery_sources` gộp; watch channel với API giả | `discovery_expansion: false` |
| P1-02 | Verify model & provider cho Claude/Sol | `config/models.yaml`, `src/hunt_v2/llm_client.py` | Chỉ ramcloud | Probe `GET https://ramclouds.me/v1/models` xem có route claude/gpt không; nếu không → provider `anthropic` (env `ANTHROPIC_API_KEY`, Messages API) và `openai` (env `OPENAI_API_KEY`). **Model ID chưa chốt** — `gpt-5.6-sol` trong guide phải verify tồn tại; ghi kết quả probe vào `docs/scratch/models_probe_<ngày>.md`. | Chi phí Claude/Sol trên shortlist 10–20 + 5–8/lane × 9 lane ≈ 250 call/ngày — cần user duyệt ngân sách | `--live` test 1 call mỗi provider | `fallback` về gemini trong `models.yaml` (chỉ để không crash; **không** coi PASS) |
| P1-03 | `opportunity_gate.py` (Claude) | `src/hunt_v2/opportunity_gate.py`, `prompts/opportunity_v1.txt` | Không có | Chạy trên `shortlist_n: 15`/lane (top viral_score có SEMANTIC+FORMAT PASS). Schema §15. Reject khi `celebrity_dependency ≥ 80 or external_event_dependency ≥ 80 or production_compatibility < 40` (rules). Cache + log như P0-03. | Model chấm chủ quan → chỉ dùng `opportunity_score` normalize vào ranking, decision REJECT chỉ theo fatal rules | Test client giả: fatal → REJECT; UNCERTAIN khi `viral_score ≥ 90` không tự reject (§25) | `opportunity_gate: false` |
| P1-04 | `final_qc.py` (Sol) | `src/hunt_v2/final_qc.py`, `prompts/finalqc_v1.txt` | Không có | Top `final_qc_n: 6`/lane. Prompt "tự đánh giá độc lập trước, rồi mới đọc assessment trước và chỉ ra bất đồng" (§16). Schema §16. `fatal_issue != null` → `final_qc_pass=false`. API lỗi → `FINAL_QC_STATUS=ERROR`. | Sol chậm/đắt → giới hạn 6/lane, timeout 120s | Test: fatal → fail; ERROR ≠ PASS; disagreements được lưu | `final_qc: false` (→ V2 tự động không production-select) |
| P1-05 | Ranking đủ 4 cờ + chuyển RESEARCH sang V2 | `src/hunt_v2/ranker.py`, `src/run_video_hunt.py` | RESEARCH = OLD | `require_flags` thêm `final_qc`. Khi `shadow_mode=false`: `all_picks[lane] = v2.selected` nếu ≥1, **fallback OLD pick cho lane V2 trống** + ghi `RUN_MODE=OLD_FALLBACK` vào audit (tránh ô trống). `hunt_v2_pick` chống chọn lại. `pick_per_lane` giữ 2. | Đổi nguồn pick là thay đổi output production duy nhất của cả kế hoạch → chỉ bật sau khi đạt 80% | Test: thiếu `final_qc_pass` → không selected; shadow=false + V2 rỗng → OLD fallback | `shadow_mode: true` (1 dòng yaml) |
| P1-06 | Metrics + shadow compare report | `src/hunt_v2/audit_writer.py`, `src/hunt_v2/run_store.py` | In log | `report.md` thêm: acceptance rate Top2 (đọc `HUMAN_DECISION`), wrong topic/format rate, false reject (OLD accepted mà V2 reject), unique channel, breakout detection, LLM calls/cost ước (token usage từ response `usage`). Bảng `video | old_selected | v2_selected | human` (§31). | — | Test tính metric từ fixture audit rows | — |

---

## 6. P2 — FEEDBACK LEARNING + DỌN (guide Phase 6)

| ID | Task | File | Current behavior | New behavior | Risk | Test | Rollback |
|---|---|---|---|---|---|---|---|
| P2-01 | `feedback.py` | `src/hunt_v2/feedback.py`, `store.human_feedback` | Không có | Đọc `TRD_HUNT_AUDIT` (chỉ đọc) cột `HUMAN_DECISION/REJECT_REASON`, upsert `human_feedback(video_id, lane, decision, reason, note, date)`. Khi lane có ≥ 20 quyết định mới kể từ lần cuối → sinh `lanes/<lane>/feedback_proposal_<ngày>.md` + JSON đề xuất cho `negative_examples/positive_examples/query_expansion` (**không** tự ghi đè 3 file đó, **không** đụng `lane_profile.yaml`). Lệnh riêng `py -3.13 -X utf8 src/hunt_v2/feedback.py --lane X --apply` để user áp sau khi đọc. | User gõ sai enum → bỏ qua dòng + log | Test parse enum; <20 quyết định → không sinh proposal; `--apply` chỉ ghi khi file proposal tồn tại | `feedback_learning: false` |
| P2-02 | Thumbnail vào format gate | `src/hunt_v2/semantic_format_gate.py` | Chỉ text | Gửi thumbnail URL (`https://i.ytimg.com/vi/<id>/hqdefault.jpg`) vào call vision cho candidate UNCERTAIN về `real_person_present` | Cost tăng; chỉ áp cho UNCERTAIN | Test: chỉ UNCERTAIN mới có image part | flag `format_gate_thumbnail: false` |
| P2-03 | Retire đường OLD | `src/run_video_hunt.py`, `src/reup_filter.py`, `src/hunt_score.py` | 2 đường song song | Sau ≥ 2 tuần `shadow_mode=false` ổn: OLD chỉ giữ discovery+enrich; bỏ `reup_filter.classify`, bỏ hard-reject `title_matches_pool`, bỏ `fresh_mult` 2×. Cập nhật `CLAUDE.md`, `README.md`. | Mất khả năng so sánh OLD/V2 → giữ `hunt_score.py` nguyên để chạy lại khi cần | pytest xanh; 1 lượt `--dry-run` | Khôi phục từ bản sao `docs/scratch/old_pipeline_backup/` |
| P2-04 | Bật lại lịch chạy | `deploy/install_task.ps1` | Task `YouTubeTrendHunter` đang tạm dừng | Chỉ khi user ra lệnh: `Enable-ScheduledTask -TaskName YouTubeTrendHunter` (không tự làm) | — | — | Disable lại |

---

## 7. RỦI RO CHUNG & CÁCH CHẶN

| Rủi ro | Mức | Chặn |
|---|---|---|
| Ghi nhầm/xoá dữ liệu Sheet của user | Cao | Không thêm tab ngoài whitelist; audit chỉ `append`; `guard_snapshot` trước/sau; test grep cấm `delete/clear` trong `hunt_v2/` |
| Model name trong guide (`gemini-flash-3.8`, `gpt-5.6-sol`, `claude`) không tồn tại trên ramclouds | Cao | P0 chỉ dùng model đã verify `gemini-3.5-flash-low`; P1-02 probe `/v1/models` trước khi viết prompt Claude/Sol |
| ramclouds 524 sau ~100s | Trung | batch 15, timeout 90s, retry đổi Idempotency; skill `proxy-llm-api-gotchas` |
| Quota Data API 10k/ngày vượt vì baseline | Trung | Baseline chỉ cho candidate đã qua H4/H5, trần 40 kênh/lane, cache 7 ngày trong `channel_baseline` |
| Chi phí LLM Claude/Sol | Trung | Shortlist 15 + 6/lane; cache theo video_id; báo cost ước trong `report.md`; **hỏi user duyệt ngân sách trước P1-03** |
| V2 crash làm hỏng lượt OLD | Trung | Bọc `try/except` toàn bộ V2 trong `main`; OLD ghi RESEARCH xong mới chạy V2 hoặc chạy V2 sau khi đã có `all_picks` OLD |
| Pool sau bỏ hard-reject tag quá lớn | Thấp | `max_semantic_candidates_per_lane: 200` sắp theo vpd |
| Chạy lại trong ngày làm trùng dòng audit | Thấp | Khoá `(RUN_ID, VIDEO_URL)` đọc trước khi append |
| Không có git → không rollback được code | Trung | Đề xuất `git init` + commit "baseline before V2" trước P0-01 (xem mục 8) |

---

## 8. VIỆC CẦN USER QUYẾT TRƯỚC KHI BẮT ĐẦU

1. **Duyệt kế hoạch này** (P0 trước, P1/P2 sau).
2. **Cho phép `git init`** tại `E:\CLAUDE\YOUTUBE\TRENDING-RESEARCH` (đang không phải repo; `.gitignore` đã có sẵn) để có rollback thật.
3. **Ngân sách LLM cho P1**: Claude + Sol ước ~250 call/ngày trên shortlist; P0 chỉ dùng gemini (ước ~100 call/ngày, rẻ).
4. **Xác nhận tên tab audit `TRD_HUNT_AUDIT`** (guide gợi ý `HUNT_AUDIT` nhưng không nằm trong whitelist; giữ prefix `TRD_` để không nới hàng rào).
5. **6 lane chưa có handoff** (E/F/G/H/I/J): profile soạn ở mức `draft: true` từ seed_tags + ô B1 tab — user sửa tay sau lượt shadow đầu.

---

## 9. LỆNH SẼ DÙNG (sau khi code P0)

```powershell
# test offline (0 tiền)
py -3.13 -X utf8 -m pytest E:\CLAUDE\YOUTUBE\TRENDING-RESEARCH\tests -q

# shadow dry-run 1 lane (không ghi Sheet, chỉ ghi runs/)
py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\TRENDING-RESEARCH\src\run_video_hunt.py --lane shinya_shiryoshitsu --dry-run

# chạy thật shadow: RESEARCH = OLD, TRD_HUNT_AUDIT = OLD + V2
py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\TRENDING-RESEARCH\src\run_video_hunt.py

# tắt hẳn V2 (hành vi y hệt hôm nay)
py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\TRENDING-RESEARCH\src\run_video_hunt.py --no-v2
```

Output kiểm tra: `E:\CLAUDE\YOUTUBE\TRENDING-RESEARCH\runs\<YYYY-MM-DD>\<lane>\{01_discovery,02_enriched,03_hard_filter,04_semantic,05_format,06_viral,09_ranked}.json` + `report.md`; log LLM `E:\CLAUDE\YOUTUBE\TRENDING-RESEARCH\logs\llm_<YYYYMMDD>.jsonl`.
