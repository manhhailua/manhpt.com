---
title: "Domain-Aware RAG: Khi Retrieval-Augmented Generation Rời Phòng Lab Bước Vào Thực Tiễn"
authors: [manhpt]
tags: [rag, llm, ai-agent, multi-agent, benchmark, technical, vietnamese]
date: 2026-05-30
description: "Khảo sát 16 paper về domain-aware RAG trên 8 lĩnh vực: từ tài chính, y tế, pháp luật đến nông nghiệp, thiên văn và an ninh mạng. Tổng hợp xu hướng, insight và bài học cho doanh nghiệp."
---

# Domain-Aware RAG: Khi Retrieval-Augmented Generation Rời Phòng Lab Bước Vào Thực Tiễn

**RAG (Retrieval-Augmented Generation) đã đi được một chặng đường dài từ những ngày đầu "nhét context vào prompt".** Năm 2025-2026 chứng kiến sự bùng nổ của các hệ thống RAG chuyên biệt hóa theo từng domain — nơi retrieval không còn là bài toán "tìm document giống nhất", mà là bài toán "tìm thông tin hữu ích nhất cho một ngữ cảnh chuyên môn cụ thể".

Bài viết này khảo sát 22 paper mới nhất về domain-aware RAG trên 8 lĩnh vực, rút ra những insight chung và bài học thực tiễn cho ai đang xây dựng hệ thống RAG trong doanh nghiệp.

<!-- truncate -->

## Bức Tranh Tổng Quan

| Domain | Số paper | Bài toán cốt lõi | Hướng giải quyết chính |
|--------|----------|-----------------|----------------------|
| 💰 Tài chính | 3 | Similarity-utility gap, agentic retrieval | Agentic RAG + hybrid retrieval + LLM-as-a-Judge |
| 🏥 Y tế | 3 | Cross-system asymmetry, certification, data privacy | Query-conditioned alignment, claim-level cert, scoping review |
| ⚖️ Pháp luật | 3 | Hallucination, multi-turn, clause integrity | Claim-level benchmark, LegRAG dual-path, LexRAG multi-turn |
| 🌾 Nông nghiệp | 3 | English-centric, weak grounding, time-awareness | Domain-adapted RAG, multimodal, TARAG time-aware |
| 🎓 Giáo dục | 2 | Pedagogical alignment | Hybrid ICL+RAG, dialogical learning |
| 🔭 Thiên văn | 3 | Expert-level reasoning | Curated benchmark, PageRank reranking |
| 🔒 An ninh mạng | 1 | Detection→response gap | DL IDS + RAG response pipeline |
| 🏭 Kỹ thuật/SX | 5 | Multi-agent, multimodal, structured docs | ManuRAG multimodal, FAB-Bench, layout-aware chunking |

---

## 💰 Domain 1: Tài Chính

### Paper 1: Two-Phase Retrieval cho Financial Documents

**Vấn đề:** Trong tài chính, document "gần về mặt ngữ nghĩa" không đồng nghĩa với "hữu ích cho phân tích". Một báo cáo tài chính có thể chứa đoạn văn rất giống query về semantic, nhưng hoàn toàn không có giá trị phân tích — đây gọi là **similarity-utility gap**.

**Giải pháp:** Two-phase retrieval pipeline:
1. **Phase 1**: Retrieval truyền thống (semantic search) lấy candidate set rộng
2. **Phase 2**: LLM-as-a-Judge đánh giá utility score cho từng candidate, chỉ giữ lại những document thực sự có giá trị phân tích

**Tại sao đáng chú ý:** Đây là pattern xuất hiện xuyên suốt nhiều domain — retrieval không nên kết thúc ở similarity. Cần một bước đánh giá "utility" riêng.

### Paper 2: Agentic RAG cho Fintech (arXiv 2510.25518)

**Vấn đề:** Fintech domain có ontology chuyên biệt, terminology dày đặc, và vô số acronyms khiến retrieval truyền thống thất bại.

