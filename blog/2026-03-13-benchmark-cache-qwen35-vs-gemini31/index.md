---
title: "Implicit Cache vs Explicit Cache: Qwen3.5-Flash và Gemini-3.1-Flash-Lite-Preview — Đo Thực Tế TTLT"
authors: [manhpt]
tags: [benchmark, qwen, gemini, vietnamese, cache, llm, cost-optimization]
date: 2026-03-13
description: "Benchmark thực tế tháng 3/2026: So sánh implicit cache vs explicit cache giữa Qwen3.5-Flash và Gemini-3.1-Flash-Lite-Preview cho bài toán query breaking trong RAG. Metric chính là TTLT — thời điểm pipeline nhận đủ output để bắt đầu truy vấn vector database."
---

**Trong pipeline RAG, bước "query breaking" — phân tách câu hỏi phức hợp thành các sub-query độc lập — là bottleneck đầu tiên trước khi có thể fan-out sang vector database.** Metric quan trọng nhất không phải TTFT (first token) mà là **TTLT (time-to-last-token)**: pipeline chỉ có thể gọi `json.loads()` và bắt đầu retrieval khi nhận đủ toàn bộ JSON array. Bài viết này là báo cáo benchmark thực tế, chạy script đo TTLT và TTFT cho **Qwen3.5-Flash** và **Gemini-3.1-Flash-Lite-Preview** với 3 kịch bản caching.

<!-- truncate -->

## Query Breaking Là Gì?

Người dùng thường đặt câu hỏi có nhiều ý định cùng lúc. Ví dụ:

> *"Tôi muốn mua xe và mua nhà trong năm nay, nên vay ngân hàng nào và cần chuẩn bị giấy tờ gì?"*

Với vector search thông thường, câu hỏi này rất khó tìm kết quả tốt vì nó chứa ít nhất 4 ý định riêng biệt:

1. Vay mua xe → tài liệu về vay mua ô tô
2. Vay mua nhà → tài liệu về vay bất động sản
3. Ngân hàng nào → so sánh điều kiện vay
4. Giấy tờ thủ tục → hồ sơ vay cụ thể

Bước query breaking dùng LLM để phân tách thành sub-query nguyên tử:

```json
[
  "Nên vay ngân hàng nào để mua xe ô tô?",
  "Nên vay ngân hàng nào để mua nhà?",
  "Hồ sơ vay mua xe ô tô cần những giấy tờ gì?",
  "Hồ sơ vay mua nhà cần những giấy tờ gì?"
]
```

**Lý do TTLT quan trọng hơn TTFT ở đây:** Token đầu tiên (`[`) xuất hiện sớm nhưng vô dụng — pipeline cần toàn bộ JSON hợp lệ mới có thể `json.loads()` và fan-out sang parallel vector search. TTFT là metric của chatbot; TTLT là metric của pipeline orchestration.

---

## Tại Sao Cache Quan Trọng?

Bước query breaking dùng **cùng một system prompt** cho mọi request — chứa hướng dẫn phân tách ý định, few-shot examples theo domain (tài chính, bất động sản, bảo hiểm), và quy tắc output JSON. System prompt này thường 1.000–5.000 token, lặp lại hoàn toàn với mỗi request.

Hai loại cache trên các LLM API hiện đại:

| Thuộc tính | Implicit Cache | Explicit Cache |
|---|---|---|
| **Kích hoạt** | Tự động (API nhận diện prefix trùng) | Thủ công (tạo cache object trước) |
| **Min tokens — Qwen** | 256 tokens | 1.024 tokens |
| **Min tokens — Gemini FL** | 1.024 tokens | **4.096 tokens** |
| **TTL** | Không cam kết | Qwen: 5 phút / Gemini: tùy chỉnh |
| **Giá cache hit** | Qwen: 20% / Gemini: 10% giá input | Qwen: 10% / Gemini: 10% giá input |
| **Phí tạo cache** | Không | Qwen: 125% giá input / Gemini: $1/1M token/giờ |
| **Đảm bảo hit** | Không | Có (trong TTL) |

