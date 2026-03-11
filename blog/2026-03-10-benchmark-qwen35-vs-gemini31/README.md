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

## Key Findings

1. **Cost Efficiency**: Gemini 11x cheaper than Qwen
2. **Speed**: Gemini ~5x faster average response
3. **Token Usage**: Gemini uses 5.5x less output tokens
4. **Reliability**: Both models achieved 100% success rate

## Recommendation

Start with **Gemini-3.1-Flash-Lite-Preview** for most use cases due to better cost-performance ratio. Use Qwen3.5-Flash when you need very verbose responses and can afford the premium cost.

---

*Last updated: 2026-03-11 | All results are REAL (no simulation)*
