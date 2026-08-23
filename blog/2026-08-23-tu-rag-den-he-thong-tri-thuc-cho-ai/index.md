---
title: "Từ làm RAG đến xây hệ thống Tri thức cho AI"
slug: tu-rag-den-he-thong-tri-thuc-cho-ai
authors: [manhpt]
tags: [rag, retrieval, architecture, agentic-ai, ai-strategy, ai]
date: 2026-08-23
description: "Nâng cấp RAG không chỉ là thêm tính năng. Điều quan trọng hơn là phát hiện quan hệ, quy trình và biến các chunk rời rạc thành tri thức cho AI."
image: ./cover.webp
---

![Từ RAG cơ bản đến hệ thống Tri thức cho AI](./cover.webp)

Nếu hỏi tôi cách xây một hệ thống tri thức cho AI cách đây không lâu, câu trả lời sẽ khá gọn: chia tài liệu thành các chunk, tạo embedding, lưu vào vector database, lấy top-k rồi đưa cho LLM.

Cách đó không sai và vẫn là điểm bắt đầu tốt. Nhưng có một cái tủ hồ sơ chưa đồng nghĩa với việc đã có thư viện.

Khi AI làm việc lâu dài với dữ liệu thay đổi, nhiều nguồn mâu thuẫn, nhiều phạm vi truy cập và nhiều agent cùng sử dụng, câu hỏi không còn là **“tối ưu retrieval thế nào?”**. Câu hỏi quan trọng hơn là: **“AI cần biết điều gì, dựa vào nguồn nào, đúng ở thời điểm nào và làm sao để kiểm chứng?”**

Đó là lúc tôi chuyển từ việc xây một pipeline RAG sang xây **hệ thống Tri thức cho AI**. Thêm hybrid search, reranking hay knowledge graph chỉ là phần dễ thấy; thay đổi quan trọng hơn nhiều nằm ở cách tri thức được hình thành từ dữ liệu.

<!-- truncate -->

## RAG giải một phần quan trọng, không phải toàn bộ bài toán

