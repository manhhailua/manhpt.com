---
title: "Benchmark No Streaming + No Thinking: JSON vs QP-Lines (Gemini + Qwen)"
authors: [manhpt]
tags: [benchmark, gemini, qwen, vietnamese, cache, llm, cost-optimization]
date: 2026-03-15
description: "Benchmark no streaming + no thinking + explicit cache cho Gemini và Qwen, so sánh JSON array vs QP-Lines structured output để tối ưu TTLT cho query breaking trong RAG pipeline."
---

**Bài benchmark trước dùng JSON array cho structured output nhưng chưa đo tác động của format lên TTLT.** Bài này tách riêng một điều kiện chuẩn hóa — **no streaming + no thinking + explicit cache** — rồi so sánh **JSON array vs QP-Lines** trên cả **Gemini** và **Qwen** để trả lời câu hỏi: format nào nhanh hơn và ổn định hơn cho pipeline query breaking?

Tham chiếu bài trước: [Implicit Cache vs Explicit Cache: Qwen3.5-Flash và Gemini-3.1-Flash-Lite-Preview — Đo Thực Tế TTLT](/2026/03/13/benchmark-cache-qwen35-vs-gemini31).

<!-- truncate -->

## Vấn đề với JSON structured output

Bài benchmark cũ xác nhận **TTLT là metric đúng** cho pipeline query breaking — pipeline phải nhận đủ output trước khi có thể `json.loads()` và fan-out sang vector search. Tuy nhiên JSON array có overhead token cú pháp không tạo giá trị ngữ nghĩa:

```text
["sub-query 1", "sub-query 2", "sub-query 3"]
 ^             ^^             ^^             ^
 bracket    comma+space   comma+space    bracket
```

Với 4–5 sub-query, mỗi lần gọi API mang thêm khoảng 8–12 token cú pháp thuần túy. Ở scale lớn (hàng nghìn request/ngày), đây là decode time có thể loại bỏ.

## Structured output thay thế: QP-Lines

Format QP-Lines (Query Protocol Lines) — tối giản, parse tuyến tính:

```text
COUNT:4
Q:Ngân hàng nào cho vay mua xe uy tín?
Q:Ngân hàng nào có lãi suất vay mua nhà tốt?
Q:Thủ tục vay mua xe cần giấy tờ gì?
Q:Hồ sơ vay mua nhà cần chuẩn bị gì?
```

Quy ước:
- Dòng đầu `COUNT:<n>` — khai báo số sub-query.
- Mỗi dòng sau `Q:<text>` — một sub-query độc lập.
- Parse thành công khi số dòng `Q:` bằng `COUNT`.

Trade-off cần nhận thức rõ:
- JSON là chuẩn phổ thông, mọi SDK và framework hỗ trợ mặc định.
- QP-Lines cần validator riêng; parse fail khi COUNT không khớp số Q: thực tế.

## Thiết kế benchmark

### Điều kiện chuẩn hóa

| Tham số | Giá trị |
|---|---|
| `stream` | `False` |
| Thinking | Tắt (`enable_thinking: False` cho Qwen, `thinking_budget=0` cho Gemini) |
| Warm-up | **2 lượt bắt buộc** — không tính vào số liệu |
| Queries | 5 câu hỏi tài chính tiếng Việt |
| `max_tokens` | 300 |
| Sleep giữa queries | 2 giây |

### Cache mode — explicit cho cả hai provider

Benchmark này dùng **explicit cache** cho cả Gemini lẫn Qwen, nhưng cơ chế hoàn toàn khác nhau:

| Provider | Cơ chế | Xác nhận cache hit |
|---|---|---|
| **Gemini** | `CachedContent.create()` — object cache tách biệt | `cached_content_token_count > 0` ✓ |
| **Qwen** | `cache_control: {type: "ephemeral"}` marker inline trong system message | `usage.prompt_tokens_details.cached_tokens > 0` ✓ |

**Qwen explicit cache hoạt động theo flow sau:**

```
Warmup run 1:  gửi system message với cache_control marker
               → DashScope tạo cache block
               → response: cache_creation_input_tokens = ~1136, cached_tokens = 0
Warmup run 2:  gửi cùng prefix
               → cache hit confirmed
               → response: cache_creation_input_tokens = 0, cached_tokens = ~1136
Measured runs: tất cả là cache hit (cached_tokens = ~1136)
```

> **Lưu ý model ID quan trọng:** DashScope explicit cache chỉ hỗ trợ model aliases (`qwen3.5-flash`, `qwen-flash`) — **không hỗ trợ** pinned date versions như `qwen3.5-flash-2026-02-23`. Nếu dùng pinned version, `prompt_tokens_details` chỉ trả về `{text_tokens: N}` và cache không được tạo.

