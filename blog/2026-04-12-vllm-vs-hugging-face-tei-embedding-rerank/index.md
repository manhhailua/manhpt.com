---
title: "vLLM vs Hugging Face TEI cho embedding và rerank: nếu chỉ xét performance thì chọn gì?"
slug: vllm-vs-hugging-face-tei-embedding-rerank
authors: [manhpt]
tags: [embedding, rerank, llm, technical, vietnamese]
date: 2026-04-12
description: "So sánh vLLM và Hugging Face Text Embeddings Inference cho embedding và rerank, với trọng tâm là performance khi workload này là use case chuyên biệt chứ không phải tính năng phụ."
---

Nếu đang dựng một stack RAG hoặc semantic search, câu hỏi thực tế không còn là “có chạy được embedding không”, mà là: **nếu embedding và rerank là workload chuyên biệt, cái nào cho profile performance hợp lý hơn để đưa vào production**. Hai cái tên thường được đưa lên bàn cân là **vLLM** và **Hugging Face Text Embeddings Inference (TEI)**.

Điểm quan trọng là cả hai đều đã hỗ trợ embedding và rerank. Nhưng nếu đọc kỹ docs chính thức, có thể thấy chúng không tối ưu cho cùng một mục tiêu. **TEI tối ưu theo hướng specialized inference cho embedding/rerank, còn vLLM tối ưu theo hướng inference runtime hợp nhất.** Chính khác biệt đó mới quyết định performance thực chiến.

<!-- truncate -->

## Kết luận ngắn trước

Nếu chỉ cần một câu trả lời ngắn, đây là cách tôi đang nhìn vấn đề:

- **Nếu tiêu chí số 1 là performance cho embedding + rerank chuyên biệt, mặc định hãy nghiêng về TEI.**
- Nói thẳng hơn, nếu anh đang tối ưu **latency** và **throughput** cho workload embedding/rerank chuyên biệt, **TEI hiện là lựa chọn nên thử trước vLLM**.
- **Nếu tiêu chí số 1 là hợp nhất runtime và giảm độ phân mảnh hạ tầng, hãy cân nhắc vLLM.**
- Docs hiện tại của vLLM thậm chí còn nói khá thẳng rằng phần pooling models của họ **mới chủ yếu là để tiện dụng**, và **chưa đảm bảo nhanh hơn** việc dùng Hugging Face Transformers hoặc Sentence Transformers trực tiếp.

Chỉ riêng chi tiết đó đã đủ để đặt TEI ở vị trí mặc định khi bài toán của bạn là **serve embedding/rerank càng gọn và càng sát performance càng tốt**.

## Nếu điều bạn quan tâm là performance chuyên biệt

Tôi nghĩ cần nói thẳng một điểm trước khi đi sâu hơn: bài này **không phải** benchmark apples-to-apples trên cùng GPU, cùng batch size, cùng model và cùng traffic profile. Nếu muốn chốt con số tuyệt đối, bạn vẫn phải tự A/B trên hạ tầng của mình.

Nhưng ở level quyết định kiến trúc, docs chính thức hiện tại đã đủ để rút ra một kết luận thực dụng:

- **TEI được thiết kế như một service chuyên cho embedding và rerank**.
- **vLLM mới mở rộng sang embedding/rerank từ một runtime vốn mạnh nhất ở bài toán inference hợp nhất**.

Khi một hệ thống sinh ra để giải bài toán chuyên biệt, còn hệ kia thêm support cho bài toán đó như một capability mở rộng, thì mặc định hợp lý nhất là: **nếu chỉ xét performance chuyên biệt, hãy bắt đầu với TEI**.

Nói cụ thể hơn, nếu anh đang tối ưu theo hai thước đo thực chiến nhất là **latency** và **throughput**, thì positioning hiện tại của docs nghiêng về TEI rõ hơn vLLM. Tôi không coi đây là tuyên bố benchmark tuyệt đối cho mọi model, mọi GPU và mọi batch size. Nhưng ở level quyết định kiến trúc, đây là kết luận đủ mạnh để dùng làm default choice.

## Hai dự án này thực ra đang tối ưu cho hai thứ khác nhau

### TEI tối ưu cho embedding-first serving

Theo docs chính thức của Hugging Face, **Text Embeddings Inference** là toolkit để deploy và serve **text embeddings models** và **sequence classification models**. Họ nhấn mạnh các điểm rất rõ:

