---
title: "Gemini Hết Thời 'Ngon Bổ Rẻ': Trung Quốc Đang Thắng Cuộc Đua AI Mở Và Cuộc Cạnh Tranh Ngầm Giữa Các Quốc Gia"
authors: [manhpt]
tags: [gemini, deepseek, qwen, ai, llm, open-source, china, geopolitics, pricing, vietnam, vietnamese]
date: 2026-04-28
description: "Phân tích sự suy giảm của Gemini từ gói miễn phí hào phóng nhất thành tường phí, sự trỗi dậy của mô hình Trung Quốc với open-weight và giá rẻ hơn 6-18 lần, cuộc cạnh tranh AI giữa các quốc gia, và vị trí của Việt Nam trong bức tranh này."
---

# Gemini Hết Thời "Ngon Bổ Rẻ": Trung Quốc Đang Thắng Cuộc Đua AI Mở Và Cuộc Cạnh Tranh Ngầm Giữa Các Quốc Gia

**Tóm tắt** — Tháng 4/2026 đánh dấu một bước ngoặt lớn trong làng AI. Google chính thức khai tử gói miễn phí Gemini Pro, siết chặt hạn ngạch Flash, và áp trần chi tiêu bắt buộc — chấm dứt kỷ nguyên "ngon bổ rẻ" từng khiến Gemini trở thành lựa chọn số một cho lập trình viên. Cùng lúc đó, chỉ 23 ngày sau, DeepSeek tung ra V4 với open-weight, giấy phép MIT, benchmark sát Opus 4.7, giá chỉ bằng 1/6. Bài viết này phân tích vì sao đây không chỉ là câu chuyện về giá cả — mà là một cuộc chiến địa chính trị ngầm, nơi mã nguồn mở được dùng như vũ khí chiến lược, và Trung Quốc đang dần chiếm ưu thế.

<!-- truncate -->

## Lời Mở Đầu: Tháng Tư Định Mệnh

Tháng 4/2026 là một tháng "đau ví" với lập trình viên dùng Gemini.

Ngày 1/4, Google lặng lẽ đẩy một loạt thay đổi lên Gemini API — không phải trò đùa Cá tháng Tư:

- **Các mô hình Pro (2.5 Pro, 3.1 Pro) bị loại khỏi gói miễn phí hoàn toàn.** Muốn dùng Pro? Trả tiền.
- **Flash bị siết hạn ngạch:** từ ~250 yêu cầu/ngày xuống còn 20-50 yêu cầu/ngày cho gói miễn phí.
- **Trần chi tiêu bắt buộc:** Bậc 1 bị giới hạn $250/tháng, muốn nâng trần phải xác minh.
- **Thanh toán trước:** Tài khoản mới phải nạp tiền trước, không còn hình thức trả theo mức dùng linh hoạt.

Cùng thời điểm đó, Gemini 2.5 Pro có giá $1.25/1M token đầu vào và $10/1M token đầu ra — không hề rẻ so với mặt bằng chung, nhưng trước đây được bù đắp bởi gói miễn phí hào phóng. Giờ đây, cánh cửa miễn phí đã đóng sập.

Đúng 23 ngày sau — 24/4/2026 — DeepSeek tung V4: **open-weight, giấy phép MIT, 1.6 nghìn tỷ tham số, benchmark 80.6% SWE-bench (sát Opus 4.7), giá $1.74/M token đầu vào — rẻ hơn GPT-5.5 gấp 7 lần.**

Sự trùng hợp về thời điểm này không phải ngẫu nhiên. Nó là một tuyên bố chiến lược.

## Gemini: Từ Gói Miễn Phí Hào Phóng Nhất Thành "Trả Tiền Hoặc Rời Đi"

### Hành trình đánh mất thiện cảm

Nhìn lại lịch sử, Gemini từng là "cơn ác mộng" của OpenAI về mặt định giá. Khi Gemini 1.5 Pro ra mắt với cửa sổ ngữ cảnh 1M token và gói miễn phí cực kỳ hào phóng, lập trình viên đổ xô sang. Google dùng gói miễn phí như một chiến lược chiếm thị phần — và nó đã hiệu quả.

Nhưng chiến lược đó có hạn sử dụng. Đến tháng 4/2026, Google quyết định "thu phí" khoản đầu tư này:

