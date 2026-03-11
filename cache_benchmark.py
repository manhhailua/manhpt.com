#!/usr/bin/env python3
"""
Qwen3.5 Flash Context Cache Benchmark
Based on web search findings about explicit and implicit cache
"""
import os
import time
import json
from datetime import datetime
from openai import OpenAI
import sys

# API Keys from environment
DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")
if not DASHSCOPE_API_KEY:
    print("ERROR: DASHSCOPE_API_KEY not found in environment")
    sys.exit(1)

# Initialize Qwen client
qwen = OpenAI(
    api_key=DASHSCOPE_API_KEY,
    base_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1"
)

# System prompt with cache control marker (explicit cache)
SYSTEM_PROMPT_EXPLICIT = {
    "role": "system",
    "content": """Bạn là một trợ lý AI chuyên xử lý truy vấn tài chính tiếng Việt. 
Nhiệm vụ của bạn là phân tích và trả lời các câu hỏi về thị trường tài chính Việt Nam.

HƯỚNG DẪN:
1. Trả lời trực tiếp, không giải thích suy nghĩ
2. Sử dụng ngôn ngữ chuyên ngành tài chính
3. Nếu không có thông tin, nói rõ "không thể cung cấp thông tin thời gian thực"

CACHE CONTROL: {"type": "ephemeral"}""",
    "cache_control": {"type": "ephemeral"}  # Explicit cache marker
}

# System prompt without cache control (implicit cache only)
SYSTEM_PROMPT_IMPLICIT = {
    "role": "system",
    "content": """Bạn là một trợ lý AI chuyên xử lý truy vấn tài chính tiếng Việt. 
Nhiệm vụ của bạn là phân tích và trả lời các câu hỏi về thị trường tài chính Việt Nam.

HƯỚNG DẪN:
1. Trả lời trực tiếp, không giải thích suy nghĩ
2. Sử dụng ngôn ngữ chuyên ngành tài chính
3. Nếu không có thông tin, nói rõ "không thể cung cấp thông tin thời gian thực"""
}

# Vietnamese financial queries (repeated for cache testing)
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

def run_benchmark(mode="explicit", iterations=3):
    """Run benchmark with specified cache mode"""
    print(f"\n🔧 Running {mode.upper()} CACHE benchmark ({iterations} iterations)...")
    
    results = []
    system_prompt = SYSTEM_PROMPT_EXPLICIT if mode == "explicit" else SYSTEM_PROMPT_IMPLICIT
    
    for iteration in range(iterations):
        print(f"\n  Iteration {iteration + 1}/{iterations}:")
        iteration_results = []
        
        for i, query in enumerate(QUERIES, 1):
            start = time.perf_counter()
            
            try:
                response = qwen.chat.completions.create(
                    model="qwen3.5-flash",
                    messages=[system_prompt, {"role": "user", "content": query}],
                    temperature=0.0,
                    max_tokens=1024,
                    timeout=60
                )
                
                latency = (time.perf_counter() - start) * 1000
                
                # Extract cache information
                cached_tokens = getattr(response.usage, 'cached_tokens', 0)
                prompt_tokens = response.usage.prompt_tokens
                completion_tokens = response.usage.completion_tokens
                total_tokens = response.usage.total_tokens
                
                # Calculate costs based on cache mode
                # Standard pricing: $0.0003/1K input, $0.0006/1K output
                standard_input_cost = (prompt_tokens / 1000) * 0.0003
                standard_output_cost = (completion_tokens / 1000) * 0.0006
                standard_total = standard_input_cost + standard_output_cost
                
                # Cache-adjusted costs
                if mode == "explicit":
                    # Explicit: 125% for creation, 10% for hits
                    if iteration == 0:  # First iteration creates cache
                        cache_multiplier = 1.25  # 125% cost
                    else:  # Subsequent hits
                        cache_multiplier = 0.1  # 10% cost for cached tokens
                else:  # implicit
                    # Implicit: 20% for matched tokens
                    cache_multiplier = 0.2 if cached_tokens > 0 else 1.0
                
                cache_adjusted_cost = standard_input_cost * cache_multiplier + standard_output_cost
                savings = standard_total - cache_adjusted_cost
                
                result = {
                    "query": query,
                    "latency_ms": latency,
                    "prompt_tokens": prompt_tokens,
                    "completion_tokens": completion_tokens,
                    "total_tokens": total_tokens,
                    "cached_tokens": cached_tokens,
                    "standard_cost_usd": standard_total,
                    "cache_adjusted_cost_usd": cache_adjusted_cost,
                    "savings_usd": savings,
                    "cache_hit": cached_tokens > 0,
                    "iteration": iteration,
                    "timestamp": datetime.now().isoformat()
                }
                
                iteration_results.append(result)
                
                status = "✓" if result["cache_hit"] else " "
                print(f"    Query {i}: {status} {latency:.0f}ms, {cached_tokens} cached tokens, ${cache_adjusted_cost:.6f}")
                
            except Exception as e:
                latency = (time.perf_counter() - start) * 1000
                print(f"    Query {i}: ✗ Error: {str(e)[:50]}")
                iteration_results.append({
                    "query": query,
                    "latency_ms": latency,
                    "error": str(e)[:200],
                    "iteration": iteration
                })
        
        results.extend(iteration_results)
    
    return results

