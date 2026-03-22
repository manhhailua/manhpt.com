"""
Benchmark: Implicit Cache vs Explicit Cache
Qwen3.5-Flash vs Gemini-3.1-Flash-Lite-Preview

Measures TTLT (time-to-last-token) and TTFT across 6 scenarios:
  1. Qwen Baseline
  2. Qwen Implicit Cache
  3. Qwen Explicit Cache
  4. Gemini Baseline
  5. Gemini Implicit Cache
  6. Gemini Explicit Cache

Dependencies: openai, google-generativeai, python-dotenv
"""

import json
import os
import time
from dataclasses import dataclass, field, asdict
from datetime import timedelta
from statistics import mean, median
from typing import Optional
from pathlib import Path
from dotenv import load_dotenv

# Load from workspace .env first, then local .env
load_dotenv(Path(__file__).parent.parent.parent / "workspace" / ".env")
load_dotenv(Path(__file__).parent / ".env")

from openai import OpenAI
import google.generativeai as genai
from google.generativeai import caching as genai_caching

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
QWEN_MODEL = "qwen3.5-flash-2026-02-23"
QWEN_BASE_URL = "https://dashscope-intl.aliyuncs.com/compatible-mode/v1"
GEMINI_MODEL = "gemini-3.1-flash-lite-preview"

NUM_QUERIES = 5
INTER_QUERY_SLEEP = 2.0  # seconds between queries

# Pricing (per 1M tokens, USD)
QWEN_PRICE = {
    "input_no_cache": 0.10,
    "implicit_hit": 0.02,
    "explicit_create": 0.125,
    "explicit_hit": 0.01,
    "output": 0.40,
}
GEMINI_PRICE = {
    "input_no_cache": 0.025,
    "implicit_hit": 0.0025,
    "explicit_storage_per_1m_per_hr": 1.00,
    "explicit_hit": 0.0025,
    "output": 0.10,
}

