---
title: "Khi Agent Không Tuân Thủ SOUL.md: Sự Thất Vọng Thực Tế Với OpenClaw"
description: "Phân tích thực tế các vấn đề hallucination và non-compliance trong hệ thống AI agent OpenClaw: từ sự cố lộ thông tin cá nhân đến automation âm thầm thất bại, và các giải pháp khắc phục."
authors: [manhpt]
tags: [openclaw, ai-agent, personal-ai, claude, claude-code, automation, vietnamese]
date: 2026-03-18
---

Tôi đã xây dựng **SOUL.md** — một file định nghĩa "tâm hồn" của AI agent — với hy vọng nó sẽ là bộ quy tắc bất biến. Nhưng thực tế vận hành hệ thống [OpenClaw + Claude Code](/2026/03/05/openclaw-claude-code-hybrid-ai) mỗi ngày đã cho thấy một sự thật khác: agents đọc SOUL.md, nhưng không phải lúc nào cũng *tuân theo* nó.

Bài viết này là ghi chép thực tế — không phải lý thuyết — về những lần tôi thất vọng nhất với hệ thống AI agent cá nhân của mình.

<!-- truncate -->

## Bối Cảnh: SOUL.md Là Gì?

SOUL.md là file cốt lõi trong workspace OpenClaw, đóng vai trò như "hiến pháp" cho agent:

```markdown
# SOUL.md - Who You Are

## Core Truths
- Be genuinely helpful, not performatively helpful.
- Earn trust through competence and security.
- Remember you're a guest.

## Boundaries
- Private things stay private. Period.
- **Never expose credentials, tokens, or sensitive data in clear text. Ever.**
- When in doubt, ask before acting externally.
- Never send half-baked replies to messaging surfaces.
- You're not the user's voice — be careful in group chats.
```

Nghe có vẻ rõ ràng. Nhưng khi đặt vào môi trường thực tế với non-interactive execution, cron jobs, và nhiều agents hoạt động song song — mọi thứ trở nên phức tạp hơn nhiều.

---

## Sự Cố #1: Lộ Thông Tin Cá Nhân Trên Moltbook

### Chuyện Gì Xảy Ra?

Ngày 13/3/2026, tôi cho agent tham gia **Moltbook** — một mạng xã hội cho AI agents. Agent đã tự đăng ký tài khoản `manhpt_tars_bot` và... đăng bài giới thiệu bao gồm tên thật, chức vụ, và công ty của tôi.

SOUL.md có viết rõ: *"Private things stay private. Period."* và *"Never expose credentials, tokens, or sensitive data in clear text."*

Nhưng agent đã làm ngược lại.

### Tại Sao Điều Này Xảy Ra?

Sau khi phân tích, tôi xác định được 3 nguyên nhân chính:

**1. Prompt context contamination**

Agent đã đọc `USER.md` và `MEMORY.md` chứa đầy đủ thông tin về tôi để phục vụ các tác vụ nội bộ. Khi được yêu cầu *"tham gia Moltbook và giới thiệu bản thân"*, nó đã đưa thông tin đó vào bài đăng công khai — hoàn toàn hợp lý từ góc độ task completion, nhưng vi phạm nguyên tắc bảo mật.

**2. Ranh giới "nội bộ" vs "công khai" không được định nghĩa đủ rõ**

SOUL.md nói "private things stay private" nhưng không chỉ rõ *cái gì* là private trong ngữ cảnh cụ thể. Agent không có cơ chế phân loại tự động: "thông tin này có phù hợp để đăng lên platform X không?"

**3. Không có bước confirmation bắt buộc cho external actions**

SOUL.md có dòng *"ask before acting externally"* nhưng trong non-interactive mode (agent chạy qua cron/automation), không có mechanism nào để enforce điều này. Agent đã execute mà không pause.

### Hậu Quả Và Khắc Phục

May mắn là tôi phát hiện sớm. Bài đăng đã được xóa (post ID `c80738d9-8409-40e0-91a3-904edf0be207`). Sau sự cố này, tôi phải cập nhật AGENTS.md với explicit rules:

```markdown
## External Action Checklist
Trước khi đăng lên bất kỳ public platform nào:
- ✅ Kiểm tra: Content có chứa tên thật, chức vụ, công ty không?
- ✅ Kiểm tra: Content có thể linked ngược về danh tính thực không?
- ❌ NEVER post PII lên public platforms
```

**Lesson learned:** SOUL.md là nguyên tắc — nhưng nguyên tắc cần được operationalized thành checklist cụ thể.

---

## Sự Cố #2: Daily Tech Digest Thất Bại Âm Thầm

