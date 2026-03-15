"""
Benchmark: No Streaming + No Thinking + Explicit Cache
Compare structured output formats: JSON array vs QP-Lines

Providers:
  1) Gemini 3.1 Flash Lite  — explicit cache via CachedContent API
  2) Qwen 3.5 Flash         — explicit cache via cache_control marker (OpenAI-compat)

Warm-up strategy:
  - Each scenario runs WARMUP_RUNS calls before measured runs.
  - Warmup run 1 creates/seeds the cache; warmup run 2 confirms the cache hit.
  - Only post-warmup calls are included in TTLT statistics.
"""

from __future__ import annotations

import json
import os
import time
from dataclasses import asdict, dataclass
from datetime import timedelta
from pathlib import Path
from statistics import mean
from typing import Any, Callable

import requests
from dotenv import load_dotenv
from google import genai
from google.genai import types as genai_types

load_dotenv(Path(__file__).resolve().parent / ".env", override=False)

GEMINI_MODEL = "gemini-3.1-flash-lite-preview"
# DashScope explicit cache only supports model aliases (not pinned date-versioned IDs).
# See: https://www.alibabacloud.com/help/en/model-studio/context-cache#supported-models
QWEN_MODEL = "qwen3.5-flash"
QWEN_URL = "https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions"
MAX_OUTPUT_TOKENS = 300
# Warmup run 1 creates the cache, run 2 confirms hit before measured runs begin.
WARMUP_RUNS = 2
SLEEP_SECONDS = 2.0

QUERIES = [
    "Tôi muốn mua xe và mua nhà trong năm nay, nên vay ngân hàng nào và cần chuẩn bị giấy tờ gì?",
    "So sánh lãi suất tiết kiệm 6 tháng và 12 tháng tại Vietcombank và Techcombank",
    "Bảo hiểm nhân thọ Prudential và Manulife khác nhau thế nào về phí và quyền lợi bồi thường?",
    "Tôi nên đầu tư vào vàng, cổ phiếu VN30 hay gửi tiết kiệm ngân hàng với số tiền 100 triệu?",
    "Tỷ giá USD/VND và lãi suất cơ bản của NHNN ảnh hưởng thế nào đến lãi suất vay ngân hàng?",
]

# Minimum cacheable length: 1024 tokens (Qwen explicit), 1024 tokens (Gemini).
# BASE_PROMPT alone is short; PADDING repeats domain examples to cross the threshold.
BASE_PROMPT = """Bạn là AI agent query breaking cho RAG tài chính Việt Nam.
Tách câu hỏi thành các sub-query độc lập, tối đa 5, giữ nguyên tiếng Việt, không giải thích thêm."""