# ---------------------------------------------------------------------------
# System prompt: query breaking agent (~2000+ tokens)
# ---------------------------------------------------------------------------
SYSTEM_PROMPT = """Bạn là một AI agent chuyên xử lý bước "query breaking" trong pipeline RAG (Retrieval-Augmented Generation) cho lĩnh vực tài chính cá nhân và ngân hàng tại Việt Nam.

## Nhiệm vụ

Khi nhận được một câu hỏi từ người dùng, bạn phải:
1. Phân tích và xác định tất cả các ý định (intent) riêng biệt trong câu hỏi
2. Phân tách thành các sub-query độc lập, mỗi sub-query tập trung vào đúng một ý định
3. Đảm bảo mỗi sub-query đủ cụ thể để vector search tìm được tài liệu phù hợp
4. Trả về kết quả dưới dạng JSON array

## Quy tắc phân tách

- **Nguyên tắc nguyên tử**: Mỗi sub-query chỉ hỏi về một đối tượng hoặc một khía cạnh
- **Nguyên tắc độc lập**: Các sub-query không phụ thuộc vào nhau khi tìm kiếm
- **Nguyên tắc rõ ràng**: Sub-query phải chứa đủ context để hiểu được khi đứng độc lập
- **Giới hạn**: Tối đa 5 sub-query cho một câu hỏi. Nếu câu hỏi đơn giản, trả về 1 sub-query
- **Ngôn ngữ**: Giữ nguyên ngôn ngữ của câu hỏi gốc (tiếng Việt → tiếng Việt)

## Định dạng output

Trả về JSON array thuần túy, không có markdown, không có giải thích:

```
["sub-query 1", "sub-query 2", "sub-query 3"]
```

## Ví dụ mẫu theo domain

### Domain: Vay vốn

Input: "Tôi muốn mua xe và mua nhà, nên vay ngân hàng nào và lãi suất bao nhiêu?"

Output:
```json
["Lãi suất vay mua xe ô tô tại các ngân hàng Việt Nam", "Lãi suất vay mua nhà tại các ngân hàng Việt Nam", "So sánh điều kiện vay mua xe giữa các ngân hàng", "So sánh điều kiện vay mua nhà giữa các ngân hàng"]
```

### Domain: Bảo hiểm

Input: "Bảo hiểm nhân thọ Prudential và Manulife khác nhau thế nào về phí và quyền lợi?"

Output:
```json
["Gói bảo hiểm nhân thọ và quyền lợi của Prudential Việt Nam", "Gói bảo hiểm nhân thọ và quyền lợi của Manulife Việt Nam", "So sánh phí bảo hiểm nhân thọ Prudential và Manulife"]
```

### Domain: Đầu tư

Input: "Tôi nên đầu tư vào vàng, cổ phiếu hay gửi tiết kiệm ngân hàng?"

Output:
```json
["Lợi nhuận và rủi ro khi đầu tư vàng tại Việt Nam", "Lợi nhuận và rủi ro khi đầu tư cổ phiếu tại Việt Nam", "Lãi suất gửi tiết kiệm ngân hàng hiện tại tại Việt Nam", "So sánh hiệu quả đầu tư vàng cổ phiếu và tiết kiệm"]
```

### Domain: Thẻ tín dụng

Input: "Thẻ tín dụng Visa và Mastercard của VPBank có gì khác nhau, phí thường niên bao nhiêu?"

Output:
```json
["Thẻ tín dụng Visa VPBank quyền lợi và phí thường niên", "Thẻ tín dụng Mastercard VPBank quyền lợi và phí thường niên", "So sánh thẻ Visa và Mastercard VPBank"]
```

### Domain: Kế hoạch tài chính

Input: "Tôi 30 tuổi, thu nhập 20 triệu/tháng, nên phân bổ tiền như thế nào để vừa tiết kiệm vừa đầu tư?"

Output:
```json
["Nguyên tắc phân bổ tài chính cá nhân cho người thu nhập trung bình", "Tỷ lệ tiết kiệm khuyến nghị cho người 30 tuổi tại Việt Nam", "Các kênh đầu tư phù hợp với số tiền nhỏ hàng tháng tại Việt Nam"]
```

### Domain: Ngoại tệ

Input: "Tỷ giá USD/VND và EUR/VND hôm nay là bao nhiêu và có nên mua ngoại tệ không?"

Output:
```json
["Tỷ giá USD/VND hiện tại tại các ngân hàng Việt Nam", "Tỷ giá EUR/VND hiện tại tại các ngân hàng Việt Nam", "Xu hướng biến động tỷ giá ngoại tệ và thời điểm mua ngoại tệ"]
```

### Domain: Vay tiêu dùng

Input: "Vay tiêu dùng tín chấp và thế chấp khác nhau thế nào, hồ sơ cần gì?"

Output:
```json
["Điều kiện và lãi suất vay tiêu dùng tín chấp tại Việt Nam", "Điều kiện và lãi suất vay tiêu dùng thế chấp tại Việt Nam", "Hồ sơ thủ tục vay tiêu dùng tín chấp", "Hồ sơ thủ tục vay tiêu dùng thế chấp"]
```

### Domain: Lương hưu

Input: "Bảo hiểm xã hội và quỹ hưu trí tự nguyện nên chọn cái nào để đảm bảo tài chính tuổi già?"

Output:
```json
["Quyền lợi bảo hiểm xã hội bắt buộc và mức lương hưu tại Việt Nam", "Quỹ hưu trí tự nguyện hoạt động như thế nào tại Việt Nam", "So sánh bảo hiểm xã hội và quỹ hưu trí tự nguyện cho kế hoạch hưu trí"]
```

### Domain: Thuế

Input: "Tôi có hai nguồn thu nhập từ lương và kinh doanh online, cần khai thuế như thế nào?"

Output:
```json
["Cách tính thuế thu nhập cá nhân từ tiền lương tại Việt Nam", "Cách khai và nộp thuế thu nhập từ kinh doanh online tại Việt Nam", "Quy định hợp nhất hai nguồn thu nhập khi quyết toán thuế TNCN"]
```

### Domain: Tín dụng

Input: "CIC là gì và điểm tín dụng ảnh hưởng thế nào đến khả năng vay vốn ngân hàng?"

Output:
```json
["CIC là gì và cách tra cứu lịch sử tín dụng cá nhân tại Việt Nam", "Điểm tín dụng CIC ảnh hưởng như thế nào đến xét duyệt vay ngân hàng", "Cách cải thiện điểm tín dụng CIC khi bị nợ xấu"]
```

## Lưu ý đặc biệt

- Nếu câu hỏi đã đơn giản và chỉ có một ý định, trả về array với một phần tử duy nhất
- Không thêm thông tin ngoài những gì người dùng đề cập
- Không đặt câu hỏi lại cho người dùng
- Không giải thích kết quả, chỉ trả về JSON array"""

