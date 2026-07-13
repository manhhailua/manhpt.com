---
title: "RAG Không Chỉ Là Vector: Giải Phẫu Một Hệ Thống Retrieval-Augmented Generation Toàn Diện"
authors: [manhpt]
tags: [rag, embedding, rerank, llm, vietnamese]
date: 2026-07-01
description: "Bài viết phân tích toàn diện kiến trúc hệ thống RAG từ ingestion, chunking, embedding, retrieval, reranking đến generation, evaluation và production. RAG không chỉ là vector search."
---

Khi nhắc đến Retrieval-Augmented Generation (RAG), đa số developer nghĩ ngay đến: "À, embed document thành vector, nhét vào vector DB, query tìm top-k, dúi vào prompt cho LLM sinh câu trả lời." Đúng — nhưng đó mới chỉ là chương 1.

Một hệ thống RAG production-grade phức tạp hơn thế rất nhiều. Bài viết này sẽ giải phẫu từng thành phần trong pipeline RAG hiện đại, từ lúc dữ liệu thô bước vào hệ thống cho đến khi câu trả lời đến tay người dùng — và cả những gì diễn ra sau đó.

<!-- truncate -->

## 1. Data Ingestion & Preprocessing — "Garbage In, Garbage Out"

Khâu đầu tiên và thường bị đánh giá thấp nhất: đưa dữ liệu vào hệ thống.

### 1.1. Parsing

Trước khi làm gì với document, bạn phải đọc được nó. Một PDF research paper không giống một file Markdown. Một bảng Excel không giống một trang Confluence. Mỗi định dạng cần parser riêng:

- **PDF**: PyMuPDF, Unstructured.io, LlamaParse — xử lý layout phức tạp, table, hình ảnh
- **HTML/Markdown**: Tách noise (header, footer, nav), giữ lại content chính
- **Code**: AST-based parsing để hiểu cấu trúc code, không cắt ngang function
- **CSV/Excel**: Cần giữ semantic của row/column khi chunk

Công đoạn này quyết định chất lượng toàn bộ pipeline. Parser tệ → chunk tệ → retrieval tệ → answer tệ.

### 1.2. Data Cleaning

Sau parsing, cần làm sạch:
- Loại bỏ header/footer lặp lại, watermark, page number
- Chuẩn hóa encoding, Unicode
- Xử lý special characters, emoji
- Loại bỏ nội dung trùng lặp (deduplication)

### 1.3. Metadata Extraction

Mỗi chunk nên đi kèm metadata để hỗ trợ filtering và retrieval:
- Tiêu đề document, tác giả, ngày tạo
- Section/parent heading
- Page number
- Document type (policy, research paper, incident report...)
- Access control tags

Metadata cho phép hybrid retrieval: lọc theo thời gian, theo nguồn, theo department trước khi chạy vector search.

---

## 2. Chunking — Nghệ Thuật Cắt Nhỏ Mà Không Làm Mất Ngữ Nghĩa

Chunking là bước tạo ra đơn vị retrieval cơ bản. Không có một chiến lược nào "best" cho mọi use case — đây là bài toán trade-off giữa granularity và context.

### 2.1. Fixed-Size Chunking

Cắt document thành các đoạn cố định N tokens/characters, có overlap.

- **Ưu**: Đơn giản, dự đoán được, phù hợp document đồng nhất
- **Nhược**: Có thể cắt giữa câu, giữa đoạn logic

```python
# Ví dụ với LangChain
from langchain.text_splitter import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    separators=["\n\n", "\n", ". ", " ", ""]
)
```

### 2.2. Semantic Chunking

Dùng embedding để phát hiện ranh giới tự nhiên trong văn bản. Khi similarity giữa các câu liên tiếp giảm đột ngột, đó là điểm cắt.

- **Ưu**: Giữ được coherence ngữ nghĩa
- **Nhược**: Tốn compute hơn, chunk size không đồng đều

### 2.3. Sentence-Based / Paragraph-Based

Tôn trọng cấu trúc tự nhiên: mỗi chunk là một paragraph hoặc N sentences. Phù hợp với văn bản có cấu trúc rõ ràng.

### 2.4. Agentic / LLM-Based Chunking

Dùng LLM để "đọc" document và tự quyết định chunk boundary. Đắt nhất, chậm nhất — nhưng chất lượng cao nhất, hiểu được ngữ cảnh toàn document.

