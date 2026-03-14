"""
Benchmark: Implicit Cache vs Explicit Cache
Qwen3.5-Flash vs Gemini-3.1-Flash-Lite-Preview

Measures TTLT (time-to-last-token) and TTFT across 8 scenarios:
  1. Qwen Baseline
  2. Qwen Implicit Cache
  3. Qwen Explicit Cache
  4. Qwen Explicit Cache + No Streaming (TTLT only)
  5. Gemini Baseline
  6. Gemini Implicit Cache
  7. Gemini Explicit Cache
  8. Gemini No Thinking + No Streaming (TTLT only)

Dependencies: requests, google-genai, python-dotenv
"""

import json
import os
import time
import requests
from dataclasses import dataclass, field, asdict
from datetime import timedelta
from statistics import mean, median
from typing import Optional
from pathlib import Path
from dotenv import load_dotenv

# Load nearest .env files from current file parents.
_SEEN_ENV_PATHS = set()
for _parent in [Path(__file__).resolve().parent, *Path(__file__).resolve().parents]:
    for _candidate in (_parent / "workspace" / ".env", _parent / ".env"):
        if _candidate.exists() and _candidate not in _SEEN_ENV_PATHS:
            load_dotenv(_candidate, override=False)
            _SEEN_ENV_PATHS.add(_candidate)

from google import genai
from google.genai import types as genai_types

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
QWEN_MODEL = "qwen3.5-flash-2026-02-23"
QWEN_BASE_URL = "https://dashscope-intl.aliyuncs.com/compatible-mode/v1"
QWEN_CHAT_COMPLETIONS_URL = f"{QWEN_BASE_URL}/chat/completions"
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
    ttft_ms: Optional[float]
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
        ttfts = [r.ttft_ms for r in self.results if r.ttft_ms is not None]
        ttlts = [r.ttlt_ms for r in self.results]
        cached = [r.cached_tokens for r in self.results]
        ttft_mean = round(mean(ttfts), 0) if ttfts else None
        ttft_min = round(min(ttfts), 0) if ttfts else None
        ttft_max = round(max(ttfts), 0) if ttfts else None
        return {
            "ttlt_mean_ms": round(mean(ttlts), 0),
            "ttlt_min_ms": round(min(ttlts), 0),
            "ttlt_max_ms": round(max(ttlts), 0),
            "ttlt_median_ms": round(median(ttlts), 0),
            "ttft_mean_ms": ttft_mean,
            "ttft_min_ms": ttft_min,
            "ttft_max_ms": ttft_max,
            "ttft_available": bool(ttfts),
            "avg_cached_tokens": round(mean(cached), 0),
            "avg_input_tokens": round(mean([r.input_tokens for r in self.results]), 0),
            "avg_output_tokens": round(mean([r.output_tokens for r in self.results]), 0),
        }


# ---------------------------------------------------------------------------
# Qwen (DashScope OpenAI-compat)
# ---------------------------------------------------------------------------
def get_qwen_headers() -> dict:
    key = os.environ.get("DASHSCOPE_API_KEY", "")
    if not key:
        raise RuntimeError("DASHSCOPE_API_KEY not set")
    return {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
    }


def _extract_qwen_usage(usage: Optional[dict]) -> tuple[int, int, int]:
    if not usage:
        return 0, 0, 0

    input_tokens = usage.get("prompt_tokens", usage.get("input_tokens", 0)) or 0
    output_tokens = usage.get("completion_tokens", usage.get("output_tokens", 0)) or 0

    details = usage.get("prompt_tokens_details") or usage.get("input_tokens_details") or {}
    cached_tokens = details.get("cached_tokens", usage.get("cached_tokens", 0)) or 0
    return int(input_tokens), int(output_tokens), int(cached_tokens)


def _normalize_qwen_text(content) -> str:
    if content is None:
        return ""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, dict):
                parts.append(item.get("text") or item.get("content") or "")
            else:
                parts.append(str(item))
        return "".join(parts)
    return str(content)