PADDING = """
Domain tài chính Việt Nam cần xử lý bao gồm các lĩnh vực chính sau đây với các khía cạnh quan trọng cần được phân tích và xử lý trong quá trình query breaking để đảm bảo độ chính xác và đầy đủ thông tin cho người dùng cuối cùng trong hệ thống RAG tài chính thông minh. Các domain này bao gồm nhiều khía cạnh phức tạp cần được tách thành các sub-query nguyên tử để tối ưu hóa quá trình truy vấn và retrieval trong pipeline RAG hiện đại với độ trễ thấp và độ chính xác cao:
- Vay mua nhà đất bất động sản: lãi suất ưu đãi các ngân hàng, hạn mức tín dụng tối đa, hồ sơ thủ tục pháp lý, ngân hàng hỗ trợ tốt nhất, thời gian xét duyệt khoản vay trung bình, điều kiện đảm bảo tài sản thế chấp, chương trình hỗ trợ lãi suất của chính phủ, so sánh ngân hàng thương mại và ngân hàng chính sách.
- Vay mua xe ô tô xe máy: điều kiện vay vốn cơ bản, thủ tục đăng ký đăng kiểm, lãi suất ngân hàng cạnh tranh, hồ sơ cần thiết đầy đủ, thời gian giải ngân nhanh chóng, chương trình ưu đãi đặc biệt theo mùa, bảo hiểm xe bắt buộc và tự nguyện, phí trước bạ và đăng ký.
- Bảo hiểm nhân thọ và phi nhân thọ: phí bảo hiểm hàng năm chi tiết, điều khoản hợp đồng quan trọng, quyền lợi bồi thường tối đa, so sánh nhà cung cấp uy tín, thủ tục khiếu nại và giải quyết, loại trừ trách nhiệm bảo hiểm, thời gian chờ và khám sức khỏe.
- Đầu tư tài chính cá nhân: vàng miếng SJC và PNJ, cổ phiếu VN30 và HNX30, trái phiếu chính phủ và doanh nghiệp, gửi tiết kiệm ngân hàng kỳ hạn, rủi ro thị trường biến động, lợi nhuận kỳ vọng hàng năm, chiến lược phân bổ tài sản, thuế thu nhập từ đầu tư.
- Thẻ tín dụng quốc tế: phí thường niên các hạng thẻ, ưu đãi tích điểm và hoàn tiền, điều kiện mở thẻ chi tiết, so sánh ngân hàng phát hành, hạn mức chi tiêu tối đa, lãi suất quá hạn và phí phạt, bảo mật và bảo hiểm thẻ, chương trình khách hàng thân thiết.
- Ngoại tệ và tỷ giá hối đoái: tỷ giá USD/VND và EUR/VND cập nhật, biến động ngắn hạn và dài hạn, thời điểm mua bán tối ưu trong ngày, dự báo thị trường ngoại hối, phí giao dịch ngân hàng, hạn mức mua ngoại tệ, quy định của ngân hàng nhà nước.
- Thuế thu nhập cá nhân: quyết toán thuế năm cuối cùng, khấu trừ tại nguồn từ lương, ngưỡng chịu thuế theo bậc, đa nguồn thu nhập phức tạp, giảm trừ gia cảnh bản thân và người phụ thuộc, thuế thu nhập từ đầu tư và chuyển nhượng, thủ tục hoàn thuế và nộp thuế.
- Kế hoạch tài chính cá nhân: ngân sách hàng tháng chi tiết, tiết kiệm dài hạn cho mục tiêu, quỹ dự phòng khẩn cấp tối thiểu, phân bổ thu nhập hợp lý các khoản, đầu tư giáo dục và sức khỏe, bảo hiểm và phòng ngừa rủi ro, kế hoạch nghỉ hưu sớm.
- Tín dụng CIC và điểm tín dụng: tra cứu lịch sử tín dụng trực tuyến, điểm tín dụng cá nhân hiện tại, ảnh hưởng đến vay vốn ngân hàng trực tiếp, cách cải thiện điểm số nhanh chóng, xóa nợ xấu và cập nhật thông tin, thời gian lưu trữ thông tin tín dụng, dịch vụ tư vấn tín dụng chuyên nghiệp.
- Bảo hiểm xã hội và hưu trí: quyền lợi bảo hiểm y tế và thất nghiệp, mức lương hưu tính toán theo thâm niên, quỹ hưu trí tự nguyện linh hoạt, so sánh phương án đầu tư hưu trí, đóng bảo hiểm tự nguyện và bắt buộc, thủ tục hưởng chế độ ốm đau và thai sản, chính sách hỗ trợ người cao tuổi.
"""

FORMAT_JSON = """Output format (bắt buộc):
Chỉ trả về JSON array thuần, không markdown, không giải thích.
Ví dụ: ["sub-query 1", "sub-query 2", "sub-query 3"]"""

FORMAT_QP = """Output format (bắt buộc):
- Dòng 1: COUNT:<n>
- Mỗi dòng tiếp theo: Q:<sub-query>
Không markdown, không text khác ngoài format trên.
Ví dụ:
COUNT:3
Q:Lãi suất vay mua xe tại các ngân hàng Việt Nam
Q:Hồ sơ vay mua xe cần giấy tờ gì
Q:Điều kiện vay mua xe tại Vietcombank"""


def build_prompt(fmt: str) -> str:
    # Thêm extra padding để đảm bảo >1024 tokens cho Gemini
    EXTRA_PADDING = "\n" + "Thêm chi tiết về các khía cạnh tài chính cá nhân và doanh nghiệp tại Việt Nam bao gồm quản lý dòng tiền, phân tích rủi ro, kế hoạch đầu tư dài hạn, đa dạng hóa danh mục, tối ưu thuế, bảo hiểm rủi ro, quỹ hưu trí, giáo dục tài chính, fintech và ngân hàng số, blockchain và tiền điện tử, bất động sản, chứng khoán, trái phiếu, quỹ mở, ETF, và các công cụ tài chính phái sinh." * 2
    return f"{BASE_PROMPT}\n{PADDING}{EXTRA_PADDING}\n{fmt}"


