---
title: "OpenClaw + Claude Code: Kiến Trúc Hybrid AI Cá Nhân Tối Ưu Chi Phí"
description: Hướng dẫn setup thực tế OpenClaw kết hợp Claude Code tạo AI cá nhân mạnh mẽ với chi phí tối ưu: DeepSeek giá rẻ cho tác vụ tổng quát + Claude Code flat rate cho công việc kỹ thuật.
authors: [ai-enthusiast]
tags: [openclaw, claude-code, deepseek, ai-agent, cost-optimization, personal-ai, automation]
image: ./openclaw-claude-hybrid.jpg
---

**Bài toán chi phí AI cá nhân:** Làm thế nào để có trợ lý AI mạnh mẽ mà không tốn hàng trăm đô mỗi tháng? Giải pháp: Kết hợp OpenClaw (orchestrator chạy DeepSeek giá rẻ) với Claude Code (chuyên gia kỹ thuật flat rate $20/tháng).

<!-- truncate -->

## Tại Sao Cần Kiến Trúc Hybrid?

| Loại Task | Model Phù Hợp | Chi Phí | Hiệu Quả |
|-----------|---------------|---------|----------|
| Chat, Q&A, giải thích | DeepSeek Chat | ~$0.14/1M tokens | Rất tốt |
| Brainstorm, planning | DeepSeek Chat | ~$0.14/1M tokens | Tốt |
| Code review, debug | Claude Code (Opus) | Flat rate $20/tháng | Xuất sắc |
| Refactor, implement | Claude Code (Opus) | Flat rate $20/tháng | Xuất sắc |
| File operations | Claude Code | Flat rate $20/tháng | Bắt buộc |

**So sánh chi phí:**
- GPT-4 Turbo: ~$10/1M tokens input, $30/1M tokens output
- Claude 3.5 Sonnet: ~$3/1M tokens input, $15/1M tokens output  
- **DeepSeek Chat: $0.14/1M tokens input, $0.28/1M tokens output**
- **Claude Code: Flat rate $20/tháng (Claude Pro)**

## Kiến Trúc Tổng Quan: Smart Router Pattern

```
┌─────────────────────────────────────────────────┐
│            OpenClaw Orchestrator                 │
│  (DeepSeek Chat - $0.14/1M tokens)              │
│                                                 │
│  ┌─────────────┐    ┌──────────────────────┐   │
│  │  Memory     │    │   Skill Manager      │   │
│  │  System     │    │  (coding-agent,      │   │
│  │  (MEMORY.md,│    │   proactive-agent,   │   │
│  │   SOUL.md,  │    │   github, etc.)      │   │
│  │   USER.md)  │    └──────────────────────┘   │
│  └──────┬──────┘                               │
│         │                                      │
│    ┌────▼─────┐                                │
│    │  Router  │                                │
│    │ (Intent  │                                │
│    │Classifier)│                                │
│    └────┬─────┘                                │
└─────────┼──────────────────────────────────────┘
          │
    ┌─────▼────────────────────────────┐
    │                                  │
┌───▼────┐                    ┌────────▼──────┐
│General │                    │  Claude Code  │
│Tasks   │                    │  Sub-agent    │
│(90%    │                    │(Technical     │
│requests)│                    │ Tasks - 10%)  │
└────────┘                    └───────────────┘
```

## Phần 1: Setup OpenClaw Từ Đầu

### Bước 1: Cài Đặt OpenClaw

```bash
# Cài đặt OpenClaw globally
npm install -g openclaw

# Khởi tạo workspace
mkdir -p ~/.openclaw/workspace
cd ~/.openclaw/workspace

# Cấu hình model mặc định là DeepSeek (giá rẻ)
openclaw config set model.default "api-deepseek-com/deepseek-chat"

# Kiểm tra cài đặt
openclaw status
```

### Bước 2: Cấu Hình Workspace Với Các File Cốt Lõi

OpenClaw workspace cần 5 file cốt lõi để hoạt động như một AI cá nhân:

**1. SOUL.md - Định nghĩa tính cách AI:**
```markdown
# SOUL.md - Who You Are

## Core Traits
- Security-focused, analytical, pragmatic
- Prioritize safety and warn about risks
- Resourceful before asking
- Have opinions but respect boundaries

## Communication Style
- Concise when needed, thorough when it matters
- Skip filler words like "Great question!"
- Actions speak louder than words

## Technical Preferences
- Prefers direct CLI over ACP harness
- Automatically uses exec/process with pty=true for coding tasks
- No confirmation needed for routine technical work
```

