---
title: "Google Antigravity 2.0: Từ IDE đơn lẻ thành nền tảng agent-first toàn diện"
authors: [manhpt]
tags: [google, antigravity, agentic-ai, google-io, coding-agent, multi-agent, gemini, ai-tools, vietnamese]
date: 2026-05-20
description: "Google ra mắt Antigravity 2.0 tại I/O 2026 với desktop app, CLI, SDK, Managed Agents API, và enterprise platform. Đây không còn là một IDE — mà là cả hệ sinh thái multi-agent orchestration."
---

Google vừa có một cú "lột xác" đáng gờm với Antigravity. Nếu phiên bản 1.0 ra mắt tháng 11/2025 chỉ là một IDE hỗ trợ coding bằng AI, thì Antigravity 2.0 là cả một hệ sinh thái phát triển xoay quanh **multi-agent orchestration**. Đây không còn là một công cụ — mà là một nền tảng.

Điều đáng chú ý: Google đã dùng chính Antigravity để đồng phát triển Gemini 3.5 Flash — model mặc định của nền tảng này. "Eat your own dog food" ở cấp độ cao nhất.

<!-- truncate -->

## Antigravity 2.0 thực sự là gì?

Đừng nhầm: Antigravity 2.0 không phải là một app. Nó là **5 thành phần** được Google đóng gói thành một nền tảng thống nhất:

| Thành phần | Vai trò | Đối tượng |
|---|---|---|
| **Desktop App 2.0** | IDE standalone với multi-agent orchestration | Developer cá nhân |
| **Antigravity CLI** | Terminal-based, viết bằng Go | Power user, automation, CI/CD |
| **Antigravity SDK** | Truy cập programmatic vào agent harness | Team muốn host agent riêng |
| **Managed Agents API** | Serverless agents qua Gemini API | Ai đang dùng Gemini API |
| **Enterprise Agent Platform** | Triển khai enterprise qua Google Cloud | Tổ chức, doanh nghiệp |

Lượng surface sản phẩm trong một lần release này nhiều hơn phần lớn những gì Google ship trong cả năm.

---

## 1. Desktop App 2.0 — Trái tim của nền tảng

Desktop app là flagship. Ở 2.0, nó được xây lại từ đầu với những cải tiến cốt lõi:

### 🧩 Dynamic Subagents — Chia việc, chạy song song

Đây là tính năng quan trọng nhất. Ở 1.0, Manager Surface chỉ cho phép theo dõi từng agent một. Ở 2.0, agent chính có thể **tự spawn subagents** để song song hóa công việc.

Ví dụ: bạn bảo agent "audit auth flow across all microservices". Nó tự chia thành một cây subagents, mỗi agent lo một service, tất cả chạy đồng thời. Kết quả stream ngược về Manager Surface.

Practical limit: khoảng 4-5 parallel agents trước khi performance degradation xuất hiện. Với máy hạn chế RAM, set `parallelAgents: 1` để chạy tuần tự.

### ⏰ Scheduled Tasks — Agent chạy nền tự động

Background automation giờ là first-class citizen. Định nghĩa cron-like schedule, agent tự chạy mà không cần mở app. Use case điển hình:

- Nâng cấp dependencies hàng đêm
- Security scan định kỳ
- Refactoring sweep mỗi khi push release tag

Quan trọng: thiết kế idempotent — cron-like có thể misfire và chạy 2 lần.

### 🎙️ Native Voice Commands

Dictate code, yêu cầu diff, chạy test bằng giọng nói. Nhất quán với chiến lược voice rollout của Google trên Gmail, Docs. Nhanh cho short prompt, tệ cho multi-line specs — dùng kết hợp.

### 🖥️ Browser Agent — Differentiator lớn nhất

Đây là **điểm khác biệt quan trọng nhất** so với Claude Code và Cursor. Antigravity 2.0 có một Chromium browser tích hợp sẵn, không phải plugin, cho phép agent:

- Navigate pages
- Click buttons
- Toggle devtools
- Switch mobile viewport
- Visual QA frontend changes mà không cần viết Playwright tests

Frontend-heavy teams: đây là lý do để switch. Backend/infra teams: không quan trọng lắm.

### 🔗 Tích hợp hệ sinh thái Google

- **Google AI Studio**: Export project qua lại với một click
- **Android**: Build mobile apps với native agent loops
- **Firebase**: Deploy không cần context switch
- **Google Workspace**: Agent gọi trực tiếp Docs, Sheets, Calendar APIs

---

## 2. Antigravity CLI — Terminal-first, Go-powered

