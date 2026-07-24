---
title: "LLM ở Việt Nam: Cửa nào sinh lời, chủ quyền AI làm sao bền vững?"
authors: [manhpt]
tags: [ai, llm, vietnam, vietnamese, ai-strategy, geopolitics, pricing, cost-optimization, open-source, rag]
date: 2026-07-24
description: "Chủ quyền AI là bắt buộc, nhưng đốt tiền vào hạ tầng tính toán không phải con đường bền vững. Phân tích chiến lược quốc gia Việt Nam và các cửa sinh lời thực tế cho LLM: dữ liệu, vertical, fine-tune, inference và tầng ứng dụng."
---

# LLM ở Việt Nam: Cửa nào sinh lời, chủ quyền AI làm sao bền vững?

**Tóm tắt** — Việt Nam đã có khung chiến lược và pháp lý khá đầy đủ cho AI: từ Quyết định 127/QĐ-TTg (2021), Nghị quyết 57-NQ/TW, đến Luật Trí tuệ nhân tạo 134/2025/QH15 có hiệu lực từ 01/03/2026. Chủ quyền AI là hướng đi đúng. Nhưng nếu hiểu chủ quyền là "tự train foundation model từ đầu trên cụm GPU nội địa", Việt Nam sẽ đốt tiền rất nhanh mà chưa chắc có sản phẩm sống được trên thị trường. Bài này tách hai câu hỏi thường bị trộn vào nhau: **chủ quyền cần gì thật?** và **cửa nào thực sự sinh lời?**

<!-- truncate -->

## Câu hỏi sai khiến cả hệ sinh thái đi lệch

Khi nói "làm LLM ở Việt Nam", nhiều cuộc họp nhảy thẳng vào:

- Mua bao nhiêu GPU H100/B200?
- Train mô hình bao nhiêu tỷ tham số?
- Bao giờ có "GPT của Việt Nam"?

Đó là câu hỏi của nước đã có sẵn lợi thế chip, vốn, dữ liệu đa ngôn ngữ và hệ sinh thái nghiên cứu dày. Với Việt Nam, câu hỏi đúng hơn là:

1. **Chủ quyền AI cần kiểm soát lớp nào?** Dữ liệu? Inference? Model weights? Hay chỉ là quyền chuyển đổi nhà cung cấp khi rủi ro địa chính trị tăng?
2. **Giá trị kinh tế nằm ở đâu?** Pretraining? Fine-tuning? RAG/agent trên dữ liệu doanh nghiệp? Hay phần mềm ngành?
3. **Ai trả tiền liên tục?** Ngân sách nhà nước, doanh nghiệp, hay người dùng cuối?

Nếu không trả lời ba câu này trước, mọi kế hoạch "xây LLM quốc gia" dễ biến thành dự án hạ tầng đắt đỏ, vận hành lỗ, rồi chết ở giai đoạn demo.

## Chiến lược quốc gia đã nói gì?

### Từ Quyết định 127 đến Luật AI 2026

Việt Nam không thiếu định hướng. Ba lớp chính sách đáng chú ý:

| Lớp | Văn bản | Điểm then chốt |
|---|---|---|
| Chiến lược dài hạn | [Quyết định 127/QĐ-TTg](https://en.baochinhphu.vn/national-strategy-on-rd-and-application-of-artificial-intelligence-11140663.htm) (26/01/2021) | AI là công nghệ nền; mục tiêu 2030 vào nhóm 4 ASEAN và top 50 thế giới; ưu tiên sản phẩm AI có lợi thế cạnh tranh; đầu tư có trọng điểm |
| Đột phá thể chế | Nghị quyết 57-NQ/TW | AI được nâng thành hạ tầng chiến lược gắn với dữ liệu, điện toán, đổi mới sáng tạo và chủ quyền số |
| Khung pháp lý | [Luật AI 134/2025/QH15](https://mst.gov.vn/quoc-hoi-thong-qua-luat-tri-tue-nhan-tao-hoan-thien-hanh-lang-phap-ly-cho-ky-nguyen-so-197251210165544671.htm) (hiệu lực 01/03/2026) | Quản trị theo mức rủi ro; mở đường đầu tư hạ tầng AI quốc gia, dữ liệu mở có kiểm soát, tự chủ năng lực AI |

Chiến lược 127 cũng nói rõ một nguyên tắc thường bị quên: **nhận chuyển giao, làm chủ rồi nâng cấp** — không phải tự phát minh mọi thứ từ số không. Phân bổ nguồn lực vào sản phẩm/dịch vụ AI thiết yếu mà Việt Nam có lợi thế; đẩy mạnh doanh nghiệp ứng dụng và startup AI.

Nói cách khác, chính sách quốc gia **không bắt buộc** Việt Nam phải thắng cuộc đua pretraining frontier model. Nó bắt buộc Việt Nam phải có năng lực kiểm soát, ứng dụng và tạo giá trị trên AI.

### Chủ quyền ≠ sở hữu mọi thứ

Một góc nhìn hữu ích đến từ phân tích của [Tech For Good Institute](https://techforgoodinstitute.org/insights/country-spotlights/vietnams-ai-strategy-aligning-aspirations-with-adaptive-governance/): chủ quyền số không đòi hỏi sở hữu toàn bộ phần cứng và cloud. Singapore là ví dụ điển hình — giữ quyền kiểm soát tiêu chuẩn, dữ liệu, an ninh và định hướng chiến lược, đồng thời hợp tác sâu với hệ sinh thái toàn cầu.

Với Việt Nam, khung chủ quyền thực dụng có thể nhìn theo lớp:

```text
┌─────────────────────────────────────────────┐
│  Lớp 5: Ứng dụng / Agent / Workflow ngành   │  ← sinh lời nhiều nhất
├─────────────────────────────────────────────┤
│  Lớp 4: RAG, tool, eval, MLOps, bảo mật     │  ← moat kỹ thuật thực tế
├─────────────────────────────────────────────┤
│  Lớp 3: Fine-tune / adapter / domain model  │  ← chủ quyền ngôn ngữ + ngành vụ
├─────────────────────────────────────────────┤
│  Lớp 2: Inference phục vụ nội địa           │  ← chủ quyền vận hành
├─────────────────────────────────────────────┤
│  Lớp 1: Base model (open-weight / API)      │  ← tận dụng toàn cầu
├─────────────────────────────────────────────┤
│  Lớp 0: Dữ liệu tiếng Việt + dữ liệu ngành │  ← tài sản chiến lược thật
└─────────────────────────────────────────────┘
```

**Chủ quyền bắt buộc** nằm chủ yếu ở lớp 0–2 và một phần lớp 3–4: dữ liệu nhạy cảm không chảy lung tung, inference quan trọng chạy trong biên giới pháp lý mong muốn, có khả năng thay model khi bị khóa API, và có năng lực tinh chỉnh cho tiếng Việt / lĩnh vực then chốt.

**Chủ quyền optional và rất đắt** nằm ở pretraining foundation model quy mô lớn. Đó là cuộc chơi vốn + chip + điện + đội ngũ research hàng trăm người. Việt Nam có thể làm một phần cho nghiên cứu và quốc phòng, nhưng không nên lấy đó làm mô hình kinh tế mặc định cho toàn hệ sinh thái.

## Vì sao "đốt tiền GPU" dễ thành bẫy?

### Pretraining frontier không phải cửa sinh lời của Việt Nam

Train một mô hình frontier không chỉ là mua GPU. Còn có:

- **Chi phí vốn**: cụm GPU, mạng, storage, làm mát, điện
- **Chi phí vận hành**: utilization thấp là đốt tiền âm thầm
- **Chi phí dữ liệu**: thu thập, làm sạch, lọc độc hại, kiểm soát bản quyền
- **Chi phí talent**: researcher và infra engineer khan hiếm, dễ bị hút ra ngoài
- **Chu kỳ lỗi thời**: model mới ra 3–6 tháng một lần; trọng số tự train có thể hết "mới" trước khi kịp thương mại hóa

Kể cả khi train xong một model "Made in Vietnam", câu hỏi tiếp theo vẫn là: **ai trả tiền inference hàng ngày?** Nếu không có demand thực, model quốc gia chỉ là tài sản biểu tượng.

### Hạ tầng tính toán nên là tiện ích dùng chung, không phải KPI của từng doanh nghiệp

Luật AI và các định hướng gần đây đang đẩy hướng đúng: trung tâm tính toán AI quốc gia, kho dữ liệu AI, cloud chủ quyền cho khu vực then chốt. Logic kinh tế ở đây giống điện lưới hơn là giống mỗi nhà máy tự xây tổ máy phát điện.

Doanh nghiệp Việt Nam nên hỏi:

- Tôi cần **quyền truy cập compute tin cậy với giá dự đoán được**, hay tôi cần **sở hữu rack GPU**?
- Tôi cần **SLA và data residency**, hay tôi cần logo "tự train 70B"?

Với phần lớn công ty, câu trả lời là cái trước.

## Vậy cửa sinh lời nằm ở đâu?

Dưới đây là các cửa có xác suất tạo doanh thu bền vững cao hơn pretraining, xếp theo mức "gần tiền" của thị trường Việt Nam.

### 1. Vertical AI trên dữ liệu tiếng Việt và quy trình ngành

Đây là cửa rõ nhất.

Ngân hàng, bảo hiểm, y tế, giáo dục, pháp lý, logistics, xuất nhập khẩu, nông nghiệp, hành chính công — đều có:

- tài liệu tiếng Việt đặc thù
- quy trình nội bộ
- ràng buộc tuân thủ
- nhu cầu giảm chi phí vận hành, không phải nhu cầu "chat cho vui"

Sản phẩm thắng không phải chatbot đa năng, mà là hệ thống trả lời đúng trên **hồ sơ tín dụng / bệnh án / hợp đồng / biểu mẫu / sổ sách** của khách hàng đó.

Moat thật sự: dữ liệu sạch + workflow + quyền truy cập hệ thống nghiệp vụ + đánh giá chất lượng theo metric ngành.

### 2. Fine-tune và domain adaptation, không phải train từ đầu

Open-weight từ DeepSeek, Qwen và các model tương đương đã san phẳng lớp foundation. Việc còn lại của Việt Nam thường là:

- tiếp tục pretrain nhẹ trên corpus tiếng Việt chất lượng cao
- fine-tune / LoRA cho pháp lý, kế toán, chăm sóc khách hàng, lập trình nội địa
- alignment theo văn hóa, thuật ngữ, và chuẩn trả lời của ngành

Một model 7B–70B được tinh chỉnh tốt trên dữ liệu đúng thường thắng một model frontier gọi qua API ở bài toán hẹp — với chi phí thấp hơn nhiều và kiểm soát dữ liệu tốt hơn.

### 3. RAG + agent + eval: lớp "làm cho model có ích"

Nhiều dự án LLM thất bại không vì model kém, mà vì:

- retrieval sai
- tool gọi lung tung
- không có guardrail
- không đo được chất lượng theo nghiệp vụ

Đây lại là nơi Việt Nam có lợi thế kỹ sư phần mềm mạnh. Xây pipeline RAG/agent cho doanh nghiệp, kèm eval liên tục, monitoring chi phí token, và tích hợp SSO/ERP/CRM — đó là dịch vụ và sản phẩm có thể tính tiền ngay.

### 4. Inference tối ưu và AI cloud nội địa

Khi ngày càng nhiều tổ chức cần chạy model trong nước vì dữ liệu nhạy cảm, cửa hàng hóa xuất hiện:

- serving vLLM / TensorRT-LLM với giá theo token hoặc theo GPU-hour
- caching, batching, routing đa model
- private endpoint cho ngân hàng, telco, chính phủ
- hỗ trợ model open-weight phổ biến + model fine-tune của khách

Đây là nơi Viettel, FPT, VNPT, VNG và các nhà cung cấp cloud nội địa có thể kiếm tiền thực — không bằng cách tự tuyên bố "có GPT Việt", mà bằng cách bán **điện toán suy luận tin cậy**.

### 5. Dữ liệu như sản phẩm hạ tầng

Chiến lược quốc gia nhấn mạnh bộ dữ liệu mở và hạ tầng dữ liệu lớn. Nếu làm nghiêm, Việt Nam có thể tạo các "đường ray" dùng chung:

- corpus tiếng Việt chất lượng cao, có provenance
- benchmark tiếng Việt theo ngành (pháp lý, y tế, giáo dục, công vụ)
- dataset OCR/biểu mẫu hành chính Việt Nam
- synthetic data có kiểm soát cho domain thiếu dữ liệu thật

Ai làm tốt lớp này sẽ bán được API dữ liệu, license corpus, dịch vụ labeling, và nền tảng đánh giá model. Đây cũng là lớp chủ quyền khó mua bằng tiền từ nước ngoài nhất: **ngữ cảnh Việt Nam**.

### 6. Nhà nước làm "neo cầu" (anchor customer), không làm "nhà máy model" duy nhất

Một điểm mạnh trong định hướng gần đây là nhà nước đóng vai trò thị trường neo: mua AI cho hành chính công, y tế, giáo dục, giao thông, thuế/hải quan. Nếu mua sắm công được thiết kế đúng — theo kết quả, có sandbox, có chuẩn dữ liệu — doanh nghiệp tư nhân có đơn hàng để sống, thay vì chỉ có pitch deck.

Cảnh báo: nếu mua sắm chỉ ưu tiên "model tự train nội địa" bất kể chất lượng/chi phí, ngân sách sẽ nuôi dự án biểu tượng. Nếu mua sắm ưu tiên **giá trị công việc hoàn thành + chủ quyền dữ liệu + khả năng chuyển đổi nhà cung cấp**, thị trường sẽ khỏe hơn.

## Ma trận chọn cửa: đừng nhầm nhiệm vụ quốc gia với mô hình kinh doanh

| Cửa | Mức cần cho chủ quyền | Khả năng sinh lời gần | Vốn cần | Ghi chú |
|---|---|---|---|---|
| Pretrain frontier | Cao về biểu tượng, thấp về ROI | Thấp | Rất cao | Nên là nhiệm vụ nghiên cứu/quốc phòng có chọn lọc |
| Shared national compute | Cao | Trung bình (utility) | Cao | Làm tiện ích dùng chung, tính phí sử dụng |
| Fine-tune tiếng Việt / ngành | Cao | Cao | Trung bình | Cửa hợp lý nhất cho nhiều lab và startup |
| RAG/agent doanh nghiệp | Trung bình–cao | Rất cao | Thấp–trung bình | Gần tiền nhất |
| Inference cloud nội địa | Cao | Cao | Cao | Cạnh tranh bằng giá, SLA, compliance |
| Dataset + benchmark Việt | Rất cao | Trung bình–cao dài hạn | Trung bình | Tài sản quốc gia khó thay thế |
| Chatbot đa năng tiêu dùng | Thấp | Thấp ở VN | Trung bình | Khó thắng miễn phí từ DeepSeek/Qwen/Gemini |

## Mô hình bền vững trông như thế nào?

Một chiến lược LLM bền vững cho Việt Nam có thể gói trong năm nguyên tắc:

1. **Mua/thuê foundation, làm chủ phần cận thị trường.** Dùng open-weight và API toàn cầu ở lớp nền; đầu tư nội địa vào dữ liệu, fine-tune, eval, serving, ứng dụng.
2. **Compute là utility.** Tập trung cụm GPU quốc gia/doanh nghiệp lớn cho thuê; tránh mỗi bộ/ngành/công ty tự mua một cụm rồi để idle.
3. **Đo bằng công việc hoàn thành, không bằng số tham số.** "Giảm 40% thời gian xử lý hồ sơ" đáng giá hơn "model 70B made in Vietnam".
4. **Thiết kế dual-use từ ngày đầu.** Cùng một stack phục vụ được doanh nghiệp và bài toán công; tránh hai hệ sinh thái song song không nói chuyện được với nhau.
5. **Giữ lối thoát địa chính trị.** Đa model, đa cloud, ưu tiên open-weight cho hệ thống trọng yếu. Chủ quyền thật là khả năng **không bị tắt điện từ xa**.

## Việc nên làm ngay — và việc nên dừng lại

### Nên làm

- Xây corpus và benchmark tiếng Việt chất lượng cao, có giấy phép rõ
- Fine-tune model nhỏ/trung bình cho 5–10 ngành có nhu cầu trả tiền thật
- Chuẩn hóa RAG/agent stack nội địa: retrieval, guardrail, eval, cost control
- Đẩy private inference cho dữ liệu nhạy cảm (tài chính, y tế, hành chính)
- Dùng ngân sách công để mua kết quả dịch vụ AI, kèm yêu cầu data residency và portability

### Nên dừng / thận trọng

- Lấy "train model tỷ tham số" làm KPI quốc gia duy nhất
- Đua chatbot tiêu dùng miễn phí với DeepSeek/Qwen bằng tiền ngân sách
- Mua GPU trước khi có workload và mô hình thu phí rõ
- Khóa hệ sinh thái vào một nhà cung cấp API nước ngoài vì tiện trước mắt
- Nhầm pilot nội bộ thành sản phẩm thị trường

## Kết luận

Chủ quyền AI của Việt Nam là chuyện phải làm — vì dữ liệu, vì an ninh, vì tiếng Việt, vì quyền tự quyết khi cục diện địa chính trị thay đổi. Nhưng bền vững không đến từ việc đốt tiền để tự có foundation model giống Mỹ hay Trung Quốc.

Bền vững đến từ việc đứng đúng chỗ trong chuỗi giá trị:

> **Dữ liệu Việt + fine-tune/domain model + inference tin cậy + ứng dụng ngành có người trả tiền.**

Đó mới là cửa sinh lời. GPU chỉ là điều kiện cần cho một phần cửa đó — không phải là chiến lược.

---

## Tài liệu tham khảo

1. [Quyết định 127/QĐ-TTg — Chiến lược quốc gia về nghiên cứu, phát triển và ứng dụng AI đến 2030](https://en.baochinhphu.vn/national-strategy-on-rd-and-application-of-artificial-intelligence-11140663.htm)
2. [Luật Trí tuệ nhân tạo 134/2025/QH15 — Bộ KH&CN](https://mst.gov.vn/quoc-hoi-thong-qua-luat-tri-tue-nhan-tao-hoan-thien-hanh-lang-phap-ly-cho-ky-nguyen-so-197251210165544671.htm)
3. [Nghị quyết 57-NQ/TW và triển khai thể chế KHCN–ĐMST–CĐS — Bộ KH&CN](https://mst.gov.vn/nghi-quyet-so-57-nq-tw-tao-nen-tang-phat-trien-khoa-hoc-cong-nghe-doi-moi-sang-tao-va-chuyen-doi-so-197260107110747473.htm)
4. [Vietnam’s AI Strategy: Aligning Aspirations with Adaptive Governance — Tech For Good Institute](https://techforgoodinstitute.org/insights/country-spotlights/vietnams-ai-strategy-aligning-aspirations-with-adaptive-governance/)
5. [Vietnam urged to advance sovereign AI in digital era — VietnamPlus](https://en.vietnamplus.vn/vietnam-urged-to-develop-sovereign-ai-in-digital-era-post348724.vnp)
6. [Vietnam shapes AI ecosystem following Resolution 57 — VietnamPlus](https://en.vietnamplus.vn/vietnam-shapes-ai-ecosystem-following-18-month-implementation-of-resolution-57-post347781.vnp)

---

*Góc nhìn kỹ thuật–kinh tế từ thực tiễn triển khai LLM/RAG. Số liệu chính sách cập nhật đến tháng 7/2026.*
