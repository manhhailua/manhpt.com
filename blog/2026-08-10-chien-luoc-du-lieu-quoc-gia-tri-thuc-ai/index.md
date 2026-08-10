---
title: "Quyết định 1308/QĐ-TTg và hướng đi Tri thức AI của tôi"
slug: chien-luoc-du-lieu-quoc-gia-tri-thuc-ai
authors: [manhpt]
tags: [ai-strategy, rag, retrieval, ai, vietnamese]
date: 2026-08-10
description: "Phân tích Chiến lược dữ liệu quốc gia 2026–2030 và lý do tôi chọn RAG làm công nghệ chủ đạo để xây hệ thống Tri thức AI có căn cứ, kiểm soát và cập nhật được."
image: ./cover.png
---

![Chiến lược dữ liệu quốc gia và hướng đi xây dựng hệ thống Tri thức AI](./cover.png)

Ngày 18/7/2026, [Quyết định 1308/QĐ-TTg](https://vanban.chinhphu.vn/?docid=218908&pageid=27160) phê duyệt Chiến lược dữ liệu quốc gia 2026–2030, tầm nhìn 2045, đặt dữ liệu, hạ tầng tính toán và AI trong một định hướng thống nhất.

Tôi chú ý nhất tới lựa chọn nền tảng: **AI phải đi cùng dữ liệu có chất lượng, được quản trị, kết nối và bảo vệ**. Đây là động lực dài hạn để tôi xây **hệ thống Tri thức AI** bằng RAG: tìm đúng nguồn, trả lời có căn cứ và cho phép kiểm chứng.

<!-- truncate -->

## Điều mới đáng chú ý trong Quyết định 1308

[Toàn văn Quyết định 1308](https://datafiles.chinhphu.vn/cpp/files/vbpq/2026/7/1308_qd-ttg_18072026_3-signed.signed.pdf) coi dữ liệu là tài nguyên chiến lược, tài sản quốc gia và tư liệu sản xuất mới. Các mục tiêu nổi bật đến năm 2030 gồm:

| Trụ cột | Mục tiêu đáng chú ý |
|---|---|
| Quản trị | Kiến trúc, khung quản trị và từ điển dữ liệu tại bộ, ngành, địa phương |
| AI và hạ tầng | Kho dữ liệu AI quốc gia; 3 Trung tâm dữ liệu quốc gia; hạ tầng HPC và AI dùng chung; hỗ trợ ít nhất 150 sản phẩm, dịch vụ dữ liệu và mô hình AI “Make in Vietnam” |
| Kinh tế dữ liệu | Tối thiểu 5 sàn dữ liệu, 1.000 doanh nghiệp công nghệ dữ liệu và 30 tổ chức trung gian dữ liệu |

Đây là **mục tiêu chính sách**, chưa phải kết quả. Nhưng [danh mục nhiệm vụ trọng tâm](https://datafiles.chinhphu.vn/cpp/files/vbpq/2026/7/1308_qd-ttg_18072026_5-signed.pdf) đã gắn mục tiêu với cơ quan và thời hạn; dữ liệu cho AI không còn là lời khuyến khích chung chung.

## Từ dữ liệu đến Tri thức AI

[Quyết định 804/QĐ-TTg](https://vanban.chinhphu.vn/?docid=218027&pageid=27160) xác định 15 nhóm dữ liệu thiết yếu cho AI, từ tiếng Việt, tri thức quốc gia, pháp luật đến khoa học, y tế và giáo dục. Quyết định 804 trả lời **cần dữ liệu nào**; Quyết định 1308 chỉ ra cách quản trị và khai thác dài hạn.

Dữ liệu cần nguồn gốc, ngữ cảnh, phiên bản, hiệu lực và quyền truy cập mới thành tri thức. Kho dữ liệu là nền móng; Tri thức AI là lớp giúp con người hỏi và hành động.

## Vì sao tôi chọn RAG làm công nghệ chủ đạo

Quyết định 1308 **không nhắc đến RAG**. Đây là diễn giải kỹ thuật của tôi, không phải yêu cầu trong văn bản.

RAG cho mô hình ngôn ngữ truy xuất bộ nhớ ngoài, tìm bằng chứng rồi tổng hợp câu trả lời. [Nghiên cứu gốc](https://arxiv.org/abs/2005.11401) tập trung vào cập nhật tri thức và chỉ ra nguồn.

```text
Nguồn dữ liệu
  → Chuẩn hóa, siêu dữ liệu và quyền truy cập
  → Kho tri thức và chỉ mục
  → Truy xuất, xếp hạng lại
  → LLM tổng hợp
  → Trích dẫn, đánh giá và phản hồi
```

RAG phù hợp với hướng đi này vì:

- **Cập nhật được:** lập chỉ mục lại thay vì huấn luyện toàn bộ mô hình.
- **Có bằng chứng:** dẫn về tài liệu, phiên bản và đoạn nguồn.
- **Kiểm soát truy cập:** áp dụng quyền trước khi dữ liệu vào ngữ cảnh LLM.
- **Ít phụ thuộc mô hình:** thay LLM hay embedding mà vẫn giữ tài sản tri thức.

RAG không chỉ là vector search. Tùy dữ liệu, hệ thống còn cần keyword search, SQL, graph hoặc API để tìm đúng bằng chứng.

## Hệ thống tôi muốn xây

Tri thức AI cần nhiều hơn giao diện chat phủ lên vài tệp PDF. Tôi muốn hệ thống:

1. **Kiểm soát nguồn:** biết dữ liệu từ đâu và còn hiệu lực không.
2. **Ưu tiên bằng chứng:** trích dẫn nguồn; thiếu thì nói rõ.
3. **Tôn trọng phân quyền:** quyền đi cùng dữ liệu tới câu trả lời.
4. **Không khóa vào mô hình:** thay thế độc lập từng thành phần.
5. **Đo được chất lượng:** đánh giá retrieval, độ bám nguồn và hiệu quả tác vụ.

Tôi bắt đầu với nguồn công khai hoặc được cấp quyền: nhập liệu, siêu dữ liệu, phiên bản; sau đó là truy xuất kết hợp, bộ đánh giá; cuối cùng mới thành API hay trợ lý chuyên ngành. Mô hình có thể đổi vài lần trước khi dữ liệu sạch — dữ liệu bẩn thường bền bỉ hơn công nghệ.

## Động lực dài hạn, không phải bảo chứng

Chiến lược không tự tạo ra sản phẩm tốt. Kết nối không có nghĩa là truy cập tự do; mỗi loại dữ liệu có chế độ riêng. Tôi cũng không giả định mình được tiếp cận cơ sở dữ liệu quốc gia.

RAG có thể lấy nhầm tài liệu, dùng nguồn hết hiệu lực hoặc suy diễn quá mức. Quản trị, đánh giá và con người chịu trách nhiệm vẫn bắt buộc.

Quyết định 1308 cho tôi một đường chân trời đến năm 2045. Framework và mô hình sẽ đổi; nhu cầu tìm đúng tri thức, đúng quyền và trả lời có căn cứ thì không.

Tôi chọn xây phần bền hơn mô hình: **quản trị dữ liệu, truy xuất, đánh giá và khả năng kiểm chứng**. RAG là công nghệ hiện tại; Tri thức AI đáng tin cậy là mục tiêu lâu dài.

## Tài liệu tham khảo

1. [Quyết định 1308/QĐ-TTg](https://vanban.chinhphu.vn/?docid=218908&pageid=27160) — Chiến lược dữ liệu quốc gia 2026–2030.
2. [Phụ lục II của Quyết định 1308](https://datafiles.chinhphu.vn/cpp/files/vbpq/2026/7/1308_qd-ttg_18072026_5-signed.pdf) — nhiệm vụ trọng tâm.
3. [Quyết định 804/QĐ-TTg](https://vanban.chinhphu.vn/?docid=218027&pageid=27160) — dữ liệu thiết yếu phục vụ AI.
4. [Luật Dữ liệu số 60/2024/QH15](https://xaydungchinhsach.chinhphu.vn/toan-van-luat-du-lieu-119250226145839949.htm).
5. [Nghiên cứu gốc về RAG](https://arxiv.org/abs/2005.11401) — Lewis và cộng sự, 2020.

*Thông tin chính sách trong bài được kiểm chứng ngày 10/8/2026.*
