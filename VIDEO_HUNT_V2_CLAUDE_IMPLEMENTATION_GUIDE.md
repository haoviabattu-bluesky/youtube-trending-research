# VIDEO HUNT V2 — HƯỚNG DẪN TRIỂN KHAI CHO CLAUDE CODE

> Mục tiêu: xây dựng hệ thống tự động săn các video YouTube **mới đăng, đang viral/breakout, đúng chủ đề của từng lane**, để phục vụ nghiên cứu và học cấu trúc nội dung.
>
> Nguyên tắc cốt lõi:
>
> **Code làm việc tất định và số liệu. AI làm việc cần hiểu ngữ nghĩa. Không giao quyết định ngữ nghĩa cho string matching. Không giao tính toán/ranking cho AI nếu code làm được.**
>
> Phiên bản kiến trúc: VIDEO_HUNT_V2  
> Trạng thái: đề xuất triển khai mới, thay thế logic hunt cũ từng bước.

---

# 1. VẤN ĐỀ CỦA PIPELINE CŨ

Pipeline cũ hiện có:

1. Đọc tag lane từ Google Sheet.
2. Search YouTube bằng InnerTube.
3. Enrich số liệu bằng YouTube Data API.
4. Hard filter.
5. Match tiêu đề với >= 2 tag.
6. Một AI check loại channel/video.
7. Chấm view/ngày.
8. Ghi Top 2 vào Sheet.

Các lỗi chính:

- `title match >= 2 tag` không đại diện cho mức độ đúng chủ đề.
- Search dựa quá nhiều vào tag nên bỏ sót các video viral dùng cách diễn đạt khác.
- Video nhiều view nhưng viral nhờ celebrity/news/channel lớn vẫn có thể lọt.
- Chưa phân biệt:
  - video nhiều view tuyệt đối,
  - video breakout so với baseline của chính channel.
- Chưa có AI chuyên đánh giá:
  - đúng audience,
  - đúng format,
  - transferable/reusable,
  - tại sao video viral.
- Chưa có lớp QC độc lập trước khi ghi Sheet.
- Sheet chỉ chứa link nên mất toàn bộ lý do chọn.
- Human rejection chưa quay trở lại làm dữ liệu học cho lane.

VIDEO HUNT V2 phải sửa toàn bộ các điểm này.

---

# 2. KIẾN TRÚC TỔNG THỂ

```text
H0  LANE PROFILE
      |
      v
H1  DISCOVERY
      |
      v
H2  DATA ENRICH
      |
      v
H3  HARD FILTER
      |
      v
H4  GEMINI SEMANTIC GATE
      |
      v
H5  GEMINI FORMAT GATE
      |
      v
H6  VIRAL ENGINE
      |
      v
H7  CLAUDE OPPORTUNITY ANALYSIS
      |
      v
H8  SOL FINAL AUDIT
      |
      v
H9  DETERMINISTIC RANKING
      |
      v
H10 WRITE SHEET
      |
      v
H11 HUMAN FEEDBACK LEARNING
```

Không video nào được vào RANK 1 / RANK 2 nếu thiếu một trong các cờ:

```text
SEMANTIC_PASS
FORMAT_PASS
VIRAL_PASS
FINAL_QC_PASS
```

---

# 3. PHÂN CÔNG MODEL

## 3.1 Code / Python

Code phụ trách:

- đọc Google Sheet,
- search,
- YouTube API,
- dedup,
- hard filter,
- tính số liệu viral,
- percentile,
- breakout,
- freshness,
- ranking,
- ghi Sheet,
- cache,
- retry,
- logging,
- schema validation.

Code KHÔNG được tự quyết định video có “đúng ngách” bằng chuỗi từ khóa.

---

## 3.2 Gemini Flash 3.8

Vai trò:

- semantic screening số lượng lớn,
- audience fit,
- content fit,
- format detection,
- loại vlog/podcast/interview/talk show/news/TV clip/person-on-camera nếu lane không cho phép.

