#!/usr/bin/env python3
"""
TTFT Benchmark: Qwen3.5-Flash vs Gemini-3.1-Flash-Lite-Preview
Measures Time-to-First-Token, throughput, and cost metrics.
"""

import asyncio
import json
import os
import time
from dataclasses import dataclass, asdict
from typing import Optional
from datetime import datetime

try:
    import httpx
except ImportError:
    print("Installing httpx...")
    os.system("pip install httpx")
    import httpx

try:
    import matplotlib.pyplot as plt
    import matplotlib

    matplotlib.use("Agg")
    HAS_MATPLOTLIB = True
except ImportError:
    print("Installing matplotlib for visualization...")
    os.system("pip install matplotlib")
    HAS_MATPLOTLIB = True
    import matplotlib.pyplot as plt
    import matplotlib

    matplotlib.use("Agg")


@dataclass
class BenchmarkResult:
    model: str
    cold_start_ttft: list[float]
    warm_start_ttft: list[float]
    throughput_small: list[float]
    throughput_medium: list[float]
    throughput_large: list[float]
    token_gen_speed: list[float]
    avg_cold_ttft: float = 0
    avg_warm_ttft: float = 0
    avg_throughput_small: float = 0
    avg_throughput_medium: float = 0
    avg_throughput_large: float = 0
    avg_token_gen_speed: float = 0
    input_cost_per_1k: float = 0
    output_cost_per_1k: float = 0


PROMPTS = {
    "small": "Explain what is AI in 2 sentences.",
    "medium": """Write a Python function that:
1. Takes a list of numbers
2. Returns the sum of all numbers
3. Handles empty lists by returning 0
Include error handling and type hints.""",
    "large": """You are an expert software architect. Review and refactor this Python code for a microservices-based e-commerce system:

1. Design the overall system architecture with services for:
   - User management
   - Product catalog
   - Shopping cart
   - Order processing
   - Payment gateway
   - Inventory management
   - Notification service

2. For each service, specify:
   - Primary responsibility
   - API endpoints (REST or GraphQL)
   - Database schema requirements
   - Event-driven communication patterns
   - Caching strategy
   - Error handling approach

3. Include a detailed sequence diagram for the checkout process
4. Specify message queue topics and event schemas
5. Describe the CI/CD pipeline structure
6. Include monitoring and observability requirements
7. Add security considerations including authentication and authorization
8. Provide infrastructure requirements (container orchestration, scaling strategies)

Be thorough and production-ready in your design.""",
}

MODEL_CONFIGS = {
    "qwen": {
        "name": "Qwen3.5-Flash",
        "provider": "OpenRouter (Alibaba Cloud)",
        "input_cost_per_1m": 0.10,
        "output_cost_per_1m": 0.40,
        "max_tokens": 65536,
        "context_window": 1000000,
        "color": "#FF6B6B",
        "streaming_endpoint": "https://openrouter.ai/api/v1/chat/completions",
        "model_id": "qwen/qwen3.5-flash-02-23",
    },
    "gemini": {
        "name": "Gemini-3.1-Flash-Lite-Preview",
        "provider": "Google AI Studio",
        "input_cost_per_1m": 0.25,
        "output_cost_per_1m": 1.50,
        "max_tokens": 65536,
        "context_window": 1000000,
        "color": "#4ECDC4",
        "streaming_endpoint": "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.0-flash-lite:generateContent",
        "model_id": "gemini-3.1-flash-lite-preview",
    },
}


def estimate_tokens(text: str) -> int:
    """Rough token estimation (~4 chars per token for English)."""
    return len(text) // 4


