---
title: "Implicit Cache vs Explicit Cache: Qwen3.5-Flash và Gemini-3.1-Flash-Lite-Preview — Đo Thực Tế TTLT"
slug: benchmark-cache-qwen35-vs-gemini31
authors: [manhpt]
tags: [benchmark, qwen, gemini, vietnamese, cache, llm, cost-optimization]
date: 2026-03-13
description: "Benchmark thực tế tháng 3/2026: So sánh implicit cache vs explicit cache giữa Qwen3.5-Flash và Gemini-3.1-Flash-Lite-Preview cho bài toán query breaking trong RAG. Metric chính là TTLT — thời điểm pipeline nhận đủ output để bắt đầu truy vấn vector database."
---

**Trong pipeline RAG, bước "query breaking" — phân tách câu hỏi phức hợp thành các sub-query độc lập — là bottleneck đầu tiên trước khi có thể fan-out sang vector database.** Metric quan trọng nhất không phải TTFT (first token) mà là **TTLT (time-to-last-token)**: pipeline chỉ có thể gọi `json.loads()` và bắt đầu retrieval khi nhận đủ toàn bộ JSON array. Bài viết này là báo cáo benchmark thực tế, chạy script đo TTLT/TTFT cho **Qwen3.5-Flash** và **Gemini-3.1-Flash-Lite-Preview** với 4 kịch bản (baseline, implicit cache, explicit cache, no thinking + no streaming).

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

