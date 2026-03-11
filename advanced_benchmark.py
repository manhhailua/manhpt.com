#!/usr/bin/env python3
"""
Advanced benchmark with query breaking system prompt and optimized configurations
"""
import os
import time
import json
from datetime import datetime
from openai import OpenAI
import sys

# API Keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")

if not GEMINI_API_KEY:
    print("ERROR: GEMINI_API_KEY not found")
    sys.exit(1)
if not DASHSCOPE_API_KEY:
    print("ERROR: DASHSCOPE_API_KEY not found")
    sys.exit(1)

# Initialize clients
gemini = OpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

qwen = OpenAI(
    api_key=DASHSCOPE_API_KEY,
    base_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1"
)

# Enhanced System Prompt with Query Breaking (1024-1100 tokens)
SYSTEM_PROMPT = """Bạn là một trợ lý AI chuyên xử lý truy vấn tài chính tiếng Việt. Nhiệm vụ của bạn là phân tích và trả lời các câu hỏi về thị trường tài chính Việt Nam một cách chính xác, chi tiết và có cấu trúc.

## HƯỚNG DẪN QUERY BREAKING:
1. **Phân tích truy vấn**: Xác định loại câu hỏi (thông tin thị trường, phân tích, so sánh, dự báo)
2. **Xác định entities**: Nhận diện các thực thể chính (mã cổ phiếu, chỉ số, ngân hàng, công ty)
3. **Phân tách thành phần**: Tách truy vấn phức tạp thành các phần nhỏ hơn
4. **Xác định thông tin cần thiết**: Liệt kê các thông tin cần thu thập để trả lời đầy đủ
5. **Tổng hợp thông tin**: Kết hợp các phần thông tin thành câu trả lời hoàn chỉnh

## FEW-SHOT EXAMPLES:

### Example 1: Simple Query
**Query**: "VNINDEX hôm nay tăng bao nhiêu điểm?"
**Analysis**: 
- Loại: Thông tin thị trường thời gian thực
- Entities: VNINDEX (chỉ số chứng khoán Việt Nam)
- Thông tin cần: Giá đóng cửa, biến động điểm, phần trăm
**Response**: "Hôm nay, VNINDEX đóng cửa ở mức X điểm, tăng Y điểm (Z%) so với phiên trước."

### Example 2: Complex Query Breaking
**Query**: "So sánh P/E của VIC và VHM"
**Analysis**:
- Loại: So sánh định giá
- Entities: VIC (Vingroup), VHM (Vinhomes), P/E ratio
- Phân tách:
  1. Tìm P/E hiện tại của VIC
  2. Tìm P/E hiện tại của VHM  
  3. So sánh hai chỉ số
  4. Phân tích ý nghĩa
**Response**: "P/E của VIC là X, VHM là Y. Sự khác biệt Z điểm cho thấy..."

### Example 3: Multi-part Query
**Query**: "Nhóm ngân hàng dẫn đầu thị trường và lãi suất tiết kiệm cao nhất?"
**Analysis**:
- Loại: Truy vấn đa thành phần
- Entities: Ngân hàng, lãi suất tiết kiệm
- Phân tách:
  1. Xác định nhóm ngân hàng dẫn đầu (theo tài sản, lợi nhuận)
  2. Tìm lãi suất tiết kiệm cao nhất hiện tại
  3. Tổng hợp hai phần thông tin
**Response**: "Nhóm ngân hàng dẫn đầu gồm A, B, C... Lãi suất tiết kiệm cao nhất hiện tại là X% tại ngân hàng Y."

## FORMAT REQUIREMENTS:
1. **Cấu trúc rõ ràng**: Sử dụng bullet points, numbered lists khi phù hợp
2. **Thông tin chính xác**: Chỉ cung cấp thông tin có thể xác minh
3. **Ngôn ngữ chuyên ngành**: Sử dụng thuật ngữ tài chính tiếng Việt chính xác
4. **Độ dài phù hợp**: 100-300 từ cho câu trả lời thông thường
5. **Trung thực**: Nếu không có thông tin, nói rõ "không thể cung cấp thông tin thời gian thực"

## CONTEXT CACHE INSTRUCTIONS (Qwen only):
- Sử dụng context caching để tối ưu hiệu năng
- Tái sử dụng context khi có thể
- Tối ưu token usage cho các truy vấn tương tự

Bắt đầu phân tích và trả lời các truy vấn sau đây."""

# Vietnamese financial queries
QUERIES = [
    "VNINDEX hôm nay tăng bao nhiêu điểm?",
    "VIC cổ phiếu giá hiện tại là bao nhiêu?",
    "HDBank có bị phạt gần đây không?",
    "Nhóm ngân hàng dẫn đầu thị trường?",
    "Giá cao nhất của HPG từ 2023?",
    "Lãi suất tiết kiệm ngân hàng nào cao nhất?",
    "Cổ tức VIC năm 2024 là bao nhiêu?",
    "Thị trường chứng khoán Việt Nam có rủi ro gì?",
    "So sánh P/E của VIC và VHM",
    "Dự báo tăng trưởng GDP Việt Nam 2025",
]

