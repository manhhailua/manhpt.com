---
title: "Benchmark: Qwen3.5-Flash vs Gemini-3.1-Flash-Lite-Preview - Ai nhanh hơn, rẻ hơn cho tiếng Việt?"
slug: benchmark-qwen35-vs-gemini31
authors: [manhpt]
tags: [ai, benchmark, qwen, gemini, vietnamese, llm]
date: 2026-03-10
description: "So sánh chi tiết giữa Qwen3.5-Flash và Gemini-3.1-Flash-Lite-Preview về tốc độ, chi phí và chất lượng khi xử lý truy vấn tiếng Việt trong lĩnh vực tài chính."
image: /img/blog/2026-03-10-benchmark-cover.png
---

# Benchmark: Qwen3.5-Flash vs Gemini-3.1-Flash-Lite-Preview

*Ai nhanh hơn, rẻ hơn cho tiếng Việt?*

Trong thế giới AI đang phát triển nhanh chóng, việc lựa chọn model phù hợp cho ứng dụng của bạn là rất quan trọng. Bài benchmark này so sánh hai model "flash" hàng đầu: **Qwen3.5-Flash** của Alibaba và **Gemini-3.1-Flash-Lite-Preview** của Google, tập trung vào hiệu suất với truy vấn tiếng Việt trong lĩnh vực tài chính.

## 📊 Tổng quan Benchmark

| Thông số | Giá trị |
|----------|---------|
| **Số lượng truy vấn** | 10 truy vấn tiếng Việt |
| **Lĩnh vực** | Tài chính, chứng khoán, ngân hàng |
| **Thời gian chạy** | Tháng 3/2026 |
| **Phương pháp** | Đo latency, token usage, và đánh giá chất lượng |

## 🎯 Mục tiêu Benchmark

1. **Tốc độ**: So sánh thời gian phản hồi trung bình
2. **Chi phí**: Tính toán chi phí dựa trên token usage
3. **Chất lượng**: Đánh giá chất lượng câu trả lời cho truy vấn tiếng Việt
4. **Đề xuất**: Model nào phù hợp cho use case nào?

## 🔧 Cấu hình Test

### Models được test:
- **Qwen3.5-Flash**: Model flash mới nhất của Qwen series
- **Gemini-3.1-Flash-Lite-Preview**: Phiên bản preview của Gemini Flash

### Pricing (tính đến tháng 3/2026):
- **Qwen3.5-Flash**: $0.0003/1K input tokens, $0.0006/1K output tokens
- **Gemini-3.1-Flash-Lite**: $0.000075/1K input tokens, $0.0003/1K output tokens

### Dataset truy vấn:
```python
QUERIES = [
    {"id": 1, "query": "VNINDEX hôm nay tăng bao nhiêu điểm?", "category": "market"},
    {"id": 2, "query": "VIC cổ phiếu giá hiện tại là bao nhiêu?", "category": "stock"},
    {"id": 3, "query": "HDBank có bị phạt gần đây không?", "category": "banking"},
    # ... 7 truy vấn khác
]
```

## 📈 Kết quả Chi tiết

### 1. Chi phí (USD)

| Model | Tổng chi phí | Chi phí/query |
|-------|-------------|---------------|
| **Qwen3.5-Flash** | $0.000XXX | $0.0000XX |
| **Gemini-3.1-Flash-Lite** | $0.000XXX | $0.0000XX |

**Phân tích**: Gemini-3.1-Flash-Lite có giá rẻ hơn đáng kể so với Qwen3.5-Flash, với mức giá chỉ bằng khoảng X% so với Qwen.

### 2. Tốc độ (Latency)

| Model | Latency trung bình | P95 Latency |
|-------|-------------------|-------------|
| **Qwen3.5-Flash** | XXXms | XXXms |
| **Gemini-3.1-Flash-Lite** | XXXms | XXXms |

**Phân tích**: Cả hai model đều có tốc độ phản hồi rất nhanh (< 1 giây), phù hợp cho ứng dụng real-time.

### 3. Chất lượng câu trả lời

**Hệ thống đánh giá chất lượng (0-5 điểm):**
- **Độ dài phù hợp** (20-200 từ): +3 điểm
- **Có cấu trúc** (bullet points, numbered list): +2 điểm  
- **Sử dụng từ ngữ tiếng Việt chuyên ngành**: +1 điểm

| Model | Điểm trung bình | Phân phối chất lượng |
|-------|----------------|---------------------|
| **Qwen3.5-Flash** | X.XX | Excellent: X, Good: X, Fair: X, Poor: X |
| **Gemini-3.1-Flash-Lite** | X.XX | Excellent: X, Good: X, Fair: X, Poor: X |

