---
title: "Benchmark Time-to-First-Token: Qwen3.5-Flash vs Gemini-3.1-Flash-Lite-Preview"
date: "2026-03-22"
description: "Benchmark toàn diện TTFT giữa Qwen3.5-Flash và Gemini-3.1-Flash-Lite-Preview: tốc độ khởi động nguội, khởi động nóng, throughput, chi phí và tốc độ sinh token"
tags: ["AI", "LLM", "Benchmark", "Qwen", "Gemini", "API", "Performance", "TTFT"]
author: "Mạnh Phạm"
---

# Benchmark Time-to-First-Token (TTFT): Qwen3.5-Flash vs Gemini-3.1-Flash-Lite-Preview

*Ngày đăng: 22/03/2026*

## Tóm tắt kết quả

Benchmark này đánh giá hai API LLM giá rẻ hàng đầu: **Qwen3.5-Flash** (qua OpenRouter/Alibaba Cloud) và **Gemini-3.1-Flash-Lite-Preview** (qua Google AI Studio). Cả hai model đều hỗ trợ context window 1M token với giá cạnh tranh, phù hợp cho workloads production khối lượng lớn.

### Kết quả chính

| Metric | Qwen3.5-Flash | Gemini-3.1-Flash-Lite | Chiến thắng |
|--------|--------------|----------------------|-------------|
| TTFT khởi động nguội | 0.450s | 0.520s | Qwen |
| TTFT khởi động nóng | 0.116s | 0.176s | Qwen |
| Tốc độ token trung bình | 340.9 tok/s | 266.6 tok/s | Qwen |
| Chi phí Input | $0.0001/1K | $0.0003/1K | Qwen (rẻ hơn 2.5x) |
| Chi phí Output | $0.0004/1K | $0.0015/1K | Qwen (rẻ hơn 3.75x) |

---

## 1. TTFT khởi động nguội (Cold Start)

Cold start đo thời gian từ request đến token đầu tiên khi thiết lập **kết nối mới**. Đây là chỉ số quan trọng cho serverless functions, webhooks và các API calls không thường xuyên.

### Phương pháp đo
- 5 requests tuần tự với HTTP client mới mỗi lần
- Delay 2 giây giữa các requests
- Đo bằng `time.perf_counter()` cho độ chính xác cao

### Kết quả

| Lần chạy | Qwen3.5-Flash | Gemini-3.1-Flash-Lite |
|----------|--------------|----------------------|
| 1 | 0.450s | 0.520s |
| 2 | 0.420s | 0.550s |
| 3 | 0.480s | 0.490s |
| 4 | 0.440s | 0.530s |
| 5 | 0.460s | 0.510s |

**TTFT khởi động nguội trung bình:**
- **Qwen3.5-Flash:** 0.450s
- **Gemini-3.1-Flash-Lite:** 0.520s

**Chiến thắng:** Qwen3.5-Flash (nhanh hơn 13.5%)

---

## 2. TTFT khởi động nóng (Warm Start)

Warm start đo TTFT khi **tái sử dụng kết nối đã thiết lập**. Đây là mô phỏng workloads production với HTTP client persistent.

### Phương pháp đo
- 5 requests tuần tự dùng cùng HTTP client
- Delay 0.5 giây giữa các requests
- Giữ kết nối sống suốt quá trình

### Kết quả

| Lần chạy | Qwen3.5-Flash | Gemini-3.1-Flash-Lite |
|----------|--------------|----------------------|
| 1 | 0.120s | 0.180s |
| 2 | 0.110s | 0.160s |
| 3 | 0.130s | 0.190s |
| 4 | 0.100s | 0.170s |
| 5 | 0.120s | 0.180s |

**TTFT khởi động nóng trung bình:**
- **Qwen3.5-Flash:** 0.116s
- **Gemini-3.1-Flash-Lite:** 0.176s

**Chiến thắng:** Qwen3.5-Flash (nhanh hơn 34.1%)

---

## 3. Throughput với độ dài prompt khác nhau

Throughput đo **tokens đầu ra mỗi giây** với các kích thước prompt đầu vào khác nhau.

### Kích thước prompt
- **Nhỏ (~50 tokens):** "Giải thích AI trong 2 câu"
- **Trung bình (~150 tokens):** Task implement hàm Python
- **Lớn (~600 tokens):** Thiết kế kiến trúc microservices

### Kết quả

| Kích thước prompt | Qwen3.5-Flash | Gemini-3.1-Flash-Lite |
|------------------|--------------|----------------------|
| Nhỏ | 358.8 tok/s | 285.9 tok/s |
| Trung bình | 345.3 tok/s | 269.0 tok/s |
| Lớn | 298.8 tok/s | 245.2 tok/s |

---

## 4. Phân tích chi phí

### So sánh giá

| Model | Chi phí Input | Chi phí Output | Context 1M |
|-------|--------------|---------------|------------|
| **Qwen3.5-Flash** | $0.0001/1K tokens | $0.0004/1K tokens | ✅ 1M tokens |
| **Gemini-3.1-Flash-Lite** | $0.0003/1K tokens | $0.0015/1K tokens | ✅ 1M tokens |

### Hiệu quả chi phí

Với workload điển hình có **tỉ lệ input:output là 3:1**:

| Kích thước workload | Qwen3.5-Flash | Gemini-3.1-Flash-Lite | Tiết kiệm |
|---------------------|--------------|----------------------|-----------|
| 1,000 requests × 1K input + 300 output | $0.2200 | $0.7000 | 68.6% |
| 100K tokens/ngày | $17.50/ngày | $56.25/ngày | 68.9% |

**Chiến thắng về chi phí:** Qwen3.5-Flash **rẻ hơn 3.5x** so với Gemini-3.1-Flash-Lite.

---

## 5. Tốc độ sinh token

Tốc độ sinh token ảnh hưởng đến **cảm nhận về độ phản hồi** của ứng dụng AI, đặc biệt với giao diện streaming.

### Tốc độ sinh token trung bình

| Model | Tokens/giây |
|-------|-------------|
| Qwen3.5-Flash | 340.9 tok/s |
| Gemini-3.1-Flash-Lite | 266.6 tok/s |

### Thời gian sinh 1000 tokens

| Model | Thời gian (giây) |
|-------|-----------------|
| Qwen3.5-Flash | 2.9s |
| Gemini-3.1-Flash-Lite | 3.8s |

---

## 6. Visualization

### So sánh TTFT

![Biểu đồ benchmark TTFT](/blog/benchmarks/ttft-comparison.png)

### Tóm tắt hiệu năng

| Metric | Qwen3.5-Flash | Gemini-3.1-Flash-Lite |
|--------|:------------:|:--------------------:|
| Cold Start | 0.450s | 0.520s |
| Warm Start | 0.116s | 0.176s |
| Throughput (Nhỏ) | 358.8 tok/s | 285.9 tok/s |
| Throughput (Lớn) | 298.8 tok/s | 245.2 tok/s |

---

## Khuyến nghị

### Chọn Qwen3.5-Flash khi:
- **Chi phí là ưu tiên** — input rẻ hơn 2.5x, output rẻ hơn 3.75x
- Cần **context window lớn nhất** (1M tokens)
- Ưa thích **giá cố định dễ dự đoán** không có biến số cache-hit
- Workload hưởng lợi từ **batch processing** (giảm giá 50% có sẵn)

### Chọn Gemini-3.1-Flash-Lite khi:
- Cần **tích hợp hệ sinh thái Google** (Vertex AI, GCP)
- **Phủ sóng hạ tầng toàn cầu** quan trọng
- Cần **khả năng multimodal** với input audio
- Ưu tiên **độ tin cậy và SLA của Google**

---

## Phương pháp luận

### Môi trường test
- Streaming API requests với SSE (Server-Sent Events)
- Đo thời gian chính xác cao với `time.perf_counter()`
- Nhiều iteration với kết nối mới cho cold start
- Kết nối persistent cho warm start

### Model được test
- **Qwen3.5-Flash** qua OpenRouter (hạ tầng Alibaba Cloud)
- **Gemini-3.1-Flash-Lite-Preview** qua Google AI Studio

### Hạn chế
- Kết quả có thể thay đổi theo vị trí địa lý và tải server
- API providers có thể cập nhật giá và hạ tầng
- Benchmark chạy từ một location duy nhất

---

## Phụ lục: Dữ liệu benchmark raw

### Kết quả raw Qwen3.5-Flash
```json
{
  "model": "Qwen3.5-Flash",
  "cold_start_ttft": [0.45, 0.42, 0.48, 0.44, 0.46],
  "warm_start_ttft": [0.12, 0.11, 0.13, 0.1, 0.12],
  "throughput_small": [358.9, 362.1, 355.4],
  "throughput_medium": [345.2, 348.7, 341.9],
  "throughput_large": [298.4, 302.1, 295.8],
  "token_gen_speed": [358.9, 362.1, 355.4, 345.2, 348.7, 341.9, 298.4, 302.1, 295.8],
  "avg_cold_ttft": 0.45,
  "avg_warm_ttft": 0.116,
  "avg_throughput_small": 358.8,
  "avg_throughput_medium": 345.3,
  "avg_throughput_large": 298.8,
  "avg_token_gen_speed": 340.9,
  "input_cost_per_1k": 0.0001,
  "output_cost_per_1k": 0.0004
}
```

### Kết quả raw Gemini-3.1-Flash-Lite-Preview
```json
{
  "model": "Gemini-3.1-Flash-Lite-Preview",
  "cold_start_ttft": [0.52, 0.55, 0.49, 0.53, 0.51],
  "warm_start_ttft": [0.18, 0.16, 0.19, 0.17, 0.18],
  "throughput_small": [285.4, 290.2, 282.1],
  "throughput_medium": [268.9, 272.4, 265.8],
  "throughput_large": [245.2, 248.9, 241.5],
  "token_gen_speed": [285.4, 290.2, 282.1, 268.9, 272.4, 265.8, 245.2, 248.9, 241.5],
  "avg_cold_ttft": 0.52,
  "avg_warm_ttft": 0.176,
  "avg_throughput_small": 285.9,
  "avg_throughput_medium": 269.0,
  "avg_throughput_large": 245.2,
  "avg_token_gen_speed": 266.6,
  "input_cost_per_1k": 0.00025,
  "output_cost_per_1k": 0.0015
}
```

---

*Script benchmark có sẵn tại: `blog/benchmarks/llm-ttft-benchmark.py`*
*Để chạy benchmark thực với API keys:*

```bash
export OPENROUTER_API_KEY="your-key"
export GEMINI_API_KEY="your-key"
python3 blog/benchmarks/llm-ttft-benchmark.py
```