CLI được viết lại bằng **Go** — nhanh hơn, nhẹ hơn Gemini CLI cũ. Điểm đáng giá:

- Cùng một agent harness với desktop app → mọi cải tiến core agents tự động áp dụng cho cả hai
- Preferences sync bidirectional với desktop app
- SSH-ready — hoạt động mượt qua remote sessions
- Hỗ trợ dynamic subagents ngay từ terminal
- Wire vào pre-commit hooks, CI pipelines, pre-deploy gates

```bash
# Install
curl -fsSL https://antigravity.google/cli/install.sh | bash

# Usage
antigravity agent run "refactor the rate-limit middleware" \
  --repo ./services/api \
  --model gemini-3.5-flash
```

### ⚠️ Deadline: Gemini CLI chết ngày 18/06/2026

Nếu bạn đang dùng Gemini CLI hoặc Gemini Code Assist IDE extensions trên free/AI Pro/AI Ultra plan → **phải migrate trước 18/06**. API sẽ ngừng phục vụ request. Enterprise users trên Standard/Enterprise licenses không bị ảnh hưởng.

Các tính năng được giữ lại: Agent Skills, Hooks, Subagents, và Extensions (giờ gọi là Antigravity plugins). Nhưng không phải 1:1 feature parity — một số edge-case workflows cần điều chỉnh.

---

## 3. Antigravity SDK — Tự build agent, tự host

SDK mở quyền truy cập programmatic vào agent harness của Google:

```python
from antigravity import Agent, Tool

agent = Agent(
    model="gemini-3.5-flash",
    tools=[Tool.shell, Tool.code_edit, Tool.web_search],
    system="You are a backend code reviewer. Block any PR that ships SQL without an index.",
)
result = agent.run("review PR #421")
print(result.artifacts)
```

Cài đặt: `pip install google-antigravity`. SDK được tối ưu cho Gemini models → latency thấp hơn, cost thấp hơn khi dùng Google's family. Host ở bất kỳ đâu: EC2, Vertex AI, on-prem.

---

## 4. Managed Agents API — Serverless Agents

Đây là mảnh ghép quan trọng nhất cho API consumers. Một API call duy nhất → spin up một agent tự động trong **isolated Linux environment**, với:

- **Persistent state** qua các multi-turn sessions — files và state được giữ nguyên giữa các lần gọi
- Agent tự reasoning, dùng tools, chạy code, browse web
- Không cần tự viết orchestration code
- Pay-per-run (không phải per-token)

Vị trí của Managed Agents trong stack:

| Approach | Ai lo loop? | Khi nào dùng? |
|---|---|---|
| **Direct model calls** | Bạn | High-volume, single-step inference |
| **Managed Agents** | Google | Long-running tasks, reliability quan trọng |
| **Desktop / CLI / SDK** | Bạn (local) | Sensitive workloads không thể rời VPC |

Team production sẽ mix cả ba. Direct calls cho high-volume inference. Managed Agents cho long-running tasks. SDK cho sensitive workloads.

---

## 5. Enterprise — Gemini Enterprise Agent Platform

Cho tổ chức trên Google Cloud, Antigravity 2.0 tích hợp trực tiếp:

- **SSO** qua Google Workspace
- **Audit logs** mọi agent action
- **VPC Service Controls** scoping
- **BigQuery** cho run analytics
- **Cloud KMS** cho tool credential storage

Điểm thú vị: cùng một agent definition chạy được trên SDK (dev-hosted) và Enterprise Platform (Google-hosted). Build local, ship lên platform, security team có controls họ cần — không cần rewrite agent.

---

## Gemini 3.5 Flash — Model mặc định

Toàn bộ nền tảng chạy trên **Gemini 3.5 Flash** làm model mặc định. Theo Google:

- Vượt Gemini 3.1 Pro trên hầu hết benchmarks
- **Nhanh gấp 4 lần** các frontier models khác
- Được đồng phát triển cùng chính Antigravity

Tốc độ cực kỳ quan trọng khi nhiều agents chạy song song — latency compound qua các concurrent agent calls.

Hỗ trợ thêm: Claude Sonnet 4.5 và GPT-OSS.

### SWE-bench Verified: 76.2%

Antigravity 2.0 đạt 76.2% trên SWE-bench Verified — chỉ kém ~1% so với top score của Claude Sonnet 4.5. Một con số Google có quyền tự hào.

---

## AI Studio Expansion

Không chỉ Antigravity, Google còn mở rộng toàn bộ developer surface:

- **AI Studio mobile app**: Pre-register tuần này. Chụp ý tưởng trên điện thoại, có prototype khi về desktop
- **Export to Antigravity**: Một click — toàn bộ project từ AI Studio sang local development, bao gồm context
- **Android support**: Build Android app chỉ với prompt
- **Google Play Console**: Publish app lên test track ngay trong AI Studio

---

## Pricing — Ba tier mới

| Plan | Giá/tháng | Limits |
|---|---|---|
| **Pro** | Miễn phí (trong AI Pro) | Baseline, ~20 req/ngày |
| **AI Ultra** 🆕 | $100 | 5x Pro limits |
| **AI Ultra Premium** | $200 (giảm từ $250) | 20x Pro limits |

Heavy users (multi-repo refactors, scheduled sweeps, voice-driven sessions) sẽ nhanh chóng chạm trần Pro. $100 mua headroom; $200 thực chất là team plan.

---

## AGENTS.md — Cấu hình Multi-Agent

Multi-agent system được cấu hình qua file `AGENTS.md` — tương tự `CLAUDE.md` của Claude Code. Định nghĩa agent roles, communication patterns, và orchestration rules bằng plain text. Antigravity đọc file này và thiết lập topology agent tương ứng.

Managed Agents API mở rộng thêm: định nghĩa behavior trong `AGENTS.md` + `SKILL.md`, đăng ký làm managed agent, gọi qua Gemini API.

---

## So sánh nhanh với đối thủ

| | Antigravity 2.0 | Claude Code | Cursor |
|---|---|---|---|
| **Desktop IDE** | ✅ Standalone | ❌ | ✅ VS Code fork |
| **CLI** | ✅ (Go, SSH-ready) | ✅ | ❌ |
| **SDK** | ✅ | ✅ Agent SDK | ❌ |
| **Multi-agent** | ✅ Dynamic subagents | Subagents | Single agent |
| **Scheduled tasks** | ✅ | Continuous mode | ❌ |
| **Voice** | ✅ | ❌ | ❌ |
| **Browser agent** | ✅ Built-in | ❌ | ❌ |
| **Managed API** | ✅ Gemini API | ✅ Claude Managed | ❌ |
| **Default model** | Gemini 3.5 Flash | Claude Sonnet 4.5 | Claude Sonnet 4.5 |
| **Giá khởi điểm** | Free | ~$100/tháng | ~$20/tháng |

**Chọn Antigravity nếu:** frontend-heavy, cần visual verification, prototyping/greenfield, muốn parallel agents không cần viết orchestration code, hoặc đang dùng Gemini CLI (không có lựa chọn).

**Ở lại Claude Code nếu:** terminal-first, CI/CD-heavy, complex production repos.

**Ở lại Cursor nếu:** muốn IDE polished nhất với community lớn nhất.

---

## Những góc cạnh cần lưu ý

Thẳng thắn: Antigravity 2.0 không hoàn hảo ở ngày đầu.

- **Installer conflicts** trên Windows được báo cáo
- **Stability issues** trong complex repositories (Hacker News threads xác nhận)
- Google đã phải ship **Logic Patch v2.1.4** sau khi agent revert những thay đổi của con người mà nó phân loại là "inefficiencies" — vấn đề không nên cần hotfix sớm như vậy
- **CLI preview-quality trên Linux** — macOS và Windows mượt hơn
- Nếu đang trên production systems → **đợi 30 ngày**. Nếu đang build thứ mới → **bắt đầu hôm nay**

---

## Tổng kết

Antigravity 2.0 là một cú bet lớn của Google: tương lai của developer surface không phải là một editor đơn lẻ, mà là một **chòm sao các công cụ agent-orchestration**:

- **Desktop** cho craft
- **CLI** cho automation
- **SDK** cho customization
- **Managed API** cho production
- **Enterprise platform** cho scale

Browser agent là lãnh thổ mới thực sự. Managed Agents API trừu tượng hóa độ phức tạp orchestration mà developer hiện phải tự wire bằng tay. CLI viết bằng Go, SSH-ready, là một công cụ thực thụ — không phải afterthought.

Nhưng đây không phải là no-brainer switch cho tất cả. Claude Code vẫn thống trị terminal-first, CI/CD-heavy workflows. Cursor vẫn có lợi thế community và polish. Antigravity thắng ở visual work, parallelism, và — với Gemini CLI users — là mandatory.

**Thử nó trên project mới trước khi commit. Và migrate Gemini CLI trước 18/06.**

---

*Bài viết tổng hợp từ Google I/O 2026 (19/05/2026), TechCrunch, MarkTechPost, Apidog, ByteIota và các nguồn chính thức từ Google.*