Gemini là **bulk semantic classifier**.

Không dùng Gemini để quyết định ranking cuối.

---

## 3.3 Claude

Vai trò:

- tạo/duy trì `LANE_PROFILE`,
- tạo concept expansion,
- phân tích candidate đã qua vòng viral:
  - WHY viral?
  - transferable không?
  - có đáng học không?
  - hook/topic/format nào có thể áp dụng?
- tổng hợp human feedback định kỳ thành negative/positive patterns.

Claude là **strategy/opportunity analyst**.

---

## 3.4 GPT-5.6 Sol

Vai trò:

- FINAL QC trên shortlist nhỏ,
- đánh giá độc lập,
- phát hiện fatal mismatch,
- đối chiếu kết luận Gemini/Claude,
- không chạy trên hàng trăm candidate.

Sol là **final independent auditor**.

---

## 3.5 DeepSeek V4 Flash

Không nên dùng làm final judge.

Có thể dùng cho:

- fallback extraction,
- code helper,
- batch normalization,
- format conversion,
- retry provider.

Không đưa DeepSeek vào critical gate nếu không cần.

---

# 4. CẤU TRÚC THƯ MỤC ĐỀ XUẤT

```text
video_hunt/
│
├─ config/
│  ├─ .env
│  ├─ models.yaml
│  └─ hunt_rules.yaml
│
├─ lanes/
│  ├─ satori_jp/
│  │  ├─ lane_profile.yaml
│  │  ├─ query_expansion.json
│  │  ├─ watch_channels.json
│  │  ├─ positive_examples.json
│  │  ├─ negative_examples.json
│  │  └─ blacklist.json
│  └─ ...
│
├─ src/
│  ├─ hunt_tags.py
│  ├─ discovery.py
│  ├─ innertube.py
│  ├─ ytapi.py
│  ├─ enrich.py
│  ├─ hard_filter.py
│  ├─ semantic_gate.py
│  ├─ format_gate.py
│  ├─ viral_engine.py
│  ├─ opportunity_gate.py
│  ├─ final_qc.py
│  ├─ ranker.py
│  ├─ sheet_writer.py
│  ├─ feedback.py
│  ├─ schemas.py
│  └─ llm_client.py
│
├─ runs/
│  └─ YYYY-MM-DD/
│     └─ <lane_id>/
│        ├─ 01_discovery.json
│        ├─ 02_enriched.json
│        ├─ 03_hard_filter.json
│        ├─ 04_semantic.json
│        ├─ 05_format.json
│        ├─ 06_viral.json
│        ├─ 07_opportunity.json
│        ├─ 08_final_qc.json
│        ├─ 09_ranked.json
│        └─ report.md
│
└─ logs/
```

Mỗi gate phải lưu output riêng.

Không overwrite dữ liệu gate trước.

---

# 5. H0 — LANE PROFILE

Mỗi lane phải có hồ sơ cố định.

Ví dụ:

```yaml
lane_id: satori_jp

market:
  country: Japan
  language: Japanese

audience:
  age_range: "60+"
  interests:
    - 老後
    - 人間関係
    - 家族
    - 孤独
    - 人生の教訓

content_identity:
  primary:
    - narrated_story
    - emotional_story
    - senior_story

wanted_topics:
  - 老後の人間関係
  - 親子関係
  - 友情
  - 孤独
  - 後悔
  - 介護
  - 老後のお金

allowed_formats:
  - narration
  - stock_story
  - ai_image_story
  - slideshow_story

excluded_formats:
  - vlog
  - podcast
  - interview
  - talk_show
  - news
  - tv_clip
  - livestream
  - reaction

excluded_subjects:
  - celebrity gossip
  - US police bodycam
  - gaming
  - politics

duration:
  min_minutes: 8
  max_minutes: 60
```