**2. USER.md - Thông tin người dùng (tổng quát):**
```markdown
# USER.md - About Your Human

## Basic Info
- **Timezone:** Asia/Bangkok
- **Technical Level:** Advanced
- **Primary Use Case:** Software development, AI tooling

## Preferences
- Prefers technical depth over surface explanations
- Values cost optimization in AI tooling
- Appreciates automation of repetitive tasks
- Direct communication style

## Projects & Context
- Active software development projects
- AI/ML experimentation
- Open source contributions
```

**3. MEMORY.md - Long-term memory (không cá nhân hóa):**
```markdown
# MEMORY.md - Long-Term Memory

## Security Principles
1. Never expose credentials, tokens, or sensitive data in clear text
2. Security first, always
3. Handle sensitive information with utmost care

## Technical Preferences
- Prefers practical solutions over theoretical perfection
- Values cost optimization in AI tooling
- Appreciates automation of repetitive tasks

## Architecture Decisions
- Hybrid AI approach: DeepSeek for general tasks + Claude Code for technical work
- Smart router pattern for cost optimization
- Workspace-based memory system for continuity
```

**4. AGENTS.md - Workspace guidelines:**
```markdown
# AGENTS.md - Your Workspace

## Memory Management
- Write everything down (no "mental notes")
- Update MEMORY.md with significant events
- Use daily notes in memory/YYYY-MM-DD.md for raw logs

## Safety Rules
- Don't exfiltrate private data
- Ask before external actions (emails, tweets)
- `trash` > `rm` for recoverability

## Technical Workflow
- Use exec with pty=true for coding tasks
- Automatically route technical tasks to Claude Code
- Batch similar requests for efficiency
```

**5. HEARTBEAT.md - Proactive checks (tùy chọn):**
```markdown
# HEARTBEAT.md - Periodic Checks

## Daily Checks (rotate)
- [ ] Check calendar for upcoming events
- [ ] Review GitHub notifications
- [ ] Check weather if outdoor activities planned
- [ ] Review memory files for maintenance

## Weekly Maintenance
- [ ] Update MEMORY.md with significant learnings
- [ ] Review and organize workspace files
- [ ] Check for OpenClaw updates
```

### Bước 3: Cài Đặt Skills Quan Trọng

```bash
# Cài đặt coding-agent skill (quan trọng nhất)
clawhub install coding-agent

# Cài đặt proactive-agent skill  
clawhub install proactive-agent

# Cài đặt github skill
clawhub install github

# Cài đặt self-improvement skill
clawhub install self-improvement

# Kiểm tra skills đã cài đặt
ls ~/.openclaw/workspace/skills/
```

**Cấu trúc thư mục skills:**
```
~/.openclaw/workspace/skills/
├── coding-agent/
│   ├── SKILL.md          # Hướng dẫn sử dụng coding-agent
│   └── examples/         # Ví dụ thực tế
├── proactive-agent/
│   ├── SKILL.md          # Hướng dẫn proactive behavior
│   └── templates/        # Templates cho automation
├── github/
│   └── SKILL.md          # GitHub integration
└── self-improvement/
    └── SKILL.md          # Continuous learning system
```

## Phần 2: Cài Đặt Và Cấu Hình Claude Code

### Bước 1: Cài Đặt Claude Code

```bash
# Cài đặt Claude Code CLI
# Yêu cầu: Đã có Claude Pro subscription
# Tải từ https://claude.ai/code

# Sau khi cài đặt, kiểm tra
claude --version

# Cấu hình working directory mặc định
export CLAUDE_PROJECTS_DIR="~/projects/"
```

### Bước 2: Tích Hợp Claude Code Với OpenClaw

**File: ~/.openclaw/workspace/TOOLS.md**
```markdown
# TOOLS.md - Integration Notes

## Claude Code Configuration
- **CLI Path:** /usr/local/bin/claude
- **Default Model:** claude-3-5-sonnet-20241022
- **Working Directory:** ~/projects/
- **Security Scope:** Only allowed project directories

## Integration Rules
1. Use Claude Code only for technical tasks requiring file operations
2. Route general questions to DeepSeek ($0.14/1M tokens)
3. Batch similar technical tasks to minimize context switching
4. Always use pty=true when executing Claude Code via exec

## Cost Optimization
- DeepSeek: ~$2-5/month for general tasks
- Claude Code: $20 flat rate for unlimited technical work
- **Total: ~$22-25/month** (vs $50-100+ for GPT-4 only)
```