**Giải pháp:** Kiến trúc agentic RAG với modular pipeline:
- **Intelligent query reformulation**: Tự động viết lại query để cải thiện recall
- **Iterative sub-query decomposition**: Chia query phức tạp thành sub-queries, guided by keyphrase extraction
- **Contextual acronym resolution**: Giải nghĩa acronyms dựa trên ngữ cảnh fintech cụ thể
- **Cross-encoder re-ranking**: Rerank context để tăng precision

**Kết quả:** Trên dataset 85 QA pairs từ enterprise fintech knowledge base, agentic RAG outperforms baseline về retrieval precision và relevance, nhưng tăng latency.

**Bài học:** Agentic architecture cải thiện retrieval quality trong domain phức tạp, nhưng cost-latency trade-off là thực tế. Với fintech — nơi accuracy > speed — đánh đổi này xứng đáng.

### Paper 3: RAGPerf — Benchmark Financial RAG

RAGPerf cung cấp benchmark đầu tiên cho RAG trong tài chính, tập trung vào:
- Đánh giá không chỉ accuracy mà còn **analytical depth** của câu trả lời
- So sánh các chiến lược chunking, embedding model, và reranking khác nhau
- Kết luận: hybrid retrieval (dense + sparse) + LLM reranking cho kết quả tốt nhất

---

## 🏥 Domain 2: Y Tế

### Paper 3: QCEA — Query-Conditioned Evidence Alignment

**Vấn đề:** RAG trong y tế đối mặt với **cross-system asymmetry** — cùng một triệu chứng có thể được mô tả khác nhau trong西医 (Tây y) và中医 (Đông y). Retrieval system cần hiểu được sự tương đương cross-system này.

**Giải pháp:** QCEA framework:
- Query-conditioned alignment: Với mỗi query, hệ thống xác định cần align sang hệ thống y tế nào
- Evidence fusion: Kết hợp evidence từ nhiều nguồn, có trọng số dựa trên độ tin cậy của từng nguồn

### Paper 4: Claim-Selective Certification

**Vấn đề:** Trong y tế, hallucinations không thể chấp nhận được. Nhưng certification full-response tốn kém và chậm.

**Giải pháp:** Thay vì certify toàn bộ response, hệ thống certify từng **claim** riêng lẻ — mỗi factual statement được kiểm tra độc lập với nguồn. Response cuối chỉ giữ lại các claim được certified.

**Bài học:** Pattern "claim-level verification" có thể áp dụng cho bất kỳ domain high-stakes nào — pháp luật, tài chính, bảo hiểm.

### Bonus: RAG in Medicine — Scoping Review (arXiv 2511.05901)

Một scoping review toàn diện về RAG trong y tế, phân tích hàng chục paper. Các phát hiện chính:
- Nghiên cứu chủ yếu dùng **public data**, rất ít ứng dụng trên private clinical data
- Retrieval chủ yếu dùng **English-centric embedding models**, ít tận dụng medical-specific LLMs
- Evaluation: automated metrics cho generation quality + human evaluation cho accuracy, completeness, relevance
- **Gap lớn**: Thiếu deployment trên real clinical workflows với private patient data

---

## ⚖️ Domain 3: Pháp Luật

### Paper 5: ClaimRAG-LAW — Claim-Level Legal Benchmark

**Vấn đề:** Hallucination trong legal RAG đặc biệt nguy hiểm vì người dùng (luật sư, thẩm phán) cần trích dẫn chính xác điều luật, án lệ.

**Giải pháp:** ClaimRAG-LAW:
- Benchmark ở cấp độ **claim** (không phải document hay sentence)
- Hỗ trợ đa ngôn ngữ (cross-jurisdiction)
- Mỗi claim được verify với legal database trước khi đưa vào response

### Paper 6: Legal-DC + LegRAG — Chinese Legal RAG (arXiv 2603.11772)

**Vấn đề:** RAG cho legal documents tiếng Trung thiếu benchmark chuyên biệt, và hệ thống RAG hiện tại không accommodate được structured nature của legal provisions.

**Giải pháp:**
- **Legal-DC benchmark**: 480 legal documents + 2,475 QA pairs, mỗi pair được annotate với clause-level references
- **LegRAG framework**: Legal adaptive indexing (clause-boundary segmentation) + dual-path self-reflection mechanism
- Automated LLM evaluation cho high-reliability legal retrieval

