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
- Giữ thuật ngữ tiếng Anh khi đó là tên chuẩn, cách gọi quen thuộc trong ngành hoặc bản dịch làm sai sắc thái kỹ thuật: API, RAG, pipeline, cache, token, prompt, embedding, benchmark, agent, framework.
- Khi cần, viết dạng `truy xuất (retrieval)` ở lần đầu rồi dùng một cách gọi nhất quán.
- Dùng inline code cho tên file, lệnh, biến, field và đoạn mã; không dùng inline code chỉ để nhấn mạnh.
- Viết số, đơn vị, phiên bản và tên sản phẩm nhất quán. Không tự Việt hóa tên thương hiệu.
- Hạn chế dấu chấm than, emoji, ngoặc kép mỉa mai và các từ phóng đại như “đỉnh cao”, “cách mạng”, “hoàn hảo”.

“Thuần Việt” nằm ở cấu trúc câu, cách lập luận và nhịp văn, không nằm ở việc dịch bằng hết danh từ kỹ thuật. Chọn cách gọi theo ngữ cảnh:

| Trường hợp | Cách xử lý | Ví dụ |
|---|---|---|
| Có từ Việt chính xác, quen thuộc | Dùng tiếng Việt | `latency` → độ trễ; `cost` → chi phí; `access control` → kiểm soát truy cập |
| Tiếng Anh là tên khái niệm quen thuộc và bản dịch dễ gượng hoặc lệch nghĩa | Giữ tiếng Anh | pipeline, prompt, token, embedding, cache, benchmark, agent |
| Người đọc cần biết cả nghĩa lẫn từ khóa chuyên ngành | Giải thích song ngữ ở lần đầu, sau đó chọn một cách gọi | nguồn gốc dữ liệu (provenance), xếp hạng lại (reranking) |

Ưu tiên danh từ kỹ thuật đúng ngành nhưng dùng động từ, liên từ và trật tự câu tiếng Việt. Một thuật ngữ có thể được giữ bằng tiếng Anh khi đóng vai trò danh từ, còn hành động tương ứng vẫn viết bằng tiếng Việt: “retrieval chưa đủ” nhưng “hệ thống sẽ truy xuất lại”. Không chèn động từ tiếng Anh chỉ để câu nghe có vẻ kỹ thuật.

Không áp dụng bảng trên như một danh sách cấm dịch. `Workflow` có thể là “quy trình” khi nói về cách làm việc nói chung, nhưng nên giữ nguyên khi đó là tên một khái niệm hoặc thành phần cụ thể của sản phẩm. Sau khi đã chọn cách gọi cho một nghĩa, dùng nhất quán trong cùng bài; không đổi qua lại chỉ để tránh lặp từ.

Ví dụ:

- Nên: “Pipeline này lấy tài liệu, xếp hạng lại kết quả rồi đưa ngữ cảnh vào LLM.”
- Tránh: “Đường ống này retrieve document, rerank result rồi feed context vào model.”

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
