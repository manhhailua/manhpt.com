---
title: "Context Cache trong LLM: Prefix Cache vs KV Cache, Implicit vs Explicit - Phân Tích Claude, Gemini, GPT, Qwen3.5"
slug: llm-context-cache-prefix-kv-cache-analysis
authors: [manhpt]
tags: [llm, cache, optimization, latency, claude, gemini, gpt, qwen, vietnamese, technical]
date: 2026-03-15
description: "Phân tích sâu về context cache (prefix cache/KV cache) trong các model LLM hiện đại: Claude, Gemini, GPT, Qwen3.5. So sánh implicit vs explicit cache, ảnh hưởng đến TTFT và TTLT, và thực tiễn triển khai trong production."
---

# Context Cache trong LLM: Prefix Cache vs KV Cache, Implicit vs Explicit

**Context cache** (còn gọi là prefix cache hoặc KV cache) là kỹ thuật tối ưu quan trọng trong các LLM API hiện đại, giúp giảm latency và cost khi xử lý các request có phần context lặp lại. Bài viết này phân tích sâu kiến trúc cache của 4 model LLM hàng đầu (Claude, Gemini, GPT, Qwen3.5), so sánh implicit vs explicit cache, và đặc biệt tập trung vào trade-off giữa **TTFT (Time-To-First-Token)** và **TTLT (Time-To-Last-Token)** - vấn đề then chốt trong optimization thực tế.

<!-- truncate -->

## Tại Sao Context Cache Quan Trọng?

Trong các ứng dụng thực tế, LLM thường xử lý các request có cấu trúc lặp lại:

- **RAG pipelines**: System prompt chứa instructions, few-shot examples (~1,000-5,000 tokens)
- **Chat applications**: Conversation history, user preferences
- **Batch processing**: Cùng template cho nhiều documents
- **Multi-turn dialogues**: Context từ các turns trước

Without cache, mỗi request phải recompute toàn bộ context → tốn compute, tăng latency, tăng cost.

## Hai Loại Cache Kiến Trúc: Từ Lý Thuyết Đến Thực Tiễn

### 1. Prefix Cache (Context Cache) - Cache Ở Mức High-Level
- **Cơ chế**: Cache kết quả computation của prefix tokens (thường là system prompt hoặc conversation history) sau khi qua embedding layers và một phần transformer
- **Granularity**: Cache ở mức token sequence level
- **Khi nào hoạt động**: Khi request mới có prefix giống hệt request trước (exact string match)
- **Memory footprint**: Tương đối nhỏ, chỉ cache intermediate representations
- **Ví dụ thực tế**: Claude's implicit cache, Gemini's system instruction cache
- **Ưu điểm**: Dễ implement, hiệu quả cho system prompt lặp lại
- **Nhược điểm**: Không linh hoạt, yêu cầu exact match

### 2. KV Cache (Key-Value Cache) - Cache Ở Mức Low-Level
- **Cơ chế**: Cache attention key-value pairs từ tất cả các layers của transformer architecture
- **Granularity**: Cache ở mức attention mechanism level
- **Khi nào hoạt động**: Có thể cache partial context, hỗ trợ similarity-based matching
- **Memory footprint**: Lớn hơn đáng kể (cache K/V matrices cho mỗi layer)
- **Ví dụ thực tế**: GPT's advanced caching, custom inference servers (vLLM, TGI)
- **Ưu điểm**: Linh hoạt, có thể tái sử dụng cho similar contexts
- **Nhược điểm**: Memory intensive, complex implementation

### So Sánh Chi Tiết
| Aspect | Prefix Cache | KV Cache |
|--------|--------------|----------|
| **Cache level** | High-level (token sequences) | Low-level (attention K/V) |
| **Matching** | Exact string match | Semantic similarity possible |
| **Memory** | ~O(n) với n = token count | ~O(n × layers × hidden_dim) |
| **Flexibility** | Low (cần exact match) | High (partial reuse) |
| **Implementation** | Tương đối đơn giản | Phức tạp, cần deep integration |
| **Use case** | System prompt repetition | General context reuse |

## Implicit vs Explicit Cache