## Phần 3: Implement Smart Router

### File: ~/.openclaw/workspace/scripts/router.py

```python
#!/usr/bin/env python3
"""
Smart Router for OpenClaw + Claude Code Hybrid AI
Classifies user requests and routes to optimal backend
"""

import re
from typing import Dict, List, Tuple

class IntentClassifier:
    """Classify user intent for cost-optimal routing"""
    
    # Tasks suitable for DeepSeek (cheap)
    DEEPSEEK_KEYWORDS = [
        # General conversation
        "explain", "what is", "how to", "tell me about",
        "summarize", "translate", "brainstorm", "plan",
        # Information queries
        "when", "where", "who", "why", "which",
        # Light technical
        "concept", "theory", "compare", "advantages", "disadvantages",
        # Personal/organizational
        "remind", "schedule", "email", "calendar", "organize",
        "remember", "preference", "opinion", "suggest"
    ]
    
    # Tasks requiring Claude Code (technical/file operations)
    CLAUDE_CODE_KEYWORDS = [
        # File operations
        "create file", "edit file", "delete file", "modify",
        "write code", "implement", "add feature", "update",
        # Debugging
        "fix bug", "debug", "error in", "won't compile", "fix error",
        # Refactoring
        "refactor", "optimize", "clean up", "restructure", "improve",
        # Testing
        "write test", "add test", "test coverage", "unit test",
        # CI/CD & Deployment
        "deploy", "build", "pipeline", "github action", "docker",
        # Complex technical
        "architecture", "design pattern", "system design", "algorithm",
        # Code review
        "review code", "code review", "check code", "analyze code"
    ]
    
    # File extensions that indicate technical work
    FILE_EXTENSIONS = [
        '.py', '.js', '.ts', '.java', '.cpp', '.c', '.go', '.rs',
        '.php', '.rb', '.swift', '.kt', '.scala', '.sql', '.sh',
        '.yml', '.yaml', '.json', '.xml', '.html', '.css', '.scss',
        '.md', '.txt', '.csv', '.tsv'
    ]
    
    def classify(self, user_input: str) -> Dict[str, any]:
        """Classify intent with confidence score"""
        input_lower = user_input.lower()
        
        # Check for file operations or extensions
        if self._contains_file_reference(input_lower):
            return {
                "backend": "claude_code",
                "reason": "Contains file reference or extension",
                "confidence": 0.9,
                "estimated_cost": "flat_rate"
            }
        
        # Check for Claude Code keywords
        claude_matches = []
        for keyword in self.CLAUDE_CODE_KEYWORDS:
            if keyword in input_lower:
                claude_matches.append(keyword)
        
        if claude_matches:
            return {
                "backend": "claude_code",
                "reason": f"Technical task: {', '.join(claude_matches[:3])}",
                "confidence": 0.85,
                "estimated_cost": "flat_rate"
            }
        
        # Check for DeepSeek keywords
        deepseek_matches = []
        for keyword in self.DEEPSEEK_KEYWORDS:
            if keyword in input_lower:
                deepseek_matches.append(keyword)
        
        if deepseek_matches:
            return {
                "backend": "deepseek",
                "reason": f"General task: {', '.join(deepseek_matches[:3])}",
                "confidence": 0.8,
                "estimated_cost": "~$0.0001-0.001"
            }
        
        # Default to DeepSeek for cost efficiency
        return {
            "backend": "deepseek",
            "reason": "General conversation (default for cost optimization)",
            "confidence": 0.7,
            "estimated_cost": "~$0.0001"
        }
    
    def _contains_file_reference(self, text: str) -> bool:
        """Check if text contains file references"""
        # Check for common file patterns
        patterns = [
            r'\b\w+\.(py|js|ts|java|cpp|go|rs|php|rb|swift|kt|md|txt|json|yml|yaml|xml|html|css)\b',
            r'file\s+\w+',
            r'create\s+\w+\.\w+',
            r'edit\s+\w+\.\w+',
            r'open\s+\w+\.\w+'
        ]
        
        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        
        return False


class CostOptimizer:
    """Track and optimize AI usage costs"""
    
    def __init__(self):
        # Cost per 1M tokens (USD)
        self.costs = {
            "deepseek": {
                "input": 0.14 / 1_000_000,
                "output": 0.28 / 1_000_000
            },
            "claude_code": {
                "monthly": 20.0  # Flat rate
            }
        }
        
        # Usage tracking
        self.usage = {
            "deepseek_tokens": {"input": 0, "output": 0},
            "claude_code_requests": 0,
            "month_start": None
        }
    
    def estimate_request_cost(self, backend: str, input_tokens: int = 100, output_tokens: int = 200) -> float:
        """Estimate cost for a single request"""
        if backend == "deepseek":
            input_cost = input_tokens * self.costs["deepseek"]["input"]
            output_cost = output_tokens * self.costs["deepseek"]["output"]
            return input_cost + output_cost
        else:  # claude_code
            # Flat rate, so marginal cost is 0
            return 0.0
    
    def get_monthly_summary(self) -> Dict[str, any]:
        """Get monthly cost summary"""
        deepseek_cost = (
            self.usage["deepseek_tokens"]["input"] * self.costs["deepseek"]["input"] +
            self.usage["deepseek_tokens"]["output"] * self.costs["deepseek"]["output"]
        )
        
        total_cost = deepseek_cost + self.costs["claude_code"]["monthly"]
        
        # Comparison with GPT-4 only approach
        # Assuming similar usage would cost ~$50-100 with GPT-4
        gpt4_estimated = 75.0  # Conservative estimate
        savings_percent = ((gpt4_estimated - total_cost) / gpt4_estimated) * 100
        
        return {
            "deepseek_cost": round(deepseek_cost, 2),
            "claude_code_cost": self.costs["claude_code"]["monthly"],
            "total_monthly": round(total_cost, 2),
            "savings_vs_gpt4": round(savings_percent, 1),
            "savings_amount": round(gpt4_estimated - total_cost, 2),
            "usage_stats": {
                "deepseek_tokens": self.usage["deepseek_tokens"],
                "claude_code_requests": self.usage["claude_code_requests"]
            }
        }


class OpenClawRouter:
    """Main router integrating classifier and cost optimizer"""
    
    def __init__(self, workspace_dir: str = "~/.openclaw/workspace"):
        self.classifier = IntentClassifier()
        self.cost_optimizer = CostOptimizer()
        self.workspace_dir = workspace_dir
        
    def route(self, user_input: str, context: str = "") -> Dict[str, any]:
        """Route user request to appropriate backend"""
        
        # 1. Classify intent
        intent = self.classifier.classify(user_input)
        
        # 2. Update cost tracking
        if intent["backend"] == "deepseek":
            # Estimate tokens (rough approximation)
            input_tokens = len(user_input.split()) * 1.3
            output_tokens = input_tokens * 2  # Assume 2x output
            self.cost_optimizer.usage["deepseek_tokens"]["input"] += int(input_tokens)
            self.cost_optimizer.usage["deepseek_tokens"]["output"] += int(output_tokens)
        else:
            self.cost_optimizer.usage["claude_code_requests"] += 1
        
        # 3. Prepare execution command
        execution_plan = self._prepare_execution(intent["backend"], user_input, context)
        
        # 4. Return routing decision
        return {
            "intent": intent,
            "execution_plan": execution_plan,
            "cost_summary": self.cost_optimizer.get_monthly_summary(),
            "recommendation": self._get_recommendation(intent["backend"])
        }
    
    def _prepare_execution(self, backend: str, user_input: str, context: str) -> Dict[str, str]:
        """Prepare execution command based on backend"""
        if backend == "claude_code":
            return {
                "type": "claude_code",
                "command": f'claude "{user_input}"',
                "working_dir": "~/projects/",
                "notes": "Requires Claude Pro subscription. Use pty=true for terminal.",
                "estimated_time": "1-5 minutes"
            }
        else:  # deepseek
            return {
                "type": "openclaw_deepseek",
                "command": f'openclaw chat "{user_input}"',
                "working_dir": self.workspace_dir,
                "notes": "Uses DeepSeek Chat API. Cost efficient for general tasks.",
                "estimated_time": "10-30 seconds"
            }
    
    def _get_recommendation(self, backend: str) -> str:
        """Get human-readable recommendation"""
        if backend == "claude_code":
            return "Route to Claude Code: Technical task requiring file operations or complex coding."
        else:
            return "Route to DeepSeek: General conversation or light technical question. Cost efficient."


# Usage Example
if __name__ == "__main__":
    router = OpenClawRouter()
    
    # Test cases
    test_requests = [
        "Explain the difference between microservices and monolith architecture",
        "Fix the TypeScript error in src/utils/auth.ts line 89",
        "What's the weather forecast for tomorrow?",
        "Refactor the user authentication module to use JWT tokens",
        "Help me plan my weekly schedule and meetings",
        "Create a new React component for user profile with TypeScript",
        "Summarize the key points from yesterday's meeting notes"
    ]
    
    print("Smart Router Test Results:")
    print("=" * 80)
    
    for req in test_requests:
        result = router.route(req)
        print(f"\nRequest: {req[:60]}...")
        print(f"Backend: {result['intent']['backend']}")
        print(f"Reason: {result['intent']['reason']}")
        print(f"Estimated Cost: {result['intent']['estimated_cost']}")
        print(f"Recommendation: {result['recommendation']}")
        print("-" * 80)
```