| Thay đổi | Trước 4/2026 | Sau 4/2026 |
|----------|-------------|------------|
| **Gemini Pro miễn phí** | ✅ Có, giới hạn RPM | ❌ Bắt buộc trả phí |
| **Flash miễn phí (yêu cầu/ngày)** | ~250 | 20-50 |
| **Trần chi tiêu** | Tùy chọn | Bắt buộc ($250 Bậc 1) |
| **Trả trước cho tài khoản mới** | ❌ Không | ✅ Bắt buộc |

### Vấn đề không nằm ở giá — mà ở niềm tin

Điều khiến lập trình viên thất vọng nhất không phải là giá Gemini đắt. $1.25/M token đầu vào là mức giá trung bình của thị trường. Vấn đề là **sự thay đổi đột ngột và thiếu khả năng dự đoán.**

Lập trình viên đã xây dựng sản phẩm trên gói miễn phí Gemini. Họ dựa vào nó cho việc tạo mẫu, dự án phụ, MVP khởi nghiệp. Khi Google đóng gói miễn phí, họ không chỉ mất một công cụ không mất tiền — họ mất niềm tin vào cam kết dài hạn của Google với cộng đồng lập trình viên.

Trong khi đó, ở phía bên kia Thái Bình Dương...

## Trung Quốc Trỗi Dậy: Mã Nguồn Mở Là Vũ Khí Chiến Lược

### Những con số biết nói

Đến tháng 4/2026, bức tranh AI toàn cầu đã thay đổi căn bản:

| Mô hình | Đầu vào/1M token | Đầu ra/1M token | Giấy phép | Ngữ cảnh |
|---------|-----------------|-----------------|-----------|----------|
| **DeepSeek V4-Flash** | $0.30 | $0.87 | MIT (open-weight) | 1M |
| **DeepSeek V3.2** | $0.28 | $0.42 | MIT (open-weight) | 128K |
| **DeepSeek V4-Pro** | $1.74 | $3.48 | MIT (open-weight) | 1M |
| **Qwen3-Max** | $0.78 | $3.90 | Apache 2.0 (open-weight) | 262K |
| **Gemini 2.5 Pro** | $1.25 | $10.00 | Độc quyền | 1M |
| **GPT-5.5** | $5.00 | $30.00 | Độc quyền | 256K |
| **Claude Opus 4.7** | $5.00 | $25.00 | Độc quyền | 200K |

V4-Flash rẻ hơn Gemini 2.5 Pro **~4 lần** trên đầu vào, và rẻ hơn GPT-5.5 **~16 lần**. V3.2 rẻ hơn Gemini 2.5 Pro **~4.5 lần** trên đầu vào, và **~24 lần** trên đầu ra.

Nhưng giá chỉ là một phần của câu chuyện.

### Không chỉ rẻ — mà còn mở

Điểm khác biệt lớn nhất: **toàn bộ mô hình Trung Quốc trong bảng trên đều là open-weight**, với giấy phép MIT hoặc Apache 2.0.

Điều này có nghĩa là gì?

- **Bạn có thể tự vận hành.** Không phụ thuộc vào API của bên thứ ba. Không lo giới hạn tốc độ. Không lo bị khóa tài khoản.
- **Bạn có thể fine-tune.** Tùy chỉnh mô hình cho trường hợp sử dụng riêng. Không cần xin phép ai.
- **Bạn có toàn quyền kiểm soát dữ liệu.** Không gửi dữ liệu nhạy cảm qua API của Google hay OpenAI.
- **Chi phí inference tự vận hành có thể rẻ hơn 5-10 lần** so với gọi API độc quyền.

Clément Delangue, CEO của Hugging Face, đã nói thẳng:

> *"Ở Trung Quốc, mặc định là mã nguồn mở. Ở Mỹ, mặc định là mã nguồn đóng. Khối lượng mô hình được chia sẻ bởi các công ty Trung Quốc hiện tại cao hơn nhiều so với những gì đang diễn ra ở Mỹ."*

### Bằng chứng từ thị trường

Không phải lời nói suông. Dữ liệu từ Hugging Face (tháng 3/2026):