## Rule

`lane_profile.yaml` không được regenerate mỗi run.

Chỉ cập nhật khi:

- owner yêu cầu,
- feedback đủ lớn,
- Claude đề xuất thay đổi,
- sau đó vẫn phải review.

---

# 6. QUERY EXPANSION

Không chỉ search tag gốc.

Mỗi lane có:

```json
{
  "core_tags": [],
  "concept_queries": [],
  "format_queries": [],
  "audience_queries": [],
  "story_queries": []
}
```

Ví dụ:

```json
{
  "core_tags": [
    "老後",
    "シニア",
    "老後の人間関係"
  ],
  "concept_queries": [
    "友達",
    "親友",
    "絶縁",
    "孤独",
    "後悔",
    "70代 人生"
  ],
  "format_queries": [
    "朗読",
    "感動する話",
    "人生の教訓"
  ],
  "audience_queries": [
    "60代",
    "70代",
    "高齢者"
  ]
}
```

Claude tạo expansion ban đầu.

Sau đó lưu file.

---

# 7. H1 — DISCOVERY

Discovery phải có ít nhất 4 nguồn:

## A. Tag query

Từ Sheet + `core_tags`.

## B. Concept query

Từ `query_expansion.json`.

## C. Format query

Ví dụ:

```text
朗読
感動する話
シニア 人生
```

## D. Watch channel

Danh sách channel đã xác nhận cùng ngách:

```json
[
  {
    "channel_id": "...",
    "channel_name": "...",
    "confidence": 0.95
  }
]
```

Với watch channel:

- lấy video mới 1–30 ngày,
- không cần search keyword,
- merge vào discovery pool.

---

# 8. DISCOVERY TIME WINDOWS

Khuyên dùng:

```text
0–3 ngày
4–7 ngày
8–14 ngày
15–30 ngày
```

Không chỉ chia tuần/tháng.

Lý do:

- video breakout sớm cần được phát hiện riêng,
- freshness sẽ xử lý chính xác hơn.

---

# 9. H2 — DATA ENRICH

Mỗi candidate cần tối thiểu:

```json
{
  "video_id": "",
  "url": "",
  "title": "",
  "description": "",
  "channel_id": "",
  "channel_title": "",
  "published_at": "",
  "age_hours": 0,
  "age_days": 0,
  "duration_seconds": 0,
  "views": 0,
  "likes": 0,
  "comments": 0,
  "channel_subscribers": 0,
  "channel_video_count": 0,
  "tags": []
}
```

Ngoài ra phải lấy baseline channel:

```json
{
  "recent_video_views": [],
  "recent_video_age_hours": [],
  "recent_video_vph": [],
  "median_recent_views": 0,
  "median_recent_vph": 0
}
```

Ưu tiên 10 video gần nhất không tính Shorts nếu lane đang săn long-form.

---

# 10. H3 — HARD FILTER

Code-only.

Có thể loại:

```text
age > 30 days
views < configurable minimum
livestream
premiere chưa phát
video unavailable/private
duplicate
already_selected
channel blacklist
duration ngoài lane range
non-target-language rõ ràng
Shorts nếu lane không dùng Shorts
```

## QUAN TRỌNG

Rule này:

```text
"title phải match >= 2 tag"
```

KHÔNG được dùng làm hard reject.

Chỉ biến thành feature:

```text
keyword_match_score
```

Ví dụ:

```python
0.0 - 1.0
```

---

# 11. H4 — GEMINI SEMANTIC GATE

Input:

```text
LANE_PROFILE
title
description
channel_title
channel_description nếu có
tags
keyword_match_score
positive examples
negative examples
```

Prompt phải yêu cầu đánh giá độc lập theo nhiều trục.

Schema bắt buộc:

```json
{
  "topic_match": 0,
  "audience_match": 0,
  "content_identity_match": 0,
  "market_language_match": 0,
  "semantic_confidence": 0,
  "decision": "PASS|REJECT|UNCERTAIN",
  "reasons": [],
  "matched_topics": [],
  "mismatch_flags": []
}
```

Điểm 0–100.

Rule gợi ý:

```text
PASS:
topic_match >= 75
AND audience_match >= 65
AND content_identity_match >= 65

UNCERTAIN:
có score quan trọng trong vùng 55–74

REJECT:
topic_match < 55
OR content_identity_match < 50
```

Các threshold phải để trong config, không hard-code rải rác.

---

# 12. H5 — GEMINI FORMAT GATE

Có thể chạy chung call với H4 nếu muốn tiết kiệm.

Phân loại thành một trong:

```text
NARRATED_STORY
AI_STORY
STOCK_STORY
SLIDESHOW
DOCUMENTARY
NEWS
INTERVIEW
PODCAST
VLOG_PERSON
TALK_SHOW
TV_CLIP
REACTION
REUP
UNKNOWN
```

Output:

```json
{
  "format_class": "NARRATED_STORY",
  "real_person_present": false,
  "host_driven": false,
  "interview_style": false,
  "news_style": false,
  "format_confidence": 93,
  "decision": "PASS",
  "reason": ""
}
```

Nếu có thumbnail/frame analysis thì đưa vào cùng bước này.

Nếu lane cấm người thật:

```text
real_person_present = true
```

không phải lúc nào cũng reject ngay.

Ví dụ thumbnail có stock photo người thật vẫn có thể được.

Phải phân biệt:

```text
HOST / INTERVIEW PERSON
vs
ILLUSTRATIVE PHOTO
```

---

# 13. H6 — VIRAL ENGINE

Không AI.

Mục tiêu: phân biệt view lớn với viral thật.

## 13.1 Velocity

```python
vph = views / max(age_hours, 1)
vpd = views / max(age_days, 0.25)
```

---

## 13.2 Channel breakout

```python
breakout_ratio = current_vph / median_recent_vph
```

Nếu baseline VPH quá nhỏ phải có floor để tránh ratio vô hạn.

Ví dụ:

```python
baseline_vph = max(median_recent_vph, MIN_BASELINE_VPH)
```

---

## 13.3 Absolute traction

Không để video 2K view đứng top chỉ vì channel thường 50 view.

Dùng percentile hoặc log normalization.

Ví dụ feature:

```text
absolute_view_score
velocity_score
breakout_score
engagement_score
freshness_score
```

Mỗi score chuẩn hóa 0–100.

---

## 13.4 Engagement

Có thể dùng:

```python
like_rate = likes / views
comment_rate = comments / views
```

Không để engagement chiếm trọng số quá lớn.

---

## 13.5 Freshness

Khuyên dùng:

```text
0–3 ngày   => 1.35
4–7 ngày   => 1.25
8–14 ngày  => 1.15
15–30 ngày => 1.00
```

Không dùng boost 2x mặc định.

---

## 13.6 Viral score đề xuất

```text
viral_score =
0.30 * velocity_score
+ 0.30 * breakout_score
+ 0.20 * absolute_view_score
+ 0.10 * engagement_score
+ 0.10 * freshness_score
```

Có thể tinh chỉnh theo dữ liệu thực tế.

---

# 14. PHÂN LOẠI VIRAL TYPE

Mỗi video phải có:

```text
MARKET_TREND
CHANNEL_BREAKOUT
BOTH
NORMAL
```

Logic ví dụ:

```text
MARKET_TREND:
velocity percentile cao + absolute traction cao

CHANNEL_BREAKOUT:
breakout_ratio cao

BOTH:
cả hai đều cao
```

`BOTH` là nhóm ưu tiên nghiên cứu.

Không để rule cố định tuyệt đối ngay từ đầu.

Hãy để threshold trong config:

```yaml
viral:
  breakout_good: 2.0
  breakout_strong: 5.0
  breakout_extreme: 10.0
```