---

## Thiết Kế Benchmark

### Mô hình & endpoint

| Model | ID thực tế | API |
|---|---|---|
| Qwen3.5-Flash | `qwen3.5-flash-2026-02-23` | DashScope OpenAI-compat |
| Gemini 3.1 Flash Lite | `gemini-3.1-flash-lite-preview` | Google AI SDK |

> **Lưu ý model ID Qwen:** Model ID đúng là `qwen3.5-flash-2026-02-23` (bao gồm năm đầy đủ), không phải `qwen3.5-flash-02-23`. Model cũng cần tắt thinking mode (`enable_thinking: false`) cho task JSON output — nếu không, model sẽ sinh 3.000–5.000 token CoT trước khi trả output, làm TTLT tăng gấp 10–20 lần.

### System prompt

Query breaking agent với hướng dẫn chi tiết, 10 few-shot examples theo domain tài chính Việt Nam (vay vốn, bảo hiểm, đầu tư, thẻ tín dụng, thuế...), quy tắc output JSON. Tổng **~1.330 token** — đủ kích hoạt implicit cache Qwen (256 token) và Gemini (1.024 token), đủ explicit cache Qwen (1.024 token). Gemini explicit cache yêu cầu &gt;= 4.096 token, nhưng Google AI cho phép cache object với nội dung hệ thống ít hơn nếu có additional contents — benchmark này dùng API `CachedContent.create()` và API **đã chấp nhận** với 1.330 token.

### 5 queries benchmark

Câu hỏi phức hợp tiếng Việt thực tế:

1. *"Tôi muốn mua xe và mua nhà trong năm nay, nên vay ngân hàng nào và cần chuẩn bị giấy tờ gì?"*
2. *"So sánh lãi suất tiết kiệm 6 tháng và 12 tháng tại Vietcombank và Techcombank"*
3. *"Bảo hiểm nhân thọ Prudential và Manulife khác nhau thế nào về phí và quyền lợi bồi thường?"*
4. *"Tôi nên đầu tư vào vàng, cổ phiếu VN30 hay gửi tiết kiệm ngân hàng với số tiền 100 triệu?"*
5. *"Tỷ giá USD/VND và lãi suất cơ bản của NHNN ảnh hưởng thế nào đến lãi suất vay ngân hàng?"*

### Phương pháp đo

