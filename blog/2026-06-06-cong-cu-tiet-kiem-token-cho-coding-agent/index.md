---
title: "Headroom, RTK, Caveman: Các Công Cụ Tiết Kiệm Token Cho Coding Agent"
authors: [manhpt]
tags: [coding-agent, cost-optimization, ai-tools, llm, optimization, vietnamese, technical]
date: 2026-06-06
description: "Phân tích các công cụ tiết kiệm token cho coding agent như Headroom, RTK, LeanCTX và Caveman: dùng ở đâu, lợi ích, rủi ro."
---

Coding agent đang bước vào giai đoạn mà chi phí không chỉ nằm ở model nào rẻ hơn, mà ở việc **agent nhìn thấy bao nhiêu thứ không cần thiết**. Một lần `pytest` dài, một `git diff` quá rộng, một log Kubernetes ồn ào, một file `CLAUDE.md` phình dần qua nhiều tháng — tất cả đều biến thành input tokens, rồi tiếp tục bị kéo theo ở các vòng sau.

Vì vậy, vài tháng gần đây xuất hiện một lớp công cụ mới: không thay model, không thay IDE, mà đứng giữa agent và context để cắt bớt token. Bài này tập trung vào đúng nhóm đó: **Headroom, RTK, LeanCTX và Caveman**.

**Tóm tắt giải pháp**: nếu agent tốn token vì test/log/git output, bắt đầu với **RTK**. Nếu agent đọc file quá rộng trong repo lớn, thử **LeanCTX hoặc jCodeMunch**. Nếu workflow có nhiều RAG/API/log/multi-agent context, nghiên cứu **Headroom**. Nếu agent dài dòng, dùng **Caveman**. Và luôn nhớ: với security audit, repo không tin cậy, hoặc lỗi khó debug, hãy quay về raw output.

<!-- truncate -->

## Tóm Tắt Nhanh

Nếu chỉ muốn chọn nhanh, dùng bảng này:

| Công cụ | Tối ưu lớp nào | Hợp nhất khi | Cẩn thận với |
|---|---|---|---|
| **RTK** | Terminal/shell output | Agent hay chạy `git`, test, build, Docker, Kubernetes | Có thể che mất chi tiết lỗi; từng có advisory về project-local filters |
| **Headroom** | Tool output, logs, JSON, RAG, file reads, proxy/MCP | Session nhiều tool output, nhiều agent, nhiều context lặp | Thêm proxy/runtime; không phải request nào cũng giảm mạnh |
| **Caveman** | Output style, context/memory files, coding-agent CLI riêng | Agent quá dài dòng; muốn giảm assistant output và nén rules | Không giảm reasoning/tool/input tokens nhiều như headline |
| **LeanCTX** | MCP/context layer: reads, shell, search, memory | Repo vừa/lớn, cần một context layer tổng hợp | Surface area lớn, docs thay đổi nhanh |
| **jCodeMunch MCP** | Symbol-level retrieval, repo maps, AST/search bundles | Repo lớn, agent hay đọc nguyên file | Có thể miss context ngoài symbol; setup phức tạp hơn |

Điểm chung: các tool này **không làm agent thông minh hơn**. Chúng làm agent ăn ít context rác hơn. Cũng giống ăn kiêng: có thể khỏe hơn, nhưng nếu cắt nhầm chất dinh dưỡng thì ngất.

## Vì Sao Coding Agent Đốt Token Khác Chatbot?

Chatbot thường đốt token ở prompt và câu trả lời. Coding agent đốt token ở cả vòng lặp hành động:

```text
User task
  -> agent đọc rules/system prompt/tools
  -> chạy grep/cat/test/git
  -> terminal output đi vào context
  -> agent sửa file
  -> chạy test lại
  -> log mới đi vào context
  -> agent tóm tắt/commit/PR
```

Phần tốn nhất thường không phải câu trả lời cuối cùng. Nó là **input tokens từ tool output và lịch sử context**. Một nghiên cứu gần đây về token consumption trong agentic coding tasks cũng ghi nhận agentic tasks đắt hơn code chat/code reasoning rất nhiều, input tokens là nguồn chi phí lớn, và token usage giữa các lần chạy có thể biến động mạnh.

