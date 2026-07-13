---
title: "RAG Không Chỉ Là Vector: Hai Trụ Cột Retrieval và Generation"
authors: [manhpt]
tags: [rag, retrieval, llm, vietnamese]
date: 2026-07-01
description: "RAG có hai phần chính: Retrieval và Generation. Retrieval không chỉ là vector — có thể là SQL, Graph, file keyword. Mục tiêu là trả lời đúng, đủ và thông minh cho câu hỏi của người dùng."
---

Khi nghe "RAG", đa số developer nghĩ ngay: embed document thành vector, lưu vào vector DB, query top-k, dúi vào LLM. Đúng một phần — nhưng cách nghĩ đó làm mất đi bức tranh thật.

RAG viết tắt của **Retrieval-Augmented Generation**. Tên đã nói lên hai trụ cột: một bên đi tìm thông tin (Retrieval), một bên dùng thông tin đó để sinh câu trả lời (Generation). Mục tiêu cuối cùng không phải là "có vector DB", mà là trả lời **đúng, đủ và thông minh** cho câu hỏi của người dùng.

<!-- truncate -->

## Trụ Cột 1 — Retrieval: Đi Tìm Thông Tin Đúng Nơi

Đây là phần bị hiểu sai nhiều nhất. Retrieval không đồng nghĩa với vector search. Vector chỉ là *một* trong nhiều cách truy xuất, và thường không phải cách tốt nhất nếu đứng một mình.

Bản chất của Retrieval: đặt đúng câu hỏi, rồi đi lấy đúng dữ liệu từ đúng nguồn. Nguồn dữ liệu trong thực tế rất đa dạng:

- **Vector / embedding**: giỏi tìm ngữ nghĩa tương tự. Hỏi "cách giảm churn" → ra đoạn nói về "retention strategy". Nhưng yếu với tên riêng, mã sản phẩm, số liệu chính xác.
- **Keyword / BM25**: vàng cho exact match. `SKU-12345`, tên khách hàng, mã lỗi — vector bó tay, keyword lại chuẩn.
- **SQL**: khi câu hỏi là "doanh thu quý 3 của khu vực miền Nam", không chunk nào chứa sẵn câu trả lời. Cần query trực tiếp lên database.
- **Graph**: câu hỏi multi-hop kiểu "nhà cung cấp nào của Apple bị ảnh hưởng bởi lệnh cấm xuất khẩu 2023?" cần duyệt quan hệ thực thể. Vector không hiểu quan hệ, Graph hiểu.
- **File / API**: đôi khi câu trả lời nằm gọn trong một file PDF, một trang Confluence, hoặc một API thời gian thực. Đơn giản là mở ra và đọc.

Production RAG hiếm khi dùng một nguồn. **Hybrid retrieval** — kết hợp vector + keyword, hoặc agentic retrieval tự quyết định nguồn nào phù hợp câu hỏi nào — mới là chuẩn thực tế.

Retrieval tốt quyết định phần lớn chất lượng câu trả lời. Thu thập sai từ đầu, Generation dù mạnh đến đâu cũng không cứu vãn được.

## Trụ Cột 2 — Generation: Biết Đọc, Biết Suy Luận, Biết Nói Không

Có đúng dữ liệu rồi, Generation phải làm ba việc.

**Một**, tổng hợp thông tin rời rạc thành câu trả lời mạch lạc. Nhiều chunk, nhiều nguồn — LLM cần khâu lại thành văn bản có cấu trúc, không phải liệt kê rời rạc.

**Hai**, suy luận khi dữ liệu gián tiếp. Câu trả lời đôi khi không nằm sẵn trong một chunk, mà phải suy diễn từ nhiều mảnh thông tin. Đây là lúc model reasoning mạnh tỏ rõ.

**Ba**, quan trọng nhất: biết nói "không có đủ thông tin". Một hệ thống RAG tốt từ chối bịa ra câu trả lời khi retrieval không đủ căn cứ. Citation/trích dẫn nguồn là cơ chế bắt hallucination — claim mà không cite được, khả năng cao là bịa.

Generation yếu thì dù retrieval tốt, câu trả lời vẫn lan man, thiếu cấu trúc, hoặc tự nhiên hallucinate.

## Hai Trụ Cột Phải Khớp Nhau

RAG không phải hai phần rời rạc. Retrieval và Generation phải thiết kế khớp với nhau:

- Retrieval trả context thừa → LLM bị "lost in the middle", đắt token, trả lời lan man.
- Retrieval trả context thiếu → hallucination hoặc từ chối trả lời không cần thiết.
- Prompt không ràng buộc trích dẫn → LLM bịa, không kiểm chứng được.

Mục tiêu tối thượng của RAG không phải là kỹ thuật nào xịn hơn, mà là một điều duy nhất: **trả lời đúng, đủ và thông minh cho câu hỏi của người dùng**. Đúng về mặt sự thật, đủ về mặt thông tin, thông minh về cách diễn đạt và suy luận. Mọi quyết định — chọn vector hay SQL, chunk to hay nhỏ, model nào — đều phải phục vụ mục tiêu đó.

Vector là một công cụ trong hộp đồ nghề. Đừng nhầm nó với toàn bộ RAG.
