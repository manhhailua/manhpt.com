---
title: "Từ làm RAG đến xây hệ thống Tri thức cho AI"
slug: tu-rag-den-he-thong-tri-thuc-cho-ai
authors: [manhpt]
tags: [rag, retrieval, architecture, agentic-ai, ai-strategy, ai]
date: 2026-08-23
description: "RAG cơ bản giúp AI tìm đoạn văn liên quan. Một hệ thống Tri thức cho AI còn phải quản lý nguồn gốc, quan hệ, thời gian, quyền truy cập và vòng đời tri thức."
image: ./cover.webp
---

![Từ RAG cơ bản đến hệ thống Tri thức cho AI](./cover.webp)

Nếu hỏi tôi cách xây một hệ thống tri thức cho AI cách đây không lâu, câu trả lời sẽ khá gọn: chia tài liệu thành `chunk`, tạo embedding, lưu vào vector database, lấy `top-k` rồi đưa cho LLM.

Cách đó không sai. Nó vẫn là điểm bắt đầu tốt để kiểm chứng một bài toán. Nhưng có một cái tủ hồ sơ chưa đồng nghĩa với việc đã có thư viện.

Khi AI phải làm việc lâu dài với dữ liệu liên tục thay đổi, nhiều nguồn mâu thuẫn, nhiều lớp quyền và nhiều agent cùng sử dụng, câu hỏi không còn là **“làm retrieval thế nào cho chính xác hơn?”**. Câu hỏi đúng phải là: **“AI cần biết điều gì, dựa vào nguồn nào, đúng ở thời điểm nào và làm sao để kiểm chứng?”**

Đó là lúc tôi muốn chuyển cách nghĩ: từ làm một pipeline RAG sang xây **hệ thống Tri thức cho AI**.

<!-- truncate -->

## RAG giải một phần quan trọng, không phải toàn bộ bài toán