- **Mô hình mã nguồn mở Trung Quốc vượt Mỹ về tổng lượt tải**, cả hàng tháng lẫn tổng thể.
- **Top 5 mô hình trên bảng xếp hạng OpenRouter đều là của Trung Quốc**: Mimo V2 Pro, Step 3.5 Flash, DeepSeek V3.2, MiniMax M2.5, GLM 5 Turbo.
- **Qwen có hơn 113.000 biến thể** trên Hugging Face — nhiều hơn bất kỳ mô hình nào khác.
- **DeepSeek & Qwen chiếm 15% thị phần AI toàn cầu**, tăng từ 1% một năm trước.

Và quan trọng hơn: các công ty lớn đang thực sự dùng chúng trong vận hành thực tế:

- **Airbnb**: Dùng Qwen cho chatbot chăm sóc khách hàng.
- **Pinterest** (619M người dùng hàng tháng): Dùng Qwen trong hệ thống gợi ý, cải thiện độ liên quan mua sắm 30%.
- **Notion**: Tích hợp mô hình mã nguồn mở Trung Quốc vào sản phẩm.

## Cuộc Cạnh Tranh Không Còn Là Doanh Nghiệp vs Doanh Nghiệp

### Mặt trận thứ nhất: Giá cả

Khi DeepSeek V3.2 có giá $0.28/M token đầu vào, nó không chỉ rẻ — nó **định nghĩa lại mặt bằng giá toàn ngành.** GPT-5.5 giá $5/M token đầu vào đắt gấp 18 lần. Claude Opus 4.7 giá $5/M token đầu vào đắt gấp 18 lần.

Câu hỏi đặt ra: liệu sự khác biệt về chất lượng có xứng đáng với mức giá gấp 18 lần?

Với V4-Pro (80.6% SWE-bench, sát Opus 4.7 ở 80.8%), câu trả lời ngày càng nghiêng về phía "không".

### Mặt trận thứ hai: Mã nguồn mở

Mã nguồn mở không chỉ là một lựa chọn kỹ thuật. Nó là một **đòn bẩy địa chính trị.**

Khi Trung Quốc phát hành mô hình dưới giấy phép MIT, họ đạt được nhiều mục tiêu cùng lúc:

1. **Phá vỡ thế độc quyền của Mỹ** trong lĩnh vực mô hình nền tảng AI.
2. **Xây dựng hệ sinh thái toàn cầu** xoay quanh công nghệ Trung Quốc — lập trình viên trên toàn thế giới dùng, đóng góp, và phụ thuộc vào mô hình Trung Quốc.
3. **Vô hiệu hóa kiểm soát xuất khẩu** — khi mô hình là open-weight, không ai cần mua chip NVIDIA để chạy inference qua API Mỹ nữa.
4. **Sức mạnh mềm** — Trung Quốc định vị mình là bên "mở" và "hào phóng", trong khi Mỹ là bên "đóng" và "thu phí".

### Mặt trận thứ ba: Chip và phần cứng

Đây là mặt trận ít được nhắc đến nhất nhưng quan trọng nhất.

DeepSeek V4 được công bố hỗ trợ đầy đủ trên **Huawei Ascend NPU** — chip AI nội địa của Trung Quốc. Theo công bố, hiệu năng trên Ascend đạt ngang bằng NVIDIA GPU.

Điều này có ý nghĩa gì?

- **Kiểm soát xuất khẩu của Mỹ đã thất bại trong việc kìm hãm AI Trung Quốc.** Thay vì bị chặn đứng, Trung Quốc đã xây dựng hệ sinh thái chip riêng.
- **Huawei Ascend đang trở thành lựa chọn inference thực tế** cho thị trường nội địa Trung Quốc và các nước không muốn phụ thuộc vào NVIDIA.
- **Kiểm soát xuất khẩu phản tác dụng:** Chúng thúc đẩy Trung Quốc tự chủ nhanh hơn, thay vì làm chậm họ.

Và điều trớ trêu: vào tháng 1/2026, chính quyền Trump đã chính thức hóa các chính sách cho phép xuất khẩu chip AI tiên tiến sang Trung Quốc — một động thái bị chỉ trích là làm suy yếu chính sách kiềm chế mà Mỹ đã theo đuổi suốt nhiều năm.

### Mặt trận thứ tư: Benchmark và chất lượng

Cuối cùng, câu hỏi quan trọng nhất: mô hình Trung Quốc có thực sự tốt không?

**DeepSeek V4-Pro benchmark (tháng 4/2026):**