---

# 15. H7 — CLAUDE OPPORTUNITY ANALYSIS

Chỉ chạy trên shortlist sau viral engine.

Ví dụ 10–20 candidate/run.

Claude phải trả lời:

1. Video viral vì cái gì?
2. Viral có transferable không?
3. Topic có tái sử dụng được không?
4. Hook có học được không?
5. Audience có phù hợp lane không?
6. Format có phù hợp production pipeline không?
7. Viral có phụ thuộc:
   - celebrity,
   - breaking news,
   - external event,
   - channel authority,
   - interview guest,
   - controversy,
   - unique footage
   không?

Schema:

```json
{
  "why_viral": [
    "TITLE_HOOK",
    "TOPIC",
    "EMOTION"
  ],
  "transferability": 0,
  "topic_reusability": 0,
  "hook_reusability": 0,
  "audience_compatibility": 0,
  "production_compatibility": 0,
  "channel_authority_dependency": 0,
  "external_event_dependency": 0,
  "celebrity_dependency": 0,
  "opportunity_score": 0,
  "decision": "PASS|REJECT|UNCERTAIN",
  "fatal_flags": [],
  "reason": ""
}
```

Nếu:

```text
celebrity_dependency rất cao
external_event_dependency rất cao
production_compatibility thấp
```

thì candidate có thể bị reject dù viral_score cao.

---

# 16. H8 — GPT-5.6 SOL FINAL AUDIT

Chỉ chạy shortlist nhỏ.

Ví dụ:

```text
5–8 candidate
```

## Cách prompt

Không nói:

> Gemini/Claude đã PASS, hãy xác nhận.

Phải nói:

> Hãy tự đánh giá candidate này độc lập trước. Sau đó đọc assessment trước và chỉ ra điểm đồng ý/bất đồng.

Input:

```text
LANE_PROFILE
raw metadata
viral metrics
Gemini semantic result
Gemini format result
Claude opportunity result
```

Output:

```json
{
  "semantic_fit": 0,
  "format_fit": 0,
  "viral_validity": 0,
  "learning_value": 0,
  "independent_confidence": 0,
  "fatal_issue": null,
  "disagreements": [],
  "decision": "PASS|REJECT",
  "reason": ""
}
```

## Fatal issue examples

```text
WRONG_NICHE
WRONG_AUDIENCE
INTERVIEW_DEPENDENCY
CELEBRITY_DEPENDENCY
NEWS_DEPENDENCY
REAL_PERSON_FORMAT
TV_CLIP
REUP_RISK
NOT_REPLICABLE
MISLEADING_VIRAL_METRIC
```

Nếu `fatal_issue != null`:

```text
FINAL_QC_PASS = false
```

---

# 17. H9 — FINAL RANKING

Sau khi final QC PASS mới rank.

AI không tự quyết top 1/top 2.

Ví dụ:

```text
FINAL_SCORE =
0.40 * viral_score
+ 0.25 * semantic_score
+ 0.20 * opportunity_score
+ 0.10 * freshness_score
+ 0.05 * diversity_score
```

Tất cả sub-score normalize 0–100.

---

# 18. DIVERSITY RULE

Không để Top 2 quá giống nhau.

Có thể phạt nếu:

```text
same channel
same exact topic
same story angle
same source cluster
```

Ví dụ:

```python
if rank1.channel_id == candidate.channel_id:
    diversity_penalty += 25
```

Hoặc max:

```text
<= 1 video / channel / daily top results
```

---

# 19. H10 — GHI GOOGLE SHEET

Không chỉ ghi URL.

Nên có các cột:

```text
DATE
LANE
RANK
VIDEO_URL
TITLE
CHANNEL
PUBLISHED_AT
AGE_DAYS
VIEWS
VPD
VPH
BREAKOUT_RATIO
VIRAL_TYPE
VIRAL_SCORE
TOPIC_MATCH
FORMAT_CLASS
OPPORTUNITY_SCORE
FINAL_QC
WHY_VIRAL
WHY_USEFUL
CONFIDENCE
HUMAN_DECISION
REJECT_REASON
```

Nếu UI Sheet hiện tại chỉ muốn 2 link/ngày:

- vẫn giữ tab output cũ cho operation,
- tạo thêm tab:
  `HUNT_AUDIT`
  chứa full data.

Không làm mất audit trail.

---

# 20. H11 — HUMAN FEEDBACK LOOP

Thêm:

```text
HUMAN_DECISION:
ACCEPT
REJECT
SKIP
```

`REJECT_REASON` enum:

```text
WRONG_TOPIC
WRONG_AUDIENCE
WRONG_FORMAT
REAL_PERSON
INTERVIEW
NEWS
CELEBRITY
TOO_GENERIC
NOT_REPLICABLE
BAD_CHANNEL
LOW_VALUE
OTHER
```

Mỗi rejection lưu:

```json
{
  "video_id": "",
  "title": "",
  "reason": "WRONG_FORMAT",
  "note": "",
  "date": ""
}
```

---

# 21. FEEDBACK LEARNING

Sau mỗi:

```text
20–50 human decisions
```

Claude đọc:

```text
accepted examples
rejected examples
reason distribution
```

Sau đó tạo proposal cập nhật:

```text
negative_examples.json
positive_examples.json
query_expansion.json
```

Không tự sửa `lane_profile.yaml` nếu chưa có review.

---

# 22. POSITIVE / NEGATIVE EXAMPLES

Ví dụ:

```json
{
  "negative_patterns": [
    {
      "pattern": "US police interview/bodycam",
      "reason": "not narrated senior story",
      "count": 7
    },
    {
      "pattern": "two-person studio podcast",
      "reason": "wrong production format",
      "count": 4
    }
  ]
}
```

Gemini và Claude phải được cấp các examples này ở các gate sau.

---

# 23. MODEL CONFIG

Ví dụ:

```yaml
models:
  semantic_gate:
    provider: ramcloud
    model: gemini-flash-3.8

  format_gate:
    provider: ramcloud
    model: gemini-flash-3.8

  opportunity_gate:
    provider: anthropic
    model: claude

  final_qc:
    provider: openai
    model: gpt-5.6-sol

  fallback:
    provider: ramcloud
    model: deepseek-v4-flash
```

Không hard-code model string ở nhiều file.

---

# 24. LLM CLIENT REQUIREMENTS

`llm_client.py` phải hỗ trợ:

```text
provider routing
timeout
retry
schema validation
JSON repair
logging
token usage
latency
fallback
```

Mỗi response phải lưu:

```json
{
  "model": "",
  "provider": "",
  "latency_ms": 0,
  "attempt": 1,
  "raw_response": "",
  "parsed_response": {}
}
```

Không silently swallow lỗi parsing.

---

# 25. FAIL / UNCERTAIN POLICY

Không ép AI trả PASS/REJECT khi không đủ dữ liệu.

Ba trạng thái:

```text
PASS
REJECT
UNCERTAIN
```

## UNCERTAIN

Có thể:

- retry 1 lần,
- gọi model cấp cao hơn,
- giữ candidate để Sol check,
- không tự động reject nếu video có viral_score cực cao.

---

# 26. CACHE POLICY

Không gọi lại LLM nếu:

```text
video_id giống
lane_profile fingerprint giống
prompt version giống
model version giống
```

Cache key:

```text
sha256(
video_id
+ lane_profile_hash
+ gate_name
+ prompt_version
+ model_name
)
```

---

# 27. VERSION PROMPT

Mỗi gate phải có prompt version:

```text
semantic_v1
format_v1
opportunity_v1
finalqc_v1
```

Nếu prompt thay đổi:

