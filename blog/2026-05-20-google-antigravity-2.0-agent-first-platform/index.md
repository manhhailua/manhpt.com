---
title: "Google Antigravity 2.0: Từ IDE đơn lẻ thành nền tảng agent-first toàn diện"
authors: [manhpt]
tags: [google, antigravity, agentic-ai, google-io, coding-agent, multi-agent, gemini, ai-tools, vietnamese]
date: 2026-05-20
description: "Google ra mắt Antigravity 2.0 tại I/O 2026 với ứng dụng desktop, CLI, SDK, Managed Agents API, và nền tảng doanh nghiệp. Đây không còn là một IDE — mà là cả hệ sinh thái điều phối đa tác nhân."
---

Google vừa có một cú "lột xác" đáng gờm với Antigravity. Nếu phiên bản 1.0 ra mắt tháng 11/2025 chỉ là một IDE hỗ trợ viết mã bằng AI, thì Antigravity 2.0 là cả một hệ sinh thái phát triển xoay quanh **điều phối đa tác nhân (multi-agent orchestration)**. Đây không còn là một công cụ — mà là một nền tảng.

Điều đáng chú ý: Google đã dùng chính Antigravity để đồng phát triển Gemini 3.5 Flash — mô hình mặc định của nền tảng này. "Ăn cơm nhà nấu" ở cấp độ cao nhất.

<!-- truncate -->

## Antigravity 2.0 thực sự là gì?

Đừng nhầm: Antigravity 2.0 không phải là một ứng dụng. Nó là **5 thành phần** được Google đóng gói thành một nền tảng thống nhất:

| Thành phần | Vai trò | Đối tượng |
|---|---|---|
| **Desktop App 2.0** | IDE độc lập với điều phối đa tác nhân | Lập trình viên cá nhân |
| **Antigravity CLI** | Chạy trên terminal, viết bằng Go | Người dùng thành thạo, tự động hóa, CI/CD |
| **Antigravity SDK** | Truy cập lập trình vào bộ khung tác nhân | Nhóm muốn tự vận hành AI Agent |
| **Managed Agents API** | Tác nhân phi máy chủ qua Gemini API | Ai đang dùng Gemini API |
| **Enterprise Agent Platform** | Triển khai doanh nghiệp qua Google Cloud | Tổ chức, doanh nghiệp |

Lượng sản phẩm trong một đợt phát hành này nhiều hơn phần lớn những gì Google tung ra trong cả năm.

---

## 1. Desktop App 2.0 — Trái tim của nền tảng

Desktop app là sản phẩm chủ lực. Ở 2.0, nó được xây lại từ đầu với những cải tiến cốt lõi:

### 🧩 Dynamic Subagents — Chia việc, chạy song song

Đây là tính năng quan trọng nhất. Ở 1.0, Manager Surface chỉ cho phép theo dõi từng tác nhân một. Ở 2.0, AI Agent chính có thể **tự sinh tác nhân con (subagent)** để song song hóa công việc.

Ví dụ: bạn bảo AI Agent "kiểm tra luồng xác thực trên tất cả microservice". Nó tự chia thành một cây tác nhân con, mỗi tác nhân lo một dịch vụ, tất cả chạy đồng thời. Kết quả được truyền ngược về Manager Surface.

Giới hạn thực tế: khoảng 4-5 tác nhân song song trước khi hiệu năng suy giảm. Với máy hạn chế RAM, đặt `parallelAgents: 1` để chạy tuần tự.

### ⏰ Scheduled Tasks — Tác nhân chạy nền tự động

Tự động hóa nền giờ được hỗ trợ đầy đủ. Định nghĩa lịch dạng cron, AI Agent tự chạy mà không cần mở ứng dụng. Trường hợp điển hình:

- Nâng cấp thư viện phụ thuộc hàng đêm
- Quét bảo mật định kỳ
- Dọn dẹp tái cấu trúc mỗi khi đẩy thẻ phát hành

Lưu ý quan trọng: thiết kế có tính lặp lại an toàn (idempotent) — lịch dạng cron có thể kích hoạt nhầm và chạy 2 lần.

### 🎙️ Lệnh bằng giọng nói