## Phần 4: Use Cases Thực Tế

### Case 1: Debugging Complex Issue
```
User: "Có lỗi runtime trong file src/api/server.js dòng 89 khi parse JSON"
OpenClaw Router: → Claude Code (Technical task with file reference)
Claude Code: Đọc file, chạy debug, fix lỗi, chạy test
Cost: $0 (nằm trong flat rate $20/tháng)
Time: 2-3 minutes
```

### Case 2: Technical Explanation  
```
User: "Giải thích React Server Components vs Client Components với ví dụ"
OpenClaw Router: → DeepSeek (General technical explanation)
DeepSeek: Giải thích chi tiết với code examples
Cost: ~$0.0001 (vài cents)
Time: 10-20 seconds
```

### Case 3: Project Planning & Implementation
```
User: "Lên kế hoạch migrate từ REST sang GraphQL cho project Node.js"
Step 1: OpenClaw Router → DeepSeek (Planning phase)
Step 2: DeepSeek tạo migration plan với phases
Step 3: User xác nhận plan → Claude Code implement từng phase
Total Cost: ~$0.50 (planning) + flat rate (implementation)
```

### Case 4: Daily Assistant Tasks
```
User: "Nhắc tôi meeting lúc 3pm và draft email cho client về progress"
OpenClaw Router: → DeepSeek (General assistant tasks)
DeepSeek: Set reminder + draft email template
Cost: ~$0.0002
Time: 15 seconds
```