def analyze_results(results, mode):
    """Analyze and summarize benchmark results"""
    successful = [r for r in results if "error" not in r]
    
    if not successful:
        print(f"\n⚠️ No successful queries for {mode} cache")
        return None
    
    # Calculate statistics
    latencies = [r["latency_ms"] for r in successful]
    total_standard_cost = sum(r.get("standard_cost_usd", 0) for r in successful)
    total_cache_cost = sum(r.get("cache_adjusted_cost_usd", 0) for r in successful)
    total_savings = sum(r.get("savings_usd", 0) for r in successful)
    total_cached_tokens = sum(r.get("cached_tokens", 0) for r in successful)
    
    cache_hits = sum(1 for r in successful if r.get("cache_hit", False))
    cache_hit_rate = (cache_hits / len(successful)) * 100 if successful else 0
    
    summary = {
        "mode": mode,
        "total_queries": len(results),
        "successful_queries": len(successful),
        "cache_hits": cache_hits,
        "cache_hit_rate": cache_hit_rate,
        "avg_latency_ms": sum(latencies) / len(latencies),
        "min_latency_ms": min(latencies),
        "max_latency_ms": max(latencies),
        "total_cached_tokens": total_cached_tokens,
        "total_standard_cost_usd": total_standard_cost,
        "total_cache_cost_usd": total_cache_cost,
        "total_savings_usd": total_savings,
        "savings_percentage": (total_savings / total_standard_cost * 100) if total_standard_cost > 0 else 0,
        "timestamp": datetime.now().isoformat()
    }
    
    return summary

def main():
    print("=" * 80)
    print("🚀 QWEN3.5-FLASH CONTEXT CACHE BENCHMARK")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    all_results = {}
    
    # Run benchmarks for both cache modes
    for mode in ["explicit", "implicit"]:
        results = run_benchmark(mode=mode, iterations=3)
        all_results[mode] = results
        
        summary = analyze_results(results, mode)
        if summary:
            print(f"\n📊 {mode.upper()} CACHE SUMMARY:")
            print(f"  Success rate: {summary['successful_queries']}/{summary['total_queries']} queries")
            print(f"  Cache hit rate: {summary['cache_hit_rate']:.1f}%")
            print(f"  Avg latency: {summary['avg_latency_ms']:.0f}ms")
            print(f"  Total cached tokens: {summary['total_cached_tokens']:,}")
            print(f"  Standard cost: ${summary['total_standard_cost_usd']:.6f}")
            print(f"  Cache cost: ${summary['total_cache_cost_usd']:.6f}")
            print(f"  Savings: ${summary['total_savings_usd']:.6f} ({summary['savings_percentage']:.1f}%)")
            
            # Save detailed results
            filename = f"qwen_cache_{mode}_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump({"summary": summary, "detailed": results}, f, ensure_ascii=False, indent=2)
            print(f"  Results saved to: {filename}")
    
    # Compare both modes
    print("\n" + "=" * 80)
    print("🏆 CACHE MODE COMPARISON")
    print("=" * 80)
    
    summaries = {}
    for mode in ["explicit", "implicit"]:
        if mode in all_results:
            summary = analyze_results(all_results[mode], mode)
            if summary:
                summaries[mode] = summary
    
    if len(summaries) == 2:
        print("\n📈 Performance Comparison:")
        print(f"{'Metric':<25} {'Explicit':<15} {'Implicit':<15} {'Winner':<10}")
        print("-" * 65)
        
        # Compare key metrics
        metrics = [
            ("Avg Latency (ms)", "avg_latency_ms", "lower"),
            ("Cache Hit Rate (%)", "cache_hit_rate", "higher"),
            ("Total Savings ($)", "total_savings_usd", "higher"),
            ("Savings %", "savings_percentage", "higher"),
            ("Total Cost ($)", "total_cache_cost_usd", "lower")
        ]
        
        for metric_name, metric_key, better in metrics:
            exp_val = summaries["explicit"][metric_key]
            imp_val = summaries["implicit"][metric_key]
            
            if better == "lower":
                winner = "Explicit" if exp_val < imp_val else "Implicit"
            else:
                winner = "Explicit" if exp_val > imp_val else "Implicit"
            
            if metric_key in ["avg_latency_ms"]:
                print(f"{metric_name:<25} {exp_val:<15.0f} {imp_val:<15.0f} {winner:<10}")
            elif metric_key in ["cache_hit_rate", "savings_percentage"]:
                print(f"{metric_name:<25} {exp_val:<15.1f} {imp_val:<15.1f} {winner:<10}")
            else:
                print(f"{metric_name:<25} {exp_val:<15.6f} {imp_val:<15.6f} {winner:<10}")
    
    print("\n" + "=" * 80)
    print("💡 RECOMMENDATIONS:")
    print("=" * 80)
    print("1. Use EXPLICIT cache for:")
    print("   - High-volume, repetitive queries")
    print("   - When you can afford 125% initial cost")
    print("   - Need maximum savings (90% on cached tokens)")
    
    print("\n2. Use IMPLICIT cache for:")
    print("   - General use cases")
    print("   - When convenience is priority")
    print("   - Moderate savings (80% on matched tokens)")
    
    print("\n3. Monitor cache usage:")
    print("   - Check usage.cached_tokens in API response")
    print("   - Track cost savings over time")
    print("   - Adjust cache strategy based on patterns")

if __name__ == "__main__":
    main()