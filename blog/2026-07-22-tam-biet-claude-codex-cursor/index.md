---
title: "Tạm Biệt Claude: Vì Sao Tôi Dừng Claude Subscription Và Giữ Lại Codex, Cursor"
slug: tam-biet-claude-codex-cursor
authors: [manhpt]
tags: [anthropic, claude, codex, cursor, openai, claude-code, coding-agent, ai-tools, ai-strategy, vietnamese]
date: 2026-07-22
description: "Đã đến lúc Anthropic bớt ngáo quyền lực. Tôi quyết định từ bỏ Claude subscription, giữ Codex và Cursor, và thử nghiệm Cursor CLI để rũ bỏ hoàn toàn Claude. Câu chuyện cá nhân về chọn công cụ AI trong một quý đầy biến động."
---

Một quyết định đã ấp ủ từ lâu, giờ mới đủ bình tĩnh để viết ra: **tôi huỷ Claude subscription.** Không phải vì Claude yếu. Mà vì Anthropic đang hành xử như một kẻ đương nhiên được chọn, bất kể bạn trả bao nhiêu tiền.

Bài này không phải bài đánh giá benchmark. Đây là nhật ký vận hành thật của một quý dùng AI để code mỗi ngày.

<!-- truncate -->

## Anthropic Đang Bị Cái "Ngáo Quyền Lực" Kéo Đi

Sự vươn lên của Anthropic quá nhanh. Nhanh đến mức họ bắt đầu phải chọn lọc khách hàng, dành hạ tầng cho những người "quan trọng hơn". Điều đó hiểu được về mặt kinh doanh. Nhưng cách họ support khách hàng Enterprise thì không thể hiểu nổi.

Công ty tôi liên tục liên hệ với Anthropic để xử lý các trường hợp account bị chặn — không có phản hồi. Không phải phản hồi chậm. Là không có. Khi một nhà cung cấp thu tiền Enterprise mà im lặng trước sự cố chặn truy cập, đó không còn là lỗi vận hành nữa. Đó là tín hiệu rằng họ không cần bạn bằng cách bạn cần họ.

Và khi vendor nghĩ họ không cần bạn, đó là lúc cần chuẩn bị một cánh cửa thoát.

## Những Gì Tôi Giữ Lại: Codex và Cursor

### Cursor — mua vội, không hối hận

Từ tháng 11/2025, trong một phút cao hứng, tôi nạp luôn gói Pro 1 năm của Cursor. Bình thường thì đó là dạng mua sắm bốc đồng đáng tiếc. Nhưng lần này thì không. Đến giờ tôi vẫn thấy Cursor là công cụ **GUI coding tốt nhất** hiện tại. Giao diện mượt, agent mode ổn, codebase-aware.

Nhưng nói "dùng Cursor" thì nghe rất tử tế. Thực tế thì: tôi mở Cursor, rồi mở terminal ngay trong đó, rồi mở tiếp `tmux`, rồi gọi `claude code`. Một IDE xịn xò chỉ để làm khung cửa sổ cho một CLI của Anthropic. Cảm giác như mua một chiếc Porsche chỉ để chở theo chiếc xe đạp từ lúc đăng ký — tức cười, nhưng đúng là cách tôi làm việc mỗi ngày.

Đó cũng chính là vấn đề: muốn rũ bỏ Claude mà vẫn gọi Claude Code trong terminal thì coi như chưa thoát.

### Codex (desktop app) — cực kỳ hài lòng

Với Codex desktop, tôi đang rất ưng ý với **GPT 5.6 Sol High**. Thực task cực nhanh, ổn định, ít drama. Gói Plus tạm đủ cho công việc vẽ vời, brainstorm, viết tài liệu. Coding nặng thì xác định vẫn dùng Cursor một thời gian nữa rồi đánh giá lại.

OpenAI hiện đang làm đúng thứ mà Anthropic đang bỏ lỡ: sản phẩm gọn, đáng tin, và không làm người dùng cảm thấy mình đang xin việc.

## Mô Hình Trung Quốc Đang Lên Ngôi

Quý vừa rồi tôi vẫn sống rất tốt với **GLM + Claude Code (free tier)**. Không chết. Không gãy mạch làm việc. Mô hình Trung Quốc như Kimi, GLM đang nhanh chóng lấp đầy khoảng trống mà Anthropic cố tình tạo ra bằng cách siết quota và nâng giá.

Đó là thực tế quan trọng: lựa chọn thay thế đã tồn tại, và đủ tốt. Chuyện "không có Claude thì không code được" giờ là truyền thuyết, không phải dữ kiện.

Nói thẳng hơn: **Claude Code + GLM vẫn là một combo rất tốt** — miễn là bạn không cần Claude model. Harness của Claude Code vốn đã là một trong những agent terminal tốt nhất: hiểu codebase, gọi tool gọn, quản lý context sạch. Ghép với GLM-5.2 qua custom provider là tôi có một coding agent chạy mượt mà, không giới hạn quota, không phụ thuộc API key của Anthropic. Phần nhiều giá trị nằm ở harness, không chỉ ở model. Cho nên trước khi Cursor CLI chứng minh được bản thân, tôi vẫn dùng combo này làm cánh cửa thoát chính.

## Bước Tiếp Theo: Cursor CLI

Giờ tôi muốn cắt đứt Claude triệt để, không phải chỉ đổi model. Nên quyết định thử nghiệm **Cursor CLI (agent)** xem sao. Mục tiêu rõ ràng: một harness khác, không phụ thuộc Anthropic. Nếu nó tốt một nửa Cursor GUI mà không cần gọi Claude Code phía sau thì đã là thắng.

Tôi không ghét Claude hay Anthropic. Tôi chỉ không muốn phụ thuộc vào một vendor nghĩ rằng quyền lực cho phép họ được phép lờ đi khách hàng trả tiền. Thị trường đang có nhiều lựa chọn hơn, rẻ hơn, và — quan trọng nhất — tôn trọng người dùng hơn.

Khi vendor nghĩ họ không cần bạn, cách tốt nhất là chứng minh họ đúng.

---

*Cập nhật tiếp theo sau khi thử Cursor CLI một thời gian. Nếu kết quả tốt, đây sẽ không chỉ là lúc Anthropic bớt ngáo quyền lực — mà là lúc họ bớt đi một khách hàng vĩnh viễn.*