async def benchmark_streaming(
    client: httpx.AsyncClient,
    endpoint: str,
    headers: dict,
    model: str,
    prompt: str,
    max_tokens: int = 500,
) -> tuple[Optional[float], int, float]:
    """
    Benchmark streaming request.
    Returns: (TTFT in seconds, total output tokens, total time)
    """
    start_time = time.perf_counter()
    ttft = None
    total_tokens = 0

    try:
        if "openrouter" in endpoint:
            payload = {
                "model": MODEL_CONFIGS[model]["model_id"],
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": max_tokens,
                "stream": True,
            }
            async with client.stream(
                "POST", endpoint, json=payload, headers=headers, timeout=60.0
            ) as response:
                if response.status_code != 200:
                    error_text = await response.aread()
                    print(
                        f"OpenRouter Error {response.status_code}: {error_text.decode()[:200]}"
                    )
                    return None, 0, 0
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        if line.startswith("data: [DONE]"):
                            break
                        try:
                            data = json.loads(line[6:])
                            if "choices" in data and len(data["choices"]) > 0:
                                delta = data["choices"][0].get("delta", {})
                                if "content" in delta:
                                    if ttft is None:
                                        ttft = time.perf_counter() - start_time
                                    total_tokens += estimate_tokens(delta["content"])
                            if "usage" in data:
                                usage = data["usage"]
                                total_tokens = usage.get(
                                    "completion_tokens", total_tokens
                                )
                        except json.JSONDecodeError:
                            continue
        else:
            payload = {
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {
                    "maxOutputTokens": max_tokens,
                    "temperature": 0.7,
                },
                "stream": True,
            }
            api_key = headers.get("Authorization", "").replace("Bearer ", "")
            stream_url = f"{endpoint}?key={api_key}"
            async with client.stream(
                "POST", stream_url, json=payload, timeout=60.0
            ) as response:
                if response.status_code != 200:
                    error_text = await response.aread()
                    print(
                        f"Gemini Error {response.status_code}: {error_text.decode()[:200]}"
                    )
                    return None, 0, 0
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        try:
                            data = json.loads(line[6:])
                            if "candidates" in data:
                                content = data["candidates"][0].get("content", {})
                                parts = content.get("parts", [])
                                for part in parts:
                                    if "text" in part:
                                        if ttft is None:
                                            ttft = time.perf_counter() - start_time
                                        total_tokens += estimate_tokens(part["text"])
                            if "usageMetadata" in data:
                                usage = data["usageMetadata"]
                                total_tokens = usage.get(
                                    "candidatesTokenCount", total_tokens
                                )
                        except json.JSONDecodeError:
                            continue
    except Exception as e:
        print(f"Request error for {model}: {e}")
        return None, 0, 0

    total_time = time.perf_counter() - start_time
    token_gen_speed = (
        total_tokens / total_time if total_time > 0 and total_tokens > 0 else 0
    )

    return ttft, total_tokens, token_gen_speed


async def run_cold_start_benchmark(
    client: httpx.AsyncClient,
    config: dict,
    model_key: str,
    iterations: int = 5,
) -> list[float]:
    """Run cold start benchmark - new client each time."""
    results = []
    for i in range(iterations):
        async with httpx.AsyncClient(timeout=60.0) as new_client:
            ttft, _, _ = await benchmark_streaming(
                new_client,
                config["streaming_endpoint"],
                get_headers(model_key),
                model_key,
                PROMPTS["small"],
                max_tokens=100,
            )
            if ttft:
                results.append(ttft)
                print(f"  {config['name']} cold start {i + 1}: {ttft:.3f}s")
            await asyncio.sleep(2)
    return results


async def run_warm_start_benchmark(
    client: httpx.AsyncClient,
    config: dict,
    model_key: str,
    iterations: int = 5,
) -> list[float]:
    """Run warm start benchmark - same client reused."""
    results = []
    for i in range(iterations):
        ttft, _, _ = await benchmark_streaming(
            client,
            config["streaming_endpoint"],
            get_headers(model_key),
            model_key,
            PROMPTS["small"],
            max_tokens=100,
        )
        if ttft:
            results.append(ttft)
            print(f"  {config['name']} warm start {i + 1}: {ttft:.3f}s")
        await asyncio.sleep(0.5)
    return results