- không cần bước graph compilation
- image Docker nhỏ, boot nhanh
- dynamic batching theo token
- tối ưu bằng Flash Attention, Candle và cuBLASLt
- có OpenTelemetry và Prometheus metrics
- hỗ trợ cả embedding lẫn reranker endpoint khá trực tiếp

Nói ngắn gọn, TEI được đóng gói như một **microservice chuyên cho embedding/rerank**.

### vLLM tối ưu cho một inference runtime rộng hơn

Còn với vLLM, embedding và rerank nằm trong nhóm **pooling models**. vLLM support các task như:

- `embed`
- `score`
- `classify`
- `token_embed`

Tức là về mặt capability, vLLM đã không còn chỉ là text generation server nữa.

Nhưng docs của vLLM cũng nói rất rõ một câu khá quan trọng:

> hiện tại pooling models được support chủ yếu vì mục đích tiện dụng, chưa đảm bảo mang lại cải thiện hiệu năng so với dùng Hugging Face Transformers hoặc Sentence Transformers trực tiếp.

Đây là một tín hiệu kỹ thuật đáng chú ý. Nó cho thấy embedding/rerank trong vLLM hiện tại là **một capability hữu ích**, nhưng chưa chắc là **đường tối ưu nhất** nếu đó là workload chính của bạn. Nếu câu hỏi là “tôi đang tối ưu cho embedding/rerank chuyên biệt”, thì đây gần như là câu nhắc thẳng rằng **vLLM chưa tự nhận mình là lựa chọn performance-first cho đúng use case đó**.

## Với embedding, khác biệt lớn nhất là “specialized service” vs “unified runtime”

### TEI cho embedding khá thẳng tay và rõ ý đồ

Quick Tour của TEI gần như nói lên triết lý sản phẩm của họ.

Bạn chọn model, ví dụ `Qwen/Qwen3-Embedding-0.6B`, rồi chạy container:

```bash
model=Qwen/Qwen3-Embedding-0.6B
volume=$PWD/data

docker run --gpus all -p 8080:80 -v $volume:/data --pull always \
  ghcr.io/huggingface/text-embeddings-inference:cuda-1.9 \
  --model-id $model
```

Sau đó gọi luôn:

```bash
curl 127.0.0.1:8080/embed \
  -X POST \
  -d '{"inputs":"What is Deep Learning?"}' \
  -H 'Content-Type: application/json'
```

Hoặc dùng OpenAI-compatible embeddings API:

```bash
curl http://localhost:8080/v1/embeddings \
  -H "Content-Type: application/json" \
  -d '{
    "input": "What is Deep Learning?",
    "model": "text-embeddings-inference",
    "encoding_format": "float"
  }'
```

Cách đóng gói này rất hợp khi bạn muốn một service độc lập chỉ làm một việc: **nhận text và trả embedding**.

Ngoài ra TEI còn có một số chi tiết vận hành khá thực dụng:

- có thể chạy CPU hoặc GPU
- hỗ trợ batching sẵn
- có thể mount volume để tránh tải lại weights mỗi lần khởi động
- có `--pooling` để override cách pooling nếu model cho phép
- có `--auto-truncate`, `--max-batch-tokens`, `--max-concurrent-requests` để chỉnh behavior theo production traffic

### vLLM cho embedding hợp khi bạn đã ở trong hệ vLLM

Bên vLLM, embedding được support qua:

- offline API như `LLM.embed(...)`
- online API như `/v1/embeddings`
- thêm các pooling APIs riêng

Điểm hay của vLLM là nếu bạn đã dùng nó cho generation hoặc OpenAI-compatible serving, thì việc thêm embedding vào cùng mặt bằng vận hành sẽ rất tiện:

- cùng kiểu server
- cùng cách auth/API gateway
- cùng observability pattern
- cùng ecosystem client

Nói cách khác, **vLLM thắng ở sự hợp nhất**, không phải vì embedding là trọng tâm duy nhất của nó. Nếu anh đang hỏi theo hướng performance thuần cho embedding service, đây là một khác biệt rất lớn.

Có một nuance kỹ thuật đáng nói thêm ở đây: **vector do TEI và vLLM sinh ra sẽ không giống nhau hoàn toàn theo kiểu bit-by-bit identical**, ngay cả khi anh dùng cùng một embedding model. Lý do nằm ở chi tiết triển khai như kernel, dtype, batching path, hoặc cách runtime thực hiện pooling và suy luận số học.