- cache cũ không được dùng sai version.

---

# 28. LOGGING / AUDIT

Mỗi candidate phải trace được:

```text
vì sao được search
vì sao pass hard filter
Gemini nói gì
viral metrics bao nhiêu
Claude nói gì
Sol nói gì
vì sao rank
human cuối cùng accept/reject
```

Không có black box.

---

# 29. REPORT MỖI RUN

Tạo:

```text
runs/YYYY-MM-DD/<lane>/report.md
```

Nội dung:

```text
Discovery: 420
Hard pass: 180
Semantic pass: 62
Format pass: 44
Viral shortlist: 14
Opportunity pass: 8
Sol pass: 5
Final selected: 2
```

Kèm:

```text
Top rejection reasons
Model errors
API errors
Outliers
Top candidate explanations
```

---

# 30. THỨ TỰ TRIỂN KHAI

Không rewrite toàn bộ một lần.

## Phase 1 — Data foundation

Làm trước:

```text
lane_profile
query_expansion
watch_channels
baseline channel stats
viral_engine
```

Chưa đổi output production.

---

## Phase 2 — Gemini gates

Thêm:

```text
semantic_gate
format_gate
schema
cache
logs
```

Chạy shadow mode.

So output cũ vs mới.

---

## Phase 3 — Claude opportunity

Chỉ chạy trên shortlist.

Đánh giá chất lượng.

---

## Phase 4 — Sol final QC

Thêm final auditor.

---

## Phase 5 — Replace ranking

Chuyển từ ranking cũ sang V2.

---

## Phase 6 — Feedback learning

Thêm human reject/accept loop.

---

# 31. SHADOW MODE BẮT BUỘC

Trong ít nhất vài run đầu:

```text
OLD_RANK
V2_RANK
```

chạy song song.

Không xóa pipeline cũ ngay.

Tạo bảng so sánh:

```text
video
old_selected?
v2_selected?
human verdict
```

Mục tiêu:

- đo false positive,
- đo false negative,
- tinh chỉnh threshold.

---

# 32. METRIC ĐỂ ĐÁNH GIÁ PIPELINE

Không đánh giá bằng “cảm giác”.

Theo dõi:

```text
Human Acceptance Rate
Wrong Topic Rate
Wrong Format Rate
False Reject Rate
Unique Channel Count
Breakout Detection Rate
LLM Cost / Run
LLM Calls / Run
Average Candidates / Gate
```

Quan trọng nhất:

```text
Human Acceptance Rate of Top 2
```

Ví dụ:

```text
Top 2 được owner accept >= 80%
```

mới coi pipeline ổn.

---

# 33. FAIL-SAFE

Nếu Sol lỗi/API lỗi:

Không tự động coi PASS.

Ví dụ:

```text
FINAL_QC_STATUS = ERROR
```

candidate không được production-select.

Có thể fallback model nếu config cho phép.

---

# 34. KHÔNG ĐƯỢC LÀM

Claude khi triển khai KHÔNG được:

1. Thay semantic gate bằng keyword count.
2. Cho AI tự tính view/day nếu code đã có.
3. Cho Sol xử lý hàng trăm video.
4. Dùng một model duy nhất cho mọi gate.
5. Không lưu raw decision.
6. Không validate JSON.
7. Ghi Top 2 nếu thiếu final QC.
8. Regenerate lane profile mỗi ngày.
9. Đưa score AI chưa normalize thẳng vào ranking.
10. Xóa pipeline cũ trước khi shadow test.

---

# 35. NGUYÊN TẮC CHÍNH

## RULE 1

```text
SEARCH RỘNG — FILTER THÔNG MINH
```

Không search quá hẹp bằng tag.

---

## RULE 2

```text
MACHINE FOR NUMBERS
AI FOR MEANING
```

---

## RULE 3

```text
HIGH VIEW != VIRAL
```

Phải so với baseline channel.