| Benchmark | V4-Pro | Claude Opus 4.7 | GPT-5.5 | Gemini 3.1 Pro |
|-----------|--------|-----------------|---------|----------------|
| **SWE-bench Verified** | 80.6% | 80.8% | 74.2% | — |
| **LiveCodeBench** | 93.5% | 88.8% | — | 91.7% |
| **AIME 2025 (Toán)** | 94.2% | 95.1% | 91.8% | 90.3% |

V4-Pro ngang bằng hoặc vượt các mô hình đắt hơn nó 3-7 lần. Và bạn có thể chạy nó trên hạ tầng của chính mình.

## Phân Tích: Ai Được, Ai Mất?

### Bên thua cuộc

**Google (Gemini):** Mất lợi thế cạnh tranh lớn nhất — gói miễn phí hào phóng. Lập trình viên không còn lý do để chọn Gemini thay vì tự vận hành DeepSeek/Qwen với chi phí thấp hơn và toàn quyền kiểm soát. Trong một thị trường mà lập trình viên là người quyết định bộ công nghệ, đánh mất họ là đánh mất tương lai.

**OpenAI (GPT):** Vấn đề của OpenAI không phải là chất lượng — GPT-5.5 vẫn rất mạnh. Vấn đề là giá. Ở mức $5/$30 mỗi triệu token, họ đang bán iPhone trong khi đối thủ bán Android ngang cấu hình. Thị trường cao cấp vẫn còn, nhưng thị trường khối lượng lớn đang tuột khỏi tay.

**Anthropic (Claude):** Tương tự OpenAI. Opus 4.7 có chất lượng xuất sắc, nhưng $5/$25 mỗi triệu token là mức giá chỉ doanh nghiệp lớn chấp nhận được.

### Bên thắng cuộc

**DeepSeek:** Từ một startup vô danh thành kẻ thách thức toàn cầu trong 18 tháng. Chiến lược: mã nguồn mở mọi thứ, giá rẻ không tưởng, chất lượng ngang hàng đầu. Đòn kép: V4-Flash cho khối lượng ($0.30/M), V4-Pro cho chất lượng cao ($1.74/M).

**Alibaba (Qwen):** Chiến lược khác DeepSeek: thay vì tự làm tất cả, họ xây dựng hệ sinh thái. 113.000 biến thể Qwen trên Hugging Face không phải ngẫu nhiên — đó là kết quả của chiến lược "để cộng đồng làm phần còn lại". Airbnb, Pinterest, Notion dùng Qwen không phải vì được trả tiền, mà vì nó thực sự tốt.

**ByteDance (Doubao):** Tay chơi mới nhưng đáng gờm. Sở hữu lượng dữ liệu khổng lồ từ TikTok, có tiềm lực tài chính mạnh nhất trong các công ty AI Trung Quốc (nhờ doanh thu quảng cáo), và đang theo đuổi chiến lược "đi rộng" — phủ nhiều mô hình cho nhiều trường hợp sử dụng.

**Lập trình viên toàn cầu:** Chưa bao giờ có nhiều lựa chọn tốt và rẻ đến thế. Tự vận hành mô hình chất lượng hàng đầu với chi phí thấp hơn gọi API 10 lần? Năm 2024 đó là giấc mơ. Năm 2026 đó là thực tế.

## Việt Nam Trong Cuộc Cạnh Tranh AI: Cơ Hội Hay Nguy Cơ?

### Vị trí địa chính trị độc đáo

Việt Nam đang ở một vị trí đặc biệt trong cuộc đua AI toàn cầu. Không thuộc phe nào, không bị ràng buộc bởi các liên minh công nghệ cứng nhắc, Việt Nam có thể **chọn cả hai** — hoặc không chọn bên nào.

Đây vừa là lợi thế, vừa là thách thức.

### Cơ hội: Tiếp cận công nghệ đỉnh cao với chi phí thấp nhất lịch sử

Cuộc chiến giá giữa Mỹ và Trung Quốc tạo ra một "cửa sổ cơ hội" chưa từng có cho các nước đang phát triển như Việt Nam:

- **Chi phí inference giảm theo cấp số nhân.** Với DeepSeek V4-Flash ở mức $0.30/M token, một startup Việt Nam với ngân sách $100/tháng có thể xử lý hơn 300 triệu token — đủ để chạy chatbot, phân tích tài liệu, hoặc tự động hóa quy trình cho hàng nghìn người dùng.
- **Mô hình open-weight loại bỏ rào cản phụ thuộc nhà cung cấp.** Doanh nghiệp Việt Nam không cần phụ thuộc vào OpenAI hay Google. Có thể tự vận hành mô hình trên hạ tầng trong nước, bảo vệ chủ quyền dữ liệu — yếu tố đặc biệt quan trọng với các tổ chức tài chính, chính phủ, và y tế.
- **Rút ngắn khoảng cách công nghệ.** Trong quá khứ, Việt Nam luôn đi sau các nước phát triển 5-10 năm về công nghệ. Với AI mã nguồn mở, khoảng cách này có thể rút xuống còn vài tháng — vì mô hình được công khai ngay khi phát hành.
- **Cơ hội cho cộng đồng lập trình viên Việt Nam.** Với hơn 500.000 lập trình viên, Việt Nam có lực lượng kỹ sư đủ lớn để fine-tune, triển khai, và xây dựng ứng dụng trên nền mô hình open-weight. Đây là thời điểm để cộng đồng mã nguồn mở Việt Nam tạo ra những đóng góp có ý nghĩa cho hệ sinh thái toàn cầu.

### Thách thức: Bị kẹt giữa hai "gọng kìm"

Tuy nhiên, vị trí trung lập cũng mang đến những rủi ro không nhỏ:

- **Phụ thuộc công nghệ.** Nếu toàn bộ bộ công nghệ AI của Việt Nam chạy trên mô hình Trung Quốc (DeepSeek, Qwen) hoặc Mỹ (OpenAI, Anthropic), về lâu dài đây là một dạng phụ thuộc nhà cung cấp cấp quốc gia. Không khác gì phụ thuộc vào chip hay hệ điều hành.
- **Chủ quyền dữ liệu.** Gửi dữ liệu người dùng Việt Nam qua API của nước ngoài — dù là Mỹ hay Trung Quốc — đều đặt ra câu hỏi về chủ quyền dữ liệu. Đây là vấn đề nhạy cảm với mọi quốc gia, không riêng Việt Nam.
- **Hạ tầng phần cứng.** Tự vận hành mô hình chất lượng hàng đầu vẫn đòi hỏi GPU đắt tiền. NVIDIA H100/B200 giá hàng chục nghìn USD mỗi chiếc, và Việt Nam chưa có hạ tầng điện toán đám mây nội địa đủ mạnh để chạy inference ở quy mô lớn. Huawei Ascend có thể là lựa chọn thay thế rẻ hơn, nhưng cũng kéo theo câu hỏi về địa chính trị.
- **Thiếu chiến lược quốc gia về AI.** Trong khi Trung Quốc có kế hoạch 5 năm cho AI, Mỹ có CHIPS Act và các chương trình đầu tư tỷ đô, Việt Nam vẫn thiếu một chiến lược AI quốc gia rõ ràng — từ nghiên cứu cơ bản, đào tạo nhân lực, đến hạ tầng tính toán.

### Kịch bản nào cho Việt Nam?

**Kịch bản 1 — Người hưởng lợi thụ động (khả thi nhất hiện tại):**
Việt Nam tiếp tục sử dụng API và mô hình open-weight từ cả Mỹ và Trung Quốc, chọn mô hình tốt nhất cho từng trường hợp sử dụng, không đầu tư vào hạ tầng nội địa. Chi phí thấp, triển khai nhanh, nhưng phụ thuộc dài hạn và không có chủ quyền công nghệ.

**Kịch bản 2 — Trung tâm AI khu vực (tham vọng):**
Việt Nam đầu tư vào hạ tầng GPU nội địa (có thể hợp tác với NVIDIA hoặc Huawei), xây dựng trung tâm dữ liệu cho AI inference, trở thành đầu mối cung cấp dịch vụ AI cho Đông Nam Á. Tận dụng vị trí địa lý và chi phí nhân công cạnh tranh. Đòi hỏi đầu tư lớn và chiến lược dài hạn.

**Kịch bản 3 — Mất kiểm soát (xấu nhất):**
Không có chiến lược, để thị trường tự quyết định. Doanh nghiệp và chính phủ phụ thuộc hoàn toàn vào mô hình nước ngoài. Khi có biến động địa chính trị (cấm vận, ngừng dịch vụ), toàn bộ hệ thống AI trong nước tê liệt. Dữ liệu người dùng Việt nằm trên máy chủ nước ngoài không kiểm soát được.