> DashScope explicit cache yêu cầu tối thiểu 1.024 token. Prompt trong benchmark (~1.100-1.200 token system message sau khi tối ưu) vượt ngưỡng này.

### Vai trò của warm-up

Warm-up **không thay thế** explicit cache — warm-up chỉ đảm bảo cache đã được load trước khi đo:

- Lần 1: Tạo cache block (cache creation).
- Lần 2: Xác nhận cache hit — đặc biệt quan trọng với Gemini vì `cached_content_token_count` phải > 0.
- Measured runs: Tất cả đo trên trạng thái cache đã warm.

### Scenarios đo chính

1. `gemini | Explicit + No Streaming + No Thinking + JSON`
2. `gemini | Explicit + No Streaming + No Thinking + QP-Lines`
3. `qwen | Explicit + No Streaming + No Thinking + JSON`
4. `qwen | Explicit + No Streaming + No Thinking + QP-Lines`

## Kết quả thực tế

> Số liệu đo từ API thực — 5 queries × 4 scenarios, sau 2 lượt warmup mỗi scenario.

### Gemini — Explicit Cache (`CachedContent API`)

| Scenario | **TTLT mean** | TTLT min | TTLT max | Avg out tokens | Cached tokens | Parse OK |
|---|---|---|---|---|---|---|
| JSON | **2.099ms** | 1.414ms | 3.578ms | 98 | **1.136** ✓ | 5/5 (100%) |
| QP-Lines | **1.522ms** | 1.256ms | 1.858ms | 70 | **1.179** ✓ | 5/5 (100%) |

**Nhận xét Gemini:**
- QP-Lines nhanh hơn **577ms (~27.5%)** — cải thiện lớn hơn dự kiến.
- Output token giảm **28 token (~29%)**: `[ ] , "` bị loại bỏ.
- `cached_content_token_count = 1.136-1.179` ở **mọi query** → cache hit 100% xác nhận được.
- Cả hai format parse 100%.

### Qwen — Explicit Cache (`cache_control` marker, model `qwen3.5-flash`)

| Scenario | **TTLT mean** | TTLT min | TTLT max | Avg out tokens | Cached tokens | Parse OK |
|---|---|---|---|---|---|---|
| JSON | **1.312ms** | 989ms | 1.735ms | 84 | **1.090** ✓ | 5/5 (100%) |
| QP-Lines | **1.093ms** | 902ms | 1.223ms | **57** | **1.131** ✓ | 4/5 (80%) |

**Nhận xét Qwen:**
- QP-Lines nhanh hơn **219ms (~16.7%)** — cải thiện đáng kể.
- Output token giảm **27 token (~32%)** — nhiều hơn dự kiến.
- `cached_tokens = 1.090-1.131` ở tất cả responses → cache hit **100% xác nhận được** qua API.
- QP-Lines có **1/5 parse fail** (COUNT mismatch) — cần retry logic trong production.

### So sánh tổng hợp

| Provider | Format | TTLT mean | TTLT min | Out tokens | Cached tokens | Parse rate |
|---|---|---|---|---|---|---|
| Gemini | JSON | 2.099ms | 1.414ms | 98 | 1.136 ✓ | 100% |
| Gemini | **QP-Lines** | **1.522ms** | 1.256ms | **70** | 1.179 ✓ | **100%** |
| Qwen | JSON | 1.312ms | 989ms | 84 | 1.090 ✓ | **100%** |
| Qwen | **QP-Lines** | **1.093ms** | 902ms | **57** | 1.131 ✓ | 80% |

## Phân tích

### QP-Lines giảm output token — TTLT giảm theo với mức cải thiện đáng kể

Với cùng prompt và cùng câu hỏi, QP-Lines sinh ít token hơn JSON vì không cần `[`, `]`, `"`, `,` cho mỗi phần tử. Kết quả thực tế cho thấy mức cải thiện lớn hơn dự kiến:

- **Gemini**: giảm 28 token (~29%) → TTLT giảm 577ms (~27.5%) → decode speed ≈ 20.6ms/token.
- **Qwen**: giảm 27 token (~32%) → TTLT giảm 219ms (~16.7%) → decode speed ≈ 8.1ms/token.

Qwen vẫn nhanh hơn Gemini ~30-40% ở cả hai format — phù hợp với xu hướng từ bài cũ: bottleneck là **generation speed của từng model**, không phải prefill hay cache.

### QP-Lines parse failure vẫn là rủi ro thực tế

Qwen QP-Lines có **1/5 parse fail** (query 1 — model trả `COUNT:3` nhưng sinh ra số dòng `Q:` không khớp). Đây là variance model, không phải lỗi deterministic. Nếu triển khai QP-Lines, cần có retry policy (gọi lại với JSON fallback khi parse fail).