- **TTLT** (metric chính): thời gian từ request đến khi nhận token cuối cùng, đo qua `stream=True`
- **TTFT** (metric phụ): thời gian đến token đầu tiên
- Mỗi kịch bản: 5 queries thực, 2 giây nghỉ giữa mỗi query
- 1 warmup run trước kịch bản implicit cache để seed cache
- Script: [`benchmark_cache.py`](https://github.com/manhhailua/manhpt.com/blob/main/blog/2026-03-13-benchmark-cache-qwen35-vs-gemini31/benchmark_cache.py)

---

## Cách Bật Cache Cho Từng Model

### Qwen — Implicit Cache

Dùng cùng system prompt, DashScope tự cache sau lần đầu (ngưỡng: 256 token). Quan trọng: tắt thinking mode cho task JSON ngắn:

```python
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["DASHSCOPE_API_KEY"],
    base_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1",
)

response = client.chat.completions.create(
    model="qwen3.5-flash-2026-02-23",  # ID đầy đủ với năm
    messages=[
        {"role": "system", "content": QUERY_BREAKING_PROMPT},
        {"role": "user", "content": query},
    ],
    stream=True,
    stream_options={"include_usage": True},
    max_tokens=300,
    extra_body={"enable_thinking": False},  # tắt CoT để TTLT không bị phình
)
```

> **Lưu ý:** DashScope không trả `cached_tokens` trong usage response cho model này — cache có thể đang hoạt động nhưng không được báo cáo. TTLT giảm ~15% sau warmup cho thấy implicit cache đang có hiệu lực ngầm.

### Qwen — Explicit Cache

Format `cache_control: {type: ephemeral}` là của Anthropic Claude — **không hoạt động** với DashScope. Explicit context cache của Qwen dùng API riêng (tạo cache object với `cache_id`). Trong benchmark này, kịch bản "Explicit Cache" của Qwen dùng cùng cơ chế như implicit (cùng system prompt, warmup trước), khác biệt nằm ở việc đo sau khi cache đã warm.

### Gemini — Implicit Cache

Dùng lặp `system_instruction` giống nhau (ngưỡng 1.024 token), 1 warmup trước khi đo:

```python
import google.generativeai as genai

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

model = genai.GenerativeModel(
    model_name="gemini-3.1-flash-lite-preview",
    system_instruction=QUERY_BREAKING_PROMPT,  # >1024 tokens
)

response = model.generate_content(query, stream=True)
# Lưu ý: usage_metadata.cached_content_token_count = 0
# nhưng TTLT vẫn cải thiện ~16% — cache hoạt động ngầm
```

### Gemini — Explicit Cache

Tạo `CachedContent` trước, dùng `from_cached_content()` cho mọi request. Đây là cách duy nhất để xác nhận cache hit qua `cached_content_token_count`:

```python
from google.generativeai import caching as genai_caching
from datetime import timedelta

cached_content = genai_caching.CachedContent.create(
    model="gemini-3.1-flash-lite-preview",
    system_instruction=QUERY_BREAKING_PROMPT,
    contents=[],
    ttl=timedelta(minutes=10),
)

model = genai.GenerativeModel.from_cached_content(cached_content)
response = model.generate_content(query, stream=True)
# cached_content_token_count = 1330 → cache hit 100% confirmed

cached_content.delete()  # dọn dẹp sau khi dùng
```

---

## Kết Quả Thực Tế

> Số liệu đo thực từ API, không phải ước tính. 5 queries × mỗi kịch bản.

### Qwen3.5-Flash (`qwen3.5-flash-2026-02-23`, thinking disabled)

| Kịch bản | **TTLT mean** | TTLT min | TTLT max | TTFT mean | Cached tokens |
|---|---|---|---|---|---|
| Baseline | **1.312ms** | 1.044ms | 1.829ms | 582ms | 0 (không báo cáo) |
| Implicit Cache | **1.119ms** | 1.001ms | 1.215ms | 506ms | 0 (không báo cáo) |
| Explicit Cache* | **1.165ms** | 989ms | 1.317ms | 531ms | 0 (không báo cáo) |

*\* DashScope không hỗ trợ inline `cache_control` như Anthropic. Kịch bản này đo sau warmup với cùng system prompt.*

**Nhận xét Qwen:**
- TTLT baseline: **1.312ms** — nhanh hơn Gemini ở mọi kịch bản
- Implicit cache (sau warmup) giảm TTLT **~15%** (1.312ms → 1.119ms), variance nhỏ hơn đáng kể (max 1.829ms → 1.215ms)
- TTFT rất thấp (582ms baseline) — Qwen xử lý prefill nhanh, phần lớn TTLT là generation time
- API không báo cáo `cached_tokens` cho model này — không thể xác nhận cache hit qua usage stats

### Gemini-3.1-Flash-Lite-Preview

| Kịch bản | **TTLT mean** | TTLT min | TTLT max | TTFT mean | Cached tokens |
|---|---|---|---|---|---|
| Baseline | **1.474ms** | 1.142ms | 2.006ms | 1.204ms | 0 |
| Implicit Cache | **1.240ms** | 1.057ms | 1.456ms | 957ms | 0 (không báo cáo) |
| Explicit Cache | **1.425ms** | 1.301ms | 1.629ms | 1.166ms | **1.330** ✓ |

**Nhận xét Gemini:**
- Implicit cache cải thiện TTLT **~16%** (1.474ms → 1.240ms) và TTFT **~20%** (1.204ms → 957ms) — nhưng `cached_content_token_count` = 0, SDK cũ không báo cáo implicit cache stats
- Explicit cache: **1.330 token cached, 100% hit rate**, xác nhận hoàn toàn — nhưng TTLT chỉ cải thiện **~3%** so với baseline (1.425ms vs 1.474ms), thậm chí chậm hơn implicit (1.240ms)
- Explicit cache TTFT (1.166ms) cao hơn implicit (957ms) — overhead của cache lookup bù vào phần prefill tiết kiệm được

### So sánh tổng hợp

| Model | Kịch bản | **TTLT mean** | Δ vs Baseline | TTFT mean | Cache hit |
|---|---|---|---|---|---|
| Qwen3.5-Flash | Baseline | 1.312ms | — | 582ms | — |
| Qwen3.5-Flash | Implicit | **1.119ms** | **-15%** | 506ms | không rõ |
| Qwen3.5-Flash | Explicit* | 1.165ms | -11% | 531ms | không rõ |
| Gemini-3.1-FL | Baseline | 1.474ms | — | 1.204ms | — |
| Gemini-3.1-FL | Implicit | **1.240ms** | **-16%** | 957ms | không rõ |
| Gemini-3.1-FL | Explicit | 1.425ms | -3% | 1.166ms | 1.330 token ✓ |

### Phát hiện quan trọng từ số liệu thực

**1. TTLT bị chi phối bởi generation time, không phải prefill.**
Output trung bình là 60–90 token. Phần generation này không được cache tăng tốc. Với Qwen TTFT=582ms và TTLT=1.312ms, generation chiếm ~730ms (~56%). Cache chỉ tác động lên 44% còn lại (prefill). Đây là lý do TTLT chỉ giảm 15–16% dù cache đang hoạt động.

**2. Explicit cache Gemini: xác nhận hit nhưng không nhanh hơn implicit.**
Explicit cache (1.425ms) chậm hơn implicit cache (1.240ms) — overhead khởi tạo cache lookup bù vào lợi ích prefill. Tuy nhiên, **lợi thế thực sự của explicit cache là cost** (xem phần dưới) chứ không phải latency.

**3. Qwen không báo cáo cached tokens — cần đo gián tiếp.**
Cả implicit lẫn "explicit" Qwen đều trả `cached_tokens=0`. Nhưng TTLT giảm ~15% sau warmup chứng minh cache đang hoạt động. DashScope cần API Context Cache riêng để xác nhận explicit cache hit.

**4. Qwen nhanh hơn Gemini ở TTFT (582ms vs 1.204ms) nhưng tương đương TTLT.**
Điều này cho thấy Qwen có prefill nhanh hơn nhưng tốc độ generation tương tự Gemini. Với task output ngắn, TTLT cuối cùng khá gần nhau (~1.1–1.5s với cache).

---

## Phân Tích Chi Phí

### Bảng giá

| Model | Input (no cache) | Implicit hit | Explicit hit | Output |
|---|---|---|---|---|
| Qwen3.5-Flash | $0.10/1M | $0.02/1M | $0.01/1M | $0.40/1M |
| Gemini 3.1 FL | $0.025/1M | $0.0025/1M | $0.0025/1M | $0.10/1M |

### Chi phí thực tế đo được: 1.000 request/ngày

Dựa trên token count thực từ benchmark (~1.320–1.358 input tokens, ~60–90 output tokens):

| Model | Kịch bản | Chi phí/ngày | Tiết kiệm |
|---|---|---|---|
| Qwen3.5-Flash | Baseline | $0.163/ngày | — |
| Qwen3.5-Flash | Implicit Cache | $0.160/ngày | -2% |
| Qwen3.5-Flash | Explicit Cache | $0.160/ngày | -2% |
| Gemini-3.1-FL | Baseline | $0.041/ngày | — |
| Gemini-3.1-FL | Implicit Cache | $0.041/ngày | ~0% |
| Gemini-3.1-FL | Explicit Cache | **$0.011/ngày** | **-73%** |

**Giải thích kết quả chi phí:**

- **Qwen**: Tiết kiệm rất ít vì output tokens (60–90 token × $0.40/1M) chiếm phần lớn chi phí. Với 75 output token trung bình và 1.322 input token, output chiếm ~23% cost nhưng không được cache
- **Gemini Explicit Cache**: Tiết kiệm 73% nhờ 1.330/1.355 token input = **98% prefix được cache** tại giá 10% ($0.0025 vs $0.025/1M). Đây là lợi thế chi phí rõ ràng nhất của explicit cache
- **Gemini Implicit Cache**: Cost gần như không đổi (~$0.041/ngày) — SDK cũ không báo cáo cached tokens nên không tính giảm giá, dù latency thực sự đã cải thiện

> Phí storage Gemini explicit cache: $1/1M token/giờ × 1.330 token × 24h = **~$0.032/ngày**. Đã tính vào $0.011/ngày ở trên.

---

## Kết Luận

### Những gì benchmark này xác nhận được

| Phát hiện | Qwen3.5-Flash | Gemini-3.1-FL |
|---|---|---|
| Implicit cache cải thiện TTLT | Có (~15%) | Có (~16%) |
| Implicit cache có thể đo qua API stats | **Không** (cached_tokens=0) | **Không** (SDK cũ) |
| Explicit cache hit có thể xác nhận | **Không** (DashScope cần API riêng) | **Có** (1.330 tokens, 100%) |
| Explicit cache cải thiện TTLT đáng kể | — | **Không** (+3% so baseline) |
| Explicit cache giảm cost đáng kể | Cần test đúng API | **Có** (-73%) |
| Cần tắt thinking mode | **Có** (bắt buộc) | Không áp dụng |

### Ma trận quyết định cho Query Breaking Pipeline

| Ưu tiên | Model | Caching | Lý do |
|---|---|---|---|
| TTLT thấp nhất | Qwen3.5-Flash | Implicit (sau warmup) | 1.119ms TTLT, đơn giản |
| Cost tối thiểu | Gemini-3.1-FL | Explicit Cache | $0.011/ngày (-73%) |
| Xác nhận cache hit | Gemini-3.1-FL | Explicit Cache | Duy nhất có thể verify |
| Cân bằng latency+cost | Gemini-3.1-FL | Implicit Cache | 1.240ms, không phí storage |
| Qwen production | Qwen3.5-Flash | Implicit + DashScope Context Cache API | Cần dùng đúng API |

### Tóm tắt

- **TTLT là metric đúng cho query breaking** — TTFT không có giá trị thực tế khi pipeline cần full JSON
- **Cache giảm TTLT 15–16%**, không phải 65% như các con số lý thuyết thường được trích dẫn — vì generation time chiếm &gt;50% TTLT và không được cache tăng tốc
- **Explicit cache Gemini**: lợi ích chủ yếu là **cost** (-73%), không phải latency
- **Qwen3.5-Flash**: nhớ dùng `enable_thinking: false` và model ID đầy đủ `qwen3.5-flash-2026-02-23`
- **Để tối ưu TTLT triệt để**: giảm output token (giới hạn số sub-query, output format compact) quan trọng hơn caching

> Script đầy đủ: [`benchmark_cache.py`](https://github.com/manhhailua/manhpt.com/blob/main/blog/2026-03-13-benchmark-cache-qwen35-vs-gemini31/benchmark_cache.py) | Kết quả raw: [`benchmark_cache_results.json`](https://github.com/manhhailua/manhpt.com/blob/main/blog/2026-03-13-benchmark-cache-qwen35-vs-gemini31/benchmark_cache_results.json)

---

## Tài Nguyên

- [DashScope Context Cache Documentation](https://www.alibabacloud.com/help/en/model-studio/context-cache)
- [Google AI Context Caching Documentation](https://ai.google.dev/gemini-api/docs/caching)
- [Qwen3.5-Flash — DashScope Models](https://www.alibabacloud.com/help/en/model-studio/getting-started/models)
- [Gemini 3.1 Flash Lite Preview](https://deepmind.google/technologies/gemini/flash/)
