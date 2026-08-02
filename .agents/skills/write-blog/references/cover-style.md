# Quy chuẩn ảnh cover

## Mục tiêu

Tạo một ảnh giúp người đọc đoán đúng chủ đề và cảm nhận của bài trước khi đọc tiêu đề. Ưu tiên một ý thị giác rõ, có liên hệ trực tiếp với luận điểm; tránh ảnh công nghệ chung chung kiểu robot, bộ não phát sáng hoặc màn hình đầy mã nếu chúng không giải thích điều gì.

## Visual brief bắt buộc

Viết ngắn sáu mục trước khi chọn hoặc tạo ảnh:

- **Thông điệp:** một câu nêu điều cover phải truyền đạt.
- **Chủ thể:** một đối tượng hoặc nhóm đối tượng chính.
- **Ẩn dụ:** hình ảnh hóa luận điểm, xung đột hoặc trade-off của bài.
- **Bố cục:** điểm nhìn, vị trí chủ thể và khoảng thở an toàn khi bị crop.
- **Không khí và màu sắc:** phù hợp sắc thái phân tích, hướng dẫn, cảnh báo hoặc góc nhìn cá nhân.
- **Tránh:** chi tiết sai, logo giả, giao diện bịa, chữ khó đọc, hình tượng sáo mòn hoặc yếu tố không liên quan.

## Nguyên tắc hình ảnh

- Dùng tỷ lệ 16:9; mục tiêu 1600×900, tối thiểu 1200×675.
- Giữ chủ thể quan trọng trong vùng trung tâm để ảnh vẫn rõ khi social card bị crop nhẹ.
- Ưu tiên một chủ thể và một ẩn dụ mạnh hơn nhiều chi tiết nhỏ.
- Không chèn tiêu đề bài vào ảnh theo mặc định. Chỉ dùng chữ khi nội dung thật sự cần và phải kiểm tra chính tả bằng mắt.
- Không tự tạo logo thương hiệu, screenshot sản phẩm hoặc giao diện có vẻ chính thức. Dùng asset chính thức nếu cần thể hiện thương hiệu.
- Với bài so sánh, thể hiện các lựa chọn cân bằng; không ngầm tuyên bố bên thắng nếu bài chưa kết luận như vậy.
- Với bài sự cố hoặc bảo mật, truyền đạt mức độ nghiêm túc nhưng không giật gân hay gây hoảng sợ.
- Với bài hướng dẫn, ưu tiên mô hình hệ thống hoặc trạng thái kết quả hơn một collage công cụ.

## Asset và định dạng

- Ưu tiên ảnh do người dùng cung cấp, asset chính thức được phép dùng hoặc ảnh tạo mới bằng công cụ tạo ảnh.
- Không hotlink ảnh ngoài và không lấy ảnh tìm thấy trên web khi chưa rõ quyền sử dụng.
- Ưu tiên `cover.webp` cho ảnh raster; dùng `.png` hoặc `.jpg` nếu pipeline chưa hỗ trợ WebP, và dùng `.svg` cho minh họa vector được kiểm soát.
- Lưu cover cạnh `index.md` và dùng `image: ./cover.ext` để bài có thể di chuyển độc lập.
- Giữ dung lượng hợp lý; xem xét tối ưu nếu file raster vượt 2 MB.

## Kiểm tra trước khi bàn giao

Mở ảnh ở độ phân giải đầy đủ và trả lời có cho tất cả câu hỏi:

1. Người chưa đọc bài có đoán gần đúng chủ đề không?
2. Ảnh có thể hiện luận điểm cụ thể thay vì chỉ nói “đây là bài về công nghệ” không?
3. Có chi tiết kỹ thuật, chữ, logo, bàn tay, màn hình hoặc quan hệ không gian nào sai rõ ràng không?
4. Chủ thể có còn rõ khi xem thumbnail nhỏ hoặc crop nhẹ không?
5. Ảnh có đúng tỷ lệ, đủ độ phân giải và được tham chiếu bằng `image` không?