Đây là lý do RTK/Headroom/Caveman đáng chú ý: mỗi tool đánh vào một đoạn khác nhau của pipeline.

## 1. RTK: Rust Token Killer Cho Terminal Output

**RTK** là viết tắt của **Rust Token Killer**. Repo chính thức mô tả nó là CLI proxy giúp giảm token consumption 60-90% trên các dev commands phổ biến. Cách hiểu đơn giản: thay vì để agent nhìn raw output từ shell, RTK lọc nó thành bản ngắn hơn nhưng vẫn giữ tín hiệu quan trọng.

Ví dụ agent chạy:

```bash
pytest
git diff
docker logs api
gh pr checks
cargo test
```

Với RTK, command có thể được rewrite thành:

```bash
rtk pytest
rtk git diff
rtk docker logs api
rtk gh pr checks
rtk cargo test
```

Agent nhận output đã compact: failed tests, traceback chính, summary, file liên quan, đường dẫn tới raw log nếu cần.

### Cách Dùng

Cài đặt:

```bash
curl -fsSL https://raw.githubusercontent.com/rtk-ai/rtk/master/install.sh | sh
```

Khởi tạo cho Claude Code:

```bash
rtk init -g
```

Cho Codex:

```bash
rtk init -g --codex
```

Cho Cursor/Gemini/OpenCode/Windsurf/Cline:

```bash
rtk init -g --agent cursor
rtk init -g --gemini
rtk init -g --opencode
rtk init -g --agent windsurf
rtk init --agent cline
```

Xem thống kê:

```bash
rtk gain
rtk discover
rtk session
```

Theo README hiện tại, RTK hỗ trợ nhiều agent: Claude Code, GitHub Copilot, Cursor, Gemini CLI, Codex, Windsurf, Cline/Roo Code, OpenCode, OpenClaw, Pi, Hermes, Kilo Code, Google Antigravity. Cơ chế khác nhau theo agent: hook, plugin, hoặc rule/instruction fallback.

### Ưu Điểm

- **Đánh đúng pain point nhất**: terminal output là nguồn token rác lớn trong coding agent.
- **Không cần đổi model**: vẫn dùng Claude Code, Codex, Cursor, OpenCode như cũ.
- **Có analytics**: `rtk gain` giúp nhìn savings thật, thay vì tin cảm giác.
- **Có cơ chế raw output fallback**: khi command fail, RTK có thể lưu output đầy đủ để agent đọc lại.
- **Tốt cho repo có test/build/log ồn ào**: JS/TS, Rust, Python, Docker, Kubernetes, GitHub Actions.

### Nhược Điểm

- **Có thể cắt mất manh mối quan trọng**. Debug race condition, flaky test, security audit, hoặc log format đặc biệt đôi khi cần raw output.
- **Không bắt mọi tool call**. Với Claude Code, built-in `Read`, `Grep`, `Glob` không nhất thiết đi qua bash hook.
- **Hook phụ thuộc môi trường**. Windows native bị hạn chế; WSL/Linux/macOS phù hợp hơn.
- **Agent có thể tin output đã lọc như sự thật tuyệt đối**. Đây là rủi ro lớn: tool tối ưu token đang trở thành "mắt" của agent.
- **Cần theo dõi security advisory**. Đã có advisory `GHSA-fvvm-949w-qj4w` / `CVE-2026-45792` về việc RTK tin project-local filter configuration, cho phép repo độc hại can thiệp output mà agent nhìn thấy. Nên dùng RTK `>=0.32.0` hoặc bản mới nhất, yêu cầu explicit trust với project-local config, và re-review filter hash khi config đổi.

### Khi Nào Nên Dùng RTK?

Dùng RTK nếu:

- agent thường chạy test/build/grep/log;
- bạn dùng Claude Code/Codex/OpenCode nhiều qua terminal;
- context hay phình vì output dài;
- bạn muốn đo savings theo session.