# 5 compound Vietnamese financial queries
QUERIES = [
    "Tôi muốn mua xe và mua nhà trong năm nay, nên vay ngân hàng nào và cần chuẩn bị giấy tờ gì?",
    "So sánh lãi suất tiết kiệm 6 tháng và 12 tháng tại Vietcombank và Techcombank",
    "Bảo hiểm nhân thọ Prudential và Manulife khác nhau thế nào về phí và quyền lợi bồi thường?",
    "Tôi nên đầu tư vào vàng, cổ phiếu VN30 hay gửi tiết kiệm ngân hàng với số tiền 100 triệu?",
    "Tỷ giá USD/VND và lãi suất cơ bản của NHNN ảnh hưởng thế nào đến lãi suất vay ngân hàng?",
]


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------
@dataclass
class QueryResult:
    query_index: int
    ttft_ms: float
    ttlt_ms: float
    input_tokens: int
    output_tokens: int
    cached_tokens: int
    text_preview: str = ""


@dataclass
class ScenarioResult:
    model: str
    scenario: str
    results: list = field(default_factory=list)

    def stats(self) -> dict:
        ttfts = [r.ttft_ms for r in self.results]
        ttlts = [r.ttlt_ms for r in self.results]
        cached = [r.cached_tokens for r in self.results]
        return {
            "ttlt_mean_ms": round(mean(ttlts), 0),
            "ttlt_min_ms": round(min(ttlts), 0),
            "ttlt_max_ms": round(max(ttlts), 0),
            "ttlt_median_ms": round(median(ttlts), 0),
            "ttft_mean_ms": round(mean(ttfts), 0),
            "ttft_min_ms": round(min(ttfts), 0),
            "ttft_max_ms": round(max(ttfts), 0),
            "avg_cached_tokens": round(mean(cached), 0),
            "avg_input_tokens": round(mean([r.input_tokens for r in self.results]), 0),
            "avg_output_tokens": round(mean([r.output_tokens for r in self.results]), 0),
        }


# ---------------------------------------------------------------------------
# Qwen (DashScope OpenAI-compat)
# ---------------------------------------------------------------------------
def get_qwen_client() -> OpenAI:
    key = os.environ.get("DASHSCOPE_API_KEY", "")
    if not key:
        raise RuntimeError("DASHSCOPE_API_KEY not set")
    return OpenAI(api_key=key, base_url=QWEN_BASE_URL)


def call_qwen(client: OpenAI, messages: list) -> QueryResult:
    start = time.perf_counter()
    ttft_ms = None
    chunks = []
    usage_data = None

    stream = client.chat.completions.create(
        model=QWEN_MODEL,
        messages=messages,
        stream=True,
        stream_options={"include_usage": True},
        max_tokens=300,
        extra_body={"enable_thinking": False},
    )

    for chunk in stream:
        if hasattr(chunk, "usage") and chunk.usage is not None:
            usage_data = chunk.usage
        if chunk.choices:
            delta = getattr(chunk.choices[0].delta, "content", None) or ""
            if delta:
                if ttft_ms is None:
                    ttft_ms = (time.perf_counter() - start) * 1000
                chunks.append(delta)

    ttlt_ms = (time.perf_counter() - start) * 1000
    if ttft_ms is None:
        ttft_ms = ttlt_ms

    input_tokens = output_tokens = cached_tokens = 0
    if usage_data:
        input_tokens = getattr(usage_data, "prompt_tokens", 0) or 0
        output_tokens = getattr(usage_data, "completion_tokens", 0) or 0
        details = getattr(usage_data, "prompt_tokens_details", None)
        if details:
            cached_tokens = getattr(details, "cached_tokens", 0) or 0

    text = "".join(chunks)
    return ttft_ms, ttlt_ms, input_tokens, output_tokens, cached_tokens, text


def run_qwen_baseline(client, query, idx):
    msgs = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": query},
    ]
    tf, tl, inp, out, cached, text = call_qwen(client, msgs)
    return QueryResult(idx, tf, tl, inp, out, cached, text[:120])


def run_qwen_implicit(client, query, idx):
    msgs = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": query},
    ]
    tf, tl, inp, out, cached, text = call_qwen(client, msgs)
    return QueryResult(idx, tf, tl, inp, out, cached, text[:120])


def run_qwen_explicit(client, query, idx):
    msgs = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
            "cache_control": {"type": "ephemeral"},
        },
        {"role": "user", "content": query},
    ]
    tf, tl, inp, out, cached, text = call_qwen(client, msgs)
    return QueryResult(idx, tf, tl, inp, out, cached, text[:120])


