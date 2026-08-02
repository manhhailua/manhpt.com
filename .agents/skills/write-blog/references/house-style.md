# Phong cách bài viết của ManhPT

## Mục lục

- [Tính cách giọng văn](#tính-cách-giọng-văn)
- [Tiếng Việt và thuật ngữ](#tiếng-việt-và-thuật-ngữ)
- [Cấu trúc và nhịp bài](#cấu-trúc-và-nhịp-bài)
- [Hài hước vừa đủ](#hài-hước-vừa-đủ)
- [Bằng chứng và mức độ chắc chắn](#bằng-chứng-và-mức-độ-chắc-chắn)
- [Mẫu biên tập](#mẫu-biên-tập)

## Tính cách giọng văn

Viết bằng giọng của một kỹ sư thực chiến:

- đi thẳng vào vấn đề và sớm nêu luận điểm;
- tự tin nhưng không lên giọng dạy đời;
- ưu tiên tác động thực tế, cách lựa chọn và trade-off;
- nói rõ giới hạn, rủi ro và điều chưa chắc chắn;
- dùng `tôi` cho trải nghiệm hoặc nhận định cá nhân, dùng `bạn` khi hướng dẫn;
- tránh thay đổi tùy tiện giữa `tôi`, `mình`, `chúng ta` trong cùng một bài.

Không dùng giọng thông cáo báo chí, quảng cáo hoặc bản dịch máy. Tránh các mở bài như “Trong bối cảnh công nghệ phát triển không ngừng” nếu câu đó không cung cấp thông tin.

## Tiếng Việt và thuật ngữ

- Viết đủ dấu, đúng chính tả và dùng dấu câu theo cú pháp tiếng Việt.
- Dùng sentence case cho tiêu đề và heading: chỉ viết hoa từ đầu câu, tên riêng, thương hiệu và chữ viết tắt.
- Ưu tiên từ Việt tự nhiên: `hiệu năng`, `quy trình`, `bản phát hành`, `độ trễ`, `chi phí`, `giới hạn`.
- Giữ thuật ngữ Anh khi đó là tên chuẩn hoặc bản dịch làm câu khó hiểu hơn: API, RAG, cache, token, prompt, benchmark, agent, framework.
- Khi cần, viết dạng `truy xuất (retrieval)` ở lần đầu rồi dùng một cách gọi nhất quán.
- Dùng inline code cho tên file, lệnh, biến, field và đoạn mã; không dùng inline code chỉ để nhấn mạnh.
- Viết số, đơn vị, phiên bản và tên sản phẩm nhất quán. Không tự Việt hóa tên thương hiệu.
- Hạn chế dấu chấm than, emoji, ngoặc kép mỉa mai và các từ phóng đại như “đỉnh cao”, “cách mạng”, “hoàn hảo”.

Ưu tiên câu chủ động:

- Nên: “RTK lọc output trước khi agent đọc.”
- Tránh: “Output sẽ được tiến hành lọc bởi RTK trước khi được đọc bởi agent.”

## Cấu trúc và nhịp bài

Mở bài phải trả lời nhanh ba câu hỏi:

1. Vấn đề là gì?
2. Vì sao người đọc nên quan tâm?
3. Bài này sẽ giúp họ hiểu hoặc quyết định điều gì?

Đặt `<!-- truncate -->` sau phần mở bài. Phần preview phải tự đứng được nhưng không kể hết bài.

Trong phần thân:

- mỗi H2 đại diện cho một câu hỏi, bước hoặc luận điểm;
- mỗi đoạn ưu tiên 2–4 câu và một ý chính;
- mở mục bằng kết luận hoặc câu định hướng, sau đó mới đưa bằng chứng;
- dùng ví dụ cụ thể thay cho chuỗi tính từ;
- dùng bảng chỉ khi người đọc cần đối chiếu ít nhất ba mục hoặc nhiều tiêu chí;
- chuyển đoạn bằng logic nội dung, không lạm dụng “bên cạnh đó”, “hơn nữa”, “mặt khác”.

Kết bài phải cho người đọc một điểm chốt: nên làm gì, nên nhớ nguyên tắc nào, hoặc còn câu hỏi nào cần kiểm chứng. Tránh kết luận kiểu “hy vọng bài viết hữu ích”.

## Hài hước vừa đủ

Xem hài hước như một nhúm gia vị, không phải nguyên liệu chính.

- Thường chỉ cần 0–3 câu nhẹ trong một bài dài.
- Ưu tiên phép so sánh kỹ thuật, tự trào hoặc quan sát đời thường liên quan trực tiếp đến ý đang nói.
- Giữ câu đùa ngắn rồi quay lại nội dung ngay.
- Không chế giễu cá nhân, công ty, quốc gia hay nhóm người.
- Không đùa trong hướng dẫn xử lý sự cố nghiêm trọng, cảnh báo bảo mật hoặc đoạn cần độ chính xác cao.
- Không dùng meme, emoji hoặc tiếng lóng dày đặc để “cố vui”.

Ví dụ đúng mức:

> Công cụ không làm agent thông minh hơn; nó chỉ giúp agent bớt ăn context rác. Cũng như ăn kiêng, cắt đúng thì khỏe, cắt nhầm thì dễ ngất.

## Bằng chứng và mức độ chắc chắn

- Dẫn nguồn cho giá, chính sách, ngày phát hành, benchmark, lỗ hổng, thông số và tuyên bố của nhà cung cấp.
- Ưu tiên tài liệu chính thức, repository gốc, paper và advisory; chỉ dùng bài tổng hợp để bổ sung bối cảnh.
- Ghi rõ số liệu do nhà cung cấp tự công bố.
- Không biến tương quan thành quan hệ nhân quả.
- Phân biệt bằng câu chữ:
  - dữ kiện: “Tài liệu của dự án ghi…”
  - suy luận: “Điều này cho thấy…”
  - trải nghiệm: “Trong workflow của tôi…”
  - chưa chắc chắn: “Chưa có đủ dữ liệu để kết luận…”
- Với bài hướng dẫn cũ hoặc công nghệ đổi nhanh, nêu phiên bản và thời điểm kiểm chứng.

## Mẫu biên tập

Thay câu chung chung:

> Công nghệ AI đang phát triển rất nhanh và mang lại nhiều thay đổi lớn.

Bằng câu có thông tin:

> Khi coding agent bắt đầu đọc repo, chạy test và sửa code thay người dùng, chi phí context trở thành một phần của chi phí phát triển.

Thay khẳng định tuyệt đối:

> Vector search không hiểu quan hệ.

Bằng diễn đạt chính xác hơn:

> Vector search thuần túy thường không biểu diễn tốt các quan hệ nhiều bước nếu không có thêm cấu trúc hoặc bước suy luận.

Thay câu pha Anh–Việt không cần thiết:

> Team cần define boundary và optimize workflow để improve performance.

Bằng tiếng Việt tự nhiên:

> Nhóm cần xác định ranh giới hệ thống và tối ưu quy trình để cải thiện hiệu năng.
