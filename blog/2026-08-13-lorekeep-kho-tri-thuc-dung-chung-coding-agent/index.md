---
title: "Lorekeep: Kho Tri Thức Dùng Chung Cho Các Coding Agent"
slug: lorekeep-kho-tri-thuc-dung-chung-coding-agent
authors: [manhpt]
tags: [mcp, ai-agent, coding-agent, open-source, personal-ai, architecture]
date: 2026-08-13
description: "Giới thiệu Lorekeep — temporal knowledge graph mã nguồn mở giúp Claude Code, Cursor, Codex và opencode dùng chung tri thức qua MCP, trong khi dữ liệu vẫn thuộc về người dùng."
image: /img/blog/lorekeep-cover.jpeg
---

Các coding agent ngày càng mạnh, nhưng trí nhớ của chúng vẫn thường bị chia cắt theo từng công cụ và từng phiên làm việc. Những gì Codex biết hôm nay chưa chắc Cursor biết vào ngày mai; khi đổi agent, tôi lại phải giải thích mã nguồn, quyết định kiến trúc và bối cảnh cá nhân từ đầu.

Tôi xây dựng **[Lorekeep](https://github.com/manhhailua/lorekeep)** để thử giải quyết vấn đề đó: tạo một tầng tri thức do người dùng sở hữu, có thể được nhiều coding agent sử dụng chung qua MCP.

<!-- truncate -->

## Lorekeep Là Gì?

Lorekeep là một **file-sovereign temporal knowledge graph**: kho tri thức được lưu bằng tệp, có lịch sử theo thời gian và không thuộc riêng một AI agent hay nhà cung cấp mô hình nào.

Luồng xử lý cốt lõi khá đơn giản:

```text
Markdown → chunk → extract(schema) → resolve → facts.jsonl → MCP + wiki
```

Quy trình `compile` biến Markdown từ nhiều `namespace` thành `knowledge graph` trong `facts.jsonl`. Quá trình này có tính xác định: cùng một đầu vào không đổi sẽ tạo ra cùng một kết quả. Lorekeep đồng thời sinh `wiki` dạng Markdown để đọc bằng Obsidian hoặc Tolaria. Claude Code, Cursor, Codex và opencode có thể truy vấn cùng `knowledge graph` đó qua tám công cụ MCP nhỏ gọn như `search`, `get_node`, `neighbors` và `temporal_query`.

Điểm quan trọng là LLM chỉ được gọi trong giai đoạn `compile` hoặc khi người dùng chủ động yêu cầu `deep import`. Các thao tác thường xuyên như truy vấn `knowledge graph`, ghi `journal`, `resolve`, tạo `wiki`, `lint` hay kiểm tra trạng thái đều không gọi thêm LLM. Nhờ vậy, tầng truy vấn có độ trễ và chi phí dễ dự đoán hơn.

## Ba Nguyên Tắc Tôi Muốn Giữ

### 1. Tri thức phải thuộc về người dùng

Nguồn dữ liệu bền vững của Lorekeep là Markdown, `schema` và các `journal` dạng `append-only`. `Knowledge graph`, `manifest`, `wiki` và chỉ mục tìm kiếm đều là dữ liệu dẫn xuất, có thể tái tạo trên thiết bị khác.

Người dùng có thể sao lưu các đầu vào này vào một Git repository riêng tư. Cấu hình, thông tin bí mật, bộ nhớ đệm và log vẫn nằm cục bộ. Nhờ vậy, các `facts` không bị khóa trong bộ nhớ riêng của một agent hoặc một dịch vụ SaaS cụ thể.

### 2. Agent được dùng chung tri thức, nhưng không ghi trực tiếp vào `facts`

Agent có thể đề xuất thêm `facts`, liên kết thực thể hoặc cập nhật thuộc tính trong phiên làm việc. Tuy nhiên, chúng không ghi trực tiếp vào `knowledge graph` chính. Mọi đề xuất đều đi vào `journal`, bị ràng buộc bởi `namespace` và `confidence gate`, rồi chỉ trở thành `facts` được chấp nhận sau bước `resolve`.

Đây là ranh giới quan trọng: agent có quyền đóng góp, nhưng hệ thống vẫn giữ được `provenance` — nguồn gốc của dữ liệu — cùng khả năng kiểm tra và đường quay lại khi đề xuất sai.

### 3. Tri thức cần có phạm vi và thời gian

Không phải agent nào cũng nên thấy mọi dữ liệu. Lorekeep mặc định từ chối truy cập và phân quyền theo `namespace` qua một điểm kiểm soát duy nhất là `ScopedGraph`. Một `edge` chỉ được trả về khi `namespace` của chính `edge` và cả hai `node` ở hai đầu đều nằm trong phạm vi được phép.

`Knowledge graph` cũng hỗ trợ `validity window` cùng ba chế độ truy vấn `at_time`, `history` và `changes`. Vì vậy, agent không chỉ tìm các `facts` hiện có mà còn có thể hỏi chúng có hiệu lực tại thời điểm nào hoặc đã thay đổi ra sao.

## Dùng Thử Trong Vài Phút

Cách nhanh nhất để cài đặt:

```bash
curl -fsSL https://raw.githubusercontent.com/manhhailua/lorekeep/main/scripts/install.sh | bash
lorekeep init
```

`lorekeep init` sẽ tạo cấu hình, thiết lập `schema` và `namespace`, phát hiện các coding agent đang có, cấu hình MCP, nhập nhanh bộ nhớ hiện hữu, `compile` dữ liệu nếu đã có `API key` và khởi động `daemon` theo dõi thay đổi.

Sau đó, chỉ cần đặt Markdown vào `raw/<namespace>/`. `Daemon` sẽ tự `compile` khi tài liệu thay đổi; `wiki` và `knowledge graph` được cập nhật trong nền.

## Lorekeep Chưa Phải Gì?

Phiên bản hiện tại phù hợp nhất cho một cá nhân dùng nhiều coding agent trên nhiều thiết bị. Cơ chế sao lưu qua Git vẫn tuần tự, nên hai thiết bị cùng sửa một tài liệu có thể cần xử lý xung đột thủ công. Hệ thống chưa cung cấp máy chủ dùng chung cho đội ngũ với cơ chế xác thực, chưa có `hybrid retrieval` hoặc `vector retrieval`, và chưa tích hợp sẵn bộ kết nối cho kho mã nguồn, Confluence, PDF, CI hay nền tảng quan sát hệ thống.

Tôi công khai những giới hạn này vì Lorekeep đang được xây như một nền tảng tri thức có thể kiểm chứng, không phải một lớp “bộ nhớ AI” hứa nhớ mọi thứ. Mục tiêu gần nhất là làm thật tốt vòng đời: **từ tài liệu do người dùng sở hữu, thành tri thức có cấu trúc, được nhiều agent dùng chung nhưng vẫn có quyền hạn và lịch sử rõ ràng.**

Lorekeep là dự án mã nguồn mở theo giấy phép MIT. Nếu bạn cũng đang gặp bài toán bối cảnh bị phân mảnh giữa nhiều coding agent, có thể xem mã nguồn, tài liệu và lộ trình phát triển tại [github.com/manhhailua/lorekeep](https://github.com/manhhailua/lorekeep).