# ---------------------------------------------------------------------------
# Gemini
# ---------------------------------------------------------------------------
def setup_gemini():
    key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY", "")
    if not key:
        raise RuntimeError("GEMINI_API_KEY not set")
    genai.configure(api_key=key)


def call_gemini(model, query, idx) -> QueryResult:
    start = time.perf_counter()
    ttft_ms = None
    chunks = []
    usage_meta = None

    response = model.generate_content(query, stream=True)

    for chunk in response:
        text = getattr(chunk, "text", "") or ""
        if text:
            if ttft_ms is None:
                ttft_ms = (time.perf_counter() - start) * 1000
            chunks.append(text)
        if hasattr(chunk, "usage_metadata") and chunk.usage_metadata:
            usage_meta = chunk.usage_metadata

    ttlt_ms = (time.perf_counter() - start) * 1000
    if ttft_ms is None:
        ttft_ms = ttlt_ms

    input_tokens = output_tokens = cached_tokens = 0
    if usage_meta:
        input_tokens = getattr(usage_meta, "prompt_token_count", 0) or 0
        output_tokens = getattr(usage_meta, "candidates_token_count", 0) or 0
        cached_tokens = getattr(usage_meta, "cached_content_token_count", 0) or 0

    text = "".join(chunks)
    return QueryResult(idx, ttft_ms, ttlt_ms, input_tokens, output_tokens, cached_tokens, text[:120])


def run_gemini_baseline(query, idx):
    model = genai.GenerativeModel(
        model_name=GEMINI_MODEL,
        system_instruction=SYSTEM_PROMPT,
    )
    return call_gemini(model, query, idx)


def run_gemini_implicit(query, idx):
    model = genai.GenerativeModel(
        model_name=GEMINI_MODEL,
        system_instruction=SYSTEM_PROMPT,
    )
    return call_gemini(model, query, idx)


def run_gemini_explicit(cached_content, query, idx):
    model = genai.GenerativeModel.from_cached_content(cached_content)
    return call_gemini(model, query, idx)


# ---------------------------------------------------------------------------
# Scenario runner
# ---------------------------------------------------------------------------
def run_scenario(fn, label, model_name) -> ScenarioResult:
    result = ScenarioResult(model=model_name, scenario=label)
    print(f"\n{'='*65}")
    print(f"  {model_name} | {label}")
    print(f"{'='*65}")

    for i, query in enumerate(QUERIES):
        print(f"  [{i+1}/{NUM_QUERIES}] {query[:70]}...")
        try:
            qr = fn(query, i)
            result.results.append(qr)
            print(f"        TTLT={qr.ttlt_ms:.0f}ms  TTFT={qr.ttft_ms:.0f}ms  "
                  f"cached={qr.cached_tokens}  in={qr.input_tokens}  out={qr.output_tokens}")
        except Exception as e:
            print(f"        ERROR: {e}")
        if i < NUM_QUERIES - 1:
            time.sleep(INTER_QUERY_SLEEP)

    if result.results:
        s = result.stats()
        print(f"\n  → TTLT mean={s['ttlt_mean_ms']:.0f}ms  min={s['ttlt_min_ms']:.0f}ms  max={s['ttlt_max_ms']:.0f}ms  "
              f"| TTFT mean={s['ttft_mean_ms']:.0f}ms  | cached avg={s['avg_cached_tokens']:.0f}")
    return result


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def run_all() -> list:
    results = []

    # --- Qwen ---
    qwen = get_qwen_client()

    results.append(run_scenario(
        lambda q, i: run_qwen_baseline(qwen, q, i),
        "Baseline", "Qwen3.5-Flash",
    ))

    print("\n  [Qwen Implicit] Warmup run...")
    try:
        run_qwen_implicit(qwen, QUERIES[0], -1)
    except Exception as e:
        print(f"  Warmup error: {e}")
    time.sleep(2)

    results.append(run_scenario(
        lambda q, i: run_qwen_implicit(qwen, q, i),
        "Implicit Cache", "Qwen3.5-Flash",
    ))

    results.append(run_scenario(
        lambda q, i: run_qwen_explicit(qwen, q, i),
        "Explicit Cache", "Qwen3.5-Flash",
    ))

    # --- Gemini ---
    setup_gemini()

    results.append(run_scenario(
        lambda q, i: run_gemini_baseline(q, i),
        "Baseline", "Gemini-3.1-Flash-Lite",
    ))

    print("\n  [Gemini Implicit] Warmup run...")
    try:
        run_gemini_implicit(QUERIES[0], -1)
    except Exception as e:
        print(f"  Warmup error: {e}")
    time.sleep(2)

    results.append(run_scenario(
        lambda q, i: run_gemini_implicit(q, i),
        "Implicit Cache", "Gemini-3.1-Flash-Lite",
    ))

    # Explicit cache — needs >=4096 tokens; try and handle gracefully
    print("\n  [Gemini Explicit] Creating cached content (needs >=4096 tokens)...")
    cached_content = None
    try:
        cached_content = genai_caching.CachedContent.create(
            model=GEMINI_MODEL,
            system_instruction=SYSTEM_PROMPT,
            contents=[],
            ttl=timedelta(minutes=10),
        )
        print(f"  Cache created: {cached_content.name}")
        results.append(run_scenario(
            lambda q, i, cc=cached_content: run_gemini_explicit(cc, q, i),
            "Explicit Cache", "Gemini-3.1-Flash-Lite",
        ))
    except Exception as e:
        print(f"  Explicit cache creation failed: {e}")
        print("  Skipping Gemini Explicit Cache scenario.")
    finally:
        if cached_content:
            try:
                cached_content.delete()
            except Exception:
                pass

    return results


