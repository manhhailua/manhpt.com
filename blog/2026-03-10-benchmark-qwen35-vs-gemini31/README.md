# Benchmark: Qwen3.5-Flash vs Gemini-3.1-Flash-Lite-Preview (Real Results)

Bài blog so sánh hiệu năng thực tế giữa hai model AI flash hàng đầu cho truy vấn tiếng Việt tài chính.

## Kết quả chính (Cập nhật 11/03/2026)

### Gemini-3.1-Flash-Lite-Preview ✅
- **Chi phí**: $0.001347 cho 10 queries = **$0.000135/query**
- **Tốc độ**: Trung bình **3.8s** (range: 1.3s - 8.8s)
- **Success rate**: 100% (10/10 queries)
- **Tokens**: 113 input, 4,461 output

### Qwen3.5-Flash ✅
- **Chi phí**: $0.014752 cho 10 queries = **$0.001475/query**
- **Tốc độ**: Trung bình **19.0s** (range: 11.2s - 30.5s)
- **Success rate**: 100% (10/10 queries)
- **Tokens**: 211 input, 24,481 output

## 🏆 Winner: Gemini-3.1-Flash-Lite-Preview

Gemini chiến thắng cả về **chi phí** (11x rẻ hơn) lẫn **tốc độ** (5x nhanh hơn) trong benchmark thực tế.

## Tags

- `ai` - Trí tuệ nhân tạo
- `benchmark` - So sánh hiệu năng
- `qwen` - Model Qwen của Alibaba
- `gemini` - Model Gemini của Google
- `vietnamese` - Ứng dụng tiếng Việt
- `llm` - Large Language Models

## File liên quan

- `index.md` - Bài blog chính (dữ liệu thực tế)
- Code benchmark: [run_benchmark.py](../../../../run_benchmark.py)

## Chạy benchmark của bạn

```bash
# Cài đặt dependencies
pip install openai

# Set API keys
export GEMINI_API_KEY="your-key"
export DASHSCOPE_API_KEY="your-key"

# Chạy benchmark
python ../../../../run_benchmark.py
```

## Advanced Benchmark Results (11/03/2026)

Với system prompt query breaking và optimization:

### Gemini-3.1-Flash-Lite-Preview (Optimized):
- **Cost**: $0.001987 total ($0.000199/query)
- **Speed**: Avg 4.0s
- **Tokens**: 7,613 input, 4,719 output

### Qwen3.5-Flash (Optimized):
- **Cost**: $0.007867 total ($0.000787/query) - **47% cheaper** vs baseline
- **Speed**: Avg 7.6s - **60% faster** vs baseline
- **Tokens**: 7,671 input, 9,277 output

**Optimization improvements**: System prompt + context cache hint giúp Qwen cải thiện đáng kể performance.

## Key Findings

1. **Cost Efficiency**: Gemini 4x cheaper than optimized Qwen (11x vs baseline)
2. **Speed**: Gemini ~2x faster than optimized Qwen (5x vs baseline)
3. **Prompt Optimization**: System prompts có thể cải thiện Qwen performance 60%
4. **Reliability**: Both models achieved 100% success rate in all tests

## Recommendation

Start with **Gemini-3.1-Flash-Lite-Preview** for most use cases due to better cost-performance ratio. Use Qwen3.5-Flash when you need very verbose responses and can afford the premium cost.

---

*Last updated: 2026-03-11 | All results are REAL (no simulation)*