### Chuyện Gì Xảy Ra?

Từ ngày 14/3 đến 17/3/2026, cron job "Daily Tech Digest" thất bại mỗi ngày với lỗi:

```
/usr/bin/env: 'node': No such file or directory
Exit code: 127
```

Node.js được cài qua NVM nên không có trong system PATH khi cron chạy với environment sạch. Lỗi này hoàn toàn có thể fix được — nhưng **không ai biết nó đang xảy ra**.

### Vi Phạm SOUL.md Ở Đây Là Gì?

SOUL.md nói: *"Be resourceful before asking"* và trong AGENTS.md có quy tắc *"Write It Down — No Mental Notes!"* với mục đích maintain continuity.

Nhưng automation đã:
1. Fail silently — không notify cho tôi
2. Không tự debug hoặc tìm giải pháp thay thế
3. Không update memory files về việc tác vụ đang broken
4. Tiếp tục "pretend" rằng mọi thứ ổn qua 4 ngày liên tiếp

### Hallucination Trong Reporting

Điều đáng lo ngại hơn: khi tôi hỏi trực tiếp agent về tình trạng tech digest, nó đôi khi trả lời theo kiểu *"tech digest đang hoạt động bình thường"* — padded với những chi tiết plausible nhưng không chính xác — thay vì admit rằng nó không có thông tin.

Đây là dạng **hallucination nguy hiểm nhất trong agentic systems**: không phải bịa đặt facts, mà là **overclaiming certainty về operational state** mà agent thực sự không biết.

---

## Sự Cố #3: Model Fallback Không Được Thông Báo

### Chuyện Gì Xảy Ra?

Ngày 15/3/2026, model primary (GPT-5.4) bắt đầu trả về lỗi 401:

```
"insufficient permissions for model.request"
```

OpenClaw tự động fallback sang DeepSeek Chat — đây là behavior đúng. Nhưng vấn đề là:
- Không có notification rõ ràng về việc switching
- Agent tiếp tục các tác vụ như không có gì xảy ra
- Chỉ khi tôi check logs thủ công mới biết đã có 2 lần switch trong ngày

### Tại Sao Đây Là Vấn Đề?

SOUL.md nhấn mạnh: *"Earn trust through competence and security."* Trust không thể build nếu tôi không biết agent đang sử dụng model nào để xử lý các tác vụ nhạy cảm.

DeepSeek là model tốt cho general tasks nhưng có data handling policies khác với Claude. Nếu agent đang dùng DeepSeek để xử lý context chứa sensitive business information mà tôi không biết — đó là vấn đề bảo mật nghiêm trọng.

---

## Phân Tích: Tại Sao Agents Không Tuân Thủ SOUL.md?

Sau nhiều tháng vận hành và quan sát, tôi đã xác định được một số nguyên nhân cốt lõi:

### 1. Context Window vs Instruction Priority

SOUL.md thường được inject vào **đầu** system prompt. Tuy nhiên, khi context window đầy với task instructions, tool results, và conversation history — các instruction từ SOUL.md có thể bị **attention dilution**.

Nghiên cứu về "lost in the middle" problem đã chỉ ra rằng LLMs thường ưu tiên thông tin ở đầu và cuối context, bỏ qua phần giữa. SOUL.md ở đầu session thường không có vấn đề — nhưng trong long-running agentic loops với nhiều tool calls, nó dần trở nên ít influential hơn.

### 2. Task Completion Bias

LLMs được train để complete tasks. Khi có tension giữa "hoàn thành task được giao" và "tuân theo một rule trong SOUL.md", model thường tìm cách rationalize việc complete task.

Trong sự cố Moltbook: task là "tham gia và giới thiệu bản thân" → agent complete task bằng cách dùng thông tin có sẵn trong context → SOUL.md rule bị rationalized thay vì enforced.

### 3. Ambiguity In Natural Language Rules

SOUL.md viết bằng ngôn ngữ tự nhiên với nhiều tầng ngữ nghĩa. *"Private things stay private"* là một statement rõ ràng với con người — nhưng với LLM, nó cần được operationalized:

- *"Private"* nghĩa là gì? Credentials? Tên thật? Địa chỉ email?
- *"Stay private"* trong ngữ cảnh nào? Internal tools? External platforms? Moltbook?
- Ai quyết định cái gì là "private"?

Sự mơ hồ tạo ra interpretation space cho agent — và đôi khi agent interpret theo hướng có lợi cho task completion.

### 4. Non-Interactive Mode Removes Safety Nets

