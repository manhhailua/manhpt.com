---
title: "Agentic Retrieval-Augmented Generation: A Survey on Agentic RAG"
authors: [manhpt]
tags: [rag, llm, ai-agent, langgraph, vietnamese]
date: 2026-03-15
description: "Bài viết đầu tiên trong series RAG Papers: tổng hợp paper survey Agentic RAG, tóm tắt taxonomy, workflow patterns, benchmark và các điểm quan trọng để áp dụng thực tế."
---

`Agentic Retrieval-Augmented Generation: A Survey on Agentic RAG` là một paper survey khá đầy đủ cho ai đang chuyển từ RAG tuyến tính sang các hệ RAG có tính tự chủ cao hơn (agentic). Bài này không giới thiệu một mô hình mới, mà hệ thống hóa lại bức tranh tổng quan: kiến trúc, workflow pattern, framework triển khai, benchmark và những thách thức còn mở.

<!-- truncate -->

## Thông Tin Nhanh Về Paper

- **Tiêu đề:** Agentic Retrieval-Augmented Generation: A Survey on Agentic RAG
- **Tác giả:** Aditi Singh, Abul Ehtesham, Saket Kumar, Tala Talaei Khoei
- **arXiv:** `2501.09136` (cs.AI, cs.CL, cs.IR)
- **Phiên bản mới nhất:** v3 (2025-02-04)
- **DOI:** [10.48550/arXiv.2501.09136](https://doi.org/10.48550/arXiv.2501.09136)
- **Link paper:** [arXiv abstract](https://arxiv.org/abs/2501.09136) | [PDF](https://arxiv.org/pdf/2501.09136)
- **GitHub survey:** [asinghcsu/AgenticRAG-Survey](https://github.com/asinghcsu/AgenticRAG-Survey)

## Paper Này Trả Lời Câu Hỏi Gì?

Paper tập trung vào câu hỏi: **Khi nào RAG truyền thống không đủ, và vì sao cần Agentic RAG?**

Theo paper, RAG cổ điển giải quyết được vấn đề "LLM bị stale knowledge", nhưng vẫn yếu ở 3 điểm:

1. Luồng xử lý tĩnh, khó thích ứng theo từng loại câu hỏi
2. Khả năng multi-step reasoning còn hạn chế
3. Khó mở rộng khi cần phối hợp nhiều nguồn dữ liệu, nhiều công cụ, nhiều bước kiểm tra

Agentic RAG được đưa ra như một bước tiến: đưa AI agents vào pipeline để **lập kế hoạch, chọn công cụ, phản tư kết quả và lặp lại truy xuất khi cần**.

## 4 Năng Lực Agentic Cốt Lõi

Paper nhấn mạnh 4 pattern nền tảng:

- **Reflection:** tự đánh giá đầu ra trung gian để sửa lỗi
- **Planning:** chia mục tiêu lớn thành các bước truy xuất/suy luận
- **Tool Use:** gọi API, DB, search engine, vector store theo ngữ cảnh
- **Multi-Agent Collaboration:** nhiều agent chuyên biệt phối hợp song song hoặc phân tầng

Điểm đáng chú ý là Agentic RAG không chỉ "retrieve rồi generate", mà có thể **điều phối chiến lược retrieval theo thời gian thực**.

## Taxonomy Chính Của Agentic RAG

Phần hay nhất của paper là taxonomy kiến trúc. Nhóm tác giả phân loại thành:

1. **Single-agent Agentic RAG**  
   Một agent trung tâm làm routing + retrieval + synthesis. Dễ triển khai, hợp bài toán vừa và nhỏ.

2. **Multi-agent Agentic RAG**  
   Tách agent theo chuyên môn (SQL, semantic search, web, recommendation...), xử lý song song. Mạnh hơn ở truy vấn phức tạp nhưng tăng chi phí điều phối.

3. **Hierarchical Agentic RAG**  
   Agent tầng trên ra quyết định chiến lược, agent tầng dưới thực thi retrieval. Hợp bài toán enterprise nhiều ràng buộc.

4. **Corrective / Adaptive Agentic RAG**  
   Có bước chấm độ liên quan tài liệu, rewrite query, gọi thêm nguồn ngoài khi context chưa đủ.

Nếu đang xây production system, phần này giúp chọn kiến trúc theo độ phức tạp thay vì "mặc định multi-agent".

## Workflow Patterns Đáng Áp Dụng

Paper tổng hợp các workflow rất thực dụng:

- Prompt chaining
- Routing
- Parallelization
- Orchestrator-workers
- Evaluator-optimizer

Trong thực tế, 2 pattern mình thấy đáng ưu tiên nhất là:

- **Routing** (đưa đúng query về đúng retriever/tool)
- **Evaluator-optimizer** (để giảm lỗi factuality trước khi trả kết quả)

## Ứng Dụng Và Stack Công Cụ

Paper điểm qua các domain ứng dụng: customer support, healthcare, legal, finance, education, multimodal.

Các framework/công cụ được nhắc nhiều gồm:

- LangChain / LangGraph
- LlamaIndex
- CrewAI, AutoGen (AG2), OpenAI Swarm
- Vector DB và graph DB như Qdrant, Weaviate, Pinecone, Neo4j
- Nền tảng cloud: Vertex AI, Amazon Bedrock, watsonx.ai

## Benchmark Và Khoảng Trống Đánh Giá

Paper liệt kê nhiều benchmark liên quan RAG (BEIR, MS MARCO, HotpotQA, MuSiQue, RAGBench, BERGEN, FlashRAG...).

Nhưng tác giả cũng chỉ ra một khoảng trống lớn: **chưa có chuẩn đánh giá đủ tốt cho năng lực agentic** như:

- chất lượng điều phối giữa agents,
- độ ổn định khi lặp nhiều bước,
- chi phí/độ trễ của orchestration,
- khả năng tự sửa lỗi khi retrieval lệch.

Đây là điểm quan trọng nếu bạn đang làm Agentic RAG production: đừng chỉ đo answer quality cuối, mà cần đo cả trajectory của pipeline.

## 5 Ý Chính Mình Rút Ra

1. **Agentic RAG là bài toán hệ thống, không chỉ prompt engineering.**
2. **Chọn kiến trúc theo mức độ phức tạp của query**, không phải theo trend.
3. **Corrective loop nên là mặc định** ở use case có rủi ro factuality cao.
4. **Observability cho workflow là bắt buộc** (trace từng bước retrieve-plan-refine).
5. **Evaluation cần đa chiều**: chất lượng + latency + cost + reliability.

## Hạn Chế Của Paper

Vì là survey, paper rất mạnh ở tổng quan nhưng không đi sâu vào:

- so sánh thực nghiệm head-to-head giữa các framework trong cùng điều kiện,
- design pattern nào "thắng" theo từng workload cụ thể,
- hướng dẫn triển khai production ở mức chi tiết vận hành.

Nói ngắn gọn: đây là tài liệu "định hình tư duy kiến trúc", còn tối ưu hệ thống thật vẫn cần benchmark riêng theo dữ liệu nội bộ.

## Tài Nguyên

- Paper: [arXiv 2501.09136](https://arxiv.org/abs/2501.09136)
- PDF: [https://arxiv.org/pdf/2501.09136](https://arxiv.org/pdf/2501.09136)
- DOI: [https://doi.org/10.48550/arXiv.2501.09136](https://doi.org/10.48550/arXiv.2501.09136)
- GitHub Survey: [https://github.com/asinghcsu/AgenticRAG-Survey](https://github.com/asinghcsu/AgenticRAG-Survey)