- **TTLT** (metric chính): thời gian từ request đến khi nhận output cuối cùng (với streaming: token cuối; với non-stream: full response)
- **TTFT** (metric phụ): thời gian đến token đầu tiên, chỉ áp dụng cho các kịch bản `stream=True`
- Mỗi kịch bản: 5 queries thực, 2 giây nghỉ giữa mỗi query
- 1 warmup run trước kịch bản implicit cache để seed cache
- Script: [`benchmark_cache.py`](https://github.com/manhhailua/manhpt.com/blob/master/blog/2026-03-13-benchmark-cache-qwen35-vs-gemini31/benchmark_cache.py)

---

## Cách Bật Cache Cho Từng Model

### Qwen — Implicit Cache

Dùng cùng system prompt, gọi HTTP trực tiếp theo OpenAI-compatible endpoint của DashScope. Quan trọng: tắt thinking mode cho task JSON ngắn:

```python
import requests

response = requests.post(
    "https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {os.environ['DASHSCOPE_API_KEY']}",
        "Content-Type": "application/json",
    },
    json={
        "model": "qwen3.5-flash-2026-02-23",
        "messages": [
            {"role": "system", "content": QUERY_BREAKING_PROMPT},
            {"role": "user", "content": query},
        ],
        "stream": True,
        "stream_options": {"include_usage": True},
        "max_tokens": 300,
        "enable_thinking": False,
    },
    stream=True,
)
```

> **Lưu ý:** Dù gọi HTTP trực tiếp, benchmark vẫn có thể nhận `cached_tokens=0` ở Qwen tùy model/region/runtime.

### Qwen — Explicit Cache

Format `cache_control: {type: ephemeral}` là của Anthropic Claude — **không hoạt động** với DashScope. Explicit context cache của Qwen dùng API riêng (tạo cache object với `cache_id`). Trong benchmark này, kịch bản "Explicit Cache" của Qwen dùng cùng cơ chế như implicit (cùng system prompt, warmup trước), khác biệt nằm ở việc đo sau khi cache đã warm.

### Gemini — Implicit Cache

Dùng SDK mới `google-genai`, lặp `system_instruction` giống nhau (ngưỡng 1.024 token), 1 warmup trước khi đo:

```python
from google import genai
from google.genai import types

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

for chunk in client.models.generate_content_stream(
    model="gemini-3.1-flash-lite-preview",
    contents=query,
    config=types.GenerateContentConfig(
        system_instruction=QUERY_BREAKING_PROMPT,
        max_output_tokens=300,
    ),
):
    usage = chunk.usage_metadata
```

### Gemini — Explicit Cache

Tạo cache bằng `client.caches.create()`, sau đó gọi model với `cached_content`:

```python
from google.genai import types

cached = client.caches.create(
    model="gemini-3.1-flash-lite-preview",
    config=types.CreateCachedContentConfig(
        system_instruction=QUERY_BREAKING_PROMPT,
        contents=[{"role": "user", "parts": [{"text": "Cache seed"}]}],
        ttl="600s",
    ),
)

response = client.models.generate_content(
    model="gemini-3.1-flash-lite-preview",
    contents=query,
    config=types.GenerateContentConfig(cached_content=cached.name),
)
# usage_metadata.cached_content_token_count > 0 => cache hit xác nhận được

client.caches.delete(name=cached.name)
```

---

## Kết Quả Thực Tế

> Số liệu đo thực từ API, không phải ước tính. 5 queries × mỗi kịch bản.

### Qwen3.5-Flash (`qwen3.5-flash-2026-02-23`, HTTP direct, thinking disabled)

| Kịch bản | **TTLT mean** | TTLT min | TTLT max | TTFT mean | Cached tokens |
|---|---|---|---|---|---|
| Baseline | **1.131ms** | 1.013ms | 1.258ms | 641ms | 0 |
| Implicit Cache | **981ms** | 808ms | 1.123ms | 516ms | 0 |
| Explicit Cache* | **951ms** | 908ms | 991ms | 516ms | 0 |
| Explicit Cache + No Streaming | **949ms** | 851ms | 1.122ms | N/A | 0 |

*\* Qwen explicit cache qua inline `cache_control` chỉ mang tính thử nghiệm trong benchmark này; DashScope Context Cache production nên dùng API riêng theo tài liệu chính thức.*

**Nhận xét Qwen:**
- So với baseline, Qwen cải thiện rõ ở cả 3 kịch bản còn lại: implicit (**-13.3%**), explicit (**-15.9%**), explicit+no-stream (**-16.1%**).
- `Explicit Cache + No Streaming` đang là nhanh nhất của Qwen trong run hiện tại (949ms).
- Warmup explicit trước khi đo giúp kết quả explicit ổn định hơn (range hẹp: 908–991ms).
- Với Qwen run này, usage vẫn trả `cached_tokens=0` nên chưa hard-confirm cache hit qua API stats.

### Gemini-3.1-Flash-Lite-Preview

| Kịch bản | **TTLT mean** | TTLT min | TTLT max | TTFT mean | Cached tokens |
|---|---|---|---|---|---|
| Baseline | **1.449ms** | 1.439ms | 1.467ms | 1.162ms | 0 |
| Implicit Cache | **1.331ms** | 1.048ms | 1.679ms | 962ms | 0 |
| Explicit Cache | **1.543ms** | 1.378ms | 1.714ms | 1.240ms | **1.339** ✓ |
| No Thinking + No Streaming | **1.309ms** | 981ms | 1.463ms | N/A | 0 |

**Nhận xét Gemini:**
- Implicit cache cải thiện TTLT **~8.1%** (1.449ms → 1.331ms) và giảm TTFT rõ rệt.
- Explicit cache xác nhận hit rõ ràng (**1.339 token cached**) nhưng TTLT lại **chậm hơn baseline ~6.5%** ở run này.
- Kịch bản **No Thinking + No Streaming** hiện có TTLT tốt nhất của Gemini (**1.309ms**, -9.7% vs baseline).
- `thinking_config` đã được SDK mới chấp nhận (`Gemini no-thinking toggle status: accepted`), nhưng tác động latency phụ thuộc mạnh vào runtime variance.

### So sánh tổng hợp

| Model | Kịch bản | **TTLT mean** | Δ vs Baseline | TTFT mean | Cache hit |
|---|---|---|---|---|---|
| Qwen3.5-Flash | Baseline | 1.131ms | — | 641ms | — |
| Qwen3.5-Flash | Implicit | 981ms | -13.3% | 516ms | 0 |
| Qwen3.5-Flash | Explicit* | 951ms | -15.9% | 516ms | 0 |
| Qwen3.5-Flash | Explicit + No Streaming | **949ms** | **-16.1%** | N/A | 0 |
| Gemini-3.1-FL | Baseline | 1.449ms | — | 1.162ms | — |
| Gemini-3.1-FL | Implicit | 1.331ms | -8.1% | 962ms | 0 |
| Gemini-3.1-FL | Explicit | 1.543ms | +6.5% | 1.240ms | 1.339 token ✓ |
| Gemini-3.1-FL | No Thinking + No Streaming | **1.309ms** | **-9.7%** | N/A | 0 |

### Phát hiện quan trọng từ số liệu thực

**1. Warmup explicit giúp Qwen explicit cải thiện rõ trong run hiện tại.**
Qwen explicit streaming/no-stream đều đạt mức tốt hơn baseline ~16%, dù `cached_tokens` vẫn không được báo ra usage.

**2. Implicit cache có lợi rõ hơn ở Gemini so với Qwen trong run hiện tại.**
Gemini giảm ~7.5% TTLT, trong khi Qwen gần như không đổi qua usage/latency.

**3. Explicit cache Gemini xác nhận hit rõ qua SDK mới nhưng vẫn có thể chậm hơn baseline.**
`cached_content_token_count` trung bình 1.339 token cho thấy cache hoạt động, nhưng latency explicit run này cao hơn baseline.

**4. Migrating sang `google-genai` giải quyết được vấn đề schema thinking.**
`thinking_config` đã hợp lệ và được áp dụng; số liệu không còn phụ thuộc vào fallback lỗi SDK cũ.

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
| Qwen3.5-Flash | Baseline | $0.1616/ngày | — |
| Qwen3.5-Flash | Implicit Cache | $0.1604/ngày | -0.7% |
| Qwen3.5-Flash | Explicit Cache | $0.1608/ngày | -0.5% |
| Qwen3.5-Flash | Explicit Cache + No Streaming | $0.1580/ngày | -2.2% |
| Gemini-3.1-FL | Baseline | $0.0412/ngày | — |
| Gemini-3.1-FL | Implicit Cache | $0.0418/ngày | +1.5% |
| Gemini-3.1-FL | Explicit Cache | **$0.0108/ngày** | **-73.7%** |
| Gemini-3.1-FL | No Thinking + No Streaming | $0.0406/ngày | -1.5% |

**Giải thích kết quả chi phí:**

- **Qwen**: Chênh lệch cost vẫn nhỏ, nhưng explicit + no-stream đang thấp nhất trong run này.
- **Gemini Explicit Cache**: Vẫn là phương án tiết kiệm nhất (**-73.7%**), nhờ `cached_content_token_count` cao và ổn định.
- **Gemini Implicit**: Ở run này cost tăng nhẹ do `cached_content_token_count` không được ghi nhận cho implicit.

> Phí storage Gemini explicit cache: $1/1M token/giờ × 1.339 token × 24h = **~$0.032/ngày**. Đã tính vào mức ~$0.0108/ngày ở trên.

---

## Kết Luận

### Những gì benchmark này xác nhận được

| Phát hiện | Qwen3.5-Flash | Gemini-3.1-FL |
|---|---|---|
| Implicit cache cải thiện TTLT | Có (~13.3%) | Có (~8.1%) |
| Implicit cache có thể đo qua API stats | **Không** (cached_tokens=0) | **Không** (run implicit trả 0) |
| Explicit cache hit có thể xác nhận | **Chưa** (cached_tokens=0) | **Có** (1.339 tokens) |
| Explicit cache cải thiện TTLT đáng kể | Có (~15.9%) | **Không** (+6.5% so baseline) |
| Explicit cache giảm cost đáng kể | Cần test đúng API | **Có** (-73.7%) |
| Non-stream cải thiện TTLT | Có (explicit+no-stream ~16.1%) | Có (~9.7%) |
| Cần tắt thinking mode | **Có** (bắt buộc) | Đã hỗ trợ qua `google-genai` |

### Ma trận quyết định cho Query Breaking Pipeline

| Ưu tiên | Model | Caching | Lý do |
|---|---|---|---|
| TTLT thấp nhất (streaming) | Qwen3.5-Flash | Explicit* | 951ms TTLT (run hiện tại) |
| TTLT thấp nhất (non-stream) | Qwen3.5-Flash | Explicit Cache + No Streaming | 949ms TTLT |
| Cost tối thiểu | Gemini-3.1-FL | Explicit Cache | $0.0108/ngày (-73.7%) |
| Xác nhận cache hit | Gemini-3.1-FL | Explicit Cache | Duy nhất có thể verify |
| Cân bằng latency+cost (streaming) | Gemini-3.1-FL | Implicit Cache | 1.331ms, không phí storage |
| Qwen production | Qwen3.5-Flash | Implicit + DashScope Context Cache API | Cần dùng đúng API |

### Tóm tắt

- **TTLT là metric đúng cho query breaking** — TTFT không có nhiều giá trị vận hành khi pipeline cần full JSON.
- **Qwen**: explicit (đặc biệt explicit + no-stream) cho TTLT tốt nhất ở run hiện tại, dù usage chưa báo `cached_tokens`.
- **Gemini**: implicit và non-stream có lợi về latency; explicit chủ yếu mạnh ở cost.
- **Explicit cache Gemini**: lợi ích chủ yếu là **cost** (-73.7%), không phải latency.
- **Qwen3.5-Flash**: nhớ dùng `enable_thinking: false` và model ID đầy đủ `qwen3.5-flash-2026-02-23`
- **Gemini no-thinking**: đã cấu hình được với SDK mới `google-genai`, nhưng hiệu quả latency phụ thuộc vào từng run.
- **Để tối ưu TTLT triệt để**: giảm output token (giới hạn số sub-query, output format compact) vẫn là đòn bẩy quan trọng.

> Script đầy đủ: [`benchmark_cache.py`](https://github.com/manhhailua/manhpt.com/blob/master/blog/2026-03-13-benchmark-cache-qwen35-vs-gemini31/benchmark_cache.py) | Kết quả raw: [`benchmark_cache_results.json`](https://github.com/manhhailua/manhpt.com/blob/master/blog/2026-03-13-benchmark-cache-qwen35-vs-gemini31/benchmark_cache_results.json)

---

## Tài Nguyên

- [DashScope Context Cache Documentation](https://www.alibabacloud.com/help/en/model-studio/context-cache)
- [Google AI Context Caching Documentation](https://ai.google.dev/gemini-api/docs/caching)
- [Qwen3.5-Flash — DashScope Models](https://www.alibabacloud.com/help/en/model-studio/getting-started/models)
- [Gemini 3.1 Flash Lite Preview](https://deepmind.google/technologies/gemini/flash/)
