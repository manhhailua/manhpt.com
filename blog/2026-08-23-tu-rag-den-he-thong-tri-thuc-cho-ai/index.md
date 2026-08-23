---
title: "Từ làm RAG đến xây hệ thống Tri thức cho AI"
slug: tu-rag-den-he-thong-tri-thuc-cho-ai
authors: [manhpt]
tags: [rag, retrieval, architecture, agentic-ai, ai-strategy, ai]
date: 2026-08-23
description: "RAG chỉ là điểm bắt đầu. Hệ thống Tri thức cần giữ evidence nguyên văn và xây procedure để agent suy luận, kiểm chứng câu trả lời."
image: ./cover.webp
---

![Từ RAG cơ bản đến hệ thống Tri thức cho AI](./cover.webp)

Nếu hỏi tôi cách xây hệ thống tri thức cho AI cách đây không lâu, câu trả lời từng rất gọn: chia tài liệu thành chunk, tạo embedding, lưu vào vector database rồi đưa cho LLM.

Cách đó không sai và vẫn là điểm bắt đầu tốt. Nhưng có một cái tủ hồ sơ chưa đồng nghĩa với việc đã có thư viện.

Khi AI phải xử lý dữ liệu thay đổi, nguồn mâu thuẫn và câu hỏi nhiều bước, vấn đề không còn là **“tối ưu retrieval thế nào?”**. Tôi cần hai lớp tri thức: **evidence** giữ nguyên nội dung nguồn; **procedure** hướng dẫn agent tìm, suy luận và kiểm chứng câu trả lời.

<!-- truncate -->

## RAG chưa phải toàn bộ hệ thống tri thức

[Nghiên cứu RAG ban đầu](https://arxiv.org/abs/2005.11401) kết hợp bộ nhớ của mô hình với chỉ mục bên ngoài. Cách triển khai quen thuộc là:

```text
tài liệu → chunk → embedding → vector search → prompt → câu trả lời
```

Pipeline này hợp khi đáp án nằm trong vài đoạn gần nghĩa. Tối ưu retrieval có thể giúp tìm đúng đoạn hơn, nhưng chưa cho agent biết vòng tiếp theo cần tìm gì, kết hợp dữ kiện ra sao và khi nào nên dừng.

## Hai lớp: evidence và procedure

[Dense Passage Retrieval](https://aclanthology.org/2020.emnlp-main.550/) gọi đơn vị truy xuất là *passage*; [ART](https://aclanthology.org/2023.tacl-1.35/) và [FEVER](https://aclanthology.org/N18-1074/) dùng evidence theo ngữ cảnh của câu hỏi hoặc nhận định. Còn trong bài này, evidence là một quy ước kiến trúc, không mặc nhiên có nghĩa “đúng”.

### Evidence: bản ghi nguyên văn từ nguồn

Evidence không đồng nghĩa với sự thật đã được xác minh:

> **evidence = chunk nguyên văn + nguồn gốc dữ liệu (provenance) + metadata quản trị**

Chunking chỉ xác định ranh giới; nội dung không được viết lại hay tóm tắt. Ngữ cảnh bổ sung, kết quả OCR và embedding là dữ liệu dẫn xuất, không được ghi đè evidence gốc.

Mỗi evidence cần nguồn, phiên bản, vị trí, thời gian có hiệu lực, quyền truy cập và checksum. Nó chỉ chứng minh **“nguồn này đã nói như vậy”**; nội dung vẫn có thể cũ, sai hoặc mâu thuẫn. Nguồn thay đổi thì tạo evidence mới, không sửa bản cũ.

### Procedure: cách agent tìm câu trả lời

Procedure mô tả cách tìm và kiểm chứng câu trả lời. Nó không chứa sẵn đáp án, mà hướng dẫn quá trình suy luận của agent trong từng vòng lặp:

- mục tiêu, phạm vi, dữ liệu đầu vào và điều kiện áp dụng;
- bước truy xuất, nguồn hoặc công cụ cần dùng và thứ tự thực hiện;
- quy tắc suy luận, trạng thái trung gian và nhánh lựa chọn;
- cách kiểm tra, xử lý khi thiếu evidence và điều kiện dừng.

[ProPara](https://aclanthology.org/N18-1144/) và [OpenPI](https://aclanthology.org/2020.emnlp-main.520/) biểu diễn thay đổi trạng thái; [proScript](https://aclanthology.org/2021.findings-emnlp.184/) biểu diễn thứ tự; [BPMN 2.0](https://www.omg.org/spec/BPMN/2.0/PDF/) bổ sung nhánh và điều kiện. Các thành phần này có thể mô tả đường suy luận cho agent.

Tương quan giữa các chunk chỉ là tín hiệu khám phá, chưa phải procedure. Mỗi bước và nhánh phải trỏ về evidence hoặc quy tắc rõ ràng; phần agent tự suy ra phải được đánh dấu là suy luận.

## Procedure dẫn agent qua vòng lặp suy luận

Cách lưu trữ evidence và procedure không phải luận điểm chính. Quan trọng hơn, agent phải dùng procedure để quyết định bước tiếp theo trong mỗi vòng lặp.

```text
câu hỏi → agent dùng procedure chọn bước → truy xuất evidence
                ↑                              ↓
                └── chưa đủ ← kiểm chứng ← suy luận
                                      ↓ đủ
                                  câu trả lời
```

Trong mỗi vòng, agent lấy thêm evidence, cập nhật trạng thái suy luận rồi kiểm tra điều kiện dừng. Nếu căn cứ chưa đủ hoặc mâu thuẫn, procedure chỉ ra bước tiếp theo; nếu đã đủ, agent mới trả lời. Cơ chế này không bảo đảm agent luôn đúng, nhưng giúp đường suy luận nhất quán và có thể kiểm tra lại.

## Nâng cấp dần, không cần đập đi xây lại

Tôi sẽ đi theo ba bước:

1. **Xây lớp evidence:** lưu chunk nguyên văn cùng nguồn, phiên bản, quyền và checksum.
2. **Xây procedure cho câu hỏi quan trọng:** mô hình hóa bước truy xuất, quy tắc suy luận, nhánh xử lý, cách kiểm tra và điều kiện dừng; liên kết về evidence rồi kiểm tra bằng con người.
3. **Bổ sung và cải tiến trong vận hành:** liên tục bổ sung evidence từ nguồn và phiên bản mới, hoàn thiện metadata, đồng thời điều chỉnh procedure theo câu hỏi, phản hồi và lỗi thực tế; evidence gốc không bị ghi đè.

So với [cách nhìn “RAG không chỉ là vector” trước đây](/2026/07/01/rag-khong-chi-la-vector), đây là bước tiếp theo: RAG đưa đúng tri thức vào ngữ cảnh; evidence cung cấp dữ kiện; procedure dẫn đường cho vòng lặp suy luận để agent tìm và kiểm chứng câu trả lời.

## Tài liệu tham khảo

1. [Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401) — Lewis và cộng sự, 2020; paper giới thiệu RAG bằng cách kết hợp tri thức trong mô hình với nguồn ngoài có thể truy xuất.
2. [Dense Passage Retrieval](https://aclanthology.org/2020.emnlp-main.550/), [ART](https://aclanthology.org/2023.tacl-1.35/) và [FEVER](https://aclanthology.org/N18-1074/).
3. [PROV-O: The PROV Ontology](https://www.w3.org/TR/prov-o/) — W3C.
4. [ProPara](https://aclanthology.org/N18-1144/), [OpenPI](https://aclanthology.org/2020.emnlp-main.520/) và [proScript](https://aclanthology.org/2021.findings-emnlp.184/).
5. [Business Process Model and Notation 2.0](https://www.omg.org/spec/BPMN/2.0/PDF/) — Object Management Group.

*Nguồn nghiên cứu được kiểm tra ngày 23/8/2026.*