Đọc mã, yêu cầu xem khác biệt, chạy kiểm thử bằng giọng nói. Nhất quán với chiến lược triển khai giọng nói của Google trên Gmail, Docs. Nhanh cho lệnh ngắn, không hợp cho đặc tả nhiều dòng — dùng kết hợp cả hai.

### 🖥️ Browser Agent — Điểm khác biệt lớn nhất

Đây là **điểm khác biệt quan trọng nhất** so với Claude Code và Cursor. Antigravity 2.0 có một trình duyệt Chromium tích hợp sẵn, không phải tiện ích gắn thêm, cho phép AI Agent:

- Duyệt trang web
- Nhấn nút
- Bật/tắt công cụ lập trình
- Chuyển khung nhìn di động
- Kiểm tra trực quan thay đổi frontend mà không cần viết kiểm thử Playwright

Nhóm nặng frontend: đây là lý do để chuyển sang. Nhóm backend/hạ tầng: không quan trọng lắm.

### 🔗 Tích hợp hệ sinh thái Google

- **Google AI Studio**: Xuất dự án qua lại với một nhấp chuột
- **Android**: Dựng ứng dụng di động với vòng lặp tác nhân gốc
- **Firebase**: Triển khai không cần chuyển ngữ cảnh
- **Google Workspace**: AI Agent gọi trực tiếp API Docs, Sheets, Calendar

---

## 2. Antigravity CLI — Ưu tiên terminal, viết bằng Go

CLI được viết lại bằng **Go** — nhanh hơn, nhẹ hơn Gemini CLI cũ. Điểm đáng giá:

- Cùng một bộ khung tác nhân với desktop app → mọi cải tiến tác nhân lõi tự động áp dụng cho cả hai
- Tùy chọn đồng bộ hai chiều với desktop app
- Sẵn sàng SSH — hoạt động mượt qua phiên từ xa
- Hỗ trợ tác nhân con động ngay từ terminal
- Gắn vào móc kiểm tra trước khi commit, đường ống CI, cổng kiểm tra trước triển khai

```bash
# Cài đặt
curl -fsSL https://antigravity.google/cli/install.sh | bash

# Sử dụng
antigravity agent run "tái cấu trúc middleware giới hạn tốc độ" \
  --repo ./services/api \
  --model gemini-3.5-flash
```

### ⚠️ Hạn chót: Gemini CLI ngừng hoạt động ngày 18/06/2026

Nếu bạn đang dùng Gemini CLI hoặc tiện ích mở rộng Gemini Code Assist IDE trên gói miễn phí/AI Pro/AI Ultra → **phải di chuyển trước 18/06**. API sẽ ngừng phục vụ yêu cầu. Người dùng doanh nghiệp trên giấy phép Standard/Enterprise không bị ảnh hưởng.

Các tính năng được giữ lại: Agent Skill, Hooks, Subagents, và Extensions (nay gọi là Antigravity plugin). Nhưng không tương đương hoàn toàn về tính năng — một số quy trình ở trường hợp biên cần điều chỉnh.

---

## 3. Antigravity SDK — Tự dựng AI Agent, tự vận hành

SDK mở quyền truy cập lập trình vào bộ khung tác nhân của Google:

```python
from antigravity import Agent, Tool

agent = Agent(
    model="gemini-3.5-flash",
    tools=[Tool.shell, Tool.code_edit, Tool.web_search],
    system="Bạn là người duyệt mã backend. Từ chối mọi PR gửi SQL mà không có chỉ mục.",
)
result = agent.run("duyệt PR #421")
print(result.artifacts)
```

Cài đặt: `pip install google-antigravity`. SDK được tối ưu cho các mô hình Gemini → độ trễ thấp hơn, chi phí thấp hơn khi dùng họ mô hình của Google. Tự vận hành ở bất kỳ đâu: EC2, Vertex AI, tại chỗ.

---

## 4. Managed Agents API — Tác nhân phi máy chủ

Đây là mảnh ghép quan trọng nhất cho người dùng API. Một lần gọi API duy nhất → khởi tạo một AI Agent tự động trong **môi trường Linux riêng biệt**, với:

- **Trạng thái bền vững** qua các phiên nhiều lượt — tệp và trạng thái được giữ nguyên giữa các lần gọi
- AI Agent tự suy luận, dùng công cụ, chạy mã, duyệt web
- Không cần tự viết mã điều phối
- Trả tiền theo lần chạy (không phải theo token)

Vị trí của Managed Agents trong ngăn xếp:

| Cách tiếp cận | Ai lo vòng lặp? | Khi nào dùng? |
|---|---|---|
| **Gọi trực tiếp mô hình** | Bạn | Suy luận khối lượng lớn, một bước |
| **Managed Agents** | Google | Tác vụ chạy dài, độ tin cậy quan trọng |
| **Desktop / CLI / SDK** | Bạn (cục bộ) | Tải nhạy cảm không thể rời VPC |

Nhóm vận hành thực tế sẽ pha trộn cả ba. Gọi trực tiếp cho suy luận khối lượng lớn. Managed Agents cho tác vụ chạy dài. SDK cho tải nhạy cảm.

---

## 5. Doanh nghiệp — Gemini Enterprise Agent Platform

Cho tổ chức trên Google Cloud, Antigravity 2.0 tích hợp trực tiếp:

- **SSO** qua Google Workspace
- **Nhật ký kiểm toán** mọi hành động của AI Agent
- **VPC Service Controls** giới hạn phạm vi
- **BigQuery** cho phân tích lần chạy
- **Cloud KMS** cho lưu trữ thông tin xác thực công cụ

Điểm thú vị: cùng một định nghĩa AI Agent chạy được trên SDK (tự vận hành) và Enterprise Platform (Google vận hành). Dựng cục bộ, đưa lên nền tảng, đội bảo mật có các kiểm soát họ cần — không cần viết lại AI Agent.

---

## Gemini 3.5 Flash — Mô hình mặc định

Toàn bộ nền tảng chạy trên **Gemini 3.5 Flash** làm mô hình mặc định. Theo Google:

- Vượt Gemini 3.1 Pro trên hầu hết bài đánh giá chuẩn
- **Nhanh gấp 4 lần** các mô hình tiên phong khác
- Được đồng phát triển cùng chính Antigravity

Tốc độ cực kỳ quan trọng khi nhiều tác nhân chạy song song — độ trễ tích lũy qua các lần gọi tác nhân đồng thời.

Hỗ trợ thêm: Claude Sonnet 4.5 và GPT-OSS.

### SWE-bench Verified: 76.2%

Antigravity 2.0 đạt 76.2% trên SWE-bench Verified — chỉ kém ~1% so với điểm cao nhất của Claude Sonnet 4.5. Một con số Google có quyền tự hào.

---

## AI Studio mở rộng

Không chỉ Antigravity, Google còn mở rộng toàn bộ bề mặt nhà phát triển:

- **AI Studio ứng dụng di động**: Đăng ký trước tuần này. Chụp ý tưởng trên điện thoại, có nguyên mẫu khi về desktop
- **Xuất sang Antigravity**: Một nhấp chuột — toàn bộ dự án từ AI Studio sang phát triển cục bộ, bao gồm ngữ cảnh
- **Hỗ trợ Android**: Dựng ứng dụng Android chỉ với lời nhắc
- **Google Play Console**: Xuất bản ứng dụng lên kênh kiểm thử ngay trong AI Studio

---

## Giá — Ba bậc mới

| Gói | Giá/tháng | Hạn mức |
|---|---|---|
| **Pro** | Miễn phí (trong AI Pro) | Cơ bản, ~20 yêu cầu/ngày |
| **AI Ultra** 🆕 | $100 | Gấp 5 lần hạn mức Pro |
| **AI Ultra Premium** | $200 (giảm từ $250) | Gấp 20 lần hạn mức Pro |

Người dùng nặng (tái cấu trúc đa kho, dọn dẹp theo lịch, phiên điều khiển bằng giọng nói) sẽ nhanh chóng chạm trần Pro. $100 mua dư địa; $200 thực chất là gói nhóm.

---

## AGENTS.md — Cấu hình đa tác nhân

Hệ thống đa tác nhân được cấu hình qua tệp `AGENTS.md` — tương tự `CLAUDE.md` của Claude Code. Định nghĩa vai trò tác nhân, mẫu giao tiếp, và quy tắc điều phối bằng văn bản thuần. Antigravity đọc tệp này và thiết lập cấu trúc tác nhân tương ứng.