**Kết quả:** LegRAG outperforms SOTA methods 1.3% đến 5.6% trên các metrics chính.

### Paper 7: LexRAG — Multi-Turn Legal Consultation Benchmark (arXiv 2502.20640)

**Vấn đề:** Không có benchmark nào đánh giá RAG trong **multi-turn legal consultation** — nơi context tích lũy qua nhiều vòng hội thoại.

**Giải pháp:**
- **LexRAG benchmark**: 1,013 multi-turn dialogue samples, 17,228 candidate legal articles
- Mỗi sample được legal experts annotate, gồm 5 rounds progressive questioning
- **LexiT toolkit**: Comprehensive RAG implementation tailored cho legal domain
- **LLM-as-a-Judge evaluation pipeline**

**Ý nghĩa:** Đây là benchmark đầu tiên cho multi-turn legal RAG — mở ra hướng nghiên cứu về conversational legal AI.

---

## 🌾 Domain 4: Nông Nghiệp

### Paper 8: AgroLLM — RAG Chatbot cho Nông Nghiệp (arXiv 2503.04788)

**Giải pháp:** AI-powered chatbot dùng RAG framework với FAISS vector database cho agricultural knowledge retrieval. So sánh 3 model: Gemini 1.5 Flash, ChatGPT-4o Mini, Mistral-7B.

**Kết quả:** ChatGPT-4o Mini + RAG đạt **93% accuracy** — cao nhất. Hệ thống có continuous feedback mechanism để cải thiện response quality.

**Bài học:** Không cần model lớn nhất. Model nhỏ + curated agricultural database + feedback loop cho kết quả rất cạnh tranh.

### Paper 9: AgriHubi — RAG cho Nông Nghiệp Low-Resource Language

**Vấn đề:** LLM trong nông nghiệp bị hạn chế bởi:
- Training data English-centric
- Thiếu real-world evaluation
- Vấn đề nghiêm trọng hơn cho low-resource languages (tiếng Phần Lan, tiếng Việt, v.v.)

**Giải pháp:** AgriHubi:
- Tích hợp tài liệu nông nghiệp tiếng Phần Lan với PORO family models
- Explicit source grounding + user feedback loop
- 8 iterations phát triển, 2 user studies

**Kết quả:** Cải thiện rõ rệt về answer completeness, linguistic accuracy, perceived reliability. Có trade-off giữa response quality và latency khi deploy larger models.

### Paper 10: Survey — Domain-Specific vs General Purpose LLMs trong Nông Nghiệp

Survey này tổng hợp các hệ thống RAG nông nghiệp hiện có:

| Hệ thống | Đặc điểm nổi bật |
|----------|-----------------|
| **AgroLLM** | Tích hợp structured agricultural knowledge, giảm unsupported outputs |
| **AgroGPT** | Multimodal — image-based instruction tuning cho crop disease detection |
| **AgriGPT** | Tri-RAG framework với data engine và instruction dataset đa tác vụ |
| **Yunnan Arabica Coffee** | RAG + reranking cho coffee cultivation, retrieval-based grounding |

**Insight:** Domain-specific models outperform general-purpose models trong agricultural terminology, crop-related reasoning, và context-sensitive recommendations.

---

## 🎓 Domain 5: Giáo Dục

### Paper 11: Hybrid ICL + RAG cho Automatic Question Generation

**Vấn đề:** ICL (In-Context Learning) bị giới hạn bởi quality/coverage của few-shot examples. RAG độc lập có thể retrieve irrelevant documents.

**Giải pháp:** Kết hợp cả hai:
1. Retrieval relevant external documents (RAG)
2. Generate questions dùng few-shot learning (ICL) guided by retrieved context

**Kết quả:** Questions không chỉ contextually relevant mà còn **pedagogically meaningful** — nhắm đến nhiều cognitive levels khác nhau (nhớ, hiểu, áp dụng, phân tích).

### Paper 12: Dialogical Learning Support trong E-Learning

**Vấn đề:** RAG trong giáo dục chủ yếu tập trung vào answer accuracy, ít chú ý đến **pedagogical orchestration** — cách duy trì dialogue flow có tính sư phạm.

