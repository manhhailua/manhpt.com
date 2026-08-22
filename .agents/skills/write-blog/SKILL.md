---
name: write-blog
description: Soạn mới, viết lại và biên tập bài blog kỹ thuật tiếng Việt kèm ảnh cover phù hợp cho repository manhpt.com theo đúng cấu trúc Docusaurus, giọng văn của tác giả và quy ước nội dung của dự án; sau khi kiểm tra, tự động commit, push và tạo hoặc cập nhật pull request. Dùng khi cần tạo hoặc sửa bài trong blog/, chuyển ghi chú hay tài liệu nghiên cứu thành bài blog, tạo cover, chuẩn hóa frontmatter, chọn tag, cải thiện tiếng Việt, hoặc xuất bản bài qua pull request.
---

# Write Blog

Viết bài như một kỹ sư giàu trải nghiệm đang chia sẻ điều hữu ích: rõ lập trường, có căn cứ, thực tế, tiếng Việt tự nhiên và chỉ hài hước vừa đủ.

## Chuẩn bị

1. Đọc `CLAUDE.md`, `blog/tags.yml` và `blog/authors.yml` trong repository.
2. Đọc [references/house-style.md](references/house-style.md) và [references/cover-style.md](references/cover-style.md) trước khi lập dàn ý.
3. Xác định loại bài, độc giả, mục tiêu, luận điểm chính và độ dài phù hợp. Không kéo dài bài chỉ để trông có vẻ chuyên sâu.
4. Kiểm tra các bài gần nhất cùng chủ đề để tránh lặp nội dung và giữ cách gọi thuật ngữ nhất quán.
5. Với thông tin có thể thay đổi như phiên bản, giá, chính sách, benchmark, sự cố bảo mật hoặc tính năng sản phẩm, kiểm chứng bằng nguồn hiện hành; ưu tiên tài liệu chính thức và nguồn sơ cấp. Phân biệt rõ dữ kiện, suy luận và trải nghiệm cá nhân.

## Chọn khung bài

- **Hướng dẫn kỹ thuật:** vấn đề → điều kiện chuẩn bị → các bước → cách kiểm tra → lỗi thường gặp → kết luận.
- **Phân tích hoặc góc nhìn:** luận điểm → bối cảnh → bằng chứng → phản biện hoặc giới hạn → hệ quả thực tế → kết luận.
- **So sánh hoặc khảo sát:** kết luận ngắn → tiêu chí → bảng so sánh khi hữu ích → phân tích từng lựa chọn → rủi ro → khuyến nghị → nguồn.
- **Sự cố hoặc bảo mật:** tóm tắt → đối tượng bị ảnh hưởng → mức độ rủi ro → việc cần làm ngay → giải thích kỹ thuật → điều chưa chắc chắn → nguồn.
- **Tóm tắt paper:** thông tin nhanh → câu hỏi nghiên cứu → phương pháp → kết quả → hạn chế → điều có thể áp dụng → tài nguyên.

Điều chỉnh khung theo nội dung; không ép mọi bài vào cùng một khuôn.

## Tạo bài

1. Tạo file tại `blog/YYYY-MM-DD-slug/index.md`.
2. Dùng slug ASCII chữ thường, dạng kebab-case, ngắn và mô tả đúng chủ đề.
3. Dùng frontmatter sau. Luôn khai báo `image`; chỉ thêm `last_modified` hoặc trường khác khi thật sự cần:

```yaml
---
title: "Tiêu đề cụ thể, tự nhiên và không giật gân"
slug: slug-bai-viet
authors: [manhpt]
tags: [tag-da-khai-bao]
date: YYYY-MM-DD
description: "Một câu mô tả chính xác giá trị của bài viết."
image: ./cover.webp
---
```

4. Chỉ dùng tag đã có trong `blog/tags.yml`. Nếu chủ đề thật sự cần tag mới, thêm tag với đủ `label`, `permalink` và `description`; không tạo tag gần nghĩa với tag hiện có.
5. Tạo và kiểm tra ảnh cover theo quy trình bên dưới trước khi hoàn tất bản nháp.
6. Mở bài bằng 2–4 đoạn ngắn: nêu vấn đề, lý do đáng quan tâm và lời hứa cụ thể của bài. Đặt đúng một `<!-- truncate -->` sau phần mở bài và trước H2 đầu tiên.
7. Chia thân bài bằng H2; chỉ dùng H3 khi một H2 thật sự có nhiều ý con. Không dùng H1 trong nội dung.
8. Dùng bảng khi cần so sánh nhiều tiêu chí; dùng danh sách cho các mục song song; dùng code block có language identifier cho lệnh và mã nguồn.
9. Kết luận bằng quyết định, nguyên tắc hoặc bước tiếp theo. Không chỉ lặp lại nguyên văn phần mở bài.
10. Thêm mục `## Tài liệu tham khảo` cho bài dựa nhiều vào nguồn ngoài. Đặt link gần nhận định quan trọng nếu người đọc cần kiểm chứng ngay.

## Tạo ảnh cover