[Nghiên cứu RAG ban đầu](https://arxiv.org/abs/2005.11401) kết hợp bộ nhớ tham số của mô hình với chỉ mục vector bên ngoài để cập nhật tri thức và cung cấp nguồn cho câu trả lời.

Trong thực tế, cách triển khai này dần được rút gọn thành một pipeline khá cố định:

```text
tài liệu → chunk → embedding → vector search → prompt → câu trả lời
```

Pipeline này hợp với câu hỏi cục bộ có đáp án trong vài đoạn gần nghĩa với truy vấn. Nhưng nó bắt đầu hụt hơi khi phải trả lời những câu như:

- Chính sách hay con số này đã thay đổi ra sao và còn hiệu lực tại thời điểm nào?
- Các quyết định ở nhiều tài liệu liên hệ với nhau thế nào, và các bước rời rạc ghép thành quy trình nào?
- Ai được phép đọc nguồn và điều gì bị ảnh hưởng nếu nguồn đó bị thu hồi?

Đây không còn là bài toán tìm đoạn văn. Đây là bài toán quản lý tri thức.

## Nâng cấp tính năng chỉ là phần nhỏ

Hybrid search, reranking, query routing, graph hay agentic loop đều là những thành phần hữu ích của một hệ thống Tri thức. Nhưng thêm chúng vào RAG chủ yếu giúp **AI tìm và sử dụng thông tin tốt hơn**.

Chỉ cắt tài liệu thành chunk rồi lưu embedding vào vector database chưa đủ để tạo ra tri thức. Hệ thống có thể tìm kiếm tốt hơn, nhưng chưa làm rõ ai liên quan tới ai, quyết định nào dẫn đến thay đổi nào, một quy trình diễn ra qua những bước gì, điều kiện và ngoại lệ nằm ở đâu.

Phần nâng cấp quan trọng hơn là chuyển từ **đưa tài liệu vào hệ thống** sang **xây dựng tri thức từ tài liệu**: nhận diện thực thể, sự kiện và quyết định; phát hiện mối liên hệ hoặc tương quan; khôi phục quy trình; rồi gắn kết quả với nguồn, thời gian và mức độ tin cậy.

## Chunk là nguyên liệu, không phải tri thức

Chunk tiện cho indexing và retrieval, nhưng không mặc nhiên là một đơn vị tri thức. Nó có thể chỉ chứa nửa quyết định, một bước trong quy trình hoặc một mối liên hệ chỉ có nghĩa khi đặt cạnh nhiều nguồn khác.

[Contextual Retrieval của Anthropic](https://www.anthropic.com/engineering/contextual-retrieval) bổ sung ngữ cảnh cho từng chunk rồi kết hợp embedding, BM25 và reranking để giảm lỗi truy xuất. Với tôi, bài học lớn hơn là: **nội dung không thể tách khỏi bối cảnh đã tạo ra nó**.

Một vài ví dụ cho thấy khác biệt giữa lưu đoạn văn và hình thành tri thức:

| Tài liệu nói gì? | Hệ thống Tri thức cần làm rõ gì? |
|---|---|
| “A phê duyệt B từ ngày T” | thực thể, quyết định, thời điểm có hiệu lực và nguồn |
| “Nếu có X, nhóm Y phải làm Z trước W” | quy trình, người chịu trách nhiệm, điều kiện, thứ tự và quan hệ phụ thuộc |
| A và B thường xuất hiện cùng nhau trong nhiều nguồn | mối liên hệ hoặc tương quan, bằng chứng và độ tin cậy; không tự suy thành quan hệ nhân quả |

Để đi từ văn bản tới tri thức, pipeline có thể kết hợp schema extraction, entity resolution, quy tắc, LLM và bước xác nhận của con người. Kỹ thuật có thể thay đổi, nhưng tri thức dẫn xuất phải truy ngược được về nguồn; điều do hệ thống suy ra phải giữ bằng chứng và độ tin cậy thay vì âm thầm thành “sự thật”.

Một đơn vị tri thức vẫn có thể giữ chunk gốc làm bằng chứng, nhưng cần thêm nguồn và phiên bản; thực thể, sự kiện, quyết định và quan hệ; các bước, vai trò, điều kiện và ngoại lệ của quy trình; thời gian, quyền truy cập, trạng thái và độ tin cậy.

Embedding chỉ là một cách biểu diễn để tìm kiếm. Nó không nên trở thành bản gốc duy nhất của tri thức.

## Một kho tri thức cần nhiều cách nhìn

Sau khi tri thức được hình thành, hệ thống vẫn cần nhiều cách sử dụng nó: vector search cho nội dung gần nghĩa, keyword search cho tên và mã chính xác, SQL cho số liệu và knowledge graph cho quan hệ. Tài liệu gốc vẫn phải được giữ để đối chiếu.

[GraphRAG của Microsoft](https://www.microsoft.com/en-us/research/publication/from-local-to-global-a-graph-rag-approach-to-query-focused-summarization/) dùng knowledge graph và bản tóm tắt theo cụm để trả lời câu hỏi cần nhìn toàn bộ kho tài liệu. [KAG](https://arxiv.org/abs/2409.13731) liên kết graph với chunk gốc, rồi phối hợp truy xuất văn bản, truy vấn graph, phép tính và suy luận. Hai hướng này củng cố một nguyên tắc: **không có một kiểu chỉ mục phù hợp với mọi câu hỏi**.

Vì vậy, thay vì hỏi “chọn vector database nào?”, tôi muốn thiết kế một lớp tri thức có nhiều cách biểu diễn:

```text
nguồn gốc có thể kiểm tra
        ↓
đối tượng tri thức + metadata + quyền + thời gian
        ↓
vector | keyword | graph | SQL | API thời gian thực
        ↓
retrieval planner → gói bằng chứng → LLM hoặc AI agent
```

Nguồn là tài sản bền vững. Các chỉ mục chỉ là dữ liệu dẫn xuất, có thể xây lại khi công nghệ thay đổi.

## Retrieval không nên là một bước cố định

RAG cơ bản thường lấy một số lượng tài liệu cố định cho mọi câu hỏi. [Self-RAG](https://arxiv.org/abs/2310.11511) cho mô hình quyết định khi nào cần retrieval; [CRAG](https://arxiv.org/abs/2401.15884) đánh giá tài liệu lấy về để điều chỉnh chiến lược.

Không nhất thiết phải triển khai đúng hai kiến trúc đó; điều đáng học là cách thiết kế pipeline:

1. Hiểu ý định và tách câu hỏi nếu cần.
2. Chọn nguồn cùng cách truy xuất phù hợp.
3. Kiểm tra bằng chứng đã đủ, còn hiệu lực và đúng quyền truy cập chưa.
4. Truy xuất lại, đổi nguồn hoặc từ chối trước khi trả lời nếu chưa đủ căn cứ.

Câu hỏi đơn giản vẫn nên đi đường ngắn. Hệ thống thông minh không phải hệ thống lúc nào cũng gọi năm agent; đôi khi biết khỏi họp cũng là một dạng thông minh.

## Tri thức phải có lịch sử và trách nhiệm

Một chunk nói “giám đốc là A” có thể đúng hôm qua và sai hôm nay. Xóa bản cũ rồi lập chỉ mục lại giúp trả lời hiện tại, nhưng làm mất khả năng giải thích câu trả lời đã được tạo ở quá khứ.

[Temporal GraphRAG](https://arxiv.org/abs/2510.13590) đưa thời gian vào biểu diễn tri thức và giữ quan hệ ở từng thời điểm. Hướng nghiên cứu này còn mới, nhưng vấn đề rất thật: tri thức không đứng yên trong khi phần lớn benchmark RAG giả định dữ liệu tĩnh.

Hệ thống còn phải biết dữ kiện đến từ đâu, qua bước xử lý nào và ai chịu trách nhiệm. [W3C PROV](https://www.w3.org/TR/prov-overview/) dùng provenance (nguồn gốc dữ liệu) để ghi lại các thông tin này nhằm phục vụ đánh giá và kiểm chứng.

Với hệ thống Tri thức cho AI, provenance, phiên bản và quyền truy cập không nên là ba cột metadata thêm vào sau cùng. Chúng phải đi xuyên suốt từ lúc nhập dữ liệu, tạo chỉ mục, truy xuất cho tới citation ở đầu ra.

## Chất lượng phải được đo liên tục

Demo RAG thường được đánh giá bằng vài câu hỏi đã biết đáp án. Khi vận hành, [RAGAS](https://arxiv.org/abs/2309.15217) gợi ý tách việc lấy đúng ngữ cảnh, mức độ LLM bám vào ngữ cảnh và chất lượng câu trả lời; hệ thống Tri thức còn phải đo độ mới, thời gian cập nhật, lỗi phân quyền, chi phí và hiệu quả công việc.

Phản hồi của người dùng không nên tự động thành “sự thật”; nó phải tạo ra đề xuất có nguồn và được kiểm tra. Đây cũng là nguyên tắc tôi đang theo đuổi với [Lorekeep](/lorekeep-kho-tri-thuc-dung-chung-coding-agent): agent có thể đóng góp, nhưng không được âm thầm sửa ký ức chung.

## Nâng cấp dần, không cần đập đi xây lại

Không phải dự án nào cũng cần graph, agentic retrieval hay một ontology hoành tráng ngay từ đầu. Lộ trình hợp lý hơn là:

1. **Giữ nguyên liệu có thể truy vết:** lưu tài liệu gốc, phiên bản, quyền và citation; tạo bộ câu hỏi từ nhu cầu sử dụng thật.
2. **Xác định tri thức cần hình thành:** chọn các thực thể, sự kiện, quyết định, quan hệ, quy trình và quy tắc thật sự cần cho use case; trích xuất trên phạm vi nhỏ rồi kiểm tra bằng con người.
3. **Bổ sung tính năng theo lỗi quan sát được:** thêm keyword search, reranking, query routing, graph, SQL hoặc xử lý thời gian khi benchmark cho thấy cần.
4. **Tách thành dịch vụ tri thức dùng chung:** cung cấp API hoặc MCP để chatbot, workflow và nhiều agent cùng dùng một nền tri thức, thay vì mỗi ứng dụng tự tạo một kho riêng.

So với [cách nhìn “RAG không chỉ là vector” trước đây](/2026/07/01/rag-khong-chi-la-vector), đây là bước tiếp theo trong tư duy của tôi. Tôi vẫn làm RAG, nhưng trọng tâm đã chuyển từ cắt chunk và tối ưu top-k sang phát hiện, kiểm chứng các mối liên hệ và quy trình để tạo tri thức mà AI có thể sử dụng. RAG cùng các tính năng retrieval là một phần của hệ thống Tri thức — không phải toàn bộ hệ thống.

## Tài liệu tham khảo

1. [Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401) — Lewis và cộng sự, 2020.
2. [Introducing Contextual Retrieval](https://www.anthropic.com/engineering/contextual-retrieval) — Anthropic, 2024.
3. [From Local to Global: A Graph RAG Approach to Query-Focused Summarization](https://www.microsoft.com/en-us/research/publication/from-local-to-global-a-graph-rag-approach-to-query-focused-summarization/) — Microsoft Research, 2024.
4. [KAG: Boosting LLMs in Professional Domains via Knowledge Augmented Generation](https://arxiv.org/abs/2409.13731) — Liang và cộng sự, 2024.
5. [Self-RAG](https://arxiv.org/abs/2310.11511) và [Corrective Retrieval Augmented Generation](https://arxiv.org/abs/2401.15884).
6. [RAG Meets Temporal Graphs](https://arxiv.org/abs/2510.13590) — Han và cộng sự, 2025.
7. [W3C PROV Overview](https://www.w3.org/TR/prov-overview/).
8. [RAGAS: Automated Evaluation of Retrieval Augmented Generation](https://arxiv.org/abs/2309.15217) — Es và cộng sự, 2023.

*Nguồn nghiên cứu được kiểm tra ngày 23/8/2026.*