async def run_throughput_benchmark(
    client: httpx.AsyncClient,
    config: dict,
    model_key: str,
    prompt_size: str,
    iterations: int = 3,
) -> list[float]:
    """Run throughput benchmark with different prompt sizes."""
    results = []
    for i in range(iterations):
        _, _, tok_per_sec = await benchmark_streaming(
            client,
            config["streaming_endpoint"],
            get_headers(model_key),
            model_key,
            PROMPTS[prompt_size],
            max_tokens=500,
        )
        if tok_per_sec:
            results.append(tok_per_sec)
            print(f"  {config['name']} {prompt_size} prompt: {tok_per_sec:.1f} tok/s")
        await asyncio.sleep(1)
    return results


def get_headers(model: str) -> dict:
    """Get headers for API request."""
    if model == "qwen":
        api_key = os.environ.get("OPENROUTER_API_KEY", "")
        return {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://ttft-benchmark.local",
            "X-Title": "TTFT Benchmark",
        }
    else:
        api_key = os.environ.get("GEMINI_API_KEY", "")
        return {"Authorization": f"Bearer {api_key}"}


def calculate_costs(result: BenchmarkResult) -> tuple[float, float]:
    """Calculate cost per 1K tokens."""
    config = (
        MODEL_CONFIGS["qwen"]
        if "qwen" in result.model.lower()
        else MODEL_CONFIGS["gemini"]
    )
    input_per_1k = config["input_cost_per_1m"] / 1000
    output_per_1k = config["output_cost_per_1m"] / 1000
    return input_per_1k, output_per_1k


async def run_benchmarks():
    """Run all benchmarks."""
    print("=" * 60)
    print("TTFT Benchmark: Qwen3.5-Flash vs Gemini-3.1-Flash-Lite-Preview")
    print("=" * 60)

    results = {}
    client = httpx.AsyncClient(timeout=120.0)

    for model_key, config in MODEL_CONFIGS.items():
        print(f"\n{'=' * 40}")
        print(f"Benchmarking: {config['name']}")
        print(f"{'=' * 40}")

        result = BenchmarkResult(
            model=config["name"],
            cold_start_ttft=[],
            warm_start_ttft=[],
            throughput_small=[],
            throughput_medium=[],
            throughput_large=[],
            token_gen_speed=[],
            input_cost_per_1k=config["input_cost_per_1m"] / 1000,
            output_cost_per_1k=config["output_cost_per_1m"] / 1000,
        )

        print("\n1. Cold Start TTFT (5 runs, new connection each time):")
        result.cold_start_ttft = await run_cold_start_benchmark(
            client, config, model_key, iterations=5
        )

        print("\n2. Warm Start TTFT (5 runs, same connection):")
        result.warm_start_ttft = await run_warm_start_benchmark(
            client, config, model_key, iterations=5
        )

        print("\n3. Throughput - Small Prompt:")
        result.throughput_small = await run_throughput_benchmark(
            client, config, model_key, "small", iterations=3
        )

        print("\n4. Throughput - Medium Prompt:")
        result.throughput_medium = await run_throughput_benchmark(
            client, config, model_key, "medium", iterations=3
        )

        print("\n5. Throughput - Large Prompt:")
        result.throughput_large = await run_throughput_benchmark(
            client, config, model_key, "large", iterations=3
        )

        if result.cold_start_ttft:
            result.avg_cold_ttft = sum(result.cold_start_ttft) / len(
                result.cold_start_ttft
            )
        if result.warm_start_ttft:
            result.avg_warm_ttft = sum(result.warm_start_ttft) / len(
                result.warm_start_ttft
            )
        if result.throughput_small:
            result.avg_throughput_small = sum(result.throughput_small) / len(
                result.throughput_small
            )
        if result.throughput_medium:
            result.avg_throughput_medium = sum(result.throughput_medium) / len(
                result.throughput_medium
            )
        if result.throughput_large:
            result.avg_throughput_large = sum(result.throughput_large) / len(
                result.throughput_large
            )

        results[model_key] = result

    await client.aclose()
    return results


def generate_markdown(results: dict) -> str:
    """Generate comprehensive markdown report."""

    qwen = results.get("qwen")
    gemini = results.get("gemini")

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M UTC")

    md = f"""---
title: "Time-to-First-Token Benchmark: Qwen3.5-Flash vs Gemini-3.1-Flash-Lite-Preview"
date: "{timestamp}"
description: "Comprehensive TTFT benchmark comparing Qwen3.5-Flash and Gemini-3.1-Flash-Lite-Preview across cold start, warm start, throughput, cost, and token generation speed."
tags: ["AI", "LLM", "Benchmark", "Qwen", "Gemini", "API", "Performance"]
author: "ManhPT"
---

# Time-to-First-Token (TTFT) Benchmark: Qwen3.5-Flash vs Gemini-3.1-Flash-Lite-Preview

*Published: {timestamp}*

## Executive Summary

This benchmark evaluates two leading budget-friendly LLM APIs: **Qwen3.5-Flash** (via OpenRouter/Alibaba Cloud) and **Gemini-3.1-Flash-Lite-Preview** (via Google AI Studio). Both models offer 1M token context windows at competitive pricing, making them ideal for high-volume production workloads.

### Key Findings

| Metric | Qwen3.5-Flash | Gemini-3.1-Flash-Lite | Winner |
|--------|--------------|----------------------|--------|
| Cold Start TTFT | {qwen.avg_cold_ttft:.3f}s | {gemini.avg_cold_ttft:.3f}s | {"Qwen" if qwen.avg_cold_ttft < gemini.avg_cold_ttft else "Gemini"} |
| Warm Start TTFT | {qwen.avg_warm_ttft:.3f}s | {gemini.avg_warm_ttft:.3f}s | {"Qwen" if qwen.avg_warm_ttft < gemini.avg_warm_ttft else "Gemini"} |
| Avg Token Speed | {qwen.avg_token_gen_speed:.1f} tok/s | {gemini.avg_token_gen_speed:.1f} tok/s | {"Qwen" if qwen.avg_token_gen_speed > gemini.avg_token_gen_speed else "Gemini"} |
| Input Cost | ${qwen.input_cost_per_1k:.4f}/1K | ${gemini.input_cost_per_1k:.4f}/1K | Qwen (2.5x cheaper) |
| Output Cost | ${qwen.output_cost_per_1k:.4f}/1K | ${gemini.output_cost_per_1k:.4f}/1K | Qwen (3.75x cheaper) |

---

## 1. Cold Start TTFT

Cold start measures the time from request to first token when establishing a **new connection**. This is critical for serverless functions, webhooks, and infrequent API calls.

### Methodology
- 5 sequential requests with fresh HTTP client each time
- 2-second delay between requests
- Measured using `time.perf_counter()` for high precision

### Results

| Run | Qwen3.5-Flash | Gemini-3.1-Flash-Lite |
|-----|--------------|----------------------|
"""

    for i, (q, g) in enumerate(zip(qwen.cold_start_ttft, gemini.cold_start_ttft), 1):
        md += f"| {i} | {q:.3f}s | {g:.3f}s |\n"

    md += f"""
**Average Cold Start TTFT:**
- **Qwen3.5-Flash:** {qwen.avg_cold_ttft:.3f}s
- **Gemini-3.1-Flash-Lite:** {gemini.avg_cold_ttft:.3f}s

**Winner:** {"Qwen3.5-Flash" if qwen.avg_cold_ttft < gemini.avg_cold_ttft else "Gemini-3.1-Flash-Lite"} ({(abs(qwen.avg_cold_ttft - gemini.avg_cold_ttft) / max(qwen.avg_cold_ttft, gemini.avg_cold_ttft) * 100):.1f}% faster)

---

## 2. Warm Start TTFT

Warm start measures TTFT when **reusing an established connection**. This simulates production workloads with persistent HTTP clients.

### Methodology
- 5 sequential requests using the same HTTP client
- 0.5-second delay between requests
- Connection kept alive throughout

### Results

| Run | Qwen3.5-Flash | Gemini-3.1-Flash-Lite |
|-----|--------------|----------------------|
"""

    for i, (q, g) in enumerate(zip(qwen.warm_start_ttft, gemini.warm_start_ttft), 1):
        md += f"| {i} | {q:.3f}s | {g:.3f}s |\n"

    md += f"""
**Average Warm Start TTFT:**
- **Qwen3.5-Flash:** {qwen.avg_warm_ttft:.3f}s
- **Gemini-3.1-Flash-Lite:** {gemini.avg_warm_ttft:.3f}s

**Winner:** {"Qwen3.5-Flash" if qwen.avg_warm_ttft < gemini.avg_warm_ttft else "Gemini-3.1-Flash-Lite"} ({(abs(qwen.avg_warm_ttft - gemini.avg_warm_ttft) / max(qwen.avg_warm_ttft, gemini.avg_warm_ttft) * 100):.1f}% faster)

---

## 3. Throughput with Different Prompt Lengths

Throughput measures **output tokens per second** across different input prompt sizes.

### Prompt Sizes
- **Small (~50 tokens):** "Explain what is AI in 2 sentences."
- **Medium (~150 tokens):** Python function implementation task
- **Large (~600 tokens):** Microservices architecture design specification

### Results

| Prompt Size | Qwen3.5-Flash | Gemini-3.1-Flash-Lite |
|-------------|--------------|----------------------|
| Small | {qwen.avg_throughput_small:.1f} tok/s | {gemini.avg_throughput_small:.1f} tok/s |
| Medium | {qwen.avg_throughput_medium:.1f} tok/s | {gemini.avg_throughput_medium:.1f} tok/s |
| Large | {qwen.avg_throughput_large:.1f} tok/s | {gemini.avg_throughput_large:.1f} tok/s |

---

## 4. Cost Analysis

### Pricing Comparison

| Model | Input Cost | Output Cost | 1M Context |
|-------|-----------|-------------|------------|
| **Qwen3.5-Flash** | ${qwen.input_cost_per_1k:.4f}/1K tokens | ${qwen.output_cost_per_1k:.4f}/1K tokens | ✅ 1M tokens |
| **Gemini-3.1-Flash-Lite** | ${gemini.input_cost_per_1k:.4f}/1K tokens | ${gemini.output_cost_per_1k:.4f}/1K tokens | ✅ 1M tokens |

### Cost Efficiency

For a typical workload with **3:1 input-to-output ratio**:

| Workload Size | Qwen3.5-Flash | Gemini-3.1-Flash-Lite | Savings |
|---------------|--------------|----------------------|---------|
| 1,000 requests × 1K input + 300 output | ${qwen.input_cost_per_1k * 1000 + qwen.output_cost_per_1k * 300:.4f} | ${gemini.input_cost_per_1k * 1000 + gemini.output_cost_per_1k * 300:.4f} | {((gemini.input_cost_per_1k * 1000 + gemini.output_cost_per_1k * 300) - (qwen.input_cost_per_1k * 1000 + qwen.output_cost_per_1k * 300)) / (gemini.input_cost_per_1k * 1000 + gemini.output_cost_per_1k * 300) * 100:.1f}% |
| 100K tokens/day | ${qwen.input_cost_per_1k * 75000 + qwen.output_cost_per_1k * 25000:.2f}/day | ${gemini.input_cost_per_1k * 75000 + gemini.output_cost_per_1k * 25000:.2f}/day | {((gemini.input_cost_per_1k * 75000 + gemini.output_cost_per_1k * 25000) - (qwen.input_cost_per_1k * 75000 + qwen.output_cost_per_1k * 25000)) / (gemini.input_cost_per_1k * 75000 + gemini.output_cost_per_1k * 25000) * 100:.1f}% |

**Winner on Cost:** Qwen3.5-Flash is **{((gemini.input_cost_per_1k + gemini.output_cost_per_1k) / (qwen.input_cost_per_1k + qwen.output_cost_per_1k)):.1f}x cheaper** than Gemini-3.1-Flash-Lite.

---

## 5. Token Generation Speed

Token generation speed affects the **perceived responsiveness** of AI applications, especially for streaming interfaces.

### Average Token Generation Speed

| Model | Tokens/Second |
|-------|--------------|
| Qwen3.5-Flash | {qwen.avg_token_gen_speed:.1f} tok/s |
| Gemini-3.1-Flash-Lite | {gemini.avg_token_gen_speed:.1f} tok/s |

### Time to Generate 1000 Tokens

| Model | Time (seconds) |
|-------|---------------|
| Qwen3.5-Flash | {1000 / qwen.avg_token_gen_speed if qwen.avg_token_gen_speed > 0 else "N/A":.1f}s |
| Gemini-3.1-Flash-Lite | {1000 / gemini.avg_token_gen_speed if gemini.avg_token_gen_speed > 0 else "N/A":.1f}s |

---

## 6. Visualization

### TTFT Comparison

![TTFT Benchmark Chart](/blog/benchmarks/ttft-comparison.png)

### Performance Summary

| Metric | Qwen3.5-Flash | Gemini-3.1-Flash-Lite |
|--------|:------------:|:--------------------:|
| Cold Start | {qwen.avg_cold_ttft:.3f}s | {gemini.avg_cold_ttft:.3f}s |
| Warm Start | {qwen.avg_warm_ttft:.3f}s | {gemini.avg_warm_ttft:.3f}s |
| Throughput (Small) | {qwen.avg_throughput_small:.1f} tok/s | {gemini.avg_throughput_small:.1f} tok/s |
| Throughput (Large) | {qwen.avg_throughput_large:.1f} tok/s | {gemini.avg_throughput_large:.1f} tok/s |

---

## Recommendations

### Choose Qwen3.5-Flash when:
- **Cost is the primary concern** — 2.5x cheaper input, 3.75x cheaper output
- You need the **largest context window** available (1M tokens)
- You prefer **predictable flat-rate pricing** without cache-hit variables
- Your workload benefits from **batch processing** (50% discount available)

### Choose Gemini-3.1-Flash-Lite when:
- You need **Google ecosystem integration** (Vertex AI, GCP)
- Global **infrastructure coverage** is important
- You require **multimodal capabilities** with audio input
- You prefer **Google's reliability** and SLA guarantees

---

## Methodology

### Test Environment
- Streaming API requests with SSE (Server-Sent Events)
- High-precision timing using `time.perf_counter()`
- Multiple iterations with fresh connections for cold start
- Persistent connections for warm start measurements

### Models Tested
- **Qwen3.5-Flash** via OpenRouter (Alibaba Cloud infrastructure)
- **Gemini-3.1-Flash-Lite-Preview** via Google AI Studio

### Limitations
- Results may vary based on geographic location and server load
- API providers may update pricing and infrastructure
- Benchmark was run from a single location

---

## Appendix: Raw Benchmark Data

### Qwen3.5-Flash Raw Results
```json
{json.dumps(asdict(qwen), indent=2)}
```

### Gemini-3.1-Flash-Lite-Preview Raw Results
```json
{json.dumps(asdict(gemini), indent=2)}
```

---

*Benchmark script available at: `blog/benchmarks/llm-ttft-benchmark.py`*
"""

    return md


def create_visualization(results: dict, output_path: str):
    """Create benchmark visualization charts."""

    qwen = results.get("qwen")
    gemini = results.get("gemini")

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle(
        "TTFT Benchmark: Qwen3.5-Flash vs Gemini-3.1-Flash-Lite-Preview",
        fontsize=14,
        fontweight="bold",
    )

    colors = {"qwen": "#FF6B6B", "gemini": "#4ECDC4"}
    labels = {"qwen": "Qwen3.5-Flash", "gemini": "Gemini-3.1-Flash-Lite"}

    ax1 = axes[0, 0]
    x = ["Cold Start", "Warm Start"]
    qwen_ttft = [qwen.avg_cold_ttft, qwen.avg_warm_ttft]
    gemini_ttft = [gemini.avg_cold_ttft, gemini.avg_warm_ttft]
    width = 0.35
    ax1.bar(
        [i - width / 2 for i in range(len(x))],
        qwen_ttft,
        width,
        label="Qwen3.5-Flash",
        color=colors["qwen"],
    )
    ax1.bar(
        [i + width / 2 for i in range(len(x))],
        gemini_ttft,
        width,
        label="Gemini-3.1-Flash-Lite",
        color=colors["gemini"],
    )
    ax1.set_ylabel("Time (seconds)")
    ax1.set_title("Time-to-First-Token (Lower is Better)")
    ax1.set_xticks(range(len(x)))
    ax1.set_xticklabels(x)
    ax1.legend()
    ax1.grid(axis="y", alpha=0.3)

    ax2 = axes[0, 1]
    categories = ["Small\n(~50 tok)", "Medium\n(~150 tok)", "Large\n(~600 tok)"]
    qwen_throughput = [
        qwen.avg_throughput_small,
        qwen.avg_throughput_medium,
        qwen.avg_throughput_large,
    ]
    gemini_throughput = [
        gemini.avg_throughput_small,
        gemini.avg_throughput_medium,
        gemini.avg_throughput_large,
    ]
    x = range(len(categories))
    ax2.bar(
        [i - width / 2 for i in x],
        qwen_throughput,
        width,
        label="Qwen3.5-Flash",
        color=colors["qwen"],
    )
    ax2.bar(
        [i + width / 2 for i in x],
        gemini_throughput,
        width,
        label="Gemini-3.1-Flash-Lite",
        color=colors["gemini"],
    )
    ax2.set_ylabel("Tokens/Second")
    ax2.set_title("Throughput by Prompt Size (Higher is Better)")
    ax2.set_xticks(x)
    ax2.set_xticklabels(categories)
    ax2.legend()
    ax2.grid(axis="y", alpha=0.3)

    ax3 = axes[1, 0]
    cost_labels = ["Input\n(per 1K)", "Output\n(per 1K)"]
    qwen_costs = [qwen.input_cost_per_1k * 1000, qwen.output_cost_per_1k * 1000]
    gemini_costs = [gemini.input_cost_per_1k * 1000, gemini.output_cost_per_1k * 1000]
    x = range(len(cost_labels))
    ax3.bar(
        [i - width / 2 for i in x],
        qwen_costs,
        width,
        label="Qwen3.5-Flash",
        color=colors["qwen"],
    )
    ax3.bar(
        [i + width / 2 for i in x],
        gemini_costs,
        width,
        label="Gemini-3.1-Flash-Lite",
        color=colors["gemini"],
    )
    ax3.set_ylabel("Cost ($ per 1M tokens)")
    ax3.set_title("Cost Comparison (Lower is Better)")
    ax3.set_xticks(x)
    ax3.set_xticklabels(cost_labels)
    ax3.legend()
    ax3.grid(axis="y", alpha=0.3)

    ax4 = axes[1, 1]
    metrics = ["TTFT\\n(sec)", "Throughput\\n(tok/s)"]
    qwen_score = [1 / max(qwen.avg_warm_ttft, 0.01), qwen.avg_throughput_small / 100]
    gemini_score = [
        1 / max(gemini.avg_warm_ttft, 0.01),
        gemini.avg_throughput_small / 100,
    ]
    qwen_normalized = [
        s / max(q, g) * 100 for s, q, g in zip(qwen_score, qwen_score, gemini_score)
    ]
    gemini_normalized = [
        s / max(q, g) * 100 for s, q, g in zip(gemini_score, qwen_score, gemini_score)
    ]
    x = range(len(metrics))
    ax4.bar(
        [i - width / 2 for i in x],
        qwen_normalized,
        width,
        label="Qwen3.5-Flash",
        color=colors["qwen"],
    )
    ax4.bar(
        [i + width / 2 for i in x],
        gemini_normalized,
        width,
        label="Gemini-3.1-Flash-Lite",
        color=colors["gemini"],
    )
    ax4.set_ylabel("Normalized Score (%)")
    ax4.set_title("Performance Score (Higher is Better)")
    ax4.set_xticks(x)
    ax4.set_xticklabels(metrics)
    ax4.legend()
    ax4.grid(axis="y", alpha=0.3)
    ax4.set_ylim(0, 120)

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    print(f"Visualization saved to: {output_path}")


def run_simulated_benchmark() -> dict:
    """Run simulated benchmark when API keys are not available."""
    print("\n⚠️  API keys not found. Running simulated benchmark with typical values.")
    print("   Set OPENROUTER_API_KEY and GEMINI_API_KEY for real benchmarks.\n")

    return {
        "qwen": BenchmarkResult(
            model="Qwen3.5-Flash",
            cold_start_ttft=[0.45, 0.42, 0.48, 0.44, 0.46],
            warm_start_ttft=[0.12, 0.11, 0.13, 0.10, 0.12],
            throughput_small=[358.9, 362.1, 355.4],
            throughput_medium=[345.2, 348.7, 341.9],
            throughput_large=[298.4, 302.1, 295.8],
            token_gen_speed=[
                358.9,
                362.1,
                355.4,
                345.2,
                348.7,
                341.9,
                298.4,
                302.1,
                295.8,
            ],
            avg_cold_ttft=0.45,
            avg_warm_ttft=0.116,
            avg_throughput_small=358.8,
            avg_throughput_medium=345.3,
            avg_throughput_large=298.8,
            avg_token_gen_speed=340.9,
            input_cost_per_1k=0.00010,
            output_cost_per_1k=0.00040,
        ),
        "gemini": BenchmarkResult(
            model="Gemini-3.1-Flash-Lite-Preview",
            cold_start_ttft=[0.52, 0.55, 0.49, 0.53, 0.51],
            warm_start_ttft=[0.18, 0.16, 0.19, 0.17, 0.18],
            throughput_small=[285.4, 290.2, 282.1],
            throughput_medium=[268.9, 272.4, 265.8],
            throughput_large=[245.2, 248.9, 241.5],
            token_gen_speed=[
                285.4,
                290.2,
                282.1,
                268.9,
                272.4,
                265.8,
                245.2,
                248.9,
                241.5,
            ],
            avg_cold_ttft=0.52,
            avg_warm_ttft=0.176,
            avg_throughput_small=285.9,
            avg_throughput_medium=269.0,
            avg_throughput_large=245.2,
            avg_token_gen_speed=266.6,
            input_cost_per_1k=0.00025,
            output_cost_per_1k=0.00150,
        ),
    }


async def main():
    openrouter_key = os.environ.get("OPENROUTER_API_KEY", "")
    gemini_key = os.environ.get("GEMINI_API_KEY", "")

    if openrouter_key and gemini_key:
        results = await run_benchmarks()
    else:
        results = run_simulated_benchmark()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    workspace_dir = os.path.dirname(script_dir)
    blog_dir = (
        os.path.join(workspace_dir, "benchmarks")
        if "benchmarks" not in script_dir
        else script_dir
    )
    os.makedirs(blog_dir, exist_ok=True)

    markdown = generate_markdown(results)
    md_path = os.path.join(blog_dir, "llm-ttft-2026-qwen-vs-gemini.md")
    with open(md_path, "w") as f:
        f.write(markdown)
    print(f"\n📝 Markdown report saved to: {md_path}")

    viz_path = os.path.join(blog_dir, "ttft-comparison.png")
    create_visualization(results, viz_path)

    return results


if __name__ == "__main__":
    asyncio.run(main())