### Implicit Cache (Tự Động)
| Đặc điểm | Ưu điểm | Nhược điểm |
|----------|---------|------------|
| Tự động phát hiện prefix trùng | Không cần setup | Không đảm bảo hit rate |
| Ngưỡng token tối thiểu (256-1,024) | Giảm latency cho common cases | Không kiểm soát được TTL |
| Không có phí tạo cache | Cost-effective cho sporadic use | Không biết khi nào cache invalid |

### Explicit Cache (Thủ Công)
| Đặc điểm | Ưu điểm | Nhược điểm |
|----------|---------|------------|
| Tạo cache object trước | Đảm bảo hit rate trong TTL | Phí tạo cache (125-200% input cost) |
| TTL configurable (5 phút - 7 ngày) | Predictable performance | Chi phí lưu trữ (Gemini: $1/1M token/giờ) |
| Cache hit tracking | Có thể monitor hiệu quả | Complexity tăng |

## So Sánh Các Model LLM

### Claude (Anthropic)
| Loại Cache | Cơ Chế | Ngưỡng | TTL | Giá |
|------------|--------|--------|-----|-----|
| **Implicit** | Prefix cache tự động | 256 tokens | Không cam kết | 20% input cost |
| **Explicit** | `cache_control: {type: ephemeral}` | 1,024 tokens | 5 phút | 125% input cost |

**Đặc điểm Claude**:
- Implicit cache hiệu quả cho system prompt lặp lại
- Explicit cache dùng `cache_control` parameter
- TTLT cải thiện đáng kể với cache hit (30-50%)

### Gemini (Google)
| Loại Cache | Cơ Chế | Ngưỡng | TTL | Giá |
|------------|--------|--------|-----|-----|
| **Implicit** | System instruction cache | 1,024 tokens | Không cam kết | 10% input cost |
| **Explicit** | `CachedContent` API | 4,096 tokens | Configurable | 10% input cost + $1/1M token/giờ |

**Đặc điểm Gemini**:
- Implicit cache chỉ cho `system_instruction`
- Explicit cache mạnh mẽ với `CachedContent.create()`
- Cache hit tracking qua `cached_content_token_count`
- Storage cost cho long-lived cache

### GPT (OpenAI)
| Loại Cache | Cơ Chế | Ngưỡng | TTL | Giá |
|------------|--------|--------|-----|-----|
| **Implicit** | Prefix cache nâng cao | Dynamic | Không công khai | Không công khai |
| **Explicit** | Custom với fine-tuning | Enterprise-only | Enterprise-only | Enterprise-only |

**Đặc điểm GPT**:
- Cache implementation không công khai chi tiết
- Enterprise solutions có advanced caching
- Tập trung vào throughput hơn là per-request latency

### Qwen3.5 (Alibaba)
| Loại Cache | Cơ Chế | Ngưỡng | TTL | Giá |
|------------|--------|--------|-----|-----|
| **Implicit** | Prefix cache tự động | 256 tokens | Không cam kết | 20% input cost |
| **Explicit** | Cache ID API | 1,024 tokens | 5 phút | 10% input cost |

**Đặc điểm Qwen**:
- Implicit cache tương tự Claude
- Explicit cache qua cache ID system
- Hiệu quả cost (10% cho cache hit)
- DashScope API không report `cached_tokens`

## Vấn Đề Chính: TTFT vs TTLT - Phân Tích Toán Học và Thực Nghiệm

### TTFT (Time-To-First-Token) - Tại Sao Cải Thiện Nhiều?
**Công thức tổng quát**:
```
TTFT_without_cache = T_prefix_computation + T_generation_init
TTFT_with_cache = T_cache_lookup + T_generation_init
```

**Phân tích**:
- **T_prefix_computation**: Thời gian compute prefix (system prompt, history). Với prompt 1,000 tokens, có thể mất 100-300ms.
- **T_cache_lookup**: Thời gian lookup cache, thường < 10ms.
- **T_generation_init**: Thời gian khởi tạo generation, không đổi.

**Kết quả**: TTFT giảm 30-70% vì `T_prefix_computation ≫ T_cache_lookup`.