### Lời khuyên cho lập trình viên và doanh nghiệp Việt Nam

1. **Ưu tiên mô hình open-weight có thể tự vận hành.** Qwen và DeepSeek là hai lựa chọn hàng đầu hiện tại. Có thể chạy phiên bản nhỏ hơn (như V4-Flash 284B hoặc Qwen distill) trên hạ tầng khiêm tốn hơn.
2. **Không "bỏ tất cả trứng vào một giỏ".** Đừng xây dựng sản phẩm chỉ chạy trên một nhà cung cấp duy nhất. Thiết kế kiến trúc có thể hoán đổi mô hình dễ dàng.
3. **Đầu tư vào fine-tuning, không chỉ gọi API.** Mô hình nhỏ được fine-tune chạy trên hạ tầng nội địa có thể vượt mô hình lớn gọi qua API — với chi phí thấp hơn và kiểm soát tốt hơn.
4. **Theo dõi hạ tầng điện toán đám mây nội địa.** Viettel Cloud, VNG Cloud, FPT Cloud đang phát triển — khi họ hỗ trợ GPU inference cho mô hình open-weight, cánh cửa cho AI "Make in Vietnam" sẽ thực sự mở ra.

---

*Góc nhìn cá nhân:* Việt Nam đang ở thời điểm vàng. AI mã nguồn mở đã san phẳng sân chơi — lần đầu tiên trong lịch sử, một công ty 10 người ở Hà Nội có thể tiếp cận công nghệ ngang bằng với một startup ở Thung lũng Silicon. Nhưng cơ hội này có hạn. Khi các nước lớn hoàn thiện hệ sinh thái AI của họ, cánh cửa cho người đến sau sẽ hẹp dần. Thời điểm để hành động là bây giờ — không phải 2 năm nữa.

## Kết Luận: Cuộc Chơi Đã Thay Đổi

### Tóm tắt chính

1. **Gemini đã đánh mất "sức hút" với lập trình viên.** Từ chiến lược "miễn phí để chiếm thị phần" chuyển sang "thu phí để có lời", Google đã đẩy lập trình viên về phía đối thủ — đúng vào lúc đối thủ Trung Quốc đang mở rộng vòng tay.

2. **Mô hình Trung Quốc đã đạt chất lượng hàng đầu.** Không còn là "hàng nhái giá rẻ" nữa. DeepSeek V4-Pro benchmark ngang Opus 4.7, Qwen3-Max cạnh tranh sòng phẳng với GPT-5.5. Khoảng cách chất lượng đã biến mất.

3. **Mã nguồn mở là vũ khí bất đối xứng.** Mỹ dùng kiểm soát xuất khẩu để hạn chế Trung Quốc. Trung Quốc đáp trả bằng cách công khai toàn bộ trọng số mô hình, khiến kiểm soát xuất khẩu trở nên vô nghĩa. Không cần chip Mỹ nếu bạn có thể chạy mô hình Trung Quốc trên chip Trung Quốc.

4. **Cuộc chơi không còn là Google vs OpenAI vs Anthropic.** Nó đã trở thành Mỹ vs Trung Quốc, với mặt trận trải dài từ định giá, giấy phép, phần cứng, đến hệ sinh thái lập trình viên. Và Trung Quốc đang dẫn trước ở hầu hết các mặt trận đó.

5. **Việt Nam đứng trước cơ hội lịch sử.** Với AI mã nguồn mở, lần đầu tiên một startup 10 người ở Hà Nội có công nghệ ngang bằng Thung lũng Silicon. Nhưng nếu không có chiến lược quốc gia về AI, cơ hội này sẽ trôi qua và Việt Nam sẽ trở thành người tiêu dùng thụ động trong cuộc chơi của các cường quốc.

### Khuyến nghị

**Nếu bạn là lập trình viên Việt Nam:**
- Đừng xây dựng sản phẩm phụ thuộc vào một API độc quyền duy nhất. Đa dạng hóa nhà cung cấp, cân nhắc tự vận hành mô hình open-weight.
- DeepSeek V3.2/V4 và Qwen3 là những lựa chọn thay thế nghiêm túc cho Gemini/GPT/Claude ở phần lớn trường hợp sử dụng.
- Học cách fine-tune mô hình nhỏ cho lĩnh vực cụ thể — một mô hình 7B-70B được fine-tune tốt có thể vượt mô hình 1.6T đa dụng với chi phí thấp hơn 50 lần.
- Đóng góp vào cộng đồng mã nguồn mở Việt Nam: bộ dữ liệu tiếng Việt, benchmark tiếng Việt, mô hình fine-tune cho thị trường nội địa.