**Giải pháp:** Kiến trúc dialogically oriented:
- **Bounded context-aware dialogue**: Giữ lại lịch sử tương tác gần đây, hỗ trợ incremental knowledge construction
- **Two-stage retrieval pipeline**: Semantic similarity + lexical matching
- **Model-agnostic**: Cho phép tích hợp LLM khác nhau
- **EU AI Act compliant**: Transparency và controlled educational use

Đánh giá trên tiếng Bulgaria (low-resource language) — cho thấy tính applicability cho các ngôn ngữ không phải tiếng Anh.

---

## 🔭 Domain 6: Thiên Văn Học

### Paper 13: CosmoPaperQA — Benchmark RAG cho Astrophysics (ICML 2025)

**Vấn đề:** Thiếu benchmark standardized cho RAG agents trong astronomy. Các benchmark hiện có (AstroMLab, Astro-QA) dùng multiple-choice/synthetic questions — không capture complex open-ended reasoning của real research.

**Giải pháp:** CosmoPaperQA:
- 105 expert-curated QA pairs từ 5 highly-cited cosmological papers
- SciRag: Modular framework benchmark 9 RAG implementations

**Kết quả benchmark:**

| System | Accuracy | Ghi chú |
|--------|----------|---------|
| OpenAI Assistant | **91.4%** | Best overall |
| VertexAI Assistant | 86.7% | Best cost-efficiency |
| HybridOAIGem | 85.7% | Competitive |
| PaperQA2 | 81.9% | Solid academic tool |
| Perplexity (web search) | 17.1% | Web search không đủ |
| Gemini (no RAG) | 16.2% | Baseline |

**Insight đắt giá:** Unfiltered web search và non-RAG integration hoàn toàn không đủ cho expert-level scientific inquiry. Curated corpus là essential.

### Paper 14: AstroRAG — PageRank-Based RAG (IEEE CAI 2026)

**Vấn đề:** Cần RAG framework lightweight, fully local cho astronomy — privacy-sensitive, offline operation.

**Giải pháp:** AstroRAG:
- **Token-aware chunking** + Elasticsearch transient index (per-instance)
- **Two-stage retrieval**: MMR (Maximal Marginal Relevance) → **PageRank re-ranking** trên similarity graph
- **HyDE support**: Optional Hypothetical Document Embedding
- **Instance isolation**: Ingest → index → answer → erase (không contamination)

**Kết quả:** Mistral-7B + AstroRAG đạt **79.49% accuracy** (từ 21.74% baseline). Đặc biệt mạnh trên Hard questions (83.59%).

**Bài học:** PageRank trên similarity graph là một kỹ thuật reranking đáng thử — hoàn toàn local, không cần LLM reranker.

### Paper 15: RAG trong Physics and Astronomy Instruction

Hướng tiếp cận local AI với RAG cho Open Educational Materials Generation trong physics và astronomy — mở rộng ứng dụng RAG từ research sang teaching.

---

## 🔒 Domain 7: An Ninh Mạng

### Paper 16: RAG Framework cho Network Intrusion Mitigation

**Vấn đề:** IDS (Intrusion Detection Systems) machine-learning-based đạt accuracy cao trong classify attacks, nhưng không trả lời câu hỏi quan trọng nhất: **"Tôi nên làm gì tiếp theo?"**

**Giải pháp:** Two-stage framework:
1. **Deep Learning IDS**: Phát hiện và phân loại network attacks
2. **RAG Response Generator**: Sinh phản ứng cụ thể dựa trên knowledge base bảo mật

**Ý nghĩa:** Đây là pattern "detection → retrieval → action" — RAG không chỉ trả lời câu hỏi, mà còn **đề xuất hành động** dựa trên knowledge base đã được xác thực.

---

## 🏭 Domain 8: Kỹ Thuật & Sản Xuất

### Paper 17: ManuRAG — Multi-Modal RAG cho Manufacturing QA (arXiv 2601.15434)

**Vấn đề:** Conventional RAG không xử lý được multi-modal data trong manufacturing — text, images, formulas, tables.