## Phần 5: Tối Ưu Chi Phí Chi Tiết

### 1. Token Usage Optimization Strategies

**DeepSeek Optimization:**
- **Context Management:** Clear old context khi không cần
- **Response Length Limits:** Set max_tokens phù hợp với task
- **Batch Processing:** Group related questions vào một request
- **Caching:** Store frequent responses để tái sử dụng
- **Compression:** Use concise prompts và responses

**Claude Code Optimization:**
- **Task Batching:** Group code changes vào một session
- **Offline Queue:** Queue non-urgent technical tasks
- **Review Sessions:** Weekly code review thay vì từng file
- **Template Usage:** Create code templates cho common patterns

### 2. Monthly Cost Breakdown (Ước Tính Thực Tế)

| Component | Cost | Usage Pattern | Optimization Tips |
|-----------|------|---------------|-------------------|
| **DeepSeek Chat** | ~$2-5/month | 10-30k requests/day | Context management, batching |
| **Claude Code** | $20 flat rate | Unlimited technical tasks | Batch processing, offline queue |
| **Total** | **$22-25/month** | Full AI assistant | **~50-70% cheaper than GPT-4 only** |

### 3. So Sánh Với Các Giải Pháp Khác

| Solution | Monthly Cost | Technical Depth | General Intelligence | Best For |
|----------|--------------|-----------------|---------------------|----------|
| GPT-4 Only | ~$50-100 | Good | Excellent | Teams với budget lớn |
| Claude 3.5 Only | ~$40-80 | Excellent | Excellent | Technical-heavy work |
| **OpenClaw + Claude Code** | **~$22-25** | **Excellent** | **Very Good** | **Cost-conscious developers** |
| DeepSeek Only | ~$5-10 | Fair | Good | General Q&A, light usage |
| Local Models | $0 (hardware) | Variable | Variable | Privacy-focused, technical users |

**Ưu điểm của hybrid approach:**
- **Cost Efficiency:** 50-70% tiết kiệm so với GPT-4
- **Technical Excellence:** Claude Code cho coding tasks
- **General Intelligence:** DeepSeek cho conversation
- **Flexibility:** Có thể thay đổi model khi cần

## Phần 6: Best Practices Cho Production Setup

### 1. Security Hardening

```bash
# Restrict Claude Code directory access
export CLAUDE_ALLOWED_DIRS="~/projects/,~/workspace/,~/development/"
export CLAUDE_DENIED_DIRS="~/.ssh/,~/Documents/private/,~/.config/"

# OpenClaw security configuration
openclaw config set security.sandbox true
openclaw config set security.askBeforeExternal true

# Regular security audits
cron add --name "weekly-security-audit" \
  --schedule "0 0 * * 0" \
  --payload '{"kind":"agentTurn","message":"Run security audit: check for exposed credentials, review access logs, update dependencies"}' \
  --sessionTarget isolated
```