Không nên bật mù nếu:

- đang audit bảo mật;
- đang debug lỗi hiếm;
- repo đến từ nguồn không tin cậy;
- command output cần giữ nguyên từng dòng.

Quy tắc thực tế: **RTK mặc định cho routine dev, raw output cho security/debug khó**.

## 2. Headroom: Compression Layer Cho Tool Output, Logs, RAG Và Multi-Agent Context

Nếu RTK tối ưu shell output, **Headroom** tham vọng rộng hơn: nó là context optimization layer đặt trước LLM. Headroom có thể chạy như library, local proxy, MCP server, wrapper cho coding agents, hoặc integration trong LangChain/LiteLLM/Vercel AI SDK/Strands.

Repo `chopratejas/headroom` mô tả các mode chính:

- Python/TypeScript library: `compress(messages)`;
- proxy local: `headroom proxy --port 8787`;
- agent wrapper: `headroom wrap claude|codex|cursor|aider|copilot`;
- MCP server: `headroom_compress`, `headroom_retrieve`, `headroom_stats`;
- cross-agent memory và reversible compression.

### Cách Dùng

Python:

```bash
pip install "headroom-ai[all]"
```

Node/TypeScript:

```bash
npm install headroom-ai
```

Proxy local:

```bash
headroom proxy --port 8787
ANTHROPIC_BASE_URL=http://localhost:8787 claude
OPENAI_BASE_URL=http://localhost:8787/v1 your-app
```

Wrapper:

```bash
headroom wrap claude
headroom wrap codex
headroom perf
```

### Headroom Tối Ưu Gì?

Headroom không chỉ truncate. Nó route content theo loại:

- JSON/API response: nén cấu trúc, giữ field quan trọng;
- logs: giữ lỗi/outlier, bỏ progress/noise;
- code: AST-aware compression hoặc passthrough khi cần an toàn;
- RAG chunks: score và fit context;
- repeated context: align prefix để cache dễ hit;
- multi-agent context: shared compressed memory.

Điểm đáng khen là docs của Headroom không chỉ đưa số headline 60-95%. Benchmark docs cũng thừa nhận median compression ngoài thực tế có thể chỉ khoảng 4.8% vì nhiều request là short conversational turns. Savings lớn xuất hiện ở heavy tool-use sessions: logs, JSON, file reads, RAG, API results.

### Ưu Điểm

- **Rộng hơn RTK**: không chỉ terminal output, mà cả RAG, API, file reads, framework SDK.
- **Nhiều integration**: proxy, SDK, MCP, wrapper, LiteLLM, LangChain, Vercel AI SDK.
- **Local-first** theo mô tả dự án: pipeline chạy local, data ở lại máy/dev env.
- **Có reversible compression/CCR**: bản gốc có thể retrieve lại thay vì mất hẳn.
- **Hợp multi-agent**: shared compressed context, memory, dedup giữa Claude/Codex/Gemini.

### Nhược Điểm

- **Thêm một proxy/runtime vào đường đi request**: phải quản lý auth keys, latency, logs, rollback.
- **Không phải lúc nào cũng giảm mạnh**: short chat hoặc code edit đang active thường không nén nhiều.
- **TypeScript SDK vẫn phụ thuộc proxy local** theo docs, không phải pure Node pipeline hoàn toàn.
- **Compression đúng là khó**: nếu compressor hiểu sai intent, agent có thể mất context quan trọng.
- **Cần observability**: phải đo hit/miss/savings/quality, không chỉ nhìn số token giảm.

### Headroom Desktop

Có một dự án riêng là **Headroom Desktop** (`gglucass/headroom-desktop`, website `extraheadroom.com`) nhắm vào trải nghiệm Claude Code/macOS. Nó bundle Headroom và RTK, tự cài hook vào Claude Code. Bài này coi nó là packaging layer, còn Headroom OSS là engine/library/proxy rộng hơn.

### Khi Nào Nên Dùng Headroom?

Dùng Headroom nếu:

- bạn có nhiều agent hoặc nhiều framework;
- app có RAG/log/API output lớn;
- muốn proxy/OpenAI-compatible layer;
- muốn memory/dedup/retrieval lại bản gốc;
- cần tối ưu ở tầng app, không chỉ CLI.

Nếu chỉ muốn giảm output của `pytest`/`git diff`, RTK đơn giản hơn.

## 3. LeanCTX: Context Layer Kiểu "Một Tool Làm Nhiều Việc"

**LeanCTX** là một context layer viết bằng Rust cho AI coding tools. Nó kết hợp nhiều thứ trong cùng một hệ thống: MCP tools, shell hooks, file read compression, search, project graph, session memory, cache và dashboard.

Nếu RTK là "lọc terminal output", Headroom là "proxy/context compression", thì LeanCTX giống một **hệ điều hành nhỏ cho context**: agent đọc file qua `ctx_read`, tìm kiếm qua context-aware tools, dùng shell output compression, và tái sử dụng cached reads.

### Nó Tối Ưu Gì?

Theo docs chính thức, LeanCTX tập trung vào:

- file reads với các mode AST-aware như `map`, `signatures`, `entropy`, `aggressive`;
- line-range reads;
- shell hook compression cho `git`, `npm`, `cargo`, `docker`, test runners, logs;
- MCP context/project graph;
- session memory và repeated context cache;
- cấu hình `minimal_overhead` cho Codex/CI-style pipelines.

Các trang docs claim 60-90% savings mỗi read và có thể tới khoảng 99% với cached re-reads. Như mọi số liệu trong bài này, nên đọc là **project-authored benchmark**, chưa phải benchmark độc lập trên repo của bạn.

### Ưu Điểm

- **Bao phủ rộng**: file reads, shell, search, memory, cache.
- **Hợp repo lớn**: agent không cần đọc cả file nếu chỉ cần signatures/map.
- **Local-first/Rust-based**: phù hợp người muốn CLI/context layer nhanh.
- **Có MCP surface**: dễ gắn vào Claude Code/Codex/Cursor/Gemini/OpenCode nếu agent hỗ trợ MCP/rules.

### Nhược Điểm

- **Surface area lớn**: càng nhiều tool, càng nhiều thứ phải hiểu và debug.
- **Agent compliance matters**: nếu agent không dùng `ctx_read` mà cứ `cat`, savings mất.
- **Docs/version drift**: các trang chính thức có chỗ nói số lượng MCP tools khác nhau, dấu hiệu dự án đang phát triển nhanh.
- **Cần policy rõ**: security/debug task phải có đường đọc raw.

### Khi Nào Nên Dùng LeanCTX?

Dùng LeanCTX nếu bạn muốn một context layer tổng hợp cho repo vừa/lớn, nơi agent hay:

- đọc đi đọc lại cùng file;
- search rộng;
- chạy shell commands;
- cần memory qua nhiều session;
- cần dashboard/budget.

Nếu chỉ có một pain point hẹp, ví dụ `pytest` output quá dài, RTK hoặc một script lọc output tự viết có thể đơn giản hơn.

## 4. Caveman: Giảm Lời Thừa Của Agent

**Caveman** đi theo hướng khác: không nén tool output trước model, mà ép agent **nói ít hơn**. Repo chính `JuliusBrussee/caveman` mô tả nó là skill/plugin cho Claude Code và nhiều agent khác, dùng style "caveman" để cắt filler.

Ví dụ bình thường:

> Tôi sẽ kiểm tra nguyên nhân component re-render, có thể do object reference mới...

Caveman:

> New object ref each render. Wrap in `useMemo`.

Nghe buồn cười, nhưng nó đánh vào một nguồn token có thật: assistant output. Agent không chỉ trả lời cho user; nó còn đọc lại output của chính nó ở các turn sau. Output càng dài, context sau càng nặng.

### Cách Dùng

Cài skill:

```bash
curl -fsSL https://raw.githubusercontent.com/JuliusBrussee/caveman/main/install.sh | bash
```

Dry-run:

```bash
curl -fsSL https://raw.githubusercontent.com/JuliusBrussee/caveman/main/install.sh | bash -s -- --dry-run
```

Trong session:

```text
/caveman
/caveman full
/caveman ultra
normal mode
```

Caveman cũng có:

- `/caveman-stats`: xem estimated savings;
- `/caveman-compress <file>`: nén file context/memory như `CLAUDE.md`;
- `/caveman-review`, `/caveman-commit`;
- `caveman-shrink`: middleware nén tool descriptions;
- **Caveman Code**: terminal coding agent riêng, dùng nhiều lớp nén hơn.

### Ưu Điểm

- **Rất dễ hiểu**: bỏ filler, nói thẳng.
- **Giảm output tokens thật** trong các agent vốn dài dòng.
- **Đọc nhanh hơn**: con người cũng đỡ mệt.
- **Hữu ích với context files**: `caveman-compress` cho `CLAUDE.md`, notes, memory.
- **Có thể dùng như kỷ luật giao tiếp**: "ít lời, đúng ý, không văn mẫu".

### Nhược Điểm

- **Headline 65-75% dễ gây hiểu nhầm**. Caveman skill chủ yếu giảm output tokens, không tự động giảm tool output, file reads, reasoning tokens, system prompt.
- **Tổng bill có thể giảm ít hơn nhiều** nếu input/tool tokens là phần lớn.
- **Skill cũng có overhead**: session ngắn có thể không lời.
- **Output quá ngắn có thể mất nuance**: không hợp viết design doc, dạy junior, phân tích trade-off sâu.
- **Style không phải lúc nào cũng hợp thương hiệu cá nhân**. Bài blog của bạn mà toàn "code bad, fix now" thì độc giả hơi đau.

### Caveman Code

`caveman-code` là agent CLI riêng, không chỉ skill output. README claim "same model, same task, ~2x fewer tokens than Codex" trong benchmark riêng, với plan mode, autopilot loop, nhiều provider, MCP commands. Đây là hướng đáng theo dõi hơn Caveman skill đơn thuần nếu mục tiêu là full-session savings.

### Khi Nào Nên Dùng Caveman?

Dùng Caveman nếu:

- agent hay trả lời dài, nhiều filler;
- bạn làm việc trong terminal, muốn output ngắn;
- session dài và assistant output bị kéo lại nhiều lần;
- muốn nén `CLAUDE.md`/context files.

Đừng kỳ vọng Caveman thay thế RTK/Headroom. Nó xử lý **miệng agent**, không xử lý toàn bộ **đường tiêu hóa context**.

## 5. Các Tool Đáng Theo Dõi Khác

Ngoài các nhóm chính, nhóm token-saving tools đang mọc rất nhanh. Một số tool đáng để theo dõi:

| Tool | Tầng tối ưu | Điểm mạnh | Caveat |
|---|---|---|---|
| **jCodeMunch MCP** | Symbol-level retrieval, repo maps, AST/search bundles | Hợp repo lớn, nơi agent hay đọc nguyên file | Có thể miss context ngoài symbol; setup phức tạp hơn |
| **ccusage / tokentop** | Observability | Không giảm token trực tiếp, nhưng đo spend/burn/cache | Không thay thế compression/filtering |

Pattern chung: nếu agent đang **đọc quá nhiều file**, thử context layer như LeanCTX hoặc symbol/index tools như jCodeMunch. Nếu bạn chưa biết token đi đâu, đo bằng ccusage/tokentop trước. Chữa bệnh bằng số liệu vẫn đỡ hơn chữa bằng cảm giác, dù cảm giác đôi khi rất tự tin.

## Ba Lớp Token Saving

Để chọn tool đúng, hãy phân loại theo lớp:

### Lớp 1: Output Discipline

Tool: Caveman, custom `AGENTS.md` rules.

Tối ưu:

- assistant output;
- văn phong;
- retry loop;
- context file quá dài.

Rủi ro:

- giảm ít nếu input/tool tokens là phần chính;
- có thể thiếu giải thích;
- dễ bị marketing claim quá tay.