def print_table(results: list):
    print("\n\n" + "="*80)
    print("RESULTS (primary metric: TTLT = time-to-last-token)")
    print("="*80)
    print(f"{'Model':<22} {'Scenario':<18} {'TTLT mean':>10} {'TTLT min':>9} {'TTLT max':>9} {'TTFT mean':>10} {'Cached':>8}")
    print("-"*80)
    for r in results:
        if not r.results:
            continue
        s = r.stats()
        print(f"{r.model:<22} {r.scenario:<18} "
              f"{s['ttlt_mean_ms']:>9.0f}ms {s['ttlt_min_ms']:>8.0f}ms "
              f"{s['ttlt_max_ms']:>8.0f}ms {s['ttft_mean_ms']:>9.0f}ms "
              f"{s['avg_cached_tokens']:>7.0f}")
    print("="*80)


def save_json(results: list, path="benchmark_cache_results.json"):
    data = []
    for r in results:
        data.append({
            "model": r.model,
            "scenario": r.scenario,
            "stats": r.stats() if r.results else {},
            "queries": [asdict(qr) for qr in r.results],
        })
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"\nSaved → {path}")


def print_cost(results: list):
    DAILY = 1000
    print("\n" + "="*60)
    print("COST ESTIMATE (1,000 req/day)")
    print("="*60)
    for r in results:
        if not r.results:
            continue
        s = r.stats()
        avg_in = s["avg_input_tokens"]
        avg_out = s["avg_output_tokens"]
        avg_cached = s["avg_cached_tokens"]
        avg_uncached = avg_in - avg_cached

        if "Qwen" in r.model:
            p = QWEN_PRICE
            if r.scenario == "Baseline":
                cost = (avg_in * p["input_no_cache"] + avg_out * p["output"]) / 1e6
            elif r.scenario == "Implicit Cache":
                cost = (avg_uncached * p["input_no_cache"] + avg_cached * p["implicit_hit"] + avg_out * p["output"]) / 1e6
            else:
                cost = (avg_uncached * p["input_no_cache"] + avg_cached * p["explicit_hit"] + avg_out * p["output"]) / 1e6
        else:
            p = GEMINI_PRICE
            if r.scenario == "Baseline":
                cost = (avg_in * p["input_no_cache"] + avg_out * p["output"]) / 1e6
            elif r.scenario == "Implicit Cache":
                cost = (avg_uncached * p["input_no_cache"] + avg_cached * p["implicit_hit"] + avg_out * p["output"]) / 1e6
            else:
                cost = (avg_uncached * p["input_no_cache"] + avg_cached * p["explicit_hit"] + avg_out * p["output"]) / 1e6

        print(f"{r.model:<22} {r.scenario:<18} ${cost * DAILY:.4f}/day")
    print("="*60)


if __name__ == "__main__":
    print(f"Benchmark: Implicit vs Explicit Cache")
    print(f"Models: {QWEN_MODEL} | {GEMINI_MODEL}")
    print(f"Queries: {NUM_QUERIES} per scenario | Sleep: {INTER_QUERY_SLEEP}s between queries\n")

    all_results = run_all()
    print_table(all_results)
    save_json(all_results)
    print_cost(all_results)
    print("\nDone.")