**Nếu bạn là doanh nghiệp Việt Nam:**
- Lợi thế về giá của mô hình Trung Quốc là quá lớn để bỏ qua. Tính toán TCO cho việc tự vận hành so với gọi API.
- Cân nhắc yếu tố địa chính trị trong quyết định chọn mô hình — chủ quyền dữ liệu, phụ thuộc nhà cung cấp, và rủi ro bị cắt dịch vụ.
- Mô hình open-weight cho phép bạn kiểm soát hoàn toàn pipeline dữ liệu — yếu tố ngày càng quan trọng với các tổ chức tài chính, y tế, chính phủ.
- Theo dõi hạ tầng điện toán đám mây nội địa (Viettel, VNG, FPT) — khi họ hỗ trợ GPU inference, cơ hội "AI Make in Vietnam" sẽ mở ra.

### Dự báo

- **6 tháng tới:** DeepSeek V4 sẽ được fine-tune thành hàng nghìn biến thể, tương tự những gì đã xảy ra với Qwen. Hệ sinh thái mã nguồn mở Trung Quốc sẽ càng dày đặc hơn.
- **12 tháng tới:** Cuộc đua sẽ chuyển từ "ai có mô hình tốt nhất" sang "ai có hệ sinh thái inference rẻ nhất". Giá sẽ tiếp tục giảm về gần bằng không — câu hỏi là ai chịu được cuộc chiến giá này.
- **Dài hạn:** AI sẽ trở thành hạ tầng thiết yếu như điện, nước. Người thắng không phải là người bán điện đắt nhất, mà là người kiểm soát được hệ thống phân phối.

---

## Tài Liệu Tham Khảo

1. [Google Ends Free Gemini Pro API Access — AIPricing.guru](https://www.aipricing.guru/news/google-ends-free-gemini-pro-api-access/)
2. [Gemini API Pricing Guide 2026 — FindSkill](https://findskill.ai/blog/gemini-api-pricing-guide/)
3. [Gemini 2.5 Pro Pricing — PerUnit.ai](https://perunit.ai/models/gemini-2.5-pro)
4. [DeepSeek V4 Released: Open-Source at 1/6 the Cost — Nerd Level Tech](https://nerdleveltech.com/deepseek-v4-open-source-frontier-million-token-context)
5. [DeepSeek V4 Ships 1M Context, Open-Weights — WinBuzzer](https://winbuzzer.com/2026/04/27/deepseek-v4-open-weights-launch-xcxwbn/)
6. [DeepSeek API Pricing 2026 — DeployBase](https://deploybase.ai/articles/deepseek-api-pricing)
7. [DeepSeek API Pricing Guide 2026 — Ofox](https://ofox.ai/blog/deepseek-api-pricing-guide-2026/)
8. [Qwen3-Max Review & Pricing — TokenMix](https://tokenmix.ai/blog/qwen3-max-review-benchmark-pricing-2026)
9. [Why China Is Winning The Open Source AI Race — Forbes](https://www.forbes.com/sites/timkeary/2026/03/25/why-china-is-winning-the-open-source-ai-race/)
10. [China's AI Surge: Seedance, Doubao, Qwen3.5, DeepSeek V4 — AI Tool Briefing](https://aitoolbriefing.com/blog/china-ai-models-seedance-doubao-qwen-deepseek-2026/)
11. [DeepSeek's Sequel Set to Extend China's Reach — NYT](https://www.nytimes.com/2026/04/24/business/china-ai-deepseek-open-source.html)
12. [Administration Policies on Advanced AI Chips Codified — Mayer Brown](https://www.mayerbrown.com/en/insights/publications/2026/01/administration-policies-on-advanced-ai-chips-codified)
13. [How US Export Controls Have (and Haven't) Curbed Chinese AI — AI Frontiers](https://ai-frontiers.org/articles/us-chip-export-controls-china-ai)

---

*Bài viết được thực hiện vào ngày 28/04/2026. Số liệu định giá và benchmark có thể thay đổi theo thời gian.*
