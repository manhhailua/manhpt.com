---
title: "Lorekeep: Kho Tri Thức Dùng Chung Cho Các Coding Agent"
slug: lorekeep-kho-tri-thuc-dung-chung-coding-agent
authors: [manhpt]
tags: [mcp, ai-agent, coding-agent, open-source, personal-ai, architecture]
date: 2026-08-13
description: "Giới thiệu Lorekeep — temporal knowledge graph mã nguồn mở chắt lọc tri thức từ các session AI agent để Claude Code, Cursor, Codex và opencode dùng chung qua MCP."
image: /img/blog/lorekeep-cover.jpeg
---

Trong quá trình sử dụng coding agent, tri thức quan trọng không chỉ nằm trong câu hỏi và câu trả lời. Mỗi session còn mang theo thông tin từ mã nguồn, tài liệu, `log`, bảng dữ liệu hoặc các loại tệp khác mà người dùng đưa cho agent đọc và sử dụng. Đây cũng là nơi những quyết định, cách giải quyết vấn đề và hiểu biết mới được hình thành.

Nhưng tri thức tích lũy trong các session thường bị chia cắt theo từng công cụ. Những gì Codex biết hôm nay chưa chắc Cursor biết vào ngày mai; khi đổi agent, tôi lại phải giải thích mã nguồn, quyết định kiến trúc và bối cảnh cá nhân từ đầu.