---

## RULE 4

```text
VIRAL != USEFUL
```

Phải có opportunity gate.

---

## RULE 5

```text
AI PASS != FINAL PASS
```

Phải có independent final QC.

---

## RULE 6

```text
HUMAN REJECTION IS TRAINING DATA
```

Không bỏ feedback.

---

# 36. OUTPUT CONTRACT CUỐI

Một video được selected phải có record tối thiểu:

```json
{
  "video_id": "",
  "url": "",
  "lane_id": "",
  "semantic_pass": true,
  "format_pass": true,
  "viral_pass": true,
  "final_qc_pass": true,

  "viral_type": "BOTH",
  "viral_score": 91.4,
  "breakout_ratio": 7.2,

  "topic_match": 93,
  "format_class": "NARRATED_STORY",

  "opportunity_score": 90,
  "learning_value": 94,

  "why_viral": [
    "strong emotional contradiction",
    "high curiosity title",
    "topic resonance"
  ],

  "why_useful": "Transferable premise and narration format match lane.",

  "final_score": 92.1
}
```

Nếu thiếu các field critical:

```text
DO NOT SELECT
```

---

# 37. VIỆC CLAUDE CẦN LÀM SAU KHI ĐỌC FILE NÀY

Claude Code phải:

1. Đọc codebase Video Hunt hiện tại.
2. Không sửa code ngay.
3. Vẽ mapping:
   - module cũ,
   - module giữ,
   - module sửa,
   - module mới.
4. Xác định data flow hiện tại.
5. Xác định Sheet input/output hiện tại.
6. Xác định cách `LLM_MODEL` / ramcloud đang gọi.
7. Viết `IMPLEMENTATION_PLAN.md`.
8. Chia implementation thành P0/P1/P2.
9. Ưu tiên backward-compatible.
10. Bắt đầu bằng shadow mode.

---

# 38. YÊU CẦU IMPLEMENTATION_PLAN.md

Claude phải tạo bảng:

```text
Task
File
Current behavior
New behavior
Risk
Test
Rollback
```

Ví dụ:

```text
P0-01
src/hard_filter.py
reject title <2 tag
remove hard rejection, save keyword feature
risk: larger pool
test: old dataset comparison
rollback: feature flag
```

---

# 39. FEATURE FLAGS

Khuyên dùng:

```yaml
video_hunt_v2:
  enabled: true

  semantic_gate: true
  format_gate: true
  viral_engine_v2: true
  opportunity_gate: true
  final_qc: true

  shadow_mode: true
```

Có thể rollback từng gate.

---

# 40. TEST DATASET

Trước production phải tạo:

```text
tests/fixtures/video_hunt_cases.json
```

Ít nhất gồm:

- video đúng ngách / view cao,
- đúng ngách / breakout,
- sai ngách nhưng tag match,
- police bodycam,
- interview,
- podcast,
- vlog,
- celebrity,
- news,
- channel lớn view bình thường,
- channel nhỏ breakout mạnh,
- title không có tag nhưng semantic rất đúng.

Expected result:

```text
PASS / REJECT
```

---

# 41. REGRESSION CASE QUAN TRỌNG

Bắt buộc lưu các lỗi owner đã bắt được.

Ví dụ:

```text
case: US police guest / talk show
expected: REJECT
reason:
- wrong format
- wrong content identity
```

Đây phải trở thành test vĩnh viễn.

Không sửa pipeline xong rồi để lỗi cũ quay lại.

---

# 42. MỤC TIÊU CUỐI

Hệ thống không nhằm tìm:

> video có view lớn nhất.

Hệ thống phải tìm:

> video mới đang có tín hiệu tăng trưởng bất thường, đúng audience, đúng ngách, đúng format, và có insight đủ transferable để học và áp dụng cho lane.

Đây là tiêu chí cao nhất của VIDEO HUNT V2.

---

# END