### TTLT (Time-To-Last-Token) - Tại Sao Khó Cải Thiện?
**Công thức tổng quát**:
```
TTLT_without_cache = T_prefix_computation + T_generation_total + T_network
TTLT_with_cache = T_cache_lookup + T_generation_total + T_network
```

**Phân tích chi tiết**:
1. **T_generation_total**: Thời gian generate toàn bộ output. Ví dụ output 100 tokens mất ~200-400ms.
2. **T_network**: Network latency, có thể 50-200ms tùy region.
3. **T_prefix_computation vs T_cache_lookup**: Chênh lệch 100-300ms.

**Bài toán tối ưu**:
```
Improvement = (TTLT_without_cache - TTLT_with_cache) / TTLT_without_cache
           = (T_prefix_computation - T_cache_lookup) / (T_prefix_computation + T_generation_total + T_network)
```

**Ví dụ số**:
- T_prefix_computation = 200ms
- T_cache_lookup = 10ms  
- T_generation_total = 300ms
- T_network = 100ms

```
TTLT_without_cache = 200 + 300 + 100 = 600ms
TTLT_with_cache = 10 + 300 + 100 = 410ms
Improvement = (200 - 10) / 600 = 190 / 600 = 31.7%
```

**Kết luận**:
- **TTFT improvement**: 30-70% (vì mẫu số nhỏ)
- **TTLT improvement**: 10-35% (vì mẫu số lớn hơn)
- **Output length càng dài** → T_generation_total càng lớn → improvement càng nhỏ
- **Network latency cao** → T_network lớn → improvement càng nhỏ

### Ảnh Hưởng Đến Ứng Dụng Thực Tế
| Application Type | TTFT Importance | TTLT Importance | Cache Benefit |
|-----------------|-----------------|-----------------|---------------|
| **Chat streaming** | ⭐⭐⭐⭐⭐ (user perception) | ⭐⭐ (total time) | High (TTFT focus) |
| **RAG pipeline** | ⭐ (background) | ⭐⭐⭐⭐⭐ (pipeline throughput) | Moderate (TTLT limited) |
| **Batch processing** | ⭐ (not critical) | ⭐⭐⭐⭐⭐ (total job time) | Low (amortized over batch) |
| **JSON API** | ⭐⭐ (quick start) | ⭐⭐⭐⭐ (complete response) | Moderate (mixed) |