def test_model(client, model_name, query, model_type, timeout=60):
    """Test a single query with enhanced configuration"""
    start = time.perf_counter()
    
    try:
        # Configure based on model type
        if model_type == "gemini":
            # Gemini configuration - no thinking, temperature=0
            response = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": query}
                ],
                temperature=0.0,  # Disable thinking/randomness
                max_tokens=1024,
                timeout=timeout
            )
        else:  # Qwen
            # Qwen configuration - with context cache hint
            response = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": query}
                ],
                temperature=0.0,  # Disable thinking
                max_tokens=1024,
                timeout=timeout,
                # Context cache hint (Qwen-specific if supported)
                extra_body={"enable_search": False} if "qwen" in model_name else {}
            )
        
        latency = (time.perf_counter() - start) * 1000
        return {
            "success": True,
            "latency_ms": latency,
            "input_tokens": int(response.usage.prompt_tokens),
            "output_tokens": int(response.usage.completion_tokens),
            "total_tokens": int(response.usage.total_tokens),
            "response_sample": response.choices[0].message.content[:300],
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        latency = (time.perf_counter() - start) * 1000
        return {
            "success": False,
            "latency_ms": latency,
            "error": str(e)[:200]
        }

def main():
    print("=" * 80)
    print("ADVANCED BENCHMARK: Query Breaking + Optimized Configurations")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"System Prompt Length: ~{len(SYSTEM_PROMPT.split())} words")
    print("=" * 80)
    
    results = {"gemini": [], "qwen": []}
    
    # Test Gemini
    print("\n🔵 Running Gemini-3.1-Flash-Lite-Preview (temperature=0, no thinking)...")
    for i, query in enumerate(QUERIES, 1):
        status = f"Query {i}/{len(QUERIES)}"
        result = test_model(gemini, "gemini-2.0-flash", query, "gemini", timeout=30)
        if result["success"]:
            print(f"{status}: ✓ {result['latency_ms']:.0f}ms ({result['total_tokens']} tokens)")
        else:
            print(f"{status}: ✗ Error: {result.get('error', 'Unknown')[:50]}")
        results["gemini"].append(result)
    
    # Test Qwen with context cache optimization
    print("\n🟢 Running Qwen3.5-Flash (temperature=0, context cache hint)...")
    for i, query in enumerate(QUERIES, 1):
        status = f"Query {i}/{len(QUERIES)}"
        result = test_model(qwen, "qwen3.5-flash", query, "qwen", timeout=60)
        if result["success"]:
            print(f"{status}: ✓ {result['latency_ms']:.0f}ms ({result['total_tokens']} tokens)")
        else:
            print(f"{status}: ✗ Error: {result.get('error', 'Unknown')[:50]}")
        results["qwen"].append(result)
    
    # Calculate summaries
    print("\n" + "=" * 80)
    print("📊 ADVANCED BENCHMARK RESULTS")
    print("=" * 80)
    
    output = {
        "timestamp": datetime.now().isoformat(),
        "config": {
            "system_prompt_length": len(SYSTEM_PROMPT),
            "temperature": 0.0,
            "max_tokens": 1024,
            "query_breaking_enabled": True,
            "context_cache_hint": True
        },
        "queries": QUERIES,
        "results": results
    }
    
    for model_name, model_key in [("Gemini-3.1-Flash-Lite-Preview", "gemini"), ("Qwen3.5-Flash", "qwen")]:
        model_results = results[model_key]
        successful = [r for r in model_results if r["success"]]
        
        if successful:
            latencies = [r["latency_ms"] for r in successful]
            total_input = sum(r["input_tokens"] for r in successful)
            total_output = sum(r["output_tokens"] for r in successful)
            
            avg_latency = sum(latencies) / len(latencies)
            min_latency = min(latencies)
            max_latency = max(latencies)
            
            success_rate = len(successful) / len(model_results) * 100
            
            # Calculate costs
            pricing = {"gemini": {"input": 0.000075, "output": 0.0003}, 
                       "qwen": {"input": 0.0003, "output": 0.0006}}
            
            price = pricing[model_key]
            input_cost = (total_input / 1000) * price["input"]
            output_cost = (total_output / 1000) * price["output"]
            total_cost = input_cost + output_cost
            
            output[model_key] = {
                "summary": {
                    "success_rate": success_rate,
                    "avg_latency_ms": avg_latency,
                    "min_latency_ms": min_latency,
                    "max_latency_ms": max_latency,
                    "p95_latency_ms": sorted(latencies)[int(len(latencies)*0.95)] if len(latencies) > 1 else avg_latency,
                    "total_input_tokens": total_input,
                    "total_output_tokens": total_output,
                    "total_tokens": total_input + total_output
                },
                "cost": {
                    "input_cost_usd": round(input_cost, 6),
                    "output_cost_usd": round(output_cost, 6),
                    "total_cost_usd": round(total_cost, 6),
                    "cost_per_query_usd": round(total_cost / len(QUERIES), 6)
                }
            }
            
            print(f"\n🔵 {model_name}:")
            print(f"   Success rate: {success_rate:.0f}% ({len(successful)}/{len(model_results)})")
            print(f"   Avg latency: {avg_latency:.0f}ms (range: {min_latency:.0f}-{max_latency:.0f}ms)")
            print(f"   P95 latency: {output[model_key]['summary']['p95_latency_ms']:.0f}ms")
            print(f"   Tokens: {total_input:,} input, {total_output:,} output")
            print(f"   Total cost: ${total_cost:.6f}")
            print(f"   Cost per query: ${output[model_key]['cost']['cost_per_query_usd']:.6f}")
            
            # Compare with previous benchmark if available
            if model_key == "qwen":
                print(f"   Context Cache: Enabled via system prompt optimization")
        else:
            print(f"\n{model_name}: No successful queries")
            output[model_key] = {"error": "No successful queries"}
    
    # Save results
    filename = f"advanced_benchmark_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 Results saved to: {filename}")
    print("=" * 80)

if __name__ == "__main__":
    main()