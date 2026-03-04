---
title: "OpenClaw + Claude Code: Kiến Trúc AI Cá Nhân Với Cơ Chế Delegate Thông Minh"
description: Khám phá cách kết hợp một AI orchestrator tổng quát (OpenClaw) với Claude Code để xây dựng trợ lý cá nhân mạnh mẽ hơn, nơi các tác vụ đòi hỏi độ chính xác kỹ thuật cao được tự động chuyển giao cho chuyên gia.
authors: [manhpt]
tags: [ai-agent, claude, claude-code, anthropic, mcp, personalization, llm]
---

**Vấn đề cốt lõi:** Một AI assistant tổng quát giỏi nhiều thứ, nhưng khi gặp tác vụ kỹ thuật đòi hỏi độ chính xác cao — sửa bug phức tạp, refactor hàng nghìn dòng code, viết test coverage đầy đủ — nó thường không đủ "sâu". Claude Code (Anthropic's official CLI) lại được tối ưu hóa chính xác cho những tác vụ này, với khả năng đọc toàn bộ codebase, chạy lệnh, và thực hiện thay đổi thực tế trên file system.

Bài viết này đề xuất kiến trúc **delegate thông minh**: dùng OpenClaw làm AI cá nhân trung tâm, và tự động chuyển giao (delegate) các tác vụ kỹ thuật cao cho Claude Code khi cần thiết.

<!-- truncate -->

## Bài Toán: Độ Chính Xác Vs. Tính Tổng Quát

Khi xây dựng một AI cá nhân, chúng ta đối mặt với tension cơ bản:

| Thuộc tính | AI Tổng Quát | Claude Code |
|---|---|---|
| **Phạm vi** | Rộng (mọi domain) | Hẹp (software engineering) |
| **Độ chính xác kỹ thuật** | Trung bình | Rất cao |
| **Khả năng hành động** | Hạn chế | Đọc/sửa file, chạy lệnh |
| **Context về codebase** | Không có | Toàn bộ project |
| **Chi phí mỗi request** | Thấp | Cao hơn |

Câu trả lời không phải là chọn một trong hai — mà là **kết hợp cả hai** theo đúng ngữ cảnh.

## Giải Pháp: Kiến Trúc Delegate

```
┌─────────────────────────────────────────────┐
│              OpenClaw Orchestrator           │
│                                             │
│  ┌─────────────┐    ┌────────────────────┐  │
│  │  Intent     │    │   Context Manager  │  │
│  │  Classifier │    │  (memory, history) │  │
│  └──────┬──────┘    └────────────────────┘  │
│         │                                   │
│    ┌────▼─────┐                             │
│    │ Router   │                             │
│    └────┬─────┘                             │
└─────────┼───────────────────────────────────┘
          │
    ┌─────▼──────────────────────┐
    │                            │
┌───▼────┐              ┌────────▼──────┐
│General │              │  Claude Code  │
│ LLM    │              │  Sub-agent    │
│(chat,  │              │(code, debug,  │
│summary)│              │ refactor, CI) │
└────────┘              └───────────────┘
```

### Nguyên tắc Routing

OpenClaw phân loại mỗi request vào một trong hai luồng:

**→ General LLM** (xử lý nội bộ):
- Trả lời câu hỏi, giải thích khái niệm
- Tóm tắt tài liệu, dịch thuật
- Lên kế hoạch, brainstorm
- Quản lý lịch, email, reminder

**→ Claude Code** (delegate ra ngoài):
- Fix bug trong codebase thực
- Viết/chỉnh sửa code với test kèm theo
- Refactor theo pattern cụ thể
- Review PR, phân tích security vulnerability
- Thiết lập CI/CD pipeline
- Bất kỳ tác vụ nào cần đọc/ghi file thực tế

## Implementation: Bước Đầu Thực Tế

### 1. Intent Classifier

Đây là thành phần quyết định khi nào nên delegate sang Claude Code:

```python
from anthropic import Anthropic

client = Anthropic()

ROUTING_SYSTEM_PROMPT = """
Bạn là một router thông minh. Phân loại request thành một trong hai loại:
- "general": Câu hỏi, giải thích, tóm tắt, brainstorm, quản lý thông tin
- "claude_code": Tác vụ cần thao tác với code thực tế (debug, implement, refactor, test, deploy)

Trả về JSON: {"type": "general"|"claude_code", "reason": "lý do ngắn gọn"}
"""

def classify_intent(user_request: str) -> dict:
    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=100,
        system=ROUTING_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_request}]
    )
    import json
    return json.loads(response.content[0].text)
```

### 2. Claude Code Sub-agent Executor

```python
import subprocess
import os

def delegate_to_claude_code(
    task: str,
    working_dir: str,
    context: str = ""
) -> dict:
    """
    Delegate a high-precision engineering task to Claude Code.

    Claude Code có thể đọc toàn bộ codebase, chạy tests,
    và thực hiện thay đổi thực tế — điều mà general LLM không làm được.
    """
    full_prompt = task
    if context:
        full_prompt = f"Context từ OpenClaw:\n{context}\n\nTask:\n{task}"

    result = subprocess.run(
        ["claude", "--print", full_prompt],
        capture_output=True,
        text=True,
        cwd=working_dir,
        env={**os.environ, "ANTHROPIC_MODEL": "claude-opus-4-6"}
    )

    return {
        "success": result.returncode == 0,
        "output": result.stdout,
        "error": result.stderr if result.returncode != 0 else None
    }
```

### 3. OpenClaw Orchestrator — Kết Nối Mọi Thứ

```python
class OpenClawOrchestrator:
    def __init__(self, working_dir: str = "."):
        self.client = Anthropic()
        self.working_dir = working_dir
        self.conversation_history = []
        self.memory = {}  # context ngắn hạn giữa các turn

    def process(self, user_input: str) -> str:
        # 1. Phân loại intent
        intent = classify_intent(user_input)

        # 2. Route đến handler phù hợp
        if intent["type"] == "claude_code":
            print(f"[OpenClaw] Delegating to Claude Code: {intent['reason']}")

            # Truyền context từ cuộc hội thoại hiện tại
            context = self._build_context_summary()
            result = delegate_to_claude_code(
                task=user_input,
                working_dir=self.working_dir,
                context=context
            )

            response = result["output"] if result["success"] else \
                       f"Claude Code gặp lỗi: {result['error']}"
        else:
            # Xử lý nội bộ với general LLM
            self.conversation_history.append({
                "role": "user",
                "content": user_input
            })

            api_response = self.client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=2048,
                system=self._build_system_prompt(),
                messages=self.conversation_history
            )

            response = api_response.content[0].text
            self.conversation_history.append({
                "role": "assistant",
                "content": response
            })

        return response

    def _build_context_summary(self) -> str:
        """Tóm tắt ngữ cảnh hội thoại để truyền cho Claude Code"""
        if not self.conversation_history:
            return ""

        recent = self.conversation_history[-6:]  # 3 turns gần nhất
        return "\n".join([
            f"{msg['role'].upper()}: {msg['content'][:200]}..."
            if len(msg['content']) > 200 else
            f"{msg['role'].upper()}: {msg['content']}"
            for msg in recent
        ])

    def _build_system_prompt(self) -> str:
        return """Bạn là OpenClaw, trợ lý AI cá nhân thông minh.

Bạn xử lý các câu hỏi tổng quát, giải thích, tóm tắt, và lên kế hoạch.
Với các tác vụ kỹ thuật phức tạp cần thao tác code thực tế,
hệ thống sẽ tự động chuyển sang Claude Code chuyên biệt.

Hãy trả lời súc tích, chính xác và thực dụng."""
```

### 4. Sử Dụng Thực Tế

```python
# Khởi động OpenClaw với project directory
openclaw = OpenClawOrchestrator(working_dir="/path/to/my/project")

# Request tổng quát → xử lý nội bộ
response = openclaw.process(
    "Giải thích sự khác nhau giữa Saga pattern và Observer pattern"
)
# [OpenClaw xử lý với general LLM]

# Request kỹ thuật → tự động delegate sang Claude Code
response = openclaw.process(
    "Có lỗi TypeScript ở file src/auth/middleware.ts dòng 45. "
    "Fix nó và thêm test cho edge case null token."
)
# [OpenClaw] Delegating to Claude Code: task requires actual file modification and testing
# → Claude Code đọc file, fix bug, chạy tests, commit

# Request hỗn hợp — OpenClaw breakdown task trước
response = openclaw.process(
    "Tôi muốn migrate database schema từ v1 sang v2. "
    "Giải thích approach rồi implement migration script."
)
# OpenClaw giải thích strategy → Claude Code viết migration script thực tế
```

## Pattern Nâng Cao: Feedback Loop

Một điểm mạnh của kiến trúc này là Claude Code có thể báo cáo kết quả trở lại OpenClaw, tạo ra vòng lặp phản hồi thông minh:

```python
def execute_with_feedback(self, task: str) -> str:
    """
    Delegate task, sau đó dùng OpenClaw phân tích kết quả
    và đề xuất bước tiếp theo.
    """
    # Bước 1: Claude Code thực hiện tác vụ
    result = delegate_to_claude_code(task, self.working_dir)

    if not result["success"]:
        # Claude Code thất bại → OpenClaw phân tích lỗi
        analysis_prompt = f"""
Claude Code gặp lỗi khi thực hiện task:
Task: {task}
Error: {result['error']}

Phân tích nguyên nhân và đề xuất cách tiếp cận khác.
"""
        return self.process(analysis_prompt)

    # Bước 2: OpenClaw tóm tắt và đề xuất bước tiếp theo
    summary_prompt = f"""
Claude Code đã hoàn thành task: {task}

Kết quả:
{result['output'][:1000]}

Tóm tắt những gì đã làm và đề xuất bước tiếp theo (nếu có).
"""
    return self.process(summary_prompt)
```

## Tại Sao Kiến Trúc Này Hiệu Quả?

### Tận dụng thế mạnh của từng thành phần

Claude Code có một đặc điểm unique: nó **thực sự đọc và sửa file**. Không phải "giả vờ" đọc qua context window — nó dùng tool calls để `Read`, `Edit`, `Bash`, và có khả năng navigate toàn bộ codebase theo từng bước. Đây là điều mà một general LLM trong conversation mode không thể làm được hiệu quả tương đương.

Ngược lại, OpenClaw (general orchestrator) giỏi về:
- **Memory management**: Ghi nhớ ngữ cảnh dài hạn về người dùng, preferences, ongoing projects
- **Multi-domain reasoning**: Kết nối thông tin từ nhiều nguồn khác nhau
- **Planning**: Breakdown complex goals thành steps, track progress
- **Integration**: Kết nối với calendar, email, Slack qua MCP tools

### Chi phí tối ưu

Không phải mọi request đều cần sức mạnh của Claude Code. Routing thông minh giúp:
- Câu hỏi đơn giản → model nhẹ, phản hồi nhanh, chi phí thấp
- Tác vụ phức tạp → Claude Code với model mạnh nhất, đúng lúc cần

### Separation of concerns rõ ràng

OpenClaw biết **bạn là ai** (context cá nhân, lịch sử, preferences).
Claude Code biết **code của bạn** (codebase, dependencies, conventions).

Sự kết hợp này tạo ra một AI có cả hai chiều hiểu biết — điều hiếm thấy ở một hệ thống đơn lẻ.

## Thách Thức Cần Giải Quyết

**1. Context Transfer**
Chuyển đúng lượng context từ OpenClaw sang Claude Code là nghệ thuật. Quá ít → Claude Code thiếu thông tin; quá nhiều → tốn token và nhiễu.

**2. State Synchronization**
Khi Claude Code sửa file, OpenClaw cần biết điều đó đã xảy ra để không đề xuất lại những thay đổi đã được thực hiện.

**3. Error Handling Cross-system**
Claude Code có thể thất bại (compile error, test failure). OpenClaw cần interpret lỗi này và quyết định: retry, thay đổi approach, hay hỏi người dùng?

**4. Security Boundaries**
Claude Code có quyền truy cập file system. Cần định nghĩa rõ scope nào được phép (project directory) và scope nào không (system files, credentials).

```python
# Ví dụ: Sandbox configuration
ALLOWED_WORKING_DIRS = [
    "/home/user/projects/",
    "/home/user/workspace/"
]

def safe_delegate(task: str, requested_dir: str) -> dict:
    # Validate working directory trước khi delegate
    if not any(requested_dir.startswith(allowed)
               for allowed in ALLOWED_WORKING_DIRS):
        return {"success": False, "error": "Directory not in allowed scope"}

    return delegate_to_claude_code(task, requested_dir)
```

## Roadmap: Từ Prototype Đến Production

**Phase 1 — Proof of Concept** (hiện tại):
- Intent classifier đơn giản dựa trên keywords + LLM
- Subprocess call đến `claude --print`
- Manual context passing

**Phase 2 — Integration Layer**:
- Claude Code SDK thay vì subprocess (khi available)
- Structured output từ Claude Code (JSON reports về changes made)
- Persistent state giữa các sessions

**Phase 3 — Full Personal AI**:
- MCP server cho OpenClaw để Claude Code có thể query lại context
- Multi-project awareness
- Proactive suggestions ("Tôi thấy có failing test từ commit hôm qua...")

## Kết Luận

Kiến trúc OpenClaw + Claude Code không phải là "thêm một AI nữa" — mà là **phân công lao động thông minh** giữa hai hệ thống được tối ưu hóa cho mục đích khác nhau.

Trong khi cộng đồng AI đang tranh luận về "AGI" và "super-intelligence", cách tiếp cận thực dụng hơn là: **ghép đúng công cụ vào đúng vấn đề, và để một orchestrator thông minh quyết định khi nào dùng cái nào**.

Đây chính xác là những gì OpenClaw + Claude Code làm — và đây là bước đi thực tế nhất để có được một AI cá nhân thực sự hữu ích ngay hôm nay.

---

*Code trong bài viết này là prototype minh họa khái niệm. Để chạy được, bạn cần cài đặt [Claude Code](https://claude.ai/code) và có Anthropic API key hợp lệ.*