Nhưng trong thực tế, với điều kiện **cùng model, cùng preprocessing, cùng pooling contract và cùng normalization expectation**, khác biệt đó thường chỉ là **sai số số học rất nhỏ**. Nghĩa là ở level vận hành, anh hoàn toàn có thể xem chúng là **đủ gần để thay thế nhau** cho đa số use case retrieval thông thường.

Tôi vẫn sẽ giữ một lưu ý nhỏ: nếu anh cần tính tái lập tuyệt đối hoặc đang tối ưu benchmark rất sát biên, tốt nhất nên rebuild lại index bằng đúng engine sẽ dùng ở production. Nhưng nếu câu hỏi là “có thể thay TEI bằng vLLM hoặc ngược lại mà không làm semantic behavior lệch đáng kể không?”, thì trong đa số trường hợp thực tế, câu trả lời là **có**.

## Với rerank, TEI hiện cho cảm giác “native” hơn

### TEI gọi đúng tên use case này

TEI docs mô tả reranker là **cross-encoder** và có endpoint riêng `/rerank`.

Ví dụ họ đưa ra với `BAAI/bge-reranker-large`:

```bash
model=BAAI/bge-reranker-large
volume=$PWD/data

docker run --gpus all -p 8080:80 -v $volume:/data --pull always \
  ghcr.io/huggingface/text-embeddings-inference:cuda-1.9 \
  --model-id $model
```

Sau đó gọi:

```bash
curl 127.0.0.1:8080/rerank \
  -X POST \
  -d '{"query":"What is Deep Learning?", "texts": ["Deep Learning is not...", "Deep learning is..."], "raw_scores": false}' \
  -H 'Content-Type: application/json'
```

Đây là UX rất sạch cho đội nào đang build retrieval pipeline kiểu:

1. ANN lấy top-k candidates bằng embedding
2. reranker chấm lại top-k
3. đưa top-n vào LLM

### vLLM cũng làm được rerank, nhưng triết lý vẫn là pooling/scoring

vLLM support scoring models với ba nhóm `score_type`:

- `cross-encoder`
- `late-interaction`
- `bi-encoder`

Tài liệu scoring của họ còn ghi rõ rằng vLLM xử lý **phần inference** của pipeline RAG, như embedding generation và reranking, còn orchestration ở tầng cao hơn thì nên để framework khác lo.

Điều này hợp lý, nhưng cũng cho thấy một sự khác biệt:

- **TEI** cho cảm giác là một service được đóng khung rất chặt quanh embedding/rerank.
- **vLLM** cho cảm giác là một runtime lớn hơn, nơi embedding/rerank là một nhóm task nằm trong bức tranh rộng hơn.

Nếu bạn cần cross-encoder scoring và đã có cụm vLLM sẵn rồi, vLLM hoàn toàn có thể là lựa chọn hợp lý. Nhưng nếu bạn đang hỏi “cái nào tự nhiên hơn và nhiều khả năng tốt hơn về performance cho rerank chuyên biệt”, tôi vẫn nghiêng khá rõ về **TEI**.

## Điểm quyết định nằm ở fit vận hành, không chỉ ở feature list

Có một sai lầm phổ biến khi so sánh hai hệ thống serving: chỉ nhìn xem **cả hai có checkbox tính năng giống nhau hay không**.

Ví dụ ở đây, đúng là cả hai đều đã support:

- embedding
- rerank/scoring
- batching
- API serving
- một mức độ OpenAI compatibility nào đó

Nhưng production không sống bằng checkbox. Production sống bằng:

- boot time
- memory footprint
- latency profile
- mức độ dễ quan sát
- cách scale theo loại workload
- sự đơn giản khi tách service
- khả năng reuse hạ tầng đang có

Ở góc này, tôi thấy khác biệt chính là:

### Khi nào TEI hợp hơn

Chọn **TEI** nếu bạn có một trong các điều sau:

- muốn tách embedding service riêng khỏi generation service
- muốn một stack gọn, dễ giải thích cho team vận hành
- embedding/rerank là workload chính, không phải tính năng phụ
- muốn endpoint rất rõ theo use case như `/embed`, `/rerank`, `/predict`
- muốn tối ưu đường đi cho model họ sentence-transformers, BGE, E5, GTE, Qwen embedding, reranker các loại
- muốn ưu tiên boot time, batching path và resource profile cho đúng workload embedding/rerank