### 2.5. Small-to-Big / Parent-Child Retrieval

Kết hợp nhiều level: lưu chunk nhỏ để retrieval (tăng precision), nhưng trả về chunk lớn hoặc cả section gốc cho LLM (giữ context). Phổ biến trong production RAG.

```
Retrieval: chunk nhỏ (256 tokens) → precision cao
Generation: trả về parent chunk (1024 tokens) hoặc cả document section
```

---

## 3. Embedding & Vector Storage — Trái Tim Nhưng Không Phải Tất Cả

Đây là phần "vector" mà ai cũng nghĩ đến khi nói RAG.

### 3.1. Embedding Models

Không phải embedding model nào cũng như nhau. Cần chọn model phù hợp:

| Model | Dimensions | Max Tokens | Đặc điểm |
|-------|-----------|------------|----------|
| OpenAI text-embedding-3-small | 512/1536 | 8191 | Cân bằng cost/performance |
| OpenAI text-embedding-3-large | 256/1024/3072 | 8191 | Chất lượng cao, cho phép giảm dim |
| Cohere Embed v3 | 1024 | 512 | Phân loại input type (search_document, search_query) |
| BGE-M3 (BAAI) | 1024 | 8192 | Multilingual, hỗ trợ dense + sparse |
| Jina embeddings v3 | 1024 | 8192 | Late chunking, task-specific LoRA |

Key insight: **cùng một model, cách embed khác nhau cho query và document**. Nhiều model cho phép phân biệt `input_type="search_query"` vs `"search_document"`.

### 3.2. Vector Database

Lựa chọn vector DB ảnh hưởng đến scalability, latency, và cost:

- **Pinecone**: Managed, đơn giản, pricing theo pod
- **Weaviate / Qdrant**: Open-source, self-hosted hoặc cloud
- **Milvus**: Hiệu năng cao, distributed, phù hợp scale lớn
- **pgvector**: Postgres extension — tiện khi đã dùng Postgres
- **Chroma**: Nhẹ, local-first, phù hợp prototyping

### 3.3. Indexing Strategy

Không chỉ `INSERT INTO vector_db`. Cần chọn:
- **ANN index**: HNSW (nhanh, tốn RAM), IVF (tiết kiệm hơn), DiskANN (cho dataset lớn)
- **Filtering**: Pre-filtering (lọc metadata trước → chậm hơn) vs post-filtering (tìm top-k trước, lọc sau → mất recall)
- **Multi-tenancy**: Partition theo user, namespace, hoặc metadata filter

---

## 4. Retrieval — Xa Hơn Cả Dense Vector Search

Đây là nơi RAG thực sự thể hiện sự đa dạng vượt xa "vector search".

### 4.1. Dense Retrieval (Vector Similarity)

Truy vấn bằng embedding similarity — cosine, dot product, Euclidean. Là backbone của RAG, nhưng không đủ một mình.

### 4.2. Sparse Retrieval (Keyword / BM25)

Vector embedding nổi tiếng kém với:
- Từ viết tắt, mã code, mã sản phẩm (`SKU-12345`)
- Tên riêng, thuật ngữ domain-specific hiếm gặp
- Exact match queries

BM25 (Best Match 25) — thuật toán TF-IDF cải tiến — vẫn là gold standard cho keyword search, đặc biệt khi kết hợp với dense retrieval.

### 4.3. Hybrid Search

Kết hợp dense + sparse search → fuse scores (Reciprocal Rank Fusion, linear combination, weighted sum).

```
hybrid_score = α × dense_score + β × sparse_score
```

Hầu hết RAG production-grade đều dùng hybrid search. Một số vector DB (Weaviate, Pinecone, Elasticsearch) hỗ trợ sẵn.

### 4.4. Multi-Vector / ColBERT

Thay vì 1 vector cho cả chunk, ColBERT lưu 1 vector cho mỗi token. Tại query time, so khớp từng token query với từng token document (MaxSim). Chi tiết hơn → precision cao hơn, đặc biệt với code search hoặc legal document.

### 4.5. GraphRAG — Khi Dữ Liệu Có Cấu Trúc Quan Hệ

