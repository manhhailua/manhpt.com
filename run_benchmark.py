#!/usr/bin/env python3
"""
Full benchmark with proper timeout handling for Qwen's slow responses
"""
import os
import time
import json
from datetime import datetime
from openai import OpenAI
import sys

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")

gemini = OpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

qwen = OpenAI(
    api_key=DASHSCOPE_API_KEY,
    base_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1"
)

# Vietnamese financial queries from the blog
QUERIES = [
    {"id": 1, "query": "VNINDEX hôm nay tăng bao nhiêu điểm?", "category": "market"},
    {"id": 2, "query": "VIC cổ phiếu giá hiện tại là bao nhiêu?", "category": "stock"},
    {"id": 3, "query": "HDBank có bị phạt gần đây không?", "category": "banking"},
    {"id": 4, "query": "Nhóm ngân hàng dẫn đầu thị trường?", "category": "banking"},
    {"id": 5, "query": "Giá cao nhất của HPG từ 2023?", "category": "stock"},
    {"id": 6, "query": "Lãi suất tiết kiệm ngân hàng nào cao nhất?", "category": "banking"},
    {"id": 7, "query": "Cổ tức VIC năm 2024 là bao nhiêu?", "category": "dividend"},
    {"id": 8, "query": "Thị trường chứng khoán Việt Nam có rủi ro gì?", "category": "analysis"},
    {"id": 9, "query": "So sánh P/E của VIC và VHM", "category": "valuation"},
    {"id": 10, "query": "Dự báo tăng trưởng GDP Việt Nam 2025", "category": "macro"},
]

def test_model(client, model_name, query_text, query_id, timeout=60):
    """Test a single query with configurable timeout"""
    start = time.perf_counter()
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": query_text}],
            temperature=0.1,
            timeout=timeout
        )
        
        latency = (time.perf_counter() - start) * 1000
        return {
            "success": True,
            "query_id": query_id,
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
            "query_id": query_id,
            "latency_ms": latency,
            "error": str(e)[:200]
        }

def main():
    print("=" * 80)
    print("BENCHMARK: Qwen3.5-Flash vs Gemini-3.1-Flash-Lite-Preview")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Queries: {len(QUERIES)} Vietnamese financial questions")
    print("=" * 80)
    
    results = {"gemini": [], "qwen": []}
    
    # Test Gemini first (fast)
    print("\n🔵 Running Gemini-3.1-Flash-Lite-Preview (10 queries)...")
    for i, q in enumerate(QUERIES, 1):
        status = f"Query {i}/{len(QUERIES)}"
        result = test_model(gemini, "gemini-2.0-flash", q["query"], q["id"], timeout=30)
        if result["success"]:
            print(f"{status}: ✓ {result['latency_ms']:.0f}ms ({result['total_tokens']} tokens)")
        else:
            print(f"{status}: ✗ Error: {result.get('error', 'Unknown')[:50]}")
        results["gemini"].append(result)
    
    # Test Qwen (slow)
    print("\n🟢 Running Qwen3.5-Flash (10 queries, ~60s timeout each)...")
    for i, q in enumerate(QUERIES, 1):
        status = f"Query {i}/{len(QUERIES)}"
        result = test_model(qwen, "qwen3.5-flash", q["query"], q["id"], timeout=60)
        if result["success"]:
            print(f"{status}: ✓ {result['latency_ms']:.0f}ms ({result['total_tokens']} tokens)")
        else:
            print(f"{status}: ✗ Error: {result.get('error', 'Unknown')[:50]}")
        results["qwen"].append(result)
    
    # Calculate summaries
    print("\n" + "=" * 80)
    print("📊 RESULTS SUMMARY")
    print("=" * 80)
    
    output = {
        "timestamp": datetime.now().isoformat(),
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
        else:
            print(f"\n{model_name}: No successful queries")
            output[model_key] = {"error": "No successful queries"}
    
    # Save results
    filename = f"benchmark_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 Results saved to: {filename}")
    print("=" * 80)

if __name__ == "__main__":
    main()