### 2. Monitoring & Analytics

**File: ~/.openclaw/workspace/scripts/monitor.py**
```python
#!/usr/bin/env python3
"""
Monitoring and analytics for hybrid AI setup
"""

import json
import time
from datetime import datetime, timedelta
import sqlite3
from pathlib import Path

class AICostMonitor:
    """Monitor AI usage and costs"""
    
    def __init__(self, db_path: str = "~/.openclaw/ai_usage.db"):
        self.db_path = Path(db_path).expanduser()
        self._init_db()
    
    def _init_db(self):
        """Initialize database schema"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usage_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                backend TEXT NOT NULL,
                request_type TEXT,
                input_tokens INTEGER,
                output_tokens INTEGER,
                duration_ms INTEGER,
                success BOOLEAN,
                cost_estimate REAL
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS daily_summary (
                date DATE PRIMARY KEY,
                deepseek_requests INTEGER DEFAULT 0,
                claude_code_requests INTEGER DEFAULT 0,
                total_cost REAL DEFAULT 0.0,
                avg_response_time_ms INTEGER DEFAULT 0
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def log_request(self, backend: str, request_type: str, 
                   input_tokens: int = 0, output_tokens: int = 0,
                   duration_ms: int = 0, success: bool = True):
        """Log a single request"""
        # Calculate cost estimate
        if backend == "deepseek":
            cost = (input_tokens * 0.14/1_000_000) + (output_tokens * 0.28/1_000_000)
        else:
            cost = 0.0  # Flat rate
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO usage_log 
            (backend, request_type, input_tokens, output_tokens, duration_ms, success, cost_estimate)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (backend, request_type, input_tokens, output_tokens, duration_ms, success, cost))
        
        conn.commit()
        conn.close()
        
        # Update daily summary
        self._update_daily_summary(backend, cost, duration_ms)
    
    def _update_daily_summary(self, backend: str, cost: float, duration_ms: int):
        """Update daily summary statistics"""
        today = datetime.now().date().isoformat()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get or create today's summary
        cursor.execute('SELECT * FROM daily_summary WHERE date = ?', (today,))
        row = cursor.fetchone()
        
        if row:
            if backend == "deepseek":
                cursor.execute('''
                    UPDATE daily_summary 
                    SET deepseek_requests = deepseek_requests + 1,
                        total_cost = total_cost + ?,
                        avg_response_time_ms = ((avg_response_time_ms * deepseek_requests) + ?) / (deepseek_requests + 1)
                    WHERE date = ?
                ''', (cost, duration_ms, today))
            else:
                cursor.execute('''
                    UPDATE daily_summary 
                    SET claude_code_requests = claude_code_requests + 1,
                        total_cost = total_cost + ?
                    WHERE date = ?
                ''', (cost, today))
        else:
            if backend == "deepseek":
                cursor.execute('''
                    INSERT INTO daily_summary (date, deepseek_requests, total_cost, avg_response_time_ms)
                    VALUES (?, 1, ?, ?)
                ''', (today, cost, duration_ms))
            else:
                cursor.execute('''
                    INSERT INTO daily_summary (date, claude_code_requests, total_cost)
                    VALUES (?, 1, ?)
                ''', (today, cost))
        
        conn.commit()
        conn.close()
    
    def get_daily_report(self, date: str = None) -> Dict:
        """Get daily usage report"""
        if date is None:
            date = datetime.now().date().isoformat()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM daily_summary WHERE date = ?', (date,))
        row = cursor.fetchone()
        
        if not row:
            return {"error": "No data for date"}
        
        # Calculate savings vs GPT-4
        # Assume similar usage would cost 3x more with GPT-4
        estimated_gpt4_cost = row[3] * 3  # total_cost * 3
        savings = estimated_gpt4_cost - row[3]
        savings_percent = (savings / estimated_gpt4_cost) * 100 if estimated_gpt4_cost > 0 else 0
        
        report = {
            "date": row[0],
            "deepseek_requests": row[1],
            "claude_code_requests": row[2],
            "total_cost": round(row[3], 4),
            "avg_response_time_ms": row[4] if row[4] else 0,
            "estimated_gpt4_cost": round(estimated_gpt4_cost, 2),
            "savings": round(savings, 2),
            "savings_percent": round(savings_percent, 1)
        }
        
        conn.close()
        return report
    
    def get_weekly_summary(self) -> Dict:
        """Get weekly summary"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get last 7 days
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=6)
        
        cursor.execute('''
            SELECT 
                SUM(deepseek_requests) as total_deepseek,
                SUM(claude_code_requests) as total_claude,
                SUM(total_cost) as weekly_cost,
                AVG(avg_response_time_ms) as avg_response_time
            FROM daily_summary 
            WHERE date BETWEEN ? AND ?
        ''', (start_date.isoformat(), end_date.isoformat()))
        
        row = cursor.fetchone()
        conn.close()
        
        if not row or row[0] is None:
            return {"error": "No data for period"}
        
        weekly_cost = row[2] or 0
        estimated_monthly = weekly_cost * 4.33  # Extrapolate to monthly
        
        return {
            "period": f"{start_date} to {end_date}",
            "total_deepseek_requests": row[0] or 0,
            "total_claude_code_requests": row[1] or 0,
            "weekly_cost": round(weekly_cost, 2),
            "estimated_monthly_cost": round(estimated_monthly, 2),
            "avg_response_time_ms": round(row[3] or 0, 0)
        }


# Integration with OpenClaw
def create_monitoring_cron():
    """Create cron job for daily monitoring report"""
    cron_config = {
        "name": "daily-ai-usage-report",
        "schedule": {
            "kind": "cron",
            "expr": "0 9 * * *",  # 9:00 AM daily
            "tz": "Asia/Bangkok"
        },
        "payload": {
            "kind": "agentTurn",
            "message": "Generate daily AI usage report. Check monitoring database and send summary to user."
        },
        "sessionTarget": "isolated",
        "delivery": {
            "mode": "announce",
            "channel": "telegram"
        }
    }
    
    return cron_config
```