def call_qwen(headers: dict, messages: list, stream: bool = True, enable_thinking: bool = False):
    start = time.perf_counter()
    ttft_ms = None
    chunks = []
    usage_data = {}

    payload = dict(
        model=QWEN_MODEL,
        messages=messages,
        stream=stream,
        max_tokens=300,
        enable_thinking=enable_thinking,
    )
    if stream:
        payload["stream_options"] = {"include_usage": True}

    response = requests.post(
        QWEN_CHAT_COMPLETIONS_URL,
        headers=headers,
        json=payload,
        stream=stream,
        timeout=120,
    )
    response.raise_for_status()

    if not stream:
        ttlt_ms = (time.perf_counter() - start) * 1000
        body = response.json()
        usage_data = body.get("usage", {})
        choices = body.get("choices") or []
        text = ""
        if choices:
            msg = (choices[0] or {}).get("message", {})
            text = _normalize_qwen_text(msg.get("content"))
        input_tokens, output_tokens, cached_tokens = _extract_qwen_usage(usage_data)
        return ttft_ms, ttlt_ms, input_tokens, output_tokens, cached_tokens, text

    for raw_line in response.iter_lines(decode_unicode=True):
        if not raw_line:
            continue
        if not raw_line.startswith("data:"):
            continue
        data = raw_line[len("data:"):].strip()
        if data == "[DONE]":
            break
        try:
            chunk = json.loads(data)
        except json.JSONDecodeError:
            continue

        if chunk.get("usage"):
            usage_data = chunk["usage"]

        choices = chunk.get("choices") or []
        if not choices:
            continue
        delta_obj = (choices[0] or {}).get("delta", {})
        delta = _normalize_qwen_text(delta_obj.get("content"))
        if delta:
            if ttft_ms is None:
                ttft_ms = (time.perf_counter() - start) * 1000
            chunks.append(delta)

    ttlt_ms = (time.perf_counter() - start) * 1000
    if ttft_ms is None:
        ttft_ms = ttlt_ms

    input_tokens, output_tokens, cached_tokens = _extract_qwen_usage(usage_data)
    text = "".join(chunks)
    return ttft_ms, ttlt_ms, input_tokens, output_tokens, cached_tokens, text


def run_qwen_baseline(headers, query, idx):
    msgs = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": query},
    ]
    tf, tl, inp, out, cached, text = call_qwen(headers, msgs)
    return QueryResult(idx, tf, tl, inp, out, cached, text[:120])


def run_qwen_implicit(headers, query, idx):
    msgs = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": query},
    ]
    tf, tl, inp, out, cached, text = call_qwen(headers, msgs)
    return QueryResult(idx, tf, tl, inp, out, cached, text[:120])


def run_qwen_explicit(headers, query, idx):
    msgs = [
        {
            "role": "system",
            "content": [
                {
                    "type": "text",
                    "text": SYSTEM_PROMPT,
                    "cache_control": {"type": "ephemeral"},
                }
            ],
        },
        {"role": "user", "content": query},
    ]
    tf, tl, inp, out, cached, text = call_qwen(headers, msgs)
    return QueryResult(idx, tf, tl, inp, out, cached, text[:120])


def run_qwen_explicit_no_stream(headers, query, idx):
    msgs = [
        {
            "role": "system",
            "content": [
                {
                    "type": "text",
                    "text": SYSTEM_PROMPT,
                    "cache_control": {"type": "ephemeral"},
                }
            ],
        },
        {"role": "user", "content": query},
    ]
    tf, tl, inp, out, cached, text = call_qwen(headers, msgs, stream=False, enable_thinking=False)
    return QueryResult(idx, tf, tl, inp, out, cached, text[:120])


# ---------------------------------------------------------------------------
# Gemini
# ---------------------------------------------------------------------------
def setup_gemini():
    key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY", "")
    if not key:
        raise RuntimeError("GEMINI_API_KEY not set")
    return genai.Client(api_key=key)


GEMINI_NO_THINKING_STATUS = "unknown"
GEMINI_NO_THINKING_CONFIG = genai_types.GenerateContentConfig(
    system_instruction=SYSTEM_PROMPT,
    thinking_config=genai_types.ThinkingConfig(thinking_budget=0),
    max_output_tokens=300,
)


def _extract_gemini_usage(usage_meta) -> tuple[int, int, int]:
    if not usage_meta:
        return 0, 0, 0

    prompt = getattr(usage_meta, "prompt_token_count", 0) or 0
    output = getattr(usage_meta, "candidates_token_count", 0) or 0
    cached = getattr(usage_meta, "cached_content_token_count", 0) or 0
    return int(prompt), int(output), int(cached)


def _gemini_default_config() -> genai_types.GenerateContentConfig:
    return genai_types.GenerateContentConfig(
        system_instruction=SYSTEM_PROMPT,
        max_output_tokens=300,
    )


def call_gemini(
    client: genai.Client,
    query: str,
    idx: int,
    stream: bool = True,
    config: Optional[genai_types.GenerateContentConfig] = None,
) -> QueryResult:
    start = time.perf_counter()
    ttft_ms = None
    chunks = []
    usage_meta = None

    if stream:
        response = client.models.generate_content_stream(
            model=GEMINI_MODEL,
            contents=query,
            config=config or _gemini_default_config(),
        )
    else:
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=query,
            config=config or _gemini_default_config(),
        )

    if not stream:
        ttlt_ms = (time.perf_counter() - start) * 1000
        usage_meta = getattr(response, "usage_metadata", None)
        input_tokens, output_tokens, cached_tokens = _extract_gemini_usage(usage_meta)
        text = getattr(response, "text", "") or ""
        return QueryResult(idx, None, ttlt_ms, input_tokens, output_tokens, cached_tokens, text[:120])

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

    input_tokens, output_tokens, cached_tokens = _extract_gemini_usage(usage_meta)

    text = "".join(chunks)
    return QueryResult(idx, ttft_ms, ttlt_ms, input_tokens, output_tokens, cached_tokens, text[:120])