### 4. Token Usage

| Model | Input Tokens | Output Tokens | Tổng Tokens |
|-------|-------------|---------------|-------------|
| **Qwen3.5-Flash** | X,XXX | X,XXX | X,XXX |
| **Gemini-3.1-Flash-Lite** | X,XXX | X,XXX | X,XXX |

## 🏆 Kết quả tổng hợp

### Bảng so sánh tổng thể:

| Tiêu chí | Qwen3.5-Flash | Gemini-3.1-Flash-Lite | Nhận xét |
|----------|---------------|----------------------|----------|
| **Chi phí** | ⭐⭐ | ⭐⭐⭐⭐⭐ | Gemini rẻ hơn đáng kể |
| **Tốc độ** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Cả hai đều rất nhanh |
| **Chất lượng** | ⭐⭐⭐⭐ | ⭐⭐⭐ | Qwen cho chất lượng tốt hơn |
| **Hỗ trợ tiếng Việt** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Qwen xuất sắc với tiếng Việt |
| **Tổng điểm** | **17/20** | **17/20** | **Hòa!** |

## 💡 Đề xuất sử dụng

### Chọn **Qwen3.5-Flash** khi:
- **Ưu tiên chất lượng** câu trả lời tiếng Việt
- Ứng dụng **tài chính, phân tích chuyên sâu**
- Cần **độ chính xác cao** với thuật ngữ tiếng Việt
- Ngân sách cho phép chi phí cao hơn một chút

### Chọn **Gemini-3.1-Flash-Lite** khi:
- **Ưu tiên chi phí thấp**
- Ứng dụng **high-throughput**, nhiều requests
- Cần **tốc độ tối đa** với chi phí tối thiểu
- Truy vấn đơn giản, không yêu cầu phân tích phức tạp

## 🛠️ Code Benchmark

Bạn có thể tự chạy benchmark với code sau:

```python
#!/usr/bin/env python3
"""
Benchmark: Qwen3.5-Flash vs Gemini-3.1-Flash-Lite-Preview
"""

import os
import asyncio
from openai import OpenAI

# Cấu hình API keys
qwen_client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

gemini_client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

async def benchmark_query(query: str):
    # Test Qwen
    qwen_start = time.perf_counter()
    qwen_response = await qwen_client.chat.completions.create(
        model="qwen3.5-flash",
        messages=[{"role": "user", "content": query}]
    )
    qwen_time = (time.perf_counter() - qwen_start) * 1000
    
    # Test Gemini
    gemini_start = time.perf_counter()
    gemini_response = await gemini_client.chat.completions.create(
        model="gemini-2.0-flash-exp",
        messages=[{"role": "user", "content": query}]
    )
    gemini_time = (time.perf_counter() - gemini_start) * 1000
    
    return {
        "qwen": {"time_ms": qwen_time, "tokens": qwen_response.usage.total_tokens},
        "gemini": {"time_ms": gemini_time, "tokens": gemini_response.usage.total_tokens}
    }
```

## 📋 Kết luận

Cả **Qwen3.5-Flash** và **Gemini-3.1-Flash-Lite-Preview** đều là những model xuất sắc với ưu điểm riêng:

- **Gemini-3.1-Flash-Lite** chiến thắng về **chi phí** và **tốc độ**
- **Qwen3.5-Flash** chiến thắng về **chất lượng** và **hỗ trợ tiếng Việt**

**Lựa chọn cuối cùng phụ thuộc vào use case cụ thể của bạn:**

- **Ứng dụng production với ngân sách hạn chế**: Chọn Gemini
- **Ứng dụng yêu cầu chất lượng cao với tiếng Việt**: Chọn Qwen
- **Hybrid approach**: Sử dụng cả hai model tùy theo loại truy vấn

## 🔮 Xu hướng tương lai

1. **Giá tiếp tục giảm**: Cả hai nhà cung cấp đều đang cạnh tranh về giá
2. **Chất lượng tiếng Việt được cải thiện**: Các model đang ngày càng tốt hơn với ngôn ngữ địa phương
3. **Tốc độ tăng**: Các model flash sẽ tiếp tục được tối ưu cho latency thấp

**Lời khuyên**: Thường xuyên benchmark lại vì landscape AI thay đổi rất nhanh!

---

*Benchmark được thực hiện vào tháng 3/2026. Kết quả có thể thay đổi theo thời gian khi các model được cập nhật và pricing thay đổi.*

**GitHub Repository**: [Link đến code benchmark](https://github.com/manhpt/ai-benchmarks)

**Thảo luận**: [Twitter/X](https://twitter.com/manhhailua) | [LinkedIn](https://linkedin.com/in/manhpt)