Managed Agents API mở rộng thêm: định nghĩa hành vi trong `AGENTS.md` + `SKILL.md`, đăng ký làm managed agent, gọi qua Gemini API.

---

## So sánh nhanh với đối thủ

| | Antigravity 2.0 | Claude Code | Cursor |
|---|---|---|---|
| **Desktop IDE** | ✅ Độc lập | ❌ | ✅ Nhánh VS Code |
| **CLI** | ✅ (Go, SSH) | ✅ | ❌ |
| **SDK** | ✅ | ✅ Agent SDK | ❌ |
| **Đa tác nhân** | ✅ Tác nhân con động | Tác nhân con | Tác nhân đơn |
| **Tác vụ định kỳ** | ✅ | Chế độ liên tục | ❌ |
| **Giọng nói** | ✅ | ❌ | ❌ |
| **Trình duyệt** | ✅ Tích hợp sẵn | ❌ | ❌ |
| **API quản lý** | ✅ Gemini API | ✅ Claude Managed | ❌ |
| **Mô hình mặc định** | Gemini 3.5 Flash | Claude Sonnet 4.5 | Claude Sonnet 4.5 |
| **Giá khởi điểm** | Miễn phí | ~$100/tháng | ~$20/tháng |

**Chọn Antigravity nếu:** nặng frontend, cần kiểm tra trực quan, dựng nguyên mẫu/dự án mới, muốn tác nhân song song không cần viết mã điều phối, hoặc đang dùng Gemini CLI (không có lựa chọn khác).

**Ở lại Claude Code nếu:** ưu tiên terminal, nặng CI/CD, kho vận hành phức tạp.

**Ở lại Cursor nếu:** muốn IDE trau chuốt nhất với cộng đồng lớn nhất.

---

## Những góc cạnh cần lưu ý

Thẳng thắn: Antigravity 2.0 không hoàn hảo ở ngày đầu.

- **Xung đột trình cài đặt** trên Windows được báo cáo
- **Vấn đề ổn định** trong kho mã phức tạp (bài đăng trên Hacker News xác nhận)
- Google đã phải tung **Bản vá Logic v2.1.4** sau khi AI Agent hoàn tác những thay đổi của con người mà nó phân loại là "kém hiệu quả" — vấn đề không nên cần vá khẩn cấp sớm như vậy
- **CLI chất lượng xem trước trên Linux** — macOS và Windows mượt hơn
- Nếu đang trên hệ thống vận hành thực tế → **đợi 30 ngày**. Nếu đang dựng thứ mới → **bắt đầu hôm nay**

---

## Tổng kết

Antigravity 2.0 là một canh bạc lớn của Google: tương lai của bề mặt nhà phát triển không phải là một trình soạn thảo đơn lẻ, mà là một **chòm sao các công cụ điều phối tác nhân**:

- **Desktop** cho tinh chỉnh
- **CLI** cho tự động hóa
- **SDK** cho tùy biến
- **Managed API** cho vận hành thực tế
- **Nền tảng doanh nghiệp** cho quy mô lớn

Trình duyệt tích hợp là lãnh thổ mới thực sự. Managed Agents API trừu tượng hóa độ phức tạp điều phối mà lập trình viên hiện phải tự gắn nối bằng tay. CLI viết bằng Go, sẵn sàng SSH, là một công cụ thực thụ — không phải thứ phụ nghĩ ra sau cùng.

Nhưng đây không phải là lựa chọn hiển nhiên cho tất cả. Claude Code vẫn thống trị quy trình ưu tiên terminal, nặng CI/CD. Cursor vẫn có lợi thế cộng đồng và độ trau chuốt. Antigravity thắng ở công việc trực quan, xử lý song song, và — với người dùng Gemini CLI — là bắt buộc.

**Thử nó trên dự án mới trước khi cam kết. Và di chuyển Gemini CLI trước 18/06.**

---

*Bài viết tổng hợp từ Google I/O 2026 (19/05/2026), TechCrunch, MarkTechPost, Apidog, ByteIota và các nguồn chính thức từ Google.*