def run_gemini_baseline(client, query, idx):
    return call_gemini(client, query, idx, config=_gemini_default_config())


def run_gemini_implicit(client, query, idx):
    return call_gemini(client, query, idx, config=_gemini_default_config())


def run_gemini_explicit(client, cached_content_name: str, query, idx):
    cfg = genai_types.GenerateContentConfig(
        cached_content=cached_content_name,
        max_output_tokens=300,
    )
    return call_gemini(client, query, idx, config=cfg)


def run_gemini_no_stream(client, query, idx):
    global GEMINI_NO_THINKING_STATUS
    if GEMINI_NO_THINKING_STATUS != "unsupported":
        try:
            qr = call_gemini(client, query, idx, stream=False, config=GEMINI_NO_THINKING_CONFIG)
            if GEMINI_NO_THINKING_STATUS == "unknown":
                GEMINI_NO_THINKING_STATUS = "accepted"
            return qr
        except Exception as e:
            if GEMINI_NO_THINKING_STATUS == "unknown":
                print(f"  [Gemini No Thinking] Config not supported, fallback to default: {e}")
            GEMINI_NO_THINKING_STATUS = "unsupported"
    return call_gemini(client, query, idx, stream=False, config=_gemini_default_config())


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
            ttft_txt = f"{qr.ttft_ms:.0f}ms" if qr.ttft_ms is not None else "N/A"
            print(f"        TTLT={qr.ttlt_ms:.0f}ms  TTFT={ttft_txt}  "
                  f"cached={qr.cached_tokens}  in={qr.input_tokens}  out={qr.output_tokens}")
        except Exception as e:
            print(f"        ERROR: {e}")
        if i < NUM_QUERIES - 1:
            time.sleep(INTER_QUERY_SLEEP)

    if result.results:
        s = result.stats()
        ttft_mean_txt = f"{s['ttft_mean_ms']:.0f}ms" if s["ttft_mean_ms"] is not None else "N/A"
        print(f"\n  → TTLT mean={s['ttlt_mean_ms']:.0f}ms  min={s['ttlt_min_ms']:.0f}ms  max={s['ttlt_max_ms']:.0f}ms  "
              f"| TTFT mean={ttft_mean_txt}  | cached avg={s['avg_cached_tokens']:.0f}")
    return result


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def run_all() -> list:
    results = []

    # --- Qwen ---
    qwen_headers = get_qwen_headers()

    results.append(run_scenario(
        lambda q, i: run_qwen_baseline(qwen_headers, q, i),
        "Baseline", "Qwen3.5-Flash",
    ))

    print("\n  [Qwen Implicit] Warmup run...")
    try:
        run_qwen_implicit(qwen_headers, QUERIES[0], -1)
    except Exception as e:
        print(f"  Warmup error: {e}")
    time.sleep(2)

    qwen_implicit_result = run_scenario(
        lambda q, i: run_qwen_implicit(qwen_headers, q, i),
        "Implicit Cache", "Qwen3.5-Flash",
    )
    results.append(qwen_implicit_result)

    print("\n  [Qwen Explicit] Warmup run...")
    try:
        run_qwen_explicit(qwen_headers, QUERIES[0], -1)
    except Exception as e:
        print(f"  Warmup error: {e}")
    time.sleep(2)

    qwen_explicit_result = run_scenario(
        lambda q, i: run_qwen_explicit(qwen_headers, q, i),
        "Explicit Cache", "Qwen3.5-Flash",
    )
    results.append(qwen_explicit_result)

    print("\n  [Qwen Explicit + No Streaming] Warmup run...")
    try:
        run_qwen_explicit_no_stream(qwen_headers, QUERIES[0], -1)
    except Exception as e:
        print(f"  Warmup error: {e}")
    time.sleep(2)
    results.append(run_scenario(
        lambda q, i: run_qwen_explicit_no_stream(qwen_headers, q, i),
        "Explicit Cache + No Streaming", "Qwen3.5-Flash",
    ))

    qwen_implicit_cached = qwen_implicit_result.stats()["avg_cached_tokens"] if qwen_implicit_result.results else 0
    qwen_explicit_cached = qwen_explicit_result.stats()["avg_cached_tokens"] if qwen_explicit_result.results else 0
    if qwen_implicit_cached > 0 or qwen_explicit_cached > 0:
        print(
            f"  [Qwen Cache Verification] Confirmed via usage cached_tokens: "
            f"implicit_avg={qwen_implicit_cached}, explicit_avg={qwen_explicit_cached}"
        )
    else:
        print(
            "  [Qwen Cache Verification] cached_tokens not reported by API for this run; "
            "cannot hard-confirm cache hits via usage fields."
        )

    # --- Gemini ---
    gemini_client = setup_gemini()

    results.append(run_scenario(
        lambda q, i: run_gemini_baseline(gemini_client, q, i),
        "Baseline", "Gemini-3.1-Flash-Lite",
    ))

    print("\n  [Gemini Implicit] Warmup run...")
    try:
        run_gemini_implicit(gemini_client, QUERIES[0], -1)
    except Exception as e:
        print(f"  Warmup error: {e}")
    time.sleep(2)

    results.append(run_scenario(
        lambda q, i: run_gemini_implicit(gemini_client, q, i),
        "Implicit Cache", "Gemini-3.1-Flash-Lite",
    ))

    # Explicit cache — needs >=4096 tokens; try and handle gracefully
    print("\n  [Gemini Explicit] Creating cached content (needs >=4096 tokens)...")
    cached_content = None
    try:
        cached_content = gemini_client.caches.create(
            model=GEMINI_MODEL,
            config=genai_types.CreateCachedContentConfig(
                system_instruction=SYSTEM_PROMPT,
                contents=[
                    {
                        "role": "user",
                        "parts": [{"text": "Cache seed for query breaking benchmark."}],
                    }
                ],
                ttl=f"{int(timedelta(minutes=10).total_seconds())}s",
            ),
        )
        print(f"  Cache created: {cached_content.name}")
        print("\n  [Gemini Explicit] Warmup run...")
        try:
            run_gemini_explicit(gemini_client, cached_content.name, QUERIES[0], -1)
        except Exception as e:
            print(f"  Warmup error: {e}")
        time.sleep(2)
        results.append(run_scenario(
            lambda q, i, cc=cached_content.name: run_gemini_explicit(gemini_client, cc, q, i),
            "Explicit Cache", "Gemini-3.1-Flash-Lite",
        ))
    except Exception as e:
        print(f"  Explicit cache creation failed: {e}")
        print("  Skipping Gemini Explicit Cache scenario.")
    finally:
        if cached_content:
            try:
                gemini_client.caches.delete(name=cached_content.name)
            except Exception:
                pass
    results.append(run_scenario(
        lambda q, i: run_gemini_no_stream(gemini_client, q, i),
        "No Thinking + No Streaming", "Gemini-3.1-Flash-Lite",
    ))

    return results