@dataclass
class QueryResult:
    idx: int
    ttlt_ms: float
    input_tokens: int
    output_tokens: int
    cached_tokens: int
    parse_ok: bool
    parsed_count: int
    text_preview: str


@dataclass
class ScenarioSummary:
    provider: str
    model: str
    name: str
    cache_mode: str
    warmup_runs: int
    ttlt_mean_ms: float
    ttlt_min_ms: float
    ttlt_max_ms: float
    avg_input_tokens: float
    avg_output_tokens: float
    avg_cached_tokens: float
    parse_success_rate: float


def parse_json_output(text: str) -> tuple[bool, int]:
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return False, 0
    ok = isinstance(data, list) and all(isinstance(x, str) and x.strip() for x in data)
    return (ok, len(data) if ok else 0)


def parse_qp_output(text: str) -> tuple[bool, int]:
    lines = [x.strip() for x in text.splitlines() if x.strip()]
    if not lines or not lines[0].startswith("COUNT:"):
        return False, 0
    try:
        expected = int(lines[0].split(":", 1)[1].strip())
    except ValueError:
        return False, 0
    actual = len([x for x in lines[1:] if x.startswith("Q:") and x[2:].strip()])
    return (expected == actual, actual)


# ---------------------------------------------------------------------------
# Gemini
# ---------------------------------------------------------------------------

def gemini_call(
    client: genai.Client,
    query: str,
    cfg: genai_types.GenerateContentConfig,
) -> tuple[float, int, int, int, str]:
    start = time.perf_counter()
    res = client.models.generate_content(model=GEMINI_MODEL, contents=query, config=cfg)
    ttlt = (time.perf_counter() - start) * 1000
    usage = getattr(res, "usage_metadata", None)
    in_t = int(getattr(usage, "prompt_token_count", 0) or 0) if usage else 0
    out_t = int(getattr(usage, "candidates_token_count", 0) or 0) if usage else 0
    c_t = int(getattr(usage, "cached_content_token_count", 0) or 0) if usage else 0
    return ttlt, in_t, out_t, c_t, (getattr(res, "text", "") or "").strip()


# ---------------------------------------------------------------------------
# Qwen — explicit cache via cache_control marker (OpenAI-compat)
#
# DashScope explicit cache flow:
#   1. Warmup call 1: cache_control marker triggers cache creation
#      → usage.prompt_tokens_details.cache_creation_input_tokens > 0
#   2. Warmup call 2: cache hit confirmed
#      → usage.prompt_tokens_details.cached_tokens > 0
#   3. Measured calls: all should be cache hits
# ---------------------------------------------------------------------------

def qwen_call(
    headers: dict[str, str],
    query: str,
    prompt: str,
) -> tuple[float, int, int, int, str, int]:
    """Returns (ttlt_ms, input_tokens, output_tokens, cached_tokens, text, cache_creation_tokens)."""
    payload = {
        "model": QWEN_MODEL,
        "messages": [
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",
                        "text": prompt,
                        # explicit cache marker — DashScope creates a cache block on first call
                        "cache_control": {"type": "ephemeral"},
                    }
                ],
            },
            {"role": "user", "content": query},
        ],
        "stream": False,
        "max_tokens": MAX_OUTPUT_TOKENS,
        "enable_thinking": False,
    }
    start = time.perf_counter()
    res = requests.post(QWEN_URL, headers=headers, json=payload, timeout=120)
    res.raise_for_status()
    ttlt = (time.perf_counter() - start) * 1000

    body = res.json()
    usage = body.get("usage", {})
    in_t = int(usage.get("prompt_tokens", usage.get("input_tokens", 0)) or 0)
    out_t = int(usage.get("completion_tokens", usage.get("output_tokens", 0)) or 0)
    # DashScope returns cached_tokens under usage.prompt_tokens_details.cached_tokens
    details = usage.get("prompt_tokens_details") or {}
    c_t = int(details.get("cached_tokens", 0) or 0)
    creation_t = int(details.get("cache_creation_input_tokens", 0) or 0)

    choices = body.get("choices") or []
    text = (((choices[0] or {}).get("message", {}) or {}).get("content", "") if choices else "")
    return ttlt, in_t, out_t, c_t, (text or "").strip(), creation_t


# ---------------------------------------------------------------------------
# Generic scenario runner
# ---------------------------------------------------------------------------

def run_scenario(
    provider: str,
    model: str,
    name: str,
    cache_mode: str,
    call_fn: Callable[[str], tuple[float, int, int, int, str]],
    parser_fn: Callable[[str], tuple[bool, int]],
) -> dict[str, Any]:
    print(f"\n{'=' * 84}")
    print(f"{provider} | {name}")
    print(f"{'=' * 84}")
    print(f"Warm-up: {WARMUP_RUNS} run(s) [run 1 creates cache, run 2 confirms hit]")

    for i in range(WARMUP_RUNS):
        try:
            result = call_fn(QUERIES[0])
            ttlt_w = result[0]
            c_t_w = result[3]
            creation_t_w = result[5] if len(result) > 5 else 0
            if creation_t_w > 0:
                print(f"  warmup {i + 1}/{WARMUP_RUNS}: ok — cache CREATED ({creation_t_w} tokens, TTLT={ttlt_w:.0f}ms)")
            elif c_t_w > 0:
                print(f"  warmup {i + 1}/{WARMUP_RUNS}: ok — cache HIT ({c_t_w} cached tokens, TTLT={ttlt_w:.0f}ms)")
            else:
                print(f"  warmup {i + 1}/{WARMUP_RUNS}: ok — TTLT={ttlt_w:.0f}ms  *** cached_tokens=0, cache_creation=0 ***")
        except Exception as exc:
            print(f"  warmup {i + 1}/{WARMUP_RUNS}: error -> {exc}")
        time.sleep(1.0)

    rows: list[QueryResult] = []
    for i, q in enumerate(QUERIES):
        result = call_fn(q)
        ttlt, in_t, out_t, c_t = result[0], result[1], result[2], result[3]
        text = result[4]
        ok, count = parser_fn(text)
        _ = result[5] if len(result) > 5 else None  # creation_t (not used in measured rows)
        rows.append(QueryResult(i, ttlt, in_t, out_t, c_t, ok, count, text[:180]))
        print(
            f"  [{i + 1}/{len(QUERIES)}] TTLT={ttlt:.0f}ms "
            f"in={in_t} out={out_t} cached={c_t} parse_ok={ok}"
        )
        if i < len(QUERIES) - 1:
            time.sleep(SLEEP_SECONDS)

    summary = ScenarioSummary(
        provider=provider,
        model=model,
        name=name,
        cache_mode=cache_mode,
        warmup_runs=WARMUP_RUNS,
        ttlt_mean_ms=round(mean([x.ttlt_ms for x in rows]), 1),
        ttlt_min_ms=round(min([x.ttlt_ms for x in rows]), 1),
        ttlt_max_ms=round(max([x.ttlt_ms for x in rows]), 1),
        avg_input_tokens=round(mean([x.input_tokens for x in rows]), 1),
        avg_output_tokens=round(mean([x.output_tokens for x in rows]), 1),
        avg_cached_tokens=round(mean([x.cached_tokens for x in rows]), 1),
        parse_success_rate=round(
            100.0 * mean([1.0 if x.parse_ok else 0.0 for x in rows]), 1
        ),
    )
    return {"summary": asdict(summary), "queries": [asdict(x) for x in rows]}


# ---------------------------------------------------------------------------
# Provider runners
# ---------------------------------------------------------------------------