### 3. Performance Tuning

```bash
# Optimize OpenClaw response time
openclaw config set model.timeout 30
openclaw config set model.maxTokens 4096
openclaw config set model.temperature 0.7

# Configure Claude Code for optimal performance
export CLAUDE_MAX_TOKENS=8192
export CLAUDE_TEMPERATURE=0.2  # Lower for coding tasks
export CLAUDE_THINKING_BUDGET=3000

# Set up performance monitoring
cron add --name "weekly-performance-review" \
  --schedule "0 0 * * 0" \
  --payload '{"kind":"agentTurn","message":"Review AI performance: response times, success rates, user satisfaction. Suggest optimizations."}' \
  --sessionTarget isolated
```

## Phần 7: Troubleshooting & Maintenance

### Common Issues & Solutions

**Issue 1: Claude Code không chạy được**
```bash
# Kiểm tra cài đặt
claude --version

# Kiểm tra Claude Pro subscription
# Truy cập https://claude.ai/account

# Kiểm tra permissions
ls -la ~/.claude/
chmod 755 ~/.claude/
```

**Issue 2: OpenClaw không nhận diện được file workspace**
```bash
# Kiểm tra workspace directory
ls -la ~/.openclaw/workspace/

# Kiểm tra các file cốt lõi
test -f ~/.openclaw/workspace/SOUL.md && echo "SOUL.md exists" || echo "Missing SOUL.md"
test -f ~/.openclaw/workspace/USER.md && echo "USER.md exists" || echo "Missing USER.md"
test -f ~/.openclaw/workspace/MEMORY.md && echo "MEMORY.md exists" || echo "Missing MEMORY.md"

# Khởi tạo lại nếu cần
openclaw init --force
```

**Issue 3: Chi phí cao hơn dự kiến**
```bash
# Kiểm tra usage logs
openclaw logs --last 100 | grep -i "tokens\|cost"

# Review routing decisions
python3 ~/.openclaw/workspace/scripts/router.py --analyze

# Adjust routing thresholds
# Giảm confidence threshold cho Claude Code nếu quá nhiều request
```

**Issue 4: Memory không persist giữa sessions**
```bash
# Kiểm tra memory files
ls -la ~/.openclaw/workspace/memory/

# Kiểm tra permissions
chmod 644 ~/.openclaw/workspace/memory/*.md 2>/dev/null

# Kiểm tra git status nếu dùng git
cd ~/.openclaw/workspace && git status

# Tạo daily memory file nếu chưa có
date_str=$(date +%Y-%m-%d)
touch ~/.openclaw/workspace/memory/${date_str}.md
```

### Monthly Maintenance Checklist