Tôi xây dựng **[Lorekeep](https://github.com/manhhailua/lorekeep)** để thử giải quyết vấn đề đó: chắt lọc tri thức từ các session thành một tầng dữ liệu do người dùng sở hữu, có thể được nhiều coding agent sử dụng chung qua MCP.

<!-- truncate -->

## Lorekeep Là Gì?

Lorekeep là một **file-sovereign temporal knowledge graph**. Nguồn tri thức quan trọng nhất là các session hình thành khi người dùng làm việc với AI agent, bao gồm cả thông tin agent đã đọc và sử dụng từ những tệp được đưa vào session. Lorekeep thu nhận `memory` và `transcript` từ các agent được hỗ trợ, sau đó chuẩn hóa chúng thành Markdown để người dùng có thể đọc, kiểm tra và sở hữu lâu dài.

Luồng xử lý cốt lõi khá đơn giản:

```text
AI-agent sessions
(conversation + memory + context from files)
        ↓
normalized Markdown → chunk → extract(schema) → resolve → facts.jsonl → MCP + wiki
```

Markdown vì vậy là định dạng chuẩn hóa và bền vững của Lorekeep, không phải giới hạn về nguồn tri thức. Quy trình `compile` biến Markdown từ nhiều `namespace` thành `knowledge graph` gồm các `facts` có cấu trúc, được xuất ra `facts.jsonl`. Quá trình này có tính xác định: cùng một đầu vào không đổi sẽ tạo ra cùng một kết quả.

Lorekeep đồng thời sinh `wiki` dạng Markdown để đọc bằng Obsidian hoặc Tolaria. Claude Code, Cursor, Codex và opencode có thể truy vấn cùng `knowledge graph` đó qua tám công cụ MCP nhỏ gọn như `search`, `get_node`, `neighbors` và `temporal_query`.

Điểm quan trọng là LLM chỉ được gọi trong giai đoạn `compile` hoặc khi người dùng chủ động yêu cầu `deep import`. Các thao tác thường xuyên như truy vấn `knowledge graph`, ghi `journal`, `resolve`, tạo `wiki`, `lint` hay kiểm tra trạng thái đều không gọi thêm LLM. Nhờ vậy, tầng truy vấn có độ trễ và chi phí dễ dự đoán hơn.

## Ba Nguyên Tắc Tôi Muốn Giữ

### 1. Session tạo ra tri thức, nhưng dữ liệu phải thuộc về người dùng

Sự phân lớp này rất quan trọng: session là nguồn tri thức về mặt ngữ nghĩa; Markdown là định dạng biểu diễn bền vững. Các `hook` và tiến trình theo dõi sẽ chuyển `memory`, `transcript` cùng ngữ cảnh được hỗ trợ thành các lô Markdown có kích thước giới hạn và có thể tái tạo. Người dùng vẫn có thể bổ sung Markdown thủ công khi cần.

Ở lớp lưu trữ, Markdown đã chuẩn hóa, `schema` và các `journal` dạng `append-only` là đầu vào bền vững. Các thành phần `knowledge graph`, `manifest`, `wiki` và chỉ mục tìm kiếm đều là dữ liệu dẫn xuất, có thể tái tạo trên thiết bị khác.

Người dùng có thể sao lưu các đầu vào này vào một Git repository riêng tư. Cấu hình, thông tin bí mật, bộ nhớ đệm và `log` vận hành vẫn nằm cục bộ. Nhờ vậy, các `facts` không bị khóa trong bộ nhớ riêng của một agent hoặc một dịch vụ SaaS cụ thể.

### 2. Agent được dùng chung tri thức, nhưng không ghi trực tiếp vào `facts`

Agent có thể đề xuất thêm `facts`, liên kết thực thể hoặc cập nhật thuộc tính trong phiên làm việc. Tuy nhiên, chúng không ghi trực tiếp vào `knowledge graph` chính. Mọi đề xuất đều đi vào `journal`, bị ràng buộc bởi `namespace` và `confidence gate`, rồi chỉ trở thành `facts` được chấp nhận sau bước `resolve`.

Đây là ranh giới quan trọng: agent có quyền đóng góp, nhưng hệ thống vẫn giữ được `provenance` — nguồn gốc của dữ liệu — cùng khả năng kiểm tra và đường quay lại khi đề xuất sai.

### 3. Tri thức cần có phạm vi và thời gian

Không phải agent nào cũng nên thấy mọi dữ liệu. Lorekeep mặc định từ chối truy cập và phân quyền theo `namespace` qua một điểm kiểm soát duy nhất là `ScopedGraph`. Một `edge` chỉ được trả về khi `namespace` của chính `edge` và cả hai `node` ở hai đầu đều nằm trong phạm vi được phép.

Ngoài ra, `knowledge graph` còn hỗ trợ `validity window` cùng ba chế độ truy vấn `at_time`, `history` và `changes`. Vì vậy, agent không chỉ tìm các `facts` hiện có mà còn có thể hỏi chúng có hiệu lực tại thời điểm nào hoặc đã thay đổi ra sao.

## Dùng Thử Trong Vài Phút

Cách nhanh nhất để cài đặt:

```bash
curl -fsSL https://raw.githubusercontent.com/manhhailua/lorekeep/main/scripts/install.sh | bash
lorekeep init
```

`lorekeep init` sẽ tạo cấu hình, thiết lập `schema` và `namespace`, phát hiện các coding agent đang có, cấu hình MCP, nhập nhanh `memory` hiện hữu, cài `session-end hook`, `compile` dữ liệu nếu đã có `API key` và khởi động `daemon` theo dõi thay đổi.

Sau đó, người dùng chỉ cần tiếp tục làm việc với Claude Code, Cursor, Codex hoặc opencode. Các session được hỗ trợ sẽ được kết xuất thành Markdown trong những `namespace` tương ứng như `raw/codex-session/` hay `raw/cursor-session/`. Tiến trình `daemon` tự `compile` khi dữ liệu thay đổi; `wiki` và `knowledge graph` được cập nhật trong nền. Markdown cũng có thể được thêm trực tiếp vào `raw/<namespace>/`.

## Lorekeep Chưa Phải Gì?

Phiên bản hiện tại phù hợp nhất cho một cá nhân dùng nhiều coding agent trên nhiều thiết bị. Cơ chế sao lưu qua Git vẫn tuần tự, nên hai thiết bị cùng sửa một tài liệu có thể cần xử lý xung đột thủ công. Hệ thống chưa cung cấp máy chủ dùng chung cho đội ngũ với cơ chế xác thực và chưa có `hybrid retrieval` hoặc `vector retrieval`.

Lorekeep cũng chưa `ingest` trực tiếp mọi định dạng tệp hay có sẵn bộ kết nối cho kho mã nguồn, Confluence, PDF, CI và nền tảng quan sát hệ thống. Với những nguồn này, Lorekeep hiện tiếp nhận phần thông tin đã được agent đọc, sử dụng và lưu lại trong session; nó không thay thế một quy trình chuyên biệt để `parse` nguyên bản PDF, DOCX hay các định dạng dữ liệu khác.

Tôi công khai những giới hạn này vì Lorekeep đang được xây như một nền tảng tri thức có thể kiểm chứng, không phải một lớp “bộ nhớ AI” hứa nhớ mọi thứ. Mục tiêu gần nhất là làm thật tốt vòng đời: **từ các session sử dụng AI agent, thành `facts` có cấu trúc, được nhiều agent dùng chung nhưng vẫn có quyền hạn và lịch sử rõ ràng.**

Lorekeep là dự án mã nguồn mở theo giấy phép MIT. Nếu bạn cũng đang gặp bài toán bối cảnh bị phân mảnh giữa nhiều coding agent, có thể xem mã nguồn, tài liệu và lộ trình phát triển tại [github.com/manhhailua/lorekeep](https://github.com/manhhailua/lorekeep).