Vector search không hiểu được mối quan hệ giữa các thực thể. Ví dụ: "Công ty nào cung cấp linh kiện cho Apple trong năm 2023 và bị ảnh hưởng bởi lệnh cấm xuất khẩu của Trung Quốc?"

Câu hỏi này cần multi-hop reasoning — truy xuất từ A → B → C. GraphRAG xây dựng knowledge graph từ document (entity + relation extraction bằng LLM), sau đó dùng graph traversal để trả lời truy vấn phức tạp.

Microsoft GraphRAG, Neo4j + LangChain, LightRAG là các implementation phổ biến.

**Trade-off**: Chi phí build graph ban đầu cao, cần refresh định kỳ khi dữ liệu thay đổi.

### 4.6. Agentic RAG

Không còn là pipeline tuyến tính: `query → embed → search → trả về`. Thay vào đó, một AI agent tự quyết định:
1. Cần search không? Hay đã có đủ context?
2. Search ở vector DB, SQL DB, hay gọi API bên ngoài?
3. Kết quả đã đủ tốt chưa? Cần refine query không?
4. Cần web search để bổ sung thông tin thời gian thực?

Agentic RAG biến RAG từ retrieval tool thành reasoning system. Các framework: LangGraph, CrewAI, AutoGen.

### 4.7. Self-Reflective RAG (Self-RAG, CRAG)

Hệ thống **tự đánh giá** chất lượng retrieval trước khi gửi cho generator:
- **CRAG**: Dùng lightweight evaluator chấm điểm relevance của retrieved chunks. Nếu điểm thấp → re-retrieve hoặc web search.
- **Self-RAG**: Finetune model với "reflection tokens" để tự quyết định cần retrieve gì và đánh giá output của chính mình.

---

## 5. Reranking — Lọc Tinh Trước Khi Đưa Vào Prompt

Retrieval trả về top-k (thường k=20-50). Không phải chunk rank 1 luôn là tốt nhất. Reranker là bước **tinh chỉnh ranking** trước khi chọn top-n đưa vào LLM.

### 5.1. Cross-Encoder Reranking

Mô hình cross-encoder nhận cả (query, chunk) làm input và trả về relevance score. Chính xác hơn nhiều so với cosine similarity, vì nó "đọc" cả hai cùng lúc thay vì so sánh hai vector độc lập.

```
Top-50 từ vector search → Reranker chọn Top-5 → Đưa vào prompt
```

Các model phổ biến:
- **Cohere Rerank** (v3): Managed, chất lượng cao
- **BGE Reranker v2** (BAAI): Open-source, cross-encoder
- **Jina Reranker**: Hỗ trợ multilingual
- **ColBERT**: Late interaction reranking

### 5.2. Diversity / MMR Reranking

Đôi khi top-k đều là các chunk gần giống nhau (cùng một section). Maximal Marginal Relevance (MMR) chọn chunk vừa relevant vừa diverse để tăng coverage cho LLM.

---

## 6. Generation — Prompt Engineering Cho RAG

Có context tốt rồi, nhưng cách bạn "dúi" context đó vào LLM cũng quan trọng không kém.

### 6.1. Prompt Template

```markdown
Bạn là trợ lý trả lời câu hỏi dựa trên tài liệu được cung cấp.

## Quy tắc:
1. Chỉ dùng thông tin trong ngữ cảnh bên dưới
2. Nếu ngữ cảnh không đủ, nói "Tôi không có đủ thông tin để trả lời"
3. Trích dẫn nguồn cụ thể (số tham chiếu)

## Ngữ cảnh:
[1] {chunk_1}
[2] {chunk_2}
...

## Câu hỏi:
{query}
```

### 6.2. Citation / Grounding

Citation không chỉ để tăng trust — nó còn là cơ chế phát hiện hallucination. Nếu LLM claim một fact mà không cite được chunk nào → khả năng cao là hallucination.

### 6.3. Context Window Management

Đừng nhồi nhét mọi thứ vào prompt:
- Context stuffing → "lost in the middle" (LLM tập trung đầu/cuối, bỏ qua giữa)
- Cost tỉ lệ thuận với token count (cả input lẫn output)
- Cắt ngắn chunk thông minh: extract-only relevant sentences, không đưa cả chunk dài

### 6.4. Streaming & Latency

Người dùng không chờ nổi 10 giây. Streaming response + streaming token-level citation giúp UX mượt hơn.