**Mỗi tuần:**
```bash
# 1. Review và update MEMORY.md
openclaw chat "Review recent memory files and update MEMORY.md with significant learnings"

# 2. Clean up old files
find ~/.openclaw/workspace/tmp -type f -mtime +7 -delete

# 3. Update skills
clawhub update --all

# 4. Backup workspace
tar -czf ~/backups/openclaw-workspace-$(date +%Y%m%d).tar.gz ~/.openclaw/workspace/
```

**Mỗi tháng:**
```bash
# 1. Review cost optimization
python3 ~/.openclaw/workspace/scripts/monitor.py --monthly-report

# 2. Update model configurations
openclaw config get model.default
# Kiểm tra có model mới tốt hơn không

# 3. Security audit
openclaw chat "Run security audit: check for exposed credentials, review access logs"

# 4. Performance review
openclaw chat "Review AI performance metrics and suggest improvements"
```

## Phần 8: Kết Luận

### Tóm Tắt Lợi Ích

**1. Chi Phí Tối Ưu (~$22-25/tháng):**
- DeepSeek: $2-5 cho general tasks (90% requests)
- Claude Code: $20 flat rate cho technical work (10% requests)
- **Tiết kiệm 50-70% so với GPT-4 only**

**2. Hiệu Suất Cao:**
- Claude Code: Xuất sắc cho coding, refactoring, debugging
- DeepSeek: Rất tốt cho conversation, explanation, planning
- Smart Router: Tự động chọn model phù hợp

**3. Tính Linh Hoạt:**
- Có thể thay đổi model khi cần
- Dễ dàng tích hợp skills mới
- Workspace-based memory system

**4. Bảo Mật & Privacy:**
- Local workspace với full control
- Configurable security settings
- No data sharing với third parties

### Roadmap Phát Triển

**Short-term (1-3 tháng):**
- [ ] Thêm support cho local models (Llama, Mistral)
- [ ] Implement advanced caching system
- [ ] Add multi-language support
- [ ] Create GUI dashboard for monitoring

**Medium-term (3-6 tháng):**
- [ ] Implement team collaboration features
- [ ] Add voice interface integration
- [ ] Create plugin ecosystem
- [ ] Advanced analytics và reporting

**Long-term (6-12 tháng):**
- [ ] Autonomous project management
- [ ] Predictive task routing
- [ ] Self-optimizing architecture
- [ ] Enterprise-grade security features

### Getting Started Checklist

```bash
# 1. Cài đặt OpenClaw
npm install -g openclaw

# 2. Khởi tạo workspace
openclaw init

# 3. Cấu hình model mặc định
openclaw config set model.default "api-deepseek-com/deepseek-chat"

# 4. Tạo các file cốt lõi
touch ~/.openclaw/workspace/{SOUL.md,USER.md,MEMORY.md,AGENTS.md}

# 5. Cài đặt Claude Code
# Download từ https://claude.ai/code

# 6. Cài đặt skills
clawhub install coding-agent
clawhub install proactive-agent
clawhub install github

# 7. Deploy smart router
cp scripts/router.py ~/.openclaw/workspace/scripts/

# 8. Start using!
openclaw chat "Hello! Let's optimize our AI setup together."
```

### Tài Nguyên Hữu Ích

**Documentation:**
- [OpenClaw Docs](https://docs.openclaw.ai)
- [Claude Code Documentation](https://docs.anthropic.com/claude/code)
- [DeepSeek API Docs](https://platform.deepseek.com/api-docs)

**Community:**
- [OpenClaw Discord](https://discord.com/invite/clawd)
- [Claude Community](https://community.anthropic.com)
- [DeepSeek Forum](https://forum.deepseek.com)

**Tools & Skills:**
- [ClawHub Skill Marketplace](https://clawhub.com)
- [OpenClaw GitHub](https://github.com/openclaw/openclaw)
- [Sample Configurations](https://github.com/openclaw/examples)

---

**Lời cuối:** Kiến trúc hybrid AI này không chỉ là giải pháp tiết kiệm chi phí, mà còn là cách tiếp cận thông minh để tận dụng điểm mạnh của từng model. Với ~$25/tháng, bạn có được trợ lý AI mạnh mẽ hơn nhiều giải pháp đắt tiền khác.

**Câu hỏi hay feedback?** Hãy chia sẻ trong comments hoặc tham gia community discussion!

*Last updated: March 2026*  
*Estimated monthly savings vs GPT-4: $50-75*  
*Technical satisfaction: 9/10*  
*Cost efficiency: 10/10*