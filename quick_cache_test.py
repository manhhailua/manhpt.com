#!/usr/bin/env python3
"""
Quick Qwen cache test - minimal version
"""
import os
import time
from datetime import datetime
from openai import OpenAI

# API Key
DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY", "sk-dacb026daa1d4d26a3a6a11007ec77a7")

# Initialize client
qwen = OpenAI(
    api_key=DASHSCOPE_API_KEY,
    base_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1"
)

# Test with cache control
print("🚀 Quick Qwen Cache Test")
print("=" * 50)

# Test 1: First call (should create cache)
print("\n1. First call (cache creation):")
start = time.perf_counter()
try:
    response1 = qwen.chat.completions.create(
        model="qwen3.5-flash",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant. CACHE: {'type': 'ephemeral'}",
                "cache_control": {"type": "ephemeral"}
            },
            {"role": "user", "content": "What is 2+2?"}
        ],
        temperature=0.0,
        max_tokens=50
    )
    latency1 = (time.perf_counter() - start) * 1000
    cached1 = getattr(response1.usage, 'cached_tokens', 0)
    print(f"   Latency: {latency1:.0f}ms")
    print(f"   Cached tokens: {cached1}")
    print(f"   Response: {response1.choices[0].message.content[:100]}...")
except Exception as e:
    print(f"   Error: {e}")

# Wait a bit
time.sleep(2)

# Test 2: Second call (should hit cache)
print("\n2. Second call (cache hit expected):")
start = time.perf_counter()
try:
    response2 = qwen.chat.completions.create(
        model="qwen3.5-flash",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant. CACHE: {'type': 'ephemeral'}",
                "cache_control": {"type": "ephemeral"}
            },
            {"role": "user", "content": "What is 2+2?"}
        ],
        temperature=0.0,
        max_tokens=50
    )
    latency2 = (time.perf_counter() - start) * 1000
    cached2 = getattr(response2.usage, 'cached_tokens', 0)
    print(f"   Latency: {latency2:.0f}ms")
    print(f"   Cached tokens: {cached2}")
    print(f"   Response: {response2.choices[0].message.content[:100]}...")
    
    # Compare
    if cached2 > 0:
        print(f"   ✅ CACHE HIT! {cached2} tokens cached")
        speedup = ((latency1 - latency2) / latency1) * 100
        print(f"   Speed improvement: {speedup:.1f}% faster")
    else:
        print("   ⚠️ No cache hit detected")
        
except Exception as e:
    print(f"   Error: {e}")

# Test 3: Different query (no cache expected)
print("\n3. Different query (no cache expected):")
start = time.perf_counter()
try:
    response3 = qwen.chat.completions.create(
        model="qwen3.5-flash",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant. CACHE: {'type': 'ephemeral'}",
                "cache_control": {"type": "ephemeral"}
            },
            {"role": "user", "content": "What is 3+3?"}
        ],
        temperature=0.0,
        max_tokens=50
    )
    latency3 = (time.perf_counter() - start) * 1000
    cached3 = getattr(response3.usage, 'cached_tokens', 0)
    print(f"   Latency: {latency3:.0f}ms")
    print(f"   Cached tokens: {cached3}")
    print(f"   Response: {response3.choices[0].message.content[:100]}...")
except Exception as e:
    print(f"   Error: {e}")

print("\n" + "=" * 50)
print("📊 Summary:")
print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("Cache test completed!")