### Lớp 2: Tool Output Filtering

Tool: RTK, scripts tự viết, shell hooks.

Tối ưu:

- `git diff`, `pytest`, `cargo test`, `npm test`;
- logs;
- GitHub CLI;
- Docker/Kubernetes output.

Rủi ro:

- che mất chi tiết lỗi;
- trust boundary lớn;
- repo độc hại có thể cố ảnh hưởng filter nếu config không khóa chặt.

### Lớp 3: Context Compression/Proxy

Tool: Headroom, custom compression middleware.

Tối ưu:

- RAG chunks;
- JSON/API/database results;
- cross-agent memory;
- file reads;
- repeated context/cache alignment.

Rủi ro:

- thêm proxy/runtime;
- cần đo quality, không chỉ token;
- compression sai làm agent tự tin sai.

## Ma Trận Chọn Tool

| Tình huống | Nên thử trước | Vì sao |
|---|---|---|
| Claude Code/Codex hay đốt token ở test/log/git | RTK | Shell output là nguồn noise lớn nhất |
| Multi-agent workflow, nhiều RAG/API/log | Headroom | Proxy/MCP/SDK bao phủ rộng hơn |
| Repo lớn, agent hay đọc file quá rộng | LeanCTX, jCodeMunch | Dùng signatures/map/symbol thay vì full file |
| Agent đọc lại cùng file/output nhiều lần | LeanCTX | Cache/dedup giúp repeated reads rẻ hơn |
| Agent trả lời quá dài, khó đọc | Caveman | Giảm output và retry overhead |
| Muốn build agent platform riêng | Headroom | Có proxy/SDK/MCP để nhúng vào pipeline |
| Chưa biết token rò ở đâu | ccusage, tokentop, `rtk gain` | Đo trước khi tối ưu |
| Security audit | Raw output + đo token thủ công | Token optimizer có thể che tín hiệu quan trọng |
| Repo không tin cậy | Tắt project-local filters | Đừng để repo quyết định agent nhìn thấy gì |

## Rủi Ro Bảo Mật: Token Optimizer Là "Mắt" Của Agent

Điểm quan trọng nhất: các công cụ này không chỉ tiết kiệm tiền. Chúng **biến đổi dữ liệu trước khi model thấy**.

Nếu một tool lọc mất dòng:

```text
cryptography==41.0.0  # vulnerable
```

agent có thể kết luận sai rằng dependency an toàn. Nếu một project-local config được repo lạ cung cấp và agent tin nó, attacker có thể định hình thứ agent nhìn thấy.

Vì vậy:

- Không bật optimizer không kiểm soát trong security audit.
- Không tin project-local config từ repo lạ.
- Giữ raw output fallback.
- Với command fail, lưu log gốc.
- Khi agent chuẩn bị kết luận quan trọng, bắt nó kiểm tra lại source/raw output.
- Không log secrets qua proxy.
- Đọc installer trước khi `curl | bash`, hoặc dùng `--dry-run`.
- Compression layer nên fail closed hoặc nói rõ đã bỏ gì. Im lặng bỏ dữ liệu là cách nhanh nhất để tạo bug tự tin.

Tiết kiệm token mà mất sự thật thì không phải tối ưu. Đó là giảm cân bằng cách cắt dây phanh.

## Benchmark: Đọc Số Liệu Thế Nào Cho Đúng?

Các tool này thường công bố số lớn:

- RTK: 60-90% trên dev command output.
- Headroom: 60-95% trên logs/JSON/RAG/tool output; median thực tế có thể thấp hơn nhiều khi request ngắn.
- Caveman: 65-75% output tokens trong benchmark riêng; không đồng nghĩa giảm 75% tổng bill.

Cách đọc đúng:

1. Hỏi **giảm phần nào**: output, input, tool output, total session, hay context file?
2. Hỏi **benchmark trên workload gì**: logs dài hay edit code ngắn?
3. Hỏi **có quality regression không**: agent có sửa đúng không?
4. Hỏi **có raw fallback không**.
5. Tự đo trên repo của mình.