[Nghiên cứu RAG ban đầu](https://arxiv.org/abs/2005.11401) kết hợp bộ nhớ tham số của mô hình với bộ nhớ ngoài là một chỉ mục vector của Wikipedia. Hai động lực quan trọng của hướng tiếp cận này là cập nhật tri thức và cung cấp nguồn cho câu trả lời.

Sau đó, cách triển khai phổ biến đã được giản lược thành một đường ống khá cố định:

```text
tài liệu → chunk → embedding → vector search → prompt → câu trả lời
```

Đường ống này rất hợp với câu hỏi cục bộ, khi đáp án nằm trong một vài đoạn văn gần nghĩa với truy vấn. Nhưng nó bắt đầu hụt hơi khi phải trả lời những câu như:

- Chính sách này thay đổi qua các phiên bản ra sao?
- Hai quyết định ở hai tài liệu khác nhau liên quan với nhau thế nào?
- Con số nào còn hiệu lực tại thời điểm được hỏi?
- Agent này có được phép đọc nguồn chứa câu trả lời không?
- Nếu tài liệu gốc bị thu hồi, những chỉ mục và câu trả lời nào bị ảnh hưởng?

Đây không còn là bài toán tìm đoạn văn. Đây là bài toán quản lý tri thức.

## `Chunk` không phải là đơn vị tri thức

Chia nhỏ tài liệu giúp việc tìm kiếm và đưa ngữ cảnh vào LLM rẻ hơn. Đổi lại, mỗi `chunk` dễ mất tiêu đề, chủ thể, thời gian và quan hệ với phần còn lại.

[Contextual Retrieval của Anthropic](https://www.anthropic.com/engineering/contextual-retrieval) cho thấy chính việc mất ngữ cảnh khi mã hóa có thể làm retrieval thất bại. Cách họ bổ sung ngữ cảnh riêng cho từng `chunk`, kết hợp embedding với BM25 và reranking, là một cải tiến thực dụng. Nhưng với tôi, bài học lớn hơn là: **nội dung không thể tách khỏi bối cảnh đã tạo ra nó**.

Trong hệ thống Tri thức, một đơn vị có thể vẫn chứa đoạn văn, nhưng phải đi cùng ít nhất:

- nguồn gốc và phiên bản tài liệu;
- thực thể, chủ đề và quan hệ liên quan;
- thời điểm ghi nhận, thời gian có hiệu lực;
- phạm vi truy cập;
- trạng thái: đã xác nhận, đang đề xuất hay đã bị thay thế.

Embedding chỉ là một cách biểu diễn để tìm kiếm. Nó không nên trở thành bản gốc duy nhất của tri thức.

## Một kho tri thức cần nhiều cách nhìn

Vector search giỏi tìm nội dung gần nghĩa. Keyword search giỏi tên riêng, mã lỗi và cụm từ chính xác. SQL giỏi con số và phép lọc xác định. Graph giỏi quan hệ giữa các thực thể. Tài liệu gốc vẫn cần để đối chiếu bằng chứng.

[GraphRAG của Microsoft](https://www.microsoft.com/en-us/research/publication/from-local-to-global-a-graph-rag-approach-to-query-focused-summarization/) chỉ ra một giới hạn cụ thể của RAG thông thường: câu hỏi cần nhìn toàn bộ kho tài liệu, chẳng hạn tìm các chủ đề chính, không phù hợp với việc lấy vài đoạn gần nhất. Graph thực thể và các bản tóm tắt theo cộng đồng được dùng để tạo góc nhìn toàn cục.

[KAG](https://arxiv.org/abs/2409.13731) đi thêm một hướng khác: liên kết qua lại giữa knowledge graph và `chunk` gốc, rồi kết hợp truy xuất văn bản, graph, phép tính và suy luận theo dạng logic. Tôi không xem đây là công thức phải chép nguyên xi, nhưng nó củng cố một nguyên tắc: **không có một kiểu chỉ mục nào phù hợp với mọi loại câu hỏi**.

Vì vậy, thay vì hỏi “chọn vector database nào?”, tôi muốn thiết kế một lớp tri thức có nhiều hình chiếu:

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

## Retrieval phải trở thành một kế hoạch

RAG cơ bản thường lấy một số lượng tài liệu cố định cho mọi câu hỏi. [Self-RAG](https://arxiv.org/abs/2310.11511) cho thấy retrieval có thể được thực hiện theo nhu cầu, đồng thời đánh giá mức độ liên quan và khả năng hỗ trợ câu trả lời. [CRAG](https://arxiv.org/abs/2401.15884) cũng đặt một bộ đánh giá trước kết quả retrieval để quyết định có cần hành động sửa sai hay không.

Trong thực tế, không nhất thiết phải huấn luyện một mô hình theo hai kiến trúc đó. Điều đáng học là cách đặt luồng xử lý:

1. Hiểu ý định và tách câu hỏi nếu cần.
2. Chọn nguồn cùng cách truy xuất phù hợp.
3. Đánh giá bằng chứng đã đủ và còn hiệu lực chưa.
4. Truy xuất lại, đổi nguồn hoặc từ chối nếu chưa đủ căn cứ.
5. Chỉ sau đó mới tổng hợp câu trả lời hay thực hiện hành động.

Câu hỏi đơn giản vẫn nên đi đường ngắn. Hệ thống thông minh không phải hệ thống lúc nào cũng gọi năm agent; đôi khi biết khỏi họp cũng là một dạng thông minh.

## Tri thức phải có lịch sử và trách nhiệm

Một `chunk` nói “giám đốc là A” có thể đúng hôm qua và sai hôm nay. Xóa bản cũ rồi lập chỉ mục lại giúp trả lời hiện tại, nhưng làm mất khả năng giải thích câu trả lời đã được tạo ở quá khứ.

[Temporal GraphRAG](https://arxiv.org/abs/2510.13590) xem thời gian là một phần của biểu diễn tri thức, giữ các quan hệ ở từng thời điểm và hỗ trợ cập nhật tăng dần. Đây là hướng nghiên cứu còn mới, nhưng vấn đề nó nêu ra rất thật: tri thức không đứng yên, trong khi phần lớn benchmark RAG giả định một kho dữ liệu tĩnh.

Thời gian vẫn chưa đủ. Hệ thống còn phải biết một dữ kiện đến từ đâu, qua bước xử lý nào và ai chịu trách nhiệm. [W3C PROV](https://www.w3.org/TR/prov-overview/) định nghĩa provenance quanh thực thể, hoạt động và con người tham gia tạo ra dữ liệu; thông tin đó giúp đánh giá chất lượng, độ tin cậy và khả năng kiểm chứng.

Với hệ thống Tri thức cho AI, provenance, phiên bản và quyền truy cập không nên là ba cột metadata thêm vào sau cùng. Chúng phải đi xuyên suốt từ lúc nhập dữ liệu, tạo chỉ mục, truy xuất cho tới citation trong đầu ra.

## Chất lượng là một vòng vận hành

Demo RAG thường được đánh giá bằng vài câu hỏi mà người làm hệ thống đã biết đáp án. Khi đưa vào sử dụng, chất lượng phải được tách thành nhiều lớp.

[RAGAS](https://arxiv.org/abs/2309.15217) đề xuất đánh giá riêng khả năng lấy đúng ngữ cảnh, mức độ LLM bám vào ngữ cảnh và chất lượng câu trả lời. Một hệ thống Tri thức còn cần đo thêm độ mới của dữ liệu, thời gian cập nhật, lỗi phân quyền, chi phí và hiệu quả công việc sau cùng.

Phản hồi của người dùng cũng không nên tự động biến thành “sự thật”. Nó nên tạo ra một đề xuất có nguồn, được kiểm tra rồi mới trở thành tri thức chính thức. Đây cũng là nguyên tắc tôi đang theo đuổi với [Lorekeep](/lorekeep-kho-tri-thuc-dung-chung-coding-agent): agent được đóng góp, nhưng không được âm thầm sửa ký ức chung.

## Nâng cấp dần, không cần đập đi xây lại

Tôi không cho rằng dự án nào cũng cần graph, agentic retrieval hay một ontology hoành tráng ngay từ ngày đầu. Lộ trình hợp lý hơn là:

1. **Làm cho nguồn có thể truy vết:** giữ tài liệu gốc, phiên bản, quyền và citation; tạo một tập câu hỏi đánh giá thật.
2. **Cải thiện retrieval theo lỗi quan sát được:** thêm keyword search, metadata filter, reranking hoặc query routing khi benchmark cho thấy cần.
3. **Mô hình hóa phần có cấu trúc:** chỉ đưa thực thể, quan hệ, quy tắc và thời gian vào graph hay database khi chúng phục vụ câu hỏi cụ thể.
4. **Tách thành dịch vụ tri thức dùng chung:** cung cấp API hoặc MCP để chatbot, workflow và nhiều agent cùng dùng một nền tri thức, thay vì mỗi ứng dụng tự tạo một kho riêng.

So với [cách nhìn “RAG không chỉ là vector” trước đây](/2026/07/01/rag-khong-chi-la-vector), đây là bước tiếp theo trong tư duy của tôi. Retrieval vẫn là công nghệ chủ đạo, nhưng mục tiêu không còn là tối ưu một pipeline hỏi đáp. Mục tiêu là xây một nền tri thức có thể cập nhật, kiểm soát, kiểm chứng và tái sử dụng.

Tôi vẫn làm RAG. Chỉ là từ giờ, RAG là một bộ phận của hệ thống — không còn là tên của cả hệ thống nữa.

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
