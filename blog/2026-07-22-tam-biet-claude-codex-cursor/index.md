---
title: "Tạm Biệt Claude: Vì Sao Tôi Dừng Claude Subscription Và Chuyển Sang Codex, Cursor"
slug: tam-biet-claude-codex-cursor
authors: [manhpt]
tags: [anthropic, claude-code, codex, cursor, coding-agent, ai-strategy]
date: 2026-07-22
description: "Tôi quyết định dừng Claude subscription, tạm bỏ hẳn Claude Code và chuyển sang Codex, Cursor CLI để tìm công cụ AI coding phù hợp lâu dài."
---

Một quyết định đã ấp ủ từ lâu, giờ mới đủ bình tĩnh để viết ra: **tôi huỷ Claude subscription và tạm dừng hoàn toàn Claude Code.** Không phải vì Claude yếu, mà vì trải nghiệm với Anthropic khiến tôi không còn muốn đặt phần lớn workflow của mình vào một nhà cung cấp duy nhất.

Bài này không phải bài đánh giá benchmark. Đây là nhật ký vận hành thật sau một quý dùng AI để code mỗi ngày.

<!-- truncate -->

## Vì Sao Tôi Mất Niềm Tin Vào Anthropic

Anthropic vươn lên rất nhanh nhờ model tốt và Claude Code xuất sắc. Nhưng trải nghiệm hỗ trợ lại khiến tôi phải đánh giá lại mức độ phụ thuộc vào họ.

Trong một số trường hợp account tại tổ chức của tôi bị chặn, các yêu cầu hỗ trợ đã không nhận được phản hồi trong thời gian mong đợi. Tôi không thể kết luận vì sao Anthropic phản hồi như vậy, nhưng với một công cụ đã đi sâu vào quy trình phát triển, sự thiếu chắc chắn đó tự nó đã là một rủi ro.

Sự cố ở cấp tổ chức không trực tiếp quyết định thuê bao cá nhân, nhưng nó thay đổi cách tôi nhìn nhận rủi ro phụ thuộc vào Anthropic. Khi một công cụ trở thành điểm tựa hằng ngày, tôi cần biết mình vẫn có đường lui nếu quota, account hoặc chính sách thay đổi.

Vì vậy, quyết định lần này không chỉ là huỷ một gói thuê bao. Tôi muốn kiểm chứng xem mình có thể rời cả model lẫn harness của Anthropic hay không.

## Những Gì Tôi Giữ Lại: Codex Và Cursor

### Cursor — mua vội, không hối hận

Từ tháng 11/2025, trong một phút cao hứng, tôi nạp luôn gói Pro một năm của Cursor. Bình thường đó là kiểu mua sắm bốc đồng dễ hối tiếc, nhưng lần này thì không. Đến giờ, Cursor vẫn là công cụ **GUI coding tốt nhất** đối với tôi: giao diện mượt, agent mode ổn và hiểu codebase tốt.

Trớ trêu là lâu nay tôi thường mở Cursor, bật terminal bên trong, vào `tmux`, rồi gọi `claude code`. Một IDE xịn chỉ để làm khung cửa sổ cho CLI của Anthropic — tức cười, nhưng đúng là workflow hằng ngày của tôi.

Điều đó cũng cho thấy nếu vẫn giữ Claude Code thì tôi chưa thực sự kiểm chứng được một lựa chọn thay thế. Vì vậy, trong giai đoạn tới tôi sẽ bỏ hẳn Claude Code và dùng **Cursor CLI** cho công việc terminal.

### Codex desktop — cực kỳ hài lòng

Với Codex desktop, tôi đang rất ưng ý với **GPT 5.6 Sol High**: chạy task nhanh, ổn định và ít làm gián đoạn mạch làm việc. Gói Plus tạm đủ cho vẽ diagram, brainstorm và viết tài liệu; với coding nặng, tôi sẽ tiếp tục dùng Cursor rồi đánh giá lại sau.

Ít nhất ở thời điểm này, Codex cho tôi cảm giác về một sản phẩm gọn và đáng tin. Đó là điều tôi cần ở một công cụ làm việc hằng ngày.

## GLM Đã Đủ Tốt Cho Nhu Cầu Của Tôi

Quý vừa rồi, trải nghiệm dùng **GLM** cho thấy tôi không bắt buộc phải dùng Claude model mới có thể duy trì công việc. GLM vẫn có giới hạn theo gói dịch vụ, nhưng quan trọng hơn là chất lượng đã đủ để trở thành một phương án thay thế thực tế trong nhiều tác vụ coding.

Kimi, GLM và các model mới cũng cho thấy thị trường đang có thêm lựa chọn. Tôi chưa cho rằng một nhóm model nào đã “lên ngôi”, nhưng câu chuyện “không có Claude thì không code được” rõ ràng không còn đúng với workflow của tôi.

## Bước Tiếp Theo: Dùng Cursor CLI Rồi Mới Chốt

Từ bây giờ, tôi sẽ **dừng hẳn Claude Code trong một thời gian** và chuyển các tác vụ CLI sang Cursor CLI. Đây không phải một buổi thử cho biết, mà là giai đoạn sử dụng thật trên đủ loại công việc: đọc codebase, sửa lỗi, refactor, viết test và xử lý task dài.

Trong thời gian đó, Codex desktop vẫn đảm nhiệm các task song song, brainstorm và tài liệu; Cursor GUI cùng Cursor CLI sẽ là môi trường coding chính. Sau khi có đủ trải nghiệm, tôi mới quyết định bộ công cụ nào đáng để gắn bó lâu dài.

Tôi không phủ nhận chất lượng của Claude hay Claude Code. Ngược lại, chính vì chúng từng quá tốt nên tôi mới phụ thuộc sâu đến vậy. Nhưng một công cụ tốt không đồng nghĩa với việc phải chấp nhận rủi ro phụ thuộc vô thời hạn.

Khi niềm tin với một nhà cung cấp giảm xuống, phản ứng tốt nhất không phải tranh cãi về động cơ của họ. Đó là xây dựng lựa chọn thay thế, chuyển workload thật sang đó và để kết quả trả lời.

---

*Tôi sẽ cập nhật lại sau một thời gian dùng Cursor CLI hoàn toàn thay cho Claude Code. Khi đó, quyết định cuối cùng sẽ dựa trên trải nghiệm vận hành thực tế, không phải cảm xúc nhất thời.*