Một metric đơn giản:

```text
cost_per_successful_task =
  (input_tokens + output_tokens + cached_tokens_adjusted + retries)
  / task_success
```

Đừng tối ưu token/request nếu làm tăng số lần retry.

## Stack Khuyến Nghị

### Solo Developer

- Bật Caveman nếu agent quá dài dòng.
- Dùng RTK cho test/log/git output.
- Dùng raw output khi debug khó.
- Đo bằng `/usage`, `rtk gain`, hoặc usage report của agent.

### Team Nhỏ

- Shared rule: "test/build commands phải qua RTK hoặc script lọc output".
- Headroom cho RAG/API/log-heavy workflow.
- Cấm project-local token filter từ repo không tin cậy.
- Có `TOKEN_OPTIMIZER_OFF=1` hoặc alias raw để escape hatch.
- Review weekly: token/session, retries, failures do thiếu context.

### Platform/Enterprise

- Headroom ở gateway/context layer.
- RTK-style filtering cho terminal agent sandbox.
- Audit logs có redaction.
- Policy rõ: security/compliance tasks dùng raw output.
- Benchmark nội bộ theo task thật, không dùng headline GitHub làm quyết định mua.

## Kết Luận

Headroom, RTK, LeanCTX và Caveman đại diện cho bốn hướng tối ưu khác nhau:

- **RTK**: giảm rác từ terminal.
- **Headroom**: nén context/tool output ở tầng proxy/SDK/MCP.
- **LeanCTX**: biến file reads/search/shell/memory thành context layer có cache.
- **Caveman**: ép agent nói ít hơn và nén một phần context files.

Nếu phải chọn một thứ để bắt đầu, tôi sẽ chọn **RTK** cho coding workflow thuần terminal, vì test/log/git output là nguồn rò token rõ nhất. Nếu repo lớn và agent hay đọc file quá rộng, hãy nhìn sang **LeanCTX hoặc jCodeMunch**. Nếu đang xây platform agent hoặc multi-agent workflow, **Headroom** đáng nghiên cứu hơn. Nếu vấn đề là agent dài dòng và lặp lại văn mẫu, **Caveman** đủ nhẹ để thử.

Nhưng nguyên tắc cuối cùng vẫn là: **đo trước, tối ưu sau, và luôn giữ đường quay về raw context**. Coding agent không cần đọc mọi thứ, nhưng nó phải được đọc đúng thứ. Đừng đổi một hóa đơn thấp hơn lấy một bug production khó hơn.

## Tài Liệu Tham Khảo

- Headroom OSS: [github.com/chopratejas/headroom](https://github.com/chopratejas/headroom)
- Headroom Docs: [headroom-docs.vercel.app/docs](https://headroom-docs.vercel.app/docs)
- Headroom PyPI: [pypi.org/project/headroom-ai](https://pypi.org/project/headroom-ai/)
- RTK OSS: [github.com/rtk-ai/rtk](https://github.com/rtk-ai/rtk)
- RTK Docs: [rtk-ai.app](https://www.rtk-ai.app/)
- RTK advisory: [GHSA-fvvm-949w-qj4w](https://github.com/advisories/GHSA-fvvm-949w-qj4w), [CVE-2026-45792](https://advisories.gitlab.com/cargo/rtk/CVE-2026-45792/)
- LeanCTX: [github.com/yvgude/lean-ctx](https://github.com/yvgude/lean-ctx), [leanctx.com](https://leanctx.com/)
- Caveman: [github.com/JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman)
- Caveman ecosystem: [getcaveman.dev](https://getcaveman.dev/)
- Caveman Code: [github.com/JuliusBrussee/caveman-code](https://github.com/JuliusBrussee/caveman-code)
- jCodeMunch MCP: [github.com/jgravelle/jcodemunch-mcp](https://github.com/jgravelle/jcodemunch-mcp)
- Token consumption study: [How Do AI Agents Spend Your Money?](https://arxiv.org/abs/2604.22750)