### Explicit cache Qwen: chỉ hoạt động với model alias, không phải pinned version

Phát hiện quan trọng trong lần chạy này: `cache_control` marker **không được nhận diện** khi dùng model `qwen3.5-flash-2026-02-23` (pinned). DashScope chỉ hỗ trợ explicit cache với model aliases như `qwen3.5-flash`. Khi dùng đúng alias, cache hoạt động hoàn toàn: warmup run 1 tạo ~1.100-1.200 tokens cache, warmup run 2 confirm hit, tất cả measured runs có `cached_tokens = ~1.100-1.200`.

## Recommendation cho production

| Ưu tiên | Model | Format | Lý do |
|---|---|---|---|
| TTLT thấp nhất | Qwen | **QP-Lines** | 1.093ms mean, cached xác nhận, nhưng cần retry khi parse fail |
| TTLT thấp + an toàn parse | Qwen | **JSON** | 1.312ms, cache hit xác nhận, parse 100% đảm bảo |
| Gemini + muốn tối ưu | Gemini | **QP-Lines** | -577ms (~27.5%), parse 100%, cache hit xác nhận được |
| Gemini + simplicity | Gemini | JSON | Cache hit xác nhận, tooling mặc định |

**Kết luận:** QP-Lines giảm output token đáng kể (~29-32%) và TTLT giảm theo (~17-28%). Lợi ích rõ rệt hơn so với ước tính ban đầu. QP-Lines với retry logic là lựa chọn tối ưu cho production nếu chấp nhận ~20% parse failure rate. Qwen JSON vẫn là lựa chọn an toàn nhất: cache xác nhận, TTLT thấp, parse 100%.

## Setup và tái lập

```bash
cd blog/2026-03-15-benchmark-explicit-no-streaming-no-thinking-structured-output

# Virtualenv mới bằng uv
uv venv .venv && source .venv/bin/activate
uv pip install google-genai python-dotenv requests

# Copy .env từ benchmark cũ hoặc tạo từ mẫu
cp ../2026-03-13-benchmark-cache-qwen35-vs-gemini31/.env .env
# hoặc: cp .env.example .env  rồi điền key

python benchmark_explicit_structured_output.py
```

`.env` cần:

```dotenv
GEMINI_API_KEY=...
DASHSCOPE_API_KEY=...
```

## Cập nhật Token Optimization & Kết Quả Thực Tế

Sau khi public bài viết, chúng tôi đã tối ưu system prompt để giảm token count từ ~3.050 xuống ~1.100-1.200 tokens, vẫn đảm bảo trên ngưỡng tối thiểu 1.024 tokens của DashScope explicit cache. Các thay đổi bao gồm:

1. **Tối ưu PADDING content**: Giữ nguyên thông tin domain tài chính nhưng trình bày cô đọng hơn
2. **Loại bỏ repetition**: Thay vì lặp PADDING 12 lần, chỉ dùng 1 lần với nội dung đầy đủ
3. **Thêm extra padding**: Đảm bảo >1024 tokens cho Gemini API
4. **Chạy benchmark thực tế**: Cập nhật số liệu với kết quả đo mới

**Kết quả thực tế cho thấy:**
- Token count: 1.090-1.179 tokens (đạt yêu cầu >1024)
- TTLT cải thiện rõ rệt: QP-Lines nhanh hơn 17-28%
- Output token giảm 29-32% (nhiều hơn dự kiến)
- Cache hit 100% xác nhận được cho cả Gemini và Qwen

Điều này chứng tỏ explicit cache hoạt động hiệu quả với prompt optimized, và QP-Lines mang lại lợi ích thực tế lớn hơn so với ước tính ban đầu.

## Tài nguyên

- [Bài benchmark cũ — Implicit vs Explicit Cache: TTLT thực tế](/2026/03/13/benchmark-cache-qwen35-vs-gemini31)
- [DashScope Context Cache — Explicit Cache với cache_control marker](https://www.alibabacloud.com/help/en/model-studio/context-cache)
- [Gemini API Context Caching](https://ai.google.dev/gemini-api/docs/caching)
- [Gemini API Thinking](https://ai.google.dev/gemini-api/docs/thinking)
- [Script benchmark](https://github.com/manhhailua/manhpt.com/blob/master/blog/2026-03-15-benchmark-explicit-no-streaming-no-thinking-structured-output/benchmark_explicit_structured_output.py) | [Kết quả raw](https://github.com/manhhailua/manhpt.com/blob/master/blog/2026-03-15-benchmark-explicit-no-streaming-no-thinking-structured-output/benchmark_results.json)