1. Chốt luận điểm và dàn ý trước, sau đó viết visual brief theo [references/cover-style.md](references/cover-style.md). Cover phải diễn đạt ý chính của bài, không chỉ minh họa một từ khóa chung chung.
2. Dùng ảnh do người dùng cung cấp hoặc asset chính thức khi phù hợp và có quyền sử dụng. Nếu không có ảnh đạt yêu cầu, dùng `$imagegen` hoặc công cụ tạo ảnh khả dụng để tạo mới; không lấy ngẫu nhiên ảnh có bản quyền từ web.
3. Tạo ảnh ngang 16:9, mục tiêu 1600×900 và tối thiểu 1200×675. Ưu tiên WebP cho ảnh raster; chấp nhận PNG, JPEG hoặc SVG khi có lý do phù hợp.
4. Lưu ảnh cùng thư mục bài viết, ưu tiên tên `cover.webp`, rồi khai báo bằng đường dẫn tương đối như `image: ./cover.webp`. Không đổi phần mở rộng nếu chưa chuyển đổi định dạng thật.
5. Xem lại ảnh ở kích thước đầy đủ sau khi tạo. Kiểm tra chủ thể, bố cục, chi tiết kỹ thuật, chữ, logo và mức độ khớp với luận điểm; tạo lại nếu ảnh chỉ đẹp nhưng kể sai câu chuyện.
6. Không bàn giao bài nếu chưa có cover hợp lệ. Nếu không thể tạo hoặc sử dụng ảnh an toàn, báo rõ blocker thay vì bỏ qua trường `image`.

## Biên tập

1. Giữ nguyên ý định và dữ kiện đúng của tác giả; sửa cấu trúc, logic, câu chữ và nhịp bài.
2. Loại bỏ câu mở đầu chung chung, đoạn lặp, từ đệm, lời quảng cáo và khẳng định tuyệt đối thiếu căn cứ.
3. Chuẩn hóa thuật ngữ theo [references/house-style.md](references/house-style.md). Giải thích thuật ngữ chuyên môn ở lần xuất hiện đầu tiên khi độc giả mục tiêu có thể chưa biết.
4. Giữ đoạn văn ngắn, mỗi đoạn tập trung một ý. Dùng câu chủ động và đưa kết luận quan trọng lên trước.
5. Chỉ thêm chút hài hước khi câu đùa làm ý dễ nhớ hơn; bỏ ngay nếu nó làm giảm độ tin cậy hoặc lấn át thông tin.

## Kiểm tra

Chạy trình kiểm tra nhanh:

```bash
python3 .agents/skills/write-blog/scripts/validate_blog_post.py \
  blog/YYYY-MM-DD-slug/index.md
```

Sửa toàn bộ lỗi và đọc lại các cảnh báo có liên quan. Sau đó chạy:

```bash
npm run build
```

## Xuất bản qua pull request

Sau khi validator và build thành công, luôn hoàn tất công việc bằng pull request; không dừng ở working tree local, trừ khi yêu cầu hiện tại nói rõ không được commit, push hoặc tạo PR.

1. Kiểm tra `git status --short --branch`; giữ nguyên mọi thay đổi không thuộc bài đang làm và chỉ stage các file trong phạm vi task.
2. Chọn branch an toàn:
   - nếu đang ở `main`, tạo branch ngắn gọn dạng `codex/blog-<slug>` từ `main` đã cập nhật;
   - nếu branch hiện tại có PR đang mở, tiếp tục dùng branch và PR đó;
   - nếu PR của branch đã đóng hoặc merge, tạo branch mới từ `main`; không tái sử dụng branch cũ bằng force-push.
3. Commit bằng Conventional Commits với subject ngắn, thường là `docs(blog): <tóm tắt>`; push branch lên `origin`.
4. Tìm PR theo head branch trước khi tạo mới:
   - nếu có PR đang mở, cập nhật title và body để phản ánh bản mới nhất; không tạo PR trùng;
   - nếu chưa có PR, tạo PR sẵn sàng review vào `main`.
5. PR body phải có tối thiểu: tóm tắt nội dung, file thay đổi, kết quả validator/build, thời lượng đọc khi đo được, thông tin cover và các nguồn chính của bài.
6. Theo dõi status check sau khi push. Sửa và push bổ sung nếu check thất bại do thay đổi trong task; nếu lỗi nằm ngoài phạm vi, báo rõ blocker cùng link check.
7. Không tự merge PR, xóa branch hoặc sửa lịch sử bằng force-push nếu người dùng chưa yêu cầu rõ.

Khi môi trường yêu cầu phê duyệt cho thao tác Git hoặc GitHub, gửi yêu cầu phê duyệt tại đúng bước cần thiết; không dùng giới hạn quyền làm lý do bỏ qua việc tạo hoặc cập nhật PR.

Trước khi bàn giao, xác nhận:

- frontmatter đúng và metadata khớp nội dung;
- cover đã được xem lại, phù hợp luận điểm, đúng tỷ lệ và được khai báo trong `image`;
- có đúng một marker `<!-- truncate -->`;
- mọi tag và tác giả đã được khai báo;
- link, ảnh, code block và lệnh mẫu hợp lệ;
- dữ kiện nhạy thời gian có nguồn và ngày kiểm chứng phù hợp;
- bài có một luận điểm xuyên suốt, tiếng Việt tự nhiên và mức hài hước tiết chế;
- không còn placeholder, ghi chú nội bộ hoặc tuyên bố chưa kiểm chứng.
- branch đã được push và pull request đã được tạo hoặc cập nhật, trừ khi người dùng yêu cầu chỉ làm local.
