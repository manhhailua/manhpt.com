---
title: "Thôi, tôi lại về dùng Claude Code"
slug: quay-lai-claude-code-sau-codex-grok-build
authors: [manhpt]
tags: [anthropic, claude-code, codex, deepseek, coding-agent, ai-strategy]
date: 2026-08-22
description: "Trải nghiệm Codex và Grok Build trong công việc thật khiến tôi quay lại Claude Code: model mạnh vẫn chưa đủ nếu công cụ cứ làm đứt mạch làm việc."
image: ./cover.png
---

![Quay lại Claude Code sau khi trải nghiệm Codex và Grok Build](./cover.png)

Một tháng trước, tôi còn viết bài [tạm biệt Claude Code](/tam-biet-claude-codex-cursor) để chuyển sang Codex và Cursor. Hôm nay tôi quay lại. Hơi giống vừa merge xong đã phải revert, nhưng ít nhất lần này tôi biết rõ vì sao phải quay đầu.

Codex thực sự rất xuất sắc. Grok Build cũng có nhiều ý tưởng hay và khá quen thuộc nếu từng dùng Claude Code. Nhưng sau khi dùng cả hai hằng ngày, tôi nhận ra model mạnh chỉ quyết định một nửa trải nghiệm. Nửa còn lại nằm ở chính công cụ: nó giúp tôi làm việc liền mạch, hay thỉnh thoảng lại bắt tôi dừng việc để sửa nó.

<!-- truncate -->

## Codex rất tốt, miễn là model hỗ trợ Responses API

Khi dùng model OpenAI, tôi gần như không có gì để chê Codex. Nó đọc kho mã tốt, biết lên kế hoạch, sửa code, chạy lệnh rồi tự kiểm tra kết quả. Với nhiều việc, đây vẫn là coding agent tôi yên tâm giao nhất.

Vướng mắc nằm ở khả năng đổi model. Trong mã nguồn Codex hiện tại, `wire_api = "chat"` không còn được hỗ trợ; khi kết nối nhà cung cấp khác, Codex chỉ chấp nhận giao thức `responses`. [Phần định nghĩa `WireApi` trong mã nguồn chính thức](https://github.com/openai/codex/blob/main/codex-rs/model-provider-info/src/lib.rs) hiện chỉ còn một giá trị là `responses`, và [thảo luận của dự án](https://github.com/openai/codex/discussions/7782) cũng xác nhận việc loại bỏ Chat Completions.

Điều đó không có nghĩa Codex chỉ chạy model OpenAI. Model của hãng khác vẫn dùng được nếu nhà cung cấp hoặc gateway hỗ trợ đủ OpenAI Responses API. Nhưng nếu model chỉ hỗ trợ Chat Completions, hoặc hỗ trợ Responses API chưa trọn vẹn, việc tích hợp sẽ cần thêm lớp chuyển đổi và dễ sinh lỗi ở tool calling, streaming hay lịch sử hội thoại.

Nếu vẫn muốn dùng Codex mà giữ chi phí thấp, DeepSeek là lựa chọn hợp lý nhất tôi thấy lúc này. [Tài liệu Responses API](https://api-docs.deepseek.com/guides/responses_api) cho biết cả `deepseek-v4-flash` và `deepseek-v4-pro` đều được hỗ trợ. [Giá](https://api-docs.deepseek.com/quick_start/pricing) bắt đầu từ $0,14 cho một triệu token đầu vào chưa cache và $0,28 cho một triệu token đầu ra. DeepSeek chưa hỗ trợ trọn vẹn mọi tính năng trong Responses API của OpenAI, nhưng đã đủ cho Codex chạy.

Đó là lựa chọn kiến trúc hợp lý, không phải lỗi. Việc chỉ dùng Responses API giúp OpenAI chuẩn hóa vòng lặp của agent và xử lý các sự kiện phức tạp. Chỉ là nó không hợp với tôi, người thường xuyên đổi model và không muốn dựng thêm một lớp chuyển đổi mỗi lần thử nhà cung cấp mới.

## Grok Build có cách dùng khá giống Claude Code

[Tài liệu Grok Build](https://docs.x.ai/build/overview) mô tả một coding agent chạy trong terminal với giao diện toàn màn hình, có thể đọc kho mã, sửa file, chạy lệnh và hỗ trợ model bên ngoài. Nhìn vào danh sách tính năng, nó gần như đúng thứ tôi muốn: cách dùng quen thuộc như Claude Code nhưng dễ đổi model hơn.

Trải nghiệm ban đầu cũng khá quen thuộc. Tôi có thể làm việc ngay trong terminal, giao những việc dài và theo dõi agent làm việc trong repo. Với model Grok, mọi thứ nhìn chung ổn.

Nhưng khi đổi sang model của hãng khác, mọi thứ không còn mượt như vậy. Có lần ứng dụng sập lúc tôi đưa ảnh vào rồi không tự phục hồi. Có thể lỗi này không xảy ra với mọi model hay mọi máy; tôi chỉ ghi lại đúng chuyện đã gặp vào tháng 8/2026.

Từng chuyện một đều nhỏ, nhưng dùng hằng ngày lại khá khó chịu. Khi Grok hiển thị đường dẫn tới pull request hay trang xác thực, không phải lúc nào tôi cũng bấm mở được; nó cũng không tự mở trình duyệt. Sao chép một đường dẫn không phải việc lớn, nhưng lặp lại đủ nhiều thì thành một việc vặt rất vô duyên.

Một coding agent có thể rất thông minh, nhưng chỉ cần nó sập hoặc bắt tôi làm tay một bước đáng ra phải tự động, mạch suy nghĩ đã đứt. Tôi trả tiền cho agent để bớt việc vặt, không phải nhận thêm việc vặt trong một giao diện terminal.

## Tôi quay lại vì dùng ổn, không phải vì benchmark

Claude Code vẫn là công cụ tôi thấy thoải mái nhất khi làm việc lâu trong terminal. Phiên làm việc ổn định, thao tác với file và công cụ ít gây bất ngờ. Đưa ảnh vào ngữ cảnh, mở đường dẫn hay tiếp tục sau lỗi cũng hiếm khi kéo tôi ra khỏi việc đang làm.

Nghe hơi ngược đời: tôi vừa than Codex khó đổi model, rồi lại quay về một công cụ gắn chặt với Claude. Nhưng sau vòng thử này, tôi đã có câu trả lời: đổi model trong file cấu hình chẳng có nhiều ý nghĩa nếu những thao tác cơ bản vẫn làm gián đoạn công việc. Lúc này tôi chọn cặp model và công cụ chạy ổn định từ đầu đến cuối. Codex vẫn ở lại cho những việc hợp với OpenAI hơn.

Lần trước tôi rời Claude Code vì muốn giảm phụ thuộc và kiểm chứng các lựa chọn thay thế. Lý do ấy vẫn còn nguyên. Quay lại không có nghĩa tôi hết lo về tài khoản, chính sách hay nguy cơ phụ thuộc vào một nhà cung cấp. Nó chỉ cho tôi thêm một kết luận rất thực tế: sau khi đem các công cụ khác vào việc thật, Claude Code vẫn khiến tôi ít phải bận tâm nhất.

## Sau một vòng thử, tôi dùng gì?

Tôi sẽ dùng **Claude Code làm coding agent chính trong terminal**. Codex vẫn ở lại cho những việc có thể chạy song song, hợp với model OpenAI hoặc không cần tôi ngồi chờ. Grok Build tạm nghỉ cho đến khi model bên ngoài chạy ổn hơn và những bất tiện nhỏ được sửa.

Đây không phải cuộc thi chọn một công cụ rồi xóa hết phần còn lại. Coding agent đang thay đổi quá nhanh để trung thành tuyệt đối với một logo. Tôi chỉ cần biết công cụ nào nên nằm ở vị trí chính, công cụ nào là phương án bổ sung và công cụ nào cần thêm thời gian.

Cuối cùng, coding agent tốt nhất với tôi không phải công cụ đứng đầu nhiều bảng xếp hạng, mà là công cụ giúp tôi tập trung vào code đủ lâu để quên mất nó đang ở đó.

Thôi, tôi lại về dùng Claude Code đây :))

## Tài liệu tham khảo

1. [Codex: định nghĩa nhà cung cấp model và `WireApi`](https://github.com/openai/codex/blob/main/codex-rs/model-provider-info/src/lib.rs).
2. [Codex: thảo luận loại bỏ Chat Completions](https://github.com/openai/codex/discussions/7782).
3. [Grok Build: tổng quan và cấu hình model bên ngoài](https://docs.x.ai/build/overview).
4. [Claude Code: cài đặt và xác thực](https://docs.anthropic.com/en/docs/claude-code/getting-started).
5. DeepSeek: [Responses API](https://api-docs.deepseek.com/guides/responses_api) và [giá](https://api-docs.deepseek.com/quick_start/pricing).

*Thông tin sản phẩm được kiểm chứng ngày 22/8/2026; các nhận xét về độ ổn định và cách dùng là trải nghiệm cá nhân của tôi.*