**Giải pháp:** ManuRAG — multi-modal RAG framework với specialized techniques cho:
- Multi-modal retrieval và generation
- Cải thiện answer accuracy, reliability, và interpretability

**Kết quả:** Đánh giá trên 3 datasets (1,515 QA pairs) — mathematical, multiple-choice, review-based. ManuRAG consistently outperforms existing methods. Framework có thể adapt sang law, healthcare, finance.

**Bài học:** Multi-modal không còn là "nice to have" trong manufacturing RAG — text-only retrieval bỏ lỡ phần lớn domain knowledge nằm trong bảng biểu, công thức, và hình ảnh kỹ thuật.

### Paper 18: FAB-Bench — RAG Benchmark cho Semiconductor Manufacturing (May 2026)

**Vấn đề:** Đánh giá RAG trong vertical domains như semiconductor manufacturing cực kỳ khó — domain complexity cao, diverse context scales, phụ thuộc nặng vào expert assessment (tốn kém, không nhất quán, không scalable).

**Giải pháp:** FAB-Bench — adaptive RAG benchmarking framework:
- Đánh giá RAG performance trong semiconductor manufacturing
- Adaptive evaluation thích nghi với domain complexity
- Giảm phụ thuộc vào manual expert assessment

### Paper 19: EngiAI — Multi-Agent Framework cho Engineering Design

**Vấn đề:** Thiếu benchmark cho multi-agent systems kết hợp simulation, retrieval, và manufacturing preparation.

**Giải pháp:** EngiAI benchmark với 3 evaluation dimensions:
1. Design effectiveness
2. Retrieval quality và resource usage
3. Integration capability với manufacturing workflows

### Paper 20: RAG cho Manufacturing Quality Control

**Bài toán:** Operators cần nhanh chóng tìm procedural specifications, tolerance standards, corrective action procedures trong manufacturing environment.

**Cách đánh giá:** Dual-measurement — kết hợp retrieval metrics (Context Precision, Recall) với **operational metrics** (time-to-correct-answer, error rate). Đây là hướng đánh giá thực tế hơn so với chỉ dùng academic metrics.

### Paper 21: RAG cho Automotive Technical Documentation

**Vấn đề:** PDF ingestion cho automotive technical manuals — complex layouts:
- Multi-column tables
- Embedded diagrams
- Cross-referenced procedures

**Giải pháp:** SemanticSplitterNodeParser thay vì fixed-window chunking. **OCR quality và layout-aware chunking là primary determinants của downstream retrieval performance.**

---

## 🔑 8 Insight Chung Xuyên Suốt 8 Domain

### 1. Semantic Similarity ≠ Domain Utility

Đây là insight quan trọng nhất. Trong tài chính, một document "gần về semantic" với query có thể hoàn toàn vô dụng cho phân tích. Trong y tế, cross-system correspondence (Tây y ↔ Đông y) đòi hỏi alignment vượt xa similarity. Trong pháp luật, cần accuracy ở claim level, không phải document level.

**Hệ quả:** Mọi hệ thống RAG domain-aware đều cần một **utility evaluation layer** sau bước retrieval — có thể là LLM-as-a-Judge, domain-specific classifier, hoặc hybrid approach.

### 2. Multimodal Là Xu Hướng Không Thể Bỏ Qua

| Domain | Loại multimodal |
|--------|----------------|
| Nông nghiệp (AgroGPT) | Hình ảnh cây trồng → disease detection |
| Kỹ thuật (Automotive) | PDF layouts phức tạp, diagrams, bảng biểu |
| Thiên văn | Tables + figures + equations trong paper |

RAG không còn chỉ là text-in, text-out. Hệ thống cần xử lý được hình ảnh, bảng biểu, và structured data.

### 3. Low-Resource Language Là Bài Toán Thực Tế

AgriHubi (tiếng Phần Lan), QCEA (TCM-WM), Dialogical Learning (tiếng Bulgaria) — tất cả đều cho thấy RAG domain-aware đặc biệt có giá trị cho các ngôn ngữ không phải tiếng Anh, nơi training data khan hiếm và domain knowledge chỉ tồn tại trong tài liệu nội bộ.

### 4. On-Premise / Local Deployment Ngày Càng Phổ Biến

Tài chính (OCBC on-premise), AstroRAG (fully local), Manufacturing (internal docs) — data governance và privacy đang đẩy RAG về hướng local deployment. Đây là cơ hội cho các giải pháp lightweight như Mistral-7B + custom retrieval pipeline.

### 5. LLM-as-a-Judge Trở Thành Pattern Chuẩn

Xuất hiện trong tài chính (utility scoring), thiên văn (calibrated AI judge), y tế (claim certification), giáo dục (pedagogical quality). Pattern: dùng LLM mạnh để đánh giá output của LLM yếu hơn hoặc của retrieval system.

**Lưu ý:** LLM-as-a-Judge không miễn phí — mỗi lần judge là một lần burn token. Cần cân nhắc cost-quality trade-off.

### 6. Benchmark Domain-Specific Đang Thiếu Trầm Trọng

Hầu hết domain đều thiếu standardized benchmark:
- CosmoPaperQA (thiên văn) và ClaimRAG-LAW (pháp luật) là ngoại lệ hiếm hoi
- Các domain còn lại dùng benchmark tự xây dựng, khó so sánh cross-paper
- Đây vừa là gap, vừa là cơ hội cho research tiếp theo

### 7. RAG Không Chỉ Là Retrieval

RAG đã tiến hóa vượt xa mô hình "retrieve rồi generate":

| Domain | Vai trò mở rộng của RAG |
|--------|------------------------|
| Y tế | Knowledge alignment + Certification |
| Giáo dục | Dialogue management + Pedagogical orchestration |
| An ninh mạng | Detection → Retrieval → Action pipeline |
| Kỹ thuật | Multi-agent coordination + Simulation integration |
| Pháp luật | Multi-turn consultation + Clause-level verification |

### 8. Agentic Architecture Đang Trở Thành Default

Từ tài chính (agentic RAG với sub-query decomposition) đến pháp luật (dual-path self-reflection trong LegRAG), pattern "agentic" đang xuất hiện khắp nơi:

- **Fintech**: Multi-agent pipeline với specialized agents cho query reformulation, acronym resolution, re-ranking
- **Legal (LegRAG)**: Dual-path self-reflection — một path retrieval, một path verify
- **Manufacturing (EngiAI)**: Multi-agent benchmark cho engineering design

**Insight:** RAG không còn là single-pass pipeline. Nó đang trở thành multi-step, multi-agent process — nơi mỗi agent đảm nhận một phần của problem, tương tự cách con người research: tìm → đọc → suy nghĩ → tìm thêm → tổng hợp.

---

## Từ Research Đến Triển Khai: 5 Bài Học Cho Doanh Nghiệp

### 1. Bắt Đầu Với Utility Evaluation — Không Phải Accuracy

Hầu hết team build RAG bắt đầu bằng việc chọn embedding model, chunk size, vector DB. Nhưng insight từ 16 paper cho thấy: **hãy bắt đầu bằng việc định nghĩa "thế nào là document hữu ích" cho domain của bạn.** Một document hoàn toàn relevant về semantic có thể vô dụng — và ngược lại.

### 2. Đừng Bỏ Qua Structured Data

Nhiều domain (tài chính, y tế, kỹ thuật) có lượng lớn structured data (bảng biểu, specs, quy trình). Hybrid retrieval — kết hợp vector search cho text + structured query cho bảng — cho kết quả tốt hơn nhiều so với pure vector search.

### 3. Design Cho Multimodal Ngay Từ Đầu

Nếu domain của bạn có hình ảnh, diagram, hoặc complex document layout — đừng đợi version 2 mới xử lý multimodal. Layout-aware chunking và image understanding nên nằm trong thiết kế ban đầu.

### 4. Cân Nhắc Local Deployment Nếu Có Data Governance

AstroRAG và các hệ thống tài chính on-premise cho thấy: bạn không cần GPU farm để chạy RAG domain-aware hiệu quả. Mistral-7B + custom retrieval pipeline có thể đạt accuracy cạnh tranh, đặc biệt khi domain knowledge được curated kỹ.

### 5. Đo Lường Bằng Operational Metrics, Không Chỉ Academic Metrics

Paper 15 (Manufacturing QC) là ví dụ điển hình: ngoài Context Precision và Recall, hãy đo **time-to-correct-answer** và **error rate trong production**. Một hệ thống RAG có accuracy 95% nhưng mất 30 giây để trả lời có thể vô dụng trong môi trường manufacturing — nơi operator cần câu trả lời trong 5 giây.

---

## Kết Luận

Domain-aware RAG không còn là research curiosity — nó đang được triển khai thực tế trong tài chính, y tế, sản xuất, và giáo dục. 3 xu hướng chính định hình tương lai của lĩnh vực này:

1. **Từ "retrieve document giống nhất" sang "retrieve document hữu ích nhất"** — utility > similarity
2. **Từ text-only sang multimodal** — hình ảnh, bảng biểu, diagram
3. **Từ cloud-only sang hybrid cloud/local** — data governance đang thúc đẩy on-premise RAG

Với doanh nghiệp, câu hỏi không còn là "có nên dùng RAG không", mà là **"RAG của bạn đã được thiết kế cho domain của bạn chưa, hay mới chỉ là generic RAG với document của bạn?"**

---

## Tài Liệu Tham Khảo

1. "Retrieval Augmented Generation (RAG) for Fintech: Agentic Design and Evaluation." arXiv 2510.25518, 2025.
2. "RAGPerf: Benchmarking Financial RAG Systems." 2025-2026.
3. "Two-Phase Retrieval for Financial Documents." 2025.
4. "QCEA: Query-Conditioned Evidence Alignment for Medical RAG." 2025.
5. "Claim-Selective Certification for Medical RAG." 2025.
6. Yang, R. et al. "Retrieval-Augmented Generation in Medicine: A Scoping Review." arXiv 2511.05901, 2025.
7. "ClaimRAG-LAW: Claim-Level Benchmark for Legal RAG." 2025.
8. Lan, Q. et al. "Legal-DC: Benchmarking RAG for Legal Documents." arXiv 2603.11772, 2026.
9. Li, H. et al. "LexRAG: Benchmarking RAG in Multi-Turn Legal Consultation." arXiv 2502.20640, 2025.
10. Ravindran, D.J.S. et al. "AgroLLM: Connecting Farmers through LLMs." arXiv 2503.04788, 2025.
11. Hasan, M.T. "AgriHubi — Domain-Adapted RAG for Finnish Agriculture." arXiv 2602.02208, 2026.
12. Uy, C.A.H. et al. "Domain-Specific vs. General Purpose LLMs in Agriculture." University of Southern Mindanao, 2025.
13. "Hybrid ICL + RAG for Automatic Question Generation in Education." ACM FIRE, 2025.
14. "Dialogical Learning Support in RAG-Based E-Learning." MDPI Information, 2026.
15. Xu, X. et al. "CosmoPaperQA: Evaluating RAG Agents for Astrophysics." ICML 2025.
16. Wang, Z. et al. "AstroRAG — PageRank-Based RAG for Astronomy QA." arXiv 2605.25039, IEEE CAI 2026.
17. Beznosko, D. et al. "RAG in Physics and Astronomy Instruction." ICRC 2025.
18. Islam, M.N.B., Saha, S. "From Detection to Response: DL and RAG for Network Intrusion Mitigation." arXiv 2605.17960, 2026.
19. Li, Y. et al. "ManuRAG: Multi-modal RAG for Manufacturing QA." arXiv 2601.15434, 2026.
20. Qian, J. et al. "FAB-Bench: Adaptive RAG Benchmarking in Semiconductor Manufacturing." arXiv, May 2026.
21. Molinari, G. et al. "EngiAI — Multi-Agent Framework for Engineering Design." arXiv 2605.19743, 2026.
22. "RAG for Manufacturing Quality Control." Politecnico di Torino, 2025.
23. Gan et al. "RAG for Automotive Technical Documentation." 2026.

---

*Bài viết được thực hiện bởi Mạnh Phạm, tổng hợp từ các paper công bố trong giai đoạn 2025-2026. Cập nhật đến 30/05/2026.*