TEI đặc biệt hợp với kiến trúc kiểu:

- **TEI** cho embedding
- **TEI** hoặc service rerank riêng cho cross-encoder
- **vLLM/TGI/SGLang** hoặc model khác cho generation

Tức là mỗi service làm đúng việc nó giỏi.

### Khi nào vLLM hợp hơn

Chọn **vLLM** nếu bạn có một trong các điều sau:

- đã có sẵn platform vLLM trong production
- muốn giảm số loại runtime phải vận hành
- muốn gom embedding, rerank và generation vào một mặt phẳng API tương đối thống nhất
- muốn reuse hạ tầng observability, autoscaling, auth, routing đã xây cho vLLM
- embedding/rerank chỉ là một phần của hệ serving lớn hơn
- chấp nhận trade-off rằng đây có thể không phải runtime chuyên biệt nhất cho embedding/rerank, nhưng lại là runtime rẻ chi phí platform hơn

Đây là quyết định khá thực dụng. Nhiều khi **không phải vì vLLM là tốt nhất cho embedding**, mà vì **nó đủ tốt và rẻ chi phí nhận thức hơn cho platform team**.

## Một cách ra quyết định đơn giản

Nếu đang phân vân, tôi thấy có thể dùng rule of thumb này:

### Chọn TEI nếu câu hỏi của bạn là:

- “Tôi cần serve embedding model nào nhanh, gọn, ít drama?”
- “Tôi cần reranker endpoint riêng cho retrieval stack?”
- “Tôi muốn một service chuyên biệt để scale độc lập?”

### Chọn vLLM nếu câu hỏi của bạn là:

- “Tôi đã có vLLM rồi, có nên gom luôn embedding/rerank vào đó không?”
- “Tôi có cần giảm số nền tảng serving trong hệ thống không?”
- “Tôi muốn cùng một runtime cho nhiều loại model-serving task không?”

## Câu trả lời của tôi ở thời điểm hiện tại

Nếu bắt đầu mới cho **embedding + rerank thuần túy**, tôi sẽ nghiêng về **Hugging Face TEI**.

Lý do không phải vì vLLM yếu. Ngược lại, vLLM đã tiến rất xa và hỗ trợ rất nhiều thứ ngoài generation. Nhưng chính docs của họ hiện tại đã nói khá thẳng rằng phần pooling models vẫn đang ở trạng thái **convenience-first**, chưa phải **performance-first**.

Còn TEI thì gần như sinh ra cho đúng workload này. Nên nếu câu hỏi được viết lại thành:

> **Tôi không quan tâm chuyện unified runtime, tôi chỉ quan tâm performance khi chuyên biệt cho embedding với rerank, chọn gì?**

thì câu trả lời của tôi là:

> **Chọn TEI trước. Chỉ quay sang vLLM khi anh có lý do platform rất mạnh để hợp nhất.**

Nếu đã có một platform lớn chạy quanh vLLM, tôi vẫn sẽ cân nhắc dùng vLLM cho embedding/rerank để giảm độ phân mảnh vận hành. Nhưng nếu hỏi tôi đâu là lựa chọn mặc định cho một pipeline retrieval chuyên biệt, câu trả lời của tôi vẫn là:

> **TEI trước, vLLM sau, trừ khi bạn có lý do platform rất rõ để hợp nhất vào vLLM.**

## Tóm lại

- **TEI** là lựa chọn mặc định mạnh hơn nếu anh đang tối ưu **performance cho embedding và rerank chuyên biệt**.
- **vLLM** phù hợp hơn khi anh ưu tiên **runtime hợp nhất** hơn là tối ưu cục bộ cho workload này.
- Nếu chỉ nhìn feature list, hai bên có vẻ gần nhau.
- Nếu nhìn theo triết lý sản phẩm và docs chính thức, khác biệt lại khá rõ: **TEI tối ưu cho workload này, còn vLLM mới chỉ mở rộng sang workload này.**

Với tôi, đó là khác biệt đủ lớn để ảnh hưởng quyết định kiến trúc, nhất là khi tiêu chí đầu bài là performance chứ không phải platform consolidation.