### Benchmark Thực Tế
Từ [bài benchmark trước](https://manhpt.com/blog/benchmark-cache-qwen35-vs-gemini31):

| Model | Scenario | TTFT Reduction | TTLT Reduction | Notes |
|-------|----------|----------------|----------------|-------|
| Qwen3.5 | Implicit Cache | ~40% | ~15% | Cache hoạt động ngầm |
| Gemini | Implicit Cache | ~35% | ~16% | System instruction cache |
| Gemini | Explicit Cache | ~45% | ~18% | CachedContent với tracking |
| Claude | Implicit Cache | ~50% | ~20% | Hiệu quả nhất trong test |

## Thực Tiễn Triển Khai

### Khi Nào Dùng Implicit Cache?
1. **System prompt lặp lại** (>256 tokens cho Claude/Qwen, >1,024 cho Gemini)
2. **Sporadic traffic** không cần guarantee
3. **Cost-sensitive** applications
4. **Simple implementations** không muốn manage cache state

### Khi Nào Dùng Explicit Cache?
1. **High-throughput pipelines** cần predictable latency
2. **Batch processing** với cùng template
3. **Enterprise applications** với SLA requirements
4. **Khi cần cache hit monitoring**

### Code Examples

#### Claude Explicit Cache
```python
# Anthropic Claude với explicit cache
from anthropic import Anthropic

client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    messages=[{"role": "user", "content": query}],
    system=system_prompt,
    max_tokens=300,
    cache_control={"type": "ephemeral"}  # 5-minute cache
)
```

#### Gemini Explicit Cache
```python
# Google Gemini với CachedContent
import google.generativeai as genai

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Tạo cache
cache = genai.CachedContent.create(
    model="gemini-3.1-flash-lite-preview",
    system_instruction=system_prompt,
    ttl=300  # 5 minutes
)

# Sử dụng cache
model = genai.GenerativeModel.from_cached_content(cache.name)
response = model.generate_content(query, stream=True)
```

#### Qwen Implicit Cache
```python
# Qwen với implicit cache (tự động)
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["DASHSCOPE_API_KEY"],
    base_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1",
)

response = client.chat.completions.create(
    model="qwen3.5-flash-2026-02-23",
    messages=[
        {"role": "system", "content": system_prompt},  # >256 tokens
        {"role": "user", "content": query},
    ],
    stream=True,
    extra_body={"enable_thinking": False},  # quan trọng cho TTLT
)
```

## Các Vấn Đề và Giải Pháp

### 1. Cache Invalidation
**Vấn đề**: Khi nào cache stale?
**Giải pháp**:
- Dùng explicit cache với TTL phù hợp
- Versioning system prompt
- Cache key với prompt hash

### 2. Memory Overhead
**Vấn đề**: Cache chiếm memory trên server
**Giải pháp**:
- Chỉ cache phần quan trọng (system prompt, không cache user input)
- Implement LRU eviction policy
- Monitor cache hit ratio vs memory usage

### 3. Cold Start Latency
**Vấn đề**: Request đầu tiên chậm
**Giải pháp**:
- Warm-up cache trước production traffic
- Pre-create cached content
- Use gradual rollout với cache warming

### 4. Cost Optimization
**Vấn đề**: Cache storage cost (đặc biệt Gemini)
**Giải pháp**:
- Tính toán break-even point: cache hit rate cần thiết
- Dùng implicit cache khi possible
- Implement cache tiering (hot/warm/cold)

## Xu Hướng và Tương Lai

### 1. Smarter Caching
- **Partial prefix matching**: Cache không yêu cầu exact match
- **Semantic caching**: Cache based on semantic similarity
- **Adaptive TTL**: Tự động điều chỉnh TTL based on access pattern

### 2. Standardization
- **Common cache API** across providers
- **Cache interoperability** between different LLMs
- **Open caching protocols**

### 3. Hardware Acceleration
- **GPU memory optimization** cho KV cache
- **Specialized cache chips** for LLM inference
- **Distributed caching** across inference clusters

### 4. Application-Level Innovations
- **Prompt compression** để giảm cache size
- **Dynamic prompt assembly** từ cached components
- **Multi-tenant cache sharing**

## Kết Luận

Context cache là công cụ mạnh mẽ để tối ưu LLM applications, nhưng cần hiểu rõ trade-off:

1. **TTFT cải thiện nhiều** với cache, nhưng **TTLT có thể không cải thiện** đáng kể
2. **Implicit cache** đơn giản nhưng unpredictable
3. **Explicit cache** predictable nhưng có cost overhead
4. **Mỗi provider có implementation khác nhau** → cần testing cụ thể

**Khuyến nghị**:
- **Start với implicit cache** cho simple use cases
- **Graduate to explicit cache** khi cần predictability
- **Monitor cả TTFT và TTLT** để hiểu real impact
- **Test với workload thực tế** của application

Cache không phải silver bullet, nhưng khi dùng đúng, nó có thể giảm latency 30-50% và cost 10-20% cho các workload phù hợp.

---

## Tài Liệu Tham Khảo

1. [Anthropic Cache Documentation](https://docs.anthropic.com/claude/docs/cache-control)
2. [Google Gemini CachedContent Guide](https://ai.google.dev/gemini-api/docs/cached-content)
3. [DashScope Qwen Cache Features](https://help.aliyun.com/zh/model-studio/developer-reference/compatibility-of-dashscope-with-openai)
4. [Benchmark: Implicit vs Explicit Cache - Qwen3.5 vs Gemini](https://manhpt.com/blog/benchmark-cache-qwen35-vs-gemini31)
5. [LLM Inference Optimization Survey](https://arxiv.org/abs/2501.01234)

*Bài viết được tổng hợp từ documentation chính thức, benchmark thực tế, và kinh nghiệm production. Cập nhật lần cuối: 15/3/2026.*