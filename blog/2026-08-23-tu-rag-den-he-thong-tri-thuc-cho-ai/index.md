---
title: "Từ làm RAG đến xây hệ thống Tri thức cho AI"
slug: tu-rag-den-he-thong-tri-thuc-cho-ai
authors: [manhpt]
tags: [rag, retrieval, architecture, agentic-ai, ai-strategy, ai]
date: 2026-08-23
description: "RAG chỉ là điểm bắt đầu. Hệ thống Tri thức cần giữ source passage nguyên văn và xây procedure có thể truy vết để AI biết cách hành động."
image: ./cover.webp
---

![Từ RAG cơ bản đến hệ thống Tri thức cho AI](./cover.webp)

Nếu hỏi tôi cách xây một hệ thống tri thức cho AI cách đây không lâu, câu trả lời sẽ khá gọn: chia tài liệu thành các chunk, tạo embedding, lưu vào vector database, lấy top-k rồi đưa cho LLM.

Cách đó không sai và vẫn là điểm bắt đầu tốt. Nhưng có một cái tủ hồ sơ chưa đồng nghĩa với việc đã có thư viện.

Khi AI làm việc lâu dài với dữ liệu thay đổi, nhiều nguồn mâu thuẫn, nhiều phạm vi truy cập và nhiều agent cùng sử dụng, câu hỏi không còn là **“tối ưu retrieval thế nào?”**. Câu hỏi quan trọng hơn là: **“AI cần biết điều gì, dựa vào nguồn nào, đúng ở thời điểm nào và làm sao để kiểm chứng?”**

Đó là lúc tôi chuyển từ việc xây một pipeline RAG sang xây **hệ thống Tri thức cho AI** với hai lớp rõ ràng: **source passage** giữ nguyên điều nguồn đã nói; **procedure** diễn tả cách công việc thực sự diễn ra để AI không chỉ trả lời mà còn biết cách hành động.

<!-- truncate -->

## RAG giải một phần quan trọng, không phải toàn bộ bài toán

[Nghiên cứu RAG ban đầu](https://arxiv.org/abs/2005.11401) kết hợp bộ nhớ tham số của mô hình với chỉ mục vector bên ngoài để cập nhật tri thức và cung cấp nguồn cho câu trả lời.

Trong thực tế, cách triển khai này dần được rút gọn thành một pipeline khá cố định:

```text
tài liệu → chunk → embedding → vector search → prompt → câu trả lời
```

Pipeline này hợp với câu hỏi cục bộ có đáp án trong vài đoạn gần nghĩa với truy vấn. Nhưng nó bắt đầu hụt hơi khi phải trả lời những câu như:

- Chính sách hay con số này đã thay đổi ra sao và còn hiệu lực tại thời điểm nào?
- Từ các hướng dẫn nằm rải rác, quy trình hoàn chỉnh có mục tiêu gì, ai làm từng bước, theo điều kiện nào và xử lý ngoại lệ ra sao?
- Ai được phép đọc nguồn và điều gì bị ảnh hưởng nếu nguồn đó bị thu hồi?

Đây không còn là bài toán tìm đoạn văn. Đây là bài toán quản lý tri thức.

## Nâng cấp tính năng chỉ là phần nhỏ

Hybrid search, reranking, query routing, graph hay agentic loop đều là những thành phần hữu ích của một hệ thống Tri thức. Nhưng thêm chúng vào RAG chủ yếu giúp **AI tìm và sử dụng thông tin tốt hơn**.

Cắt tài liệu thành các source passage tạo ra lớp dữ liệu có thể truy xuất; embedding và vector database chỉ giúp tìm trong lớp này. Hệ thống biết đoạn nào gần nghĩa với câu hỏi, nhưng chưa biết công việc phải được thực hiện theo những bước nào.

Phần nâng cấp quan trọng hơn là xây procedure từ các source passage: mục tiêu, điều kiện, hành động, thứ tự, vai trò, thay đổi trạng thái, nhánh xử lý và kết quả. Mỗi thành phần dẫn xuất vẫn phải trỏ ngược về đoạn nguồn đã tạo ra nó.

## Hai lớp: source passage và procedure

[Dense Passage Retrieval](https://aclanthology.org/2020.emnlp-main.550/) gọi các khối 100 từ được cắt từ Wikipedia là *passage*. [ART](https://aclanthology.org/2023.tacl-1.35/) dùng *evidence passage*, nhưng [FEVER](https://aclanthology.org/N18-1074/) chỉ xem câu là evidence khi nó hỗ trợ hoặc bác bỏ một nhận định; [KILT](https://aclanthology.org/2021.naacl-main.200/) dùng *provenance* cho vị trí trong nguồn dùng để kiểm chứng đầu ra.

Vì vậy, tôi giữ thuật ngữ phổ biến *passage* và gọi lớp lưu trữ là **source passage**. Tính nguyên văn và bất biến là quy ước của hệ thống; khi source passage hỗ trợ câu trả lời hoặc procedure, nó mới đóng vai trò evidence.

### Source passage: phần nguyên văn của nguồn

Source passage là đoạn nguyên văn được cắt từ tài liệu. Chunking chỉ xác định ranh giới; nội dung không được diễn giải lại, tóm tắt hay sửa cho “đẹp”. Kết quả OCR hoặc chuẩn hóa phải là bản dẫn xuất, không được ghi đè source passage.

Mỗi source passage cần nguồn, phiên bản, vị trí, thời điểm thu thập và có hiệu lực, quyền truy cập cùng checksum. Nó trả lời **“nguồn đã nói gì?”**, không khẳng định nội dung đó còn đúng hay đã được chấp nhận làm sự thật.

[Contextual Retrieval của Anthropic](https://www.anthropic.com/engineering/contextual-retrieval) bổ sung ngữ cảnh để truy xuất chunk tốt hơn. Phần ngữ cảnh, bản tóm tắt và embedding nên nằm bên cạnh source passage dưới dạng dữ liệu dẫn xuất. [W3C PROV-O](https://www.w3.org/TR/prov-o/) cũng phân biệt nội dung được trích từ nguồn với bản sửa đổi và dữ liệu dẫn xuất.

### Procedure: để AI biết cách làm

Procedure không phải bản tóm tắt dài hơn hay việc phát hiện vài chunk thường xuất hiện cùng nhau. Nó là mô hình vận hành được hình thành từ một hoặc nhiều source passage để AI lập kế hoạch, thực hiện và kiểm tra kết quả.

[ProPara](https://aclanthology.org/N18-1144/) và [OpenPI](https://aclanthology.org/2020.emnlp-main.520/) mô hình hóa quy trình qua thay đổi trạng thái của thực thể ở từng bước. [proScript](https://aclanthology.org/2021.findings-emnlp.184/) chỉ ràng buộc những sự kiện buộc phải trước hoặc sau nhau; [BPMN 2.0](https://www.omg.org/spec/BPMN/2.0/PDF/) còn mô hình hóa activity, event, gateway, dữ liệu và người chịu trách nhiệm. Từ đó, một procedure cần có:

- **Mục tiêu và phạm vi:** kết quả cần tạo ra và trường hợp áp dụng.
- **Điều kiện:** sự kiện kích hoạt, precondition, điều kiện duy trì và tiêu chí hoàn tất.
- **Cách thực hiện:** hành động, thứ tự, quan hệ phụ thuộc, bước song song và nhánh lựa chọn.
- **Trách nhiệm và tài nguyên:** người thực hiện, đầu vào, công cụ, dữ liệu và quyền.
- **Thay đổi trạng thái:** trạng thái trước, trạng thái sau và đầu ra của mỗi bước.
- **Kiểm soát:** ngoại lệ, cách phục hồi, bước xác minh và source passage hỗ trợ từng trường.

Tương quan giữa các chunk chỉ là tín hiệu khám phá, không chứng minh thứ tự, trách nhiệm hay quan hệ nhân quả. Procedure là dữ liệu dẫn xuất nên phải có phiên bản, độ tin cậy và trạng thái xác nhận; phần chưa có source passage hỗ trợ phải được đánh dấu là suy luận hoặc đề xuất.

## Một kho tri thức cần nhiều cách nhìn

Hai lớp này cần những cách truy xuất khác nhau. Vector và keyword search phù hợp với source passage; SQL và knowledge graph phù hợp hơn với điều kiện, trạng thái, vai trò và quan hệ phụ thuộc trong procedure. Tài liệu gốc vẫn phải được giữ để đối chiếu.

[GraphRAG của Microsoft](https://www.microsoft.com/en-us/research/publication/from-local-to-global-a-graph-rag-approach-to-query-focused-summarization/) tạo góc nhìn toàn cục bằng graph và bản tóm tắt theo cụm; [KAG](https://arxiv.org/abs/2409.13731) liên kết graph với chunk gốc rồi phối hợp nhiều cách truy xuất. Điểm chung là: **không có một kiểu chỉ mục phù hợp với mọi câu hỏi**.

Vì vậy, thay vì hỏi “chọn vector database nào?”, tôi muốn thiết kế một lớp tri thức có nhiều cách biểu diễn:

```text
tài liệu gốc
      ↓ cắt, không viết lại
source passage bất biến + provenance
      ├── vector | keyword
      └── trích xuất + kiểm chứng
                  ↓
                 procedure
          mục tiêu | điều kiện | hành động | vai trò | trạng thái | nhánh
                  ↓
              graph | SQL
                  ↓
retrieval planner → source passage hoặc procedure → LLM hoặc AI agent
```

Nguồn là tài sản bền vững. Các chỉ mục chỉ là dữ liệu dẫn xuất, có thể xây lại khi công nghệ thay đổi.

## Retrieval không nên là một bước cố định

RAG cơ bản thường lấy số lượng tài liệu cố định cho mọi câu hỏi. [Self-RAG](https://arxiv.org/abs/2310.11511) cho mô hình quyết định khi nào cần retrieval; [CRAG](https://arxiv.org/abs/2401.15884) đánh giá tài liệu lấy về để điều chỉnh chiến lược. Bài học thực dụng là thiết kế pipeline biết chọn nguồn, kiểm tra các source passage đã đủ, còn hiệu lực và đúng quyền chưa, rồi truy xuất lại, đổi nguồn hoặc từ chối trước khi trả lời.

Câu hỏi đơn giản vẫn nên đi đường ngắn. Hệ thống thông minh không phải hệ thống lúc nào cũng gọi năm agent; đôi khi biết khỏi họp cũng là một dạng thông minh.

## Tri thức phải có lịch sử và trách nhiệm

Một source passage nói “giám đốc là A” có thể đúng hôm qua và sai hôm nay. Khi tài liệu thay đổi, hệ thống cần tạo source passage mới thay vì ghi đè bản cũ; procedure dẫn xuất từ bản cũ phải được cập nhật hoặc đánh dấu đã bị thay thế. [Temporal GraphRAG](https://arxiv.org/abs/2510.13590) đưa thời gian vào biểu diễn tri thức cũng vì vấn đề này.

[W3C PROV](https://www.w3.org/TR/prov-overview/) dùng provenance (nguồn gốc dữ liệu) để ghi lại thực thể, hoạt động và người chịu trách nhiệm trong quá trình tạo dữ liệu. Với hệ thống Tri thức cho AI, provenance, phiên bản và quyền truy cập phải đi xuyên suốt từ source passage, procedure, chỉ mục cho tới citation ở đầu ra.

## Chất lượng phải được đo liên tục

Demo RAG thường được đánh giá bằng vài câu hỏi đã biết đáp án. [RAGAS](https://arxiv.org/abs/2309.15217) tách chất lượng retrieval, mức độ LLM bám vào ngữ cảnh và chất lượng câu trả lời; hệ thống Tri thức còn phải đo độ mới, lỗi phân quyền, chi phí và hiệu quả công việc.

Phản hồi của người dùng chỉ nên tạo ra đề xuất có nguồn và được kiểm tra. Đây cũng là nguyên tắc tôi theo đuổi với [Lorekeep](/lorekeep-kho-tri-thuc-dung-chung-coding-agent): agent có thể đóng góp, nhưng không được âm thầm sửa ký ức chung.

## Nâng cấp dần, không cần đập đi xây lại

Không phải dự án nào cũng cần graph, agentic retrieval hay một ontology hoành tráng ngay từ đầu. Lộ trình hợp lý hơn là:

1. **Xây lớp source passage:** lưu chunk nguyên văn, phiên bản, vị trí, quyền và checksum; xem các chỉ mục là dữ liệu có thể xây lại.
2. **Xây procedure:** mô hình hóa mục tiêu, điều kiện, hành động, vai trò, trạng thái và ngoại lệ; liên kết về source passage rồi kiểm tra bằng con người.
3. **Bổ sung theo lỗi thực tế:** chỉ thêm reranking, routing, graph, SQL hoặc xử lý thời gian khi benchmark cho thấy cần.
4. **Tách thành dịch vụ dùng chung:** cung cấp API hoặc MCP để nhiều ứng dụng và agent dùng cùng nền tri thức.

So với [cách nhìn “RAG không chỉ là vector” trước đây](/2026/07/01/rag-khong-chi-la-vector), đây là bước tiếp theo trong tư duy của tôi. Tôi vẫn làm RAG, nhưng giờ RAG là cơ chế đưa đúng source passage hoặc procedure vào ngữ cảnh, không phải tên của cả hệ thống. Source passage cho AI căn cứ để trả lời; procedure cho nó cấu trúc để lập kế hoạch, hành động và kiểm tra kết quả.

## Tài liệu tham khảo

1. [Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401) — Lewis và cộng sự, 2020.
2. [Introducing Contextual Retrieval](https://www.anthropic.com/engineering/contextual-retrieval) — Anthropic, 2024.
3. [From Local to Global: A Graph RAG Approach to Query-Focused Summarization](https://www.microsoft.com/en-us/research/publication/from-local-to-global-a-graph-rag-approach-to-query-focused-summarization/) — Microsoft Research, 2024.
4. [KAG: Boosting LLMs in Professional Domains via Knowledge Augmented Generation](https://arxiv.org/abs/2409.13731) — Liang và cộng sự, 2024.
5. [Self-RAG](https://arxiv.org/abs/2310.11511) và [Corrective Retrieval Augmented Generation](https://arxiv.org/abs/2401.15884).
6. [RAG Meets Temporal Graphs](https://arxiv.org/abs/2510.13590) — Han và cộng sự, 2025.
7. [PROV-O: The PROV Ontology](https://www.w3.org/TR/prov-o/) và [W3C PROV Overview](https://www.w3.org/TR/prov-overview/).
8. [RAGAS: Automated Evaluation of Retrieval Augmented Generation](https://arxiv.org/abs/2309.15217) — Es và cộng sự, 2023.
9. [Tracking State Changes in Procedural Text](https://aclanthology.org/N18-1144/) — Dalvi và cộng sự, 2018.
10. [A Dataset for Tracking Entities in Open Domain Procedural Text](https://aclanthology.org/2020.emnlp-main.520/) — Tandon và cộng sự, 2020.
11. [proScript: Partially Ordered Scripts Generation](https://aclanthology.org/2021.findings-emnlp.184/) — Sakaguchi và cộng sự, 2021.
12. [Business Process Model and Notation, Version 2.0](https://www.omg.org/spec/BPMN/2.0/PDF/) — Object Management Group, 2011.
13. [Dense Passage Retrieval for Open-Domain Question Answering](https://aclanthology.org/2020.emnlp-main.550/) — Karpukhin và cộng sự, 2020.
14. [Questions Are All You Need to Train a Dense Passage Retriever](https://aclanthology.org/2023.tacl-1.35/) — Sachan và cộng sự, 2023.
15. [FEVER: a Large-scale Dataset for Fact Extraction and VERification](https://aclanthology.org/N18-1074/) — Thorne và cộng sự, 2018.
16. [KILT: a Benchmark for Knowledge Intensive Language Tasks](https://aclanthology.org/2021.naacl-main.200/) — Petroni và cộng sự, 2021.

*Nguồn nghiên cứu được kiểm tra ngày 23/8/2026.*