---

## 7. Evaluation — Làm Sao Biết RAG Đang Chạy Tốt?

Không evaluate được thì không improve được. Đây là phần bị bỏ qua nhiều nhất.

### 7.1. RAG Evaluation Metrics

Bộ metric chuẩn từ RAGAS (RAG Assessment):

| Metric | Ý nghĩa | Cách đo |
|--------|---------|---------|
| **Faithfulness** | Câu trả lời có căn cứ vào context không? | LLM kiểm tra từng claim trong answer có được support bởi context |
| **Answer Relevancy** | Câu trả lời có liên quan đến câu hỏi? | LLM sinh câu hỏi giả định từ answer → so sánh với query gốc |
| **Context Precision** | Trong các chunk retrieved, bao nhiêu % liên quan? | Đánh giá ranking: chunk liên quan có rank cao không? |
| **Context Recall** | Các chunk retrieved có cover hết thông tin cần thiết? | So sánh context với ground truth answer |
| **Answer Correctness** | Câu trả lời có đúng thực tế không? | Semantic similarity + factual similarity với ground truth |

### 7.2. Tooling

- **RAGAS**: Open-source, Python library, tích hợp LangChain/LlamaIndex
- **DeepEval**: Unit-test style cho LLM evaluation
- **TruLens**: Tracing + evaluation trong một
- **LangSmith / LangFuse**: Managed tracing + evaluation platform

### 7.3. Synthetic Test Data

Không có ground truth data? Dùng LLM để sinh bộ test: từ document corpus, LLM sinh câu hỏi + câu trả lời mẫu. Đây là cách phổ biến để bootstrapping evaluation pipeline.

---

## 8. Production & Observability — Đưa RAG Lên Production Không Dễ

Prototype RAG mất 1 ngày. Production RAG mất 3 tháng.

### 8.1. Guardrails

Hai lớp guardrails:
- **Input guardrails**: Phát hiện prompt injection, toxic content, PII leakage
- **Output guardrails**: Kiểm tra hallucination (faithfulness < threshold → từ chối trả lời), toxicity, factual accuracy

NeMo Guardrails, Guardrails AI, hoặc custom validation layer.

### 8.2. Observability

Cần trace được toàn bộ pipeline:

```
User Query
  → Query Rewriting
    → Retrieval (which chunks? scores? latency?)
      → Reranking (before/after scores?)
        → Generation (prompt tokens? output tokens? model?)
          → Evaluation (faithfulness score?)
```

Platform: **LangFuse** (open-source, self-hosted), **LangSmith**, **Phoenix (Arize)**, **Weights & Biases**.

### 8.3. Monitoring & Alerts

Các metric cần theo dõi liên tục:
- **Retrieval quality**: Trung bình relevance score, % query có result
- **Generation quality**: Trung bình faithfulness score, hallucination rate
- **Latency**: P50, P95, P99 cho từng stage
- **Cost**: Token usage / query, embedding cost / document
- **Data drift**: Document distribution thay đổi theo thời gian

### 8.4. Feedback Loop

Production RAG cần cơ chế thu thập phản hồi:
- Explicit: Thumbs up/down từ user
- Implicit: User có copy-paste answer không? Có hỏi lại không?
- Dùng feedback để tạo training data cho evaluation và fine-tuning

---

## 9. Tổng Kết — RAG Là Một Hệ Sinh Thái

Xây dựng RAG không phải là chọn một model embedding và một vector DB. Đó là thiết kế cả một hệ thống phức tạp với nhiều thành phần tương tác:

```
Data Pipeline   →  Chunking  →  Embedding  →  Storage
                                                ↓
User Query  →  Rewriting  →  Retrieval  →  Reranking
                                              ↓
Feedback  ←  Evaluation  ←  Generation  ←  Prompt
                                              ↓
                        Monitoring & Observability
```

Vector search là một mắt xích quan trọng, nhưng chỉ là **một** mắt xích. Một hệ thống RAG thực sự tốt nằm ở cách tất cả các thành phần phối hợp với nhau — từ chunking strategy đến reranking, từ evaluation đến observability.

Bỏ qua bất kỳ khâu nào cũng giống như xây nhà mà không có móng: prototype có thể đẹp, nhưng production sẽ sập.
