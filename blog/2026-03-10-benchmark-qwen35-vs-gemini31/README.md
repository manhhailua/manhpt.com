# Benchmark: Qwen3.5-Flash vs Gemini-3.1-Flash-Lite-Preview

Bài blog so sánh hiệu năng giữa hai model AI flash hàng đầu cho truy vấn tiếng Việt.

## Nội dung

- Benchmark chi tiết về tốc độ, chi phí và chất lượng
- So sánh Qwen3.5-Flash vs Gemini-3.1-Flash-Lite-Preview
- Đề xuất sử dụng cho từng use case
- Code benchmark có thể tái sử dụng

## Tags

- `ai` - Trí tuệ nhân tạo
- `benchmark` - So sánh hiệu năng
- `qwen` - Model Qwen của Alibaba
- `gemini` - Model Gemini của Google
- `vietnamese` - Ứng dụng tiếng Việt
- `llm` - Large Language Models

## File liên quan

- `index.md` - Bài blog chính
- Code benchmark: `../../../../benchmarks/simple_benchmark.py`

## Chạy benchmark

```bash
# Cài đặt dependencies
pip install openai

# Set API keys
export DASHSCOPE_API_KEY="your-key"
export GEMINI_API_KEY="your-key"

# Chạy benchmark
python ../../../../benchmarks/simple_benchmark.py
```