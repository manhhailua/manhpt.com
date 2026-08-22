---
title: "Thôi, tôi lại về dùng Claude Code"
slug: quay-lai-claude-code-sau-codex-grok-build
authors: [manhpt]
tags: [anthropic, claude-code, codex, deepseek, coding-agent, ai-strategy]
date: 2026-08-22
description: "Trải nghiệm Codex và Grok Build cho công việc thật khiến tôi quay lại Claude Code: coding agent tốt không chỉ cần model mạnh mà còn phải ít làm gián đoạn workflow."
image: ./cover.png
---

![Quay lại Claude Code sau khi trải nghiệm Codex và Grok Build](./cover.png)

Một tháng trước, tôi còn viết bài [tạm biệt Claude Code](/tam-biet-claude-codex-cursor) để chuyển sang Codex và Cursor. Hôm nay tôi quay lại. Nhìn hơi giống một pull request vừa merge đã phải revert, nhưng ít nhất lần này tôi đã có đủ trải nghiệm thật để biết mình đang đổi vì điều gì.

Codex hoàn toàn xuất sắc. Grok Build cũng có nhiều ý tưởng hay và cho cảm giác khá gần Claude Code. Nhưng sau khi dùng cả hai trong công việc hằng ngày, tôi nhận ra model mạnh mới chỉ là một nửa câu chuyện; nửa còn lại là harness có để mình làm việc liền mạch hay cứ thỉnh thoảng kéo mình ra khỏi bài toán để sửa chính nó.

<!-- truncate -->

## Codex xuất sắc, nhưng Responses API là một ranh giới rõ

Tôi gần như không có gì để chê về chất lượng của Codex khi dùng đúng hệ OpenAI. Khả năng đọc codebase, lập kế hoạch, sửa code, chạy lệnh và tự kiểm tra kết quả đều rất tốt. Với nhiều tác vụ, Codex vẫn là coding agent khiến tôi yên tâm giao việc nhất.

Giới hạn của tôi nằm ở khả năng đổi model. Trong mã nguồn Codex hiện tại, `wire_api = "chat"` đã không còn được hỗ trợ; đường custom provider chỉ chấp nhận giao thức `responses`. [Phần định nghĩa `WireApi` trong repository chính thức](https://github.com/openai/codex/blob/main/codex-rs/model-provider-info/src/lib.rs) hiện chỉ còn một giá trị là `responses`, và [thảo luận của dự án](https://github.com/openai/codex/discussions/7782) cũng xác nhận việc loại bỏ Chat Completions.

Điều này không có nghĩa Codex chỉ chạy model OpenAI. Model ngoài vẫn có thể dùng nếu provider hoặc gateway triển khai đủ OpenAI Responses API. Nhưng với các model chỉ hỗ trợ Chat Completions, hoặc hỗ trợ Responses API chưa trọn vẹn, việc tích hợp sẽ cần thêm lớp chuyển đổi và dễ phát sinh sai khác ở tool calling, streaming hay lịch sử hội thoại.

Xét chi phí, DeepSeek là ứng cử viên tốt nhất để ghép với Codex. [Tài liệu Responses API](https://api-docs.deepseek.com/guides/responses_api) xác nhận `deepseek-v4-flash` và `deepseek-v4-pro` đều hỗ trợ; [giá](https://api-docs.deepseek.com/quick_start/pricing) từ $0,14/triệu token input chưa cache và $0,28/triệu token output. Chưa đủ mọi tính năng OpenAI, nhưng Codex vẫn chạy được.

Đây là một lựa chọn kiến trúc hợp lý của Codex, không phải lỗi. Responses API giúp OpenAI thống nhất agent loop và các loại sự kiện phức tạp. Chỉ là nó không khớp với nhu cầu của tôi: thường xuyên thử nhiều model và muốn đổi provider mà không phải dựng thêm một cây cầu chỉ để qua đường.

## Grok Build gần Claude Code trên giấy

[Tài liệu Grok Build](https://docs.x.ai/build/overview) mô tả một coding agent chạy trong terminal với TUI toàn màn hình, có thể đọc codebase, sửa file, chạy lệnh và hỗ trợ custom model. Nếu nhìn vào danh sách tính năng, đây gần như đúng thứ tôi muốn: trải nghiệm kiểu Claude Code nhưng mở hơn về model.

Khi dùng Grok, cảm giác ban đầu cũng khá quen. Tôi có thể làm việc trực tiếp trong terminal, giao task dài và theo dõi agent thao tác trên repository. Với model Grok, trải nghiệm nhìn chung ổn.

Vấn đề xuất hiện khi tôi dùng các model ngoài Grok. Trong workflow của tôi, độ tương thích chưa thực sự hoàn chỉnh: có lúc phiên làm việc bị crash khi tương tác với ảnh và không tự khôi phục được. Tôi không khẳng định lỗi này xảy ra với mọi model hay mọi máy; đây là điều tôi gặp trong quá trình sử dụng thực tế vào tháng 8/2026.

Các chi tiết UX nhỏ cũng cộng dồn khá nhanh. Khi Grok render URL của pull request hoặc luồng xác thực, link không phải lúc nào cũng dễ bấm và cũng không tự động mở trình duyệt trong những tình huống tôi gặp. Copy một URL không phải thảm họa kỹ thuật, nhưng nếu công cụ bắt mình làm việc đó đủ nhiều lần, nó trở thành một loại thuế rất lãng xẹt.

Một coding agent có thể rất thông minh, nhưng mỗi lần crash hoặc bắt người dùng xử lý thủ công một bước đáng ra tự động được là một lần nó làm đứt mạch suy nghĩ. Tôi đang trả tiền cho agent để giảm việc vặt, không phải tuyển thêm việc vặt dưới dạng TUI.

## Tôi quay lại vì harness, không phải vì bảng xếp hạng model

Claude Code vẫn cho tôi trải nghiệm hoàn chỉnh nhất khi làm việc lâu trong terminal. Session ổn định, các thao tác với file và công cụ ít gây bất ngờ, còn những việc như đưa ảnh vào ngữ cảnh, mở link hay tiếp tục sau lỗi thường không kéo tôi ra khỏi task chính.

Nghe có vẻ nghịch lý: tôi vừa phàn nàn Codex giới hạn custom model, rồi lại quay về một công cụ gắn chặt với Claude. Nhưng thử nghiệm này trả lời đúng câu hỏi đó: sự linh hoạt trong file cấu hình không giúp được nhiều nếu các tương tác cơ bản vẫn có thể làm gián đoạn công việc. Lúc này tôi chọn tổ hợp model và harness hoạt động ổn định từ đầu đến cuối; Codex vẫn ở lại cho những task phù hợp hơn với OpenAI.

Lần trước tôi rời Claude Code vì muốn giảm phụ thuộc và kiểm chứng các lựa chọn thay thế. Lý do đó vẫn còn nguyên. Việc quay lại không xóa những lo ngại về account, chính sách hay lock-in; nó chỉ cập nhật một dữ kiện mới: sau khi thử dùng công cụ khác cho workload thật, Claude Code vẫn làm tôi tốn ít sự chú ý nhất.

## Bộ công cụ của tôi sau một vòng thử nghiệm

Tôi sẽ dùng **Claude Code làm coding agent chính trong terminal**. Codex vẫn ở lại cho các task song song, những việc hợp với model OpenAI và các tình huống tôi muốn giao việc rồi quay lại xem kết quả. Grok Build tạm dừng cho đến khi trải nghiệm với custom model và những chi tiết UX cơ bản ổn định hơn.

Đây không phải cuộc thi chọn một công cụ rồi xóa hết phần còn lại. Coding agent đang thay đổi quá nhanh để trung thành tuyệt đối với một logo. Tôi chỉ cần biết công cụ nào nên nằm ở vị trí chính, công cụ nào là phương án bổ sung và công cụ nào cần thêm thời gian.

Sau cùng, coding agent tốt nhất với tôi không phải agent thắng nhiều benchmark nhất. Đó là agent giúp tôi tập trung vào code lâu nhất mà quên mất mình đang dùng một agent.

Thôi, tôi lại về dùng Claude Code đây :))

## Tài liệu tham khảo

1. [Codex: định nghĩa model provider và `WireApi`](https://github.com/openai/codex/blob/main/codex-rs/model-provider-info/src/lib.rs).
2. [Codex: thảo luận loại bỏ Chat Completions](https://github.com/openai/codex/discussions/7782).
3. [Grok Build: tổng quan và cấu hình custom model](https://docs.x.ai/build/overview).
4. [Claude Code: cài đặt và xác thực](https://docs.anthropic.com/en/docs/claude-code/getting-started).
5. DeepSeek: [Responses API](https://api-docs.deepseek.com/guides/responses_api) và [giá](https://api-docs.deepseek.com/quick_start/pricing).

*Thông tin sản phẩm được kiểm chứng ngày 22/8/2026; các nhận xét về độ ổn định và UX là trải nghiệm cá nhân trong workflow của tôi.*