def print_table(results: list):
    print("\n\n" + "="*80)
    print("RESULTS (primary metric: TTLT = time-to-last-token)")
    print("="*80)
    print(f"{'Model':<24} {'Scenario':<30} {'TTLT mean':>10} {'TTLT min':>9} {'TTLT max':>9} {'TTFT mean':>10} {'Cached':>8}")
    print("-"*80)
    for r in results:
        if not r.results:
            continue
        s = r.stats()
        ttft_mean_txt = f"{s['ttft_mean_ms']:.0f}ms" if s["ttft_mean_ms"] is not None else "N/A"
        print(f"{r.model:<24} {r.scenario:<30} "
              f"{s['ttlt_mean_ms']:>9.0f}ms {s['ttlt_min_ms']:>8.0f}ms "
              f"{s['ttlt_max_ms']:>8.0f}ms {ttft_mean_txt:>10} "
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
            if r.scenario in ("Baseline", "No Thinking + No Streaming"):
                cost = (avg_in * p["input_no_cache"] + avg_out * p["output"]) / 1e6
            elif r.scenario == "Implicit Cache":
                cost = (avg_uncached * p["input_no_cache"] + avg_cached * p["implicit_hit"] + avg_out * p["output"]) / 1e6
            else:
                cost = (avg_uncached * p["input_no_cache"] + avg_cached * p["explicit_hit"] + avg_out * p["output"]) / 1e6

        print(f"{r.model:<22} {r.scenario:<18} ${cost * DAILY:.4f}/day")
    print("="*60)


def main(output_path: str = "benchmark_cache_results.json"):
    print(f"Benchmark: Implicit vs Explicit Cache")
    print(f"Models: {QWEN_MODEL} | {GEMINI_MODEL}")
    print(f"Queries: {NUM_QUERIES} per scenario | Sleep: {INTER_QUERY_SLEEP}s between queries\n")

    all_results = run_all()
    print_table(all_results)
    save_json(all_results, path=output_path)
    print(f"Gemini no-thinking toggle status: {GEMINI_NO_THINKING_STATUS}")
    print_cost(all_results)
    print("\nDone.")


if __name__ == "__main__":
    main()
