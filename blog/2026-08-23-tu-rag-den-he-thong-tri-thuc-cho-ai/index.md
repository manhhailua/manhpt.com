---
title: "Từ làm RAG đến xây hệ thống Tri thức cho AI"
slug: tu-rag-den-he-thong-tri-thuc-cho-ai
authors: [manhpt]
tags: [rag, retrieval, architecture, agentic-ai, ai-strategy, ai]
date: 2026-08-23
description: "RAG chỉ là điểm bắt đầu. Hệ thống Tri thức cần giữ evidence ở dạng nguyên văn và xây procedure có thể truy vết để AI biết cách hành động."
image: ./cover.webp
---

![Từ RAG cơ bản đến hệ thống Tri thức cho AI](./cover.webp)

Nếu hỏi tôi cách xây hệ thống tri thức cho AI cách đây không lâu, câu trả lời sẽ khá gọn: chia tài liệu thành chunk, tạo embedding, lưu vào vector database rồi đưa kết quả cho LLM.

Cách đó không sai và vẫn là điểm bắt đầu tốt. Nhưng có một cái tủ hồ sơ chưa đồng nghĩa với việc đã có thư viện.

Khi AI phải xử lý dữ liệu thay đổi, nguồn mâu thuẫn và quy trình nằm rải rác, câu hỏi không còn là **“tối ưu retrieval thế nào?”**. Tôi cần hai lớp tri thức: **evidence** giữ nguyên nội dung nguồn; **procedure** diễn tả cách công việc thực sự diễn ra.

<!-- truncate -->

## RAG chưa phải toàn bộ hệ thống tri thức

[Nghiên cứu RAG ban đầu](https://arxiv.org/abs/2005.11401) kết hợp bộ nhớ của mô hình với chỉ mục bên ngoài. Cách triển khai quen thuộc là:

```text
tài liệu → chunk → embedding → vector search → prompt → câu trả lời
```

Pipeline này phù hợp khi đáp án nằm trong vài đoạn gần nghĩa. Hybrid search, reranking, graph hay agentic retrieval giúp tìm tốt hơn, nhưng vẫn chưa cho AI biết mục tiêu, thứ tự hành động, trách nhiệm, nhánh xử lý và ngoại lệ của một quy trình.

## Hai lớp: evidence và procedure

[Dense Passage Retrieval](https://aclanthology.org/2020.emnlp-main.550/) gọi đơn vị truy xuất là *passage*; [ART](https://aclanthology.org/2023.tacl-1.35/) và [FEVER](https://aclanthology.org/N18-1074/) dùng evidence theo ngữ cảnh của câu hỏi hoặc nhận định. Còn trong bài này, evidence là một quy ước kiến trúc, không mặc nhiên có nghĩa “đúng”.

### Evidence: bản ghi nguyên văn từ nguồn

Evidence không đồng nghĩa với sự thật đã được xác minh:

> **evidence = chunk nguyên văn + nguồn gốc dữ liệu (provenance) + metadata quản trị**

Chunking chỉ xác định ranh giới; nội dung không được viết lại hay tóm tắt. Ngữ cảnh bổ sung, kết quả OCR và embedding là dữ liệu dẫn xuất, không được ghi đè evidence gốc.

Mỗi evidence cần nguồn, phiên bản, vị trí, thời gian có hiệu lực, quyền truy cập và checksum. Nó chỉ chứng minh **“nguồn này đã nói như vậy”**; nội dung vẫn có thể cũ, sai hoặc mâu thuẫn. Nguồn thay đổi thì tạo evidence mới, không sửa bản cũ.

### Procedure: để AI biết cách làm

Procedure là mô hình vận hành được hình thành từ evidence, không phải bản tóm tắt hay vài chunk thường xuất hiện cùng nhau. Nó gồm:

- mục tiêu, phạm vi, sự kiện kích hoạt và điều kiện áp dụng;
- hành động, thứ tự, quan hệ phụ thuộc và nhánh lựa chọn;
- vai trò, tài nguyên, thay đổi trạng thái và kết quả;
- ngoại lệ, cách phục hồi và bước xác minh.

[ProPara](https://aclanthology.org/N18-1144/) và [OpenPI](https://aclanthology.org/2020.emnlp-main.520/) theo dõi thay đổi trạng thái; [proScript](https://aclanthology.org/2021.findings-emnlp.184/) biểu diễn thứ tự sự kiện; [BPMN 2.0](https://www.omg.org/spec/BPMN/2.0/PDF/) bổ sung nhánh và trách nhiệm.

Tương quan giữa các chunk chỉ là tín hiệu khám phá, không chứng minh thứ tự hay quan hệ nhân quả. Mỗi phần của procedure phải trỏ về evidence; chỗ chưa có căn cứ phải được đánh dấu là suy luận.

## Kiến trúc phải phục vụ hai lớp tri thức

Vector và keyword search phù hợp với evidence; SQL và knowledge graph phù hợp hơn với procedure. Retrieval planner chọn cách truy xuất theo câu hỏi thay vì luôn lấy một số chunk cố định.

```text
tài liệu gốc
      ↓ cắt, không viết lại
evidence bất biến + provenance
      ├── vector | keyword
      └── trích xuất + kiểm chứng → procedure → graph | SQL

câu hỏi → retrieval planner → evidence hoặc procedure → LLM hoặc AI agent
```

Evidence là tài sản bền vững; chỉ mục có thể xây lại. Provenance, phiên bản và quyền truy cập phải đi từ nguồn đến câu trả lời. Evidence đổi thì procedure liên quan phải được cập nhật hoặc đánh dấu đã lỗi thời.

## Nâng cấp dần, không cần đập đi xây lại

Tôi sẽ đi theo ba bước:

1. **Xây lớp evidence:** lưu chunk nguyên văn cùng nguồn, phiên bản, quyền và checksum.
2. **Xây procedure cho công việc quan trọng:** mô hình hóa hành động, vai trò, trạng thái và ngoại lệ; liên kết về evidence rồi kiểm tra bằng con người.
3. **Bổ sung theo lỗi thực tế:** chỉ thêm reranking, graph, SQL hay agentic retrieval khi benchmark cho thấy cần.

So với [cách nhìn “RAG không chỉ là vector” trước đây](/2026/07/01/rag-khong-chi-la-vector), đây là bước tiếp theo: RAG đưa đúng tri thức vào ngữ cảnh; evidence cho AI căn cứ để trả lời; procedure cho AI biết phải làm gì và kiểm tra kết quả ra sao.

## Tài liệu tham khảo

1. [Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401) — Lewis và cộng sự, 2020; paper giới thiệu RAG bằng cách kết hợp tri thức trong mô hình với nguồn ngoài có thể truy xuất.
2. [Dense Passage Retrieval](https://aclanthology.org/2020.emnlp-main.550/), [ART](https://aclanthology.org/2023.tacl-1.35/) và [FEVER](https://aclanthology.org/N18-1074/).
3. [PROV-O: The PROV Ontology](https://www.w3.org/TR/prov-o/) — W3C.
4. [ProPara](https://aclanthology.org/N18-1144/), [OpenPI](https://aclanthology.org/2020.emnlp-main.520/) và [proScript](https://aclanthology.org/2021.findings-emnlp.184/).
5. [Business Process Model and Notation 2.0](https://www.omg.org/spec/BPMN/2.0/PDF/) — Object Management Group.

*Nguồn nghiên cứu được kiểm tra ngày 23/8/2026.*