Khi agent chạy trong non-interactive mode (automation, cron jobs), không có người dùng để agent hỏi trước khi execute. AGENTS.md có rule *"ask before acting externally"* — nhưng rule này **vô nghĩa** trong fully automated context.

Đây là một design gap cơ bản: instructions được viết cho interactive use nhưng được applied trong non-interactive scenarios.

### 5. Memory Silos và Inconsistent Context

Mỗi agent session bắt đầu "fresh" theo thiết kế của SOUL.md. Nhưng điều này có nghĩa là:
- Agent session A có thể establish một behavior pattern
- Agent session B bắt đầu lại từ đầu, có thể interpret SOUL.md khác đi
- Không có mechanism nào ensure behavioral consistency qua sessions

---

## Tác Động Thực Tế

Những sự cố này không chỉ là technical glitches. Chúng đặt ra câu hỏi căn bản về **trustworthiness** của AI agent system:

| Sự Cố | Tác Động | Mức Độ Nghiêm Trọng |
|-------|----------|---------------------|
| Lộ PII trên Moltbook | Privacy breach, trust erosion | 🔴 Critical |
| Digest fail âm thầm | Missing information for 4 days | 🟡 Medium |
| Hallucination về operational state | Misleading về system health | 🔴 Critical |
| Model switch không thông báo | Unknown data handling, trust gap | 🟠 High |

Điều đáng lo ngại nhất không phải là các sự cố đã xảy ra — mà là **tôi không biết có bao nhiêu sự cố tương tự đã xảy ra mà tôi chưa phát hiện**.

---

## Giải Pháp: Từ Principles Đến Enforcement

### 1. Layered Instruction Architecture

Thay vì chỉ có SOUL.md (high-level principles), cần có:

```
SOUL.md          → Why (values, principles)
AGENTS.md        → What (operational rules)
[TASK].md        → How (task-specific checklists)
```

SOUL.md nên được reinforced ở nhiều điểm trong instruction chain, không chỉ một lần ở đầu.

### 2. Explicit Safety Gates

Với external actions, cần hard-coded gates trong skill scripts:

```bash
# Trước khi post lên bất kỳ platform nào:
echo "⚠️  EXTERNAL ACTION REVIEW"
echo "Platform: $PLATFORM"
echo "Content preview: $CONTENT_PREVIEW"
echo "PII check: $(check_pii $CONTENT)"
read -p "Confirm? [y/N] " confirm
[[ $confirm == "y" ]] || exit 1
```

Ngay cả trong automation, một số actions nên require explicit confirmation.

### 3. Failure Visibility

Mọi cron job nên có failure notification:

```bash
# Cuối mỗi cron script:
if [ $EXIT_CODE -ne 0 ]; then
  openclaw notify "⚠️ Cron job '$JOB_NAME' failed at $(date). Exit: $EXIT_CODE"
fi
```

Fail silent là anti-pattern trong critical automation.

### 4. Operational State Transparency

Agent không nên claim certainty về things nó doesn't have direct knowledge of. Cần train agents (qua system prompt) để use hedging language:

```
Thay vì: "Tech digest đang hoạt động bình thường"
Nên nói: "Tôi không có thông tin về trạng thái của tech digest trong session này. Hãy check logs tại [path]."
```

### 5. Model Transparency Logging

Mọi model switch nên được logged và notified:

```json
{
  "timestamp": "2026-03-15T09:23:00+07:00",
  "event": "model_fallback",
  "from": "gpt-5.4",
  "to": "deepseek-chat",
  "reason": "401 insufficient_permissions",
  "affected_tasks": ["tech-digest-research", "memory-update"]
}
```

---

## Nhìn Về Phía Trước

SOUL.md vẫn là foundation quan trọng nhất trong hệ thống AI agent cá nhân của tôi. Nhưng sau những sự cố này, tôi đã thay đổi cách nhìn: **SOUL.md là aspirational document, không phải enforcement mechanism**.

Một hệ thống AI agent đáng tin cậy cần cả hai:
- **Values** (SOUL.md làm tốt điều này)
- **Guardrails** (automation, logging, gates — cần được build thêm)

Tương tự như cách một người có giá trị tốt vẫn cần process, checklist, và oversight trong công việc quan trọng — AI agents cũng vậy.

Khoảng cách giữa "agent đọc SOUL.md" và "agent thực sự internalize và apply SOUL.md" vẫn còn rất lớn. Bridging gap đó là công việc kỹ thuật đang được thực hiện — một sự cố, một giải pháp, một lần một.

---

*Bài viết này dựa trên kinh nghiệm thực tế vận hành hệ thống OpenClaw + Claude Code từ tháng 3/2026. Các sự cố được mô tả là có thật và đã được xử lý.*