def run_gemini(client: genai.Client) -> list[dict[str, Any]]:
    p_json = build_prompt(FORMAT_JSON)
    p_qp = build_prompt(FORMAT_QP)

    print("\n[Gemini] Creating explicit caches (CachedContent API)...")
    ttl_s = f"{int(timedelta(minutes=10).total_seconds())}s"
    cache_json = client.caches.create(
        model=GEMINI_MODEL,
        config=genai_types.CreateCachedContentConfig(
            system_instruction=p_json,
            contents=[{"role": "user", "parts": [{"text": "cache seed json"}]}],
            ttl=ttl_s,
        ),
    )
    cache_qp = client.caches.create(
        model=GEMINI_MODEL,
        config=genai_types.CreateCachedContentConfig(
            system_instruction=p_qp,
            contents=[{"role": "user", "parts": [{"text": "cache seed qp"}]}],
            ttl=ttl_s,
        ),
    )
    print(f"  cache JSON : {cache_json.name}")
    print(f"  cache QP   : {cache_qp.name}")

    try:
        cfg_json = genai_types.GenerateContentConfig(
            cached_content=cache_json.name,
            max_output_tokens=MAX_OUTPUT_TOKENS,
            thinking_config=genai_types.ThinkingConfig(thinking_budget=0),
        )
        cfg_qp = genai_types.GenerateContentConfig(
            cached_content=cache_qp.name,
            max_output_tokens=MAX_OUTPUT_TOKENS,
            thinking_config=genai_types.ThinkingConfig(thinking_budget=0),
        )
        results = [
            run_scenario(
                "gemini", GEMINI_MODEL,
                "Explicit + No Streaming + No Thinking + JSON", "explicit",
                lambda q, c=cfg_json: gemini_call(client, q, c),
                parse_json_output,
            ),
            run_scenario(
                "gemini", GEMINI_MODEL,
                "Explicit + No Streaming + No Thinking + QP-Lines", "explicit",
                lambda q, c=cfg_qp: gemini_call(client, q, c),
                parse_qp_output,
            ),
        ]
    finally:
        client.caches.delete(name=cache_json.name)
        client.caches.delete(name=cache_qp.name)
        print("\n[Gemini] Caches deleted.")

    return results


def run_qwen(dashscope_key: str) -> list[dict[str, Any]]:
    """
    Qwen explicit cache via cache_control marker (OpenAI-compat).
    First warmup call creates the cache block; second warmup confirms hit.
    Minimum cacheable prefix: 1024 tokens.
    """
    headers = {
        "Authorization": f"Bearer {dashscope_key}",
        "Content-Type": "application/json",
    }
    p_json = build_prompt(FORMAT_JSON)
    p_qp = build_prompt(FORMAT_QP)

    print("\n[Qwen] Using cache_control marker for explicit cache (OpenAI-compat).")
    print("  Warmup run 1 → cache creation | Warmup run 2 → cache hit confirmation.")

    return [
        run_scenario(
            "qwen", QWEN_MODEL,
            "Explicit + No Streaming + No Thinking + JSON", "explicit",
            lambda q, p=p_json: qwen_call(headers, q, p),
            parse_json_output,
        ),
        run_scenario(
            "qwen", QWEN_MODEL,
            "Explicit + No Streaming + No Thinking + QP-Lines", "explicit",
            lambda q, p=p_qp: qwen_call(headers, q, p),
            parse_qp_output,
        ),
    ]


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main(output_path: str = "benchmark_results.json") -> None:
    scenarios: list[dict[str, Any]] = []
    missing: list[str] = []

    gem_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if gem_key:
        scenarios.extend(run_gemini(genai.Client(api_key=gem_key)))
    else:
        missing.append("GEMINI_API_KEY (or GOOGLE_API_KEY)")

    q_key = os.environ.get("DASHSCOPE_API_KEY")
    if q_key:
        scenarios.extend(run_qwen(q_key))
    else:
        missing.append("DASHSCOPE_API_KEY")

    if not scenarios:
        raise RuntimeError("No provider can run. Missing keys: " + ", ".join(missing))

    out: dict[str, Any] = {
        "meta": {
            "providers": sorted({x["summary"]["provider"] for x in scenarios}),
            "queries": len(QUERIES),
            "warmup_runs_per_scenario": WARMUP_RUNS,
            "streaming": False,
            "thinking": "disabled",
            "cache_mode": {
                "gemini": "CachedContent API (explicit)",
                "qwen": "cache_control marker in system message (explicit, OpenAI-compat)",
            },
            "missing_keys": missing,
        },
        "scenarios": scenarios,
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"\nSaved -> {output_path}")

    print("\n--- Summary ---")
    for s in scenarios:
        sm = s["summary"]
        print(
            f"  {sm['provider']:8} | {sm['name'][:55]:<55} | "
            f"TTLT={sm['ttlt_mean_ms']:>7.1f}ms "
            f"out={sm['avg_output_tokens']:>5.1f} "
            f"cached={sm['avg_cached_tokens']:>6.1f} "
            f"parse={sm['parse_success_rate']:>5.1f}%"
        )


if __name__ == "__main__":
    main()
