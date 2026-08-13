---
title: "Lorekeep: Kho Tri Thức Dùng Chung Cho Các Coding Agent"
slug: lorekeep-kho-tri-thuc-dung-chung-coding-agent
authors: [manhpt]
tags: [mcp, ai-agent, coding-agent, open-source, personal-ai, architecture]
date: 2026-08-13
description: "Giới thiệu Lorekeep — temporal knowledge graph mã nguồn mở giúp Claude Code, Cursor, Codex và opencode dùng chung tri thức qua MCP, trong khi dữ liệu vẫn thuộc về người dùng."
image: /img/blog/lorekeep-cover.jpeg
---

Các coding agent ngày càng mạnh, nhưng trí nhớ của chúng vẫn thường bị chia cắt theo từng công cụ và từng phiên làm việc. Những gì Codex biết hôm nay chưa chắc Cursor biết vào ngày mai; khi đổi agent, tôi lại phải giải thích codebase, quyết định kiến trúc và bối cảnh cá nhân từ đầu.

Tôi xây dựng **[Lorekeep](https://github.com/manhhailua/lorekeep)** để thử giải quyết vấn đề đó: tạo một tầng tri thức do người dùng sở hữu, có thể được nhiều coding agent sử dụng chung qua MCP.

<!-- truncate -->

## Lorekeep Là Gì?

Lorekeep là một **file-sovereign temporal knowledge graph**: kho tri thức được lưu bằng file, có lịch sử theo thời gian và không thuộc riêng một AI agent hay nhà cung cấp model nào.

Luồng xử lý cốt lõi khá đơn giản:

```text
Markdown → trích xuất có schema → resolve → facts.jsonl → MCP + Wiki
```

Lorekeep biên dịch Markdown từ nhiều namespace thành graph `facts.jsonl` theo cách xác định, đồng thời sinh một wiki Markdown để đọc bằng Obsidian hoặc Tolaria. Claude Code, Cursor, Codex và opencode có thể truy vấn cùng graph đó qua tám MCP tools nhỏ gọn như `search`, `get_node`, `neighbors` và `temporal_query`.

Điểm quan trọng là LLM chỉ được gọi khi compile tài liệu hoặc khi người dùng chủ động yêu cầu deep import. Các thao tác thường xuyên như truy vấn graph, ghi journal, resolve, tạo wiki, lint hay kiểm tra trạng thái đều không gọi thêm LLM. Nhờ vậy, phần serve có độ trễ và chi phí dễ dự đoán hơn.

## Ba Nguyên Tắc Tôi Muốn Giữ

### 1. Tri thức phải thuộc về người dùng

Nguồn dữ liệu bền vững của Lorekeep là Markdown, schema và các journal dạng append-only. Graph, manifest, wiki hay chỉ mục tìm kiếm đều là dữ liệu dẫn xuất và có thể tái tạo trên thiết bị khác.

Người dùng có thể sao lưu các đầu vào này vào một private Git repository. Cấu hình, secret, cache và log vẫn nằm cục bộ. Điều đó giúp tri thức không bị khóa trong memory của một agent hoặc một dịch vụ SaaS cụ thể.

### 2. Agent được dùng chung tri thức, nhưng không được tự ý sửa sự thật

Agent có thể đề xuất tạo fact, liên kết entity hoặc cập nhật thuộc tính trong phiên làm việc. Tuy nhiên, chúng không ghi trực tiếp vào graph chính. Mọi đề xuất đi vào journal, bị ràng buộc bởi namespace và confidence gate, rồi chỉ trở thành tri thức chính thức sau bước resolve.

Đây là ranh giới quan trọng: agent có quyền đóng góp, nhưng hệ thống vẫn giữ được provenance, khả năng kiểm tra và đường quay lại khi đề xuất sai.

### 3. Tri thức cần có phạm vi và thời gian

Không phải agent nào cũng nên thấy mọi dữ liệu. Lorekeep áp dụng deny-by-default namespace filtering qua một điểm kiểm soát duy nhất là `ScopedGraph`. Một edge chỉ được trả về khi namespace của edge và cả hai endpoint đều nằm trong phạm vi được phép.

Graph cũng hỗ trợ validity window, snapshot, history và change query. Vì vậy, agent không chỉ hỏi “điều gì đúng?” mà còn có thể hỏi “điều này đúng tại thời điểm nào?” hoặc “đã thay đổi những gì?”.

## Dùng Thử Trong Vài Phút

Cách nhanh nhất để cài đặt:

```bash
curl -fsSL https://raw.githubusercontent.com/manhhailua/lorekeep/main/scripts/install.sh | bash
lorekeep init
```

`lorekeep init` sẽ tạo cấu hình, thiết lập schema và namespace, phát hiện các coding agent đang có, cấu hình MCP, import nhanh memory hiện hữu, compile dữ liệu nếu đã có provider key và khởi động daemon theo dõi thay đổi.

Sau đó, chỉ cần đặt Markdown vào `raw/<namespace>/`. Daemon sẽ tự compile khi tài liệu thay đổi, còn wiki và graph được cập nhật ở nền.

## Lorekeep Chưa Phải Gì?

Phiên bản hiện tại phù hợp nhất cho một cá nhân dùng nhiều coding agent trên nhiều thiết bị. Git backup vẫn tuần tự, nên hai thiết bị cùng sửa một tài liệu có thể cần xử lý conflict thủ công. Hệ thống chưa cung cấp shared team server có authentication, chưa có hybrid/vector retrieval và chưa tích hợp sẵn connector cho repository, Confluence, PDF, CI hay observability platform.

Tôi công khai những giới hạn này vì Lorekeep đang được xây như một nền tảng tri thức có thể kiểm chứng, không phải một lớp “AI memory” hứa nhớ mọi thứ. Mục tiêu gần nhất là làm thật tốt vòng đời: **từ tài liệu do người dùng sở hữu, thành tri thức có cấu trúc, được nhiều agent dùng chung nhưng vẫn có quyền hạn và lịch sử rõ ràng.**

Lorekeep là dự án mã nguồn mở theo giấy phép MIT. Nếu bạn cũng đang gặp bài toán context bị phân mảnh giữa nhiều coding agent, có thể xem code, tài liệu và roadmap tại [github.com/manhhailua/lorekeep](https://github.com/manhhailua/lorekeep).
