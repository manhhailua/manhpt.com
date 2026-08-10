---
title: "Quyết định 1308/QĐ-TTg và hướng đi Tri thức AI của tôi"
slug: chien-luoc-du-lieu-quoc-gia-tri-thuc-ai
authors: [manhpt]
tags: [ai-strategy, rag, retrieval, ai, vietnamese]
date: 2026-08-10
description: "Phân tích Chiến lược dữ liệu quốc gia 2026–2030 và lý do tôi chọn RAG làm công nghệ chủ đạo để xây hệ thống Tri thức AI có căn cứ, kiểm soát và cập nhật được."
image: ./cover.png
---

Ngày 18/7/2026, Thủ tướng Chính phủ ban hành [Quyết định 1308/QĐ-TTg](https://vanban.chinhphu.vn/?docid=218908&pageid=27160), phê duyệt Chiến lược dữ liệu quốc gia giai đoạn 2026–2030, tầm nhìn đến năm 2045. Quyết định này thay thế Chiến lược năm 2024 và đặt dữ liệu, hạ tầng tính toán cùng trí tuệ nhân tạo vào một định hướng phát triển thống nhất.

Tôi đọc văn bản này không chỉ để biết Nhà nước sẽ xây bao nhiêu trung tâm dữ liệu hay đặt ra bao nhiêu chỉ tiêu. Điều khiến tôi chú ý hơn là một lựa chọn có tính nền tảng: **phát triển AI phải đi cùng dữ liệu quốc gia có chất lượng, được quản trị, kết nối, chia sẻ và bảo vệ trong suốt vòng đời**.

Đó cũng là động lực chính và lâu dài cho hướng tôi đang theo đuổi: xây dựng **hệ thống Tri thức AI**, với RAG là công nghệ chủ đạo. Không phải một chatbot biết nói trôi chảy, mà là một hệ thống biết tìm đúng nguồn, tổng hợp có căn cứ, tôn trọng quyền truy cập và để con người kiểm chứng được câu trả lời.

<!-- truncate -->

## Đây không phải một bản cập nhật nhỏ của chiến lược cũ

[Toàn văn Quyết định 1308/QĐ-TTg](https://datafiles.chinhphu.vn/cpp/files/vbpq/2026/7/1308_qd-ttg_18072026_3-signed.signed.pdf) xác định dữ liệu là tài nguyên chiến lược, tài sản quốc gia và tư liệu sản xuất mới. Quan trọng hơn, văn bản gắn trực tiếp việc phát triển, quản trị và khai thác dữ liệu với AI, năng suất lao động, năng lực cạnh tranh và các động lực tăng trưởng mới.

Nếu chỉ nhìn từng chỉ tiêu riêng lẻ, đây có thể trông giống một danh sách dự án số hóa rất dài. Nhìn theo hệ thống, chiến lược mới đang ghép năm mảnh vốn thường bị triển khai rời nhau:

| Mảnh ghép | Mục tiêu đáng chú ý đến năm 2030 | Ý nghĩa thực tế |
|---|---|---|
| Quản trị | Các bộ, ngành và địa phương có chiến lược, khung kiến trúc, khung quản trị và từ điển dữ liệu | Dữ liệu cần có chủ sở hữu, định nghĩa và trách nhiệm rõ ràng |
| Chất lượng và liên thông | Dữ liệu trọng yếu được số hóa, chuẩn hóa, làm sạch và đồng bộ qua hạ tầng dùng chung | Giảm tình trạng mỗi nơi giữ một bản, cùng tên nhưng khác nghĩa |
| Hạ tầng | Vận hành 3 Trung tâm dữ liệu quốc gia cùng hạ tầng tính toán hiệu năng cao (HPC) và AI dùng chung | Tạo năng lực xử lý, huấn luyện và triển khai ở quy mô lớn |
| Dữ liệu cho AI | Hình thành Kho dữ liệu AI quốc gia; dữ liệu được chuẩn hóa, làm sạch, gắn nhãn và ẩn danh | Biến dữ liệu thô thành nguyên liệu có thể khai thác an toàn |
| Kinh tế dữ liệu | Tối thiểu 5 sàn dữ liệu, 1.000 doanh nghiệp công nghệ dữ liệu và 30 tổ chức trung gian dữ liệu | Tạo đường đi từ tài nguyên dữ liệu đến sản phẩm và dịch vụ |

Chiến lược còn đặt mục tiêu hỗ trợ phát triển, huấn luyện ít nhất 150 sản phẩm, dịch vụ dữ liệu và mô hình AI “Make in Vietnam”. Những con số này là **mục tiêu chính sách**, chưa phải kết quả đã đạt được. Dù vậy, chúng cho thấy dữ liệu cho AI đã chuyển từ một ý tưởng khuyến khích thành một hạng mục có đầu mối, thời hạn và cơ chế theo dõi trong [danh mục nhiệm vụ trọng tâm](https://datafiles.chinhphu.vn/cpp/files/vbpq/2026/7/1308_qd-ttg_18072026_5-signed.pdf).

## Tín hiệu mạnh nhất nằm ở cụm từ “dữ liệu phục vụ AI”

Một mô hình AI có thể rất mạnh, nhưng nếu không tiếp cận được tri thức đúng, mới và phù hợp với Việt Nam thì nó vẫn chỉ là một người nói chuyện lưu loát với trí nhớ không đáng tin cậy.

Quyết định 1308 yêu cầu dữ liệu được tổ chức theo nguyên tắc “đúng, đủ, sạch, sống, thống nhất, dùng chung”; đồng thời đề cập từ điển dữ liệu quốc gia, không gian dữ liệu dùng chung, Cổng dữ liệu mở quốc gia và Kho dữ liệu AI quốc gia. Đây là các thành phần giúp dữ liệu có ngữ nghĩa, có khả năng kết nối và có thể sử dụng lại thay vì chỉ nằm yên trong từng cơ sở dữ liệu.

Trước đó, [Quyết định 804/QĐ-TTg ngày 6/5/2026](https://vanban.chinhphu.vn/?docid=218027&pageid=27160) đã ban hành danh mục 15 nhóm dữ liệu thiết yếu phục vụ AI. Danh mục bao gồm ngôn ngữ tiếng Việt và tiếng dân tộc thiểu số, tri thức quốc gia, văn bản pháp luật và hành chính, khoa học và công nghệ, dịch vụ công, y tế, giáo dục, nông nghiệp, giao thông, kinh tế, văn hóa và nhiều lĩnh vực khác.

Sự kết hợp của hai quyết định tạo ra một tín hiệu rõ ràng:

- Quyết định 804 trả lời câu hỏi **cần những nhóm dữ liệu nào cho AI**.
- Quyết định 1308 đặt chúng vào **hệ thống quản trị, hạ tầng, chất lượng, khai thác và phát triển thị trường** dài hạn.

Đây là điểm tôi quan tâm nhất. Dữ liệu không tự biến thành tri thức chỉ vì đã được gom vào một kho lớn. Nó cần ngữ cảnh, nguồn gốc, thời điểm hiệu lực, quan hệ giữa các thực thể, quyền truy cập và cơ chế đánh giá. Kho dữ liệu là nền móng; Tri thức AI là phần công trình giúp con người hỏi, hiểu và hành động dựa trên nền móng đó.

## Vì sao tôi chọn RAG làm công nghệ chủ đạo

Quyết định 1308 không nhắc đến thuật ngữ RAG. Việc kết nối chiến lược với RAG là **diễn giải kỹ thuật của tôi**, không phải một yêu cầu được ghi trong văn bản.

RAG, viết tắt của Retrieval-Augmented Generation, kết hợp mô hình sinh ngôn ngữ với một bộ nhớ ngoài có thể truy xuất. [Nghiên cứu gốc của Lewis và cộng sự](https://arxiv.org/abs/2005.11401) xuất phát từ hai giới hạn của mô hình chỉ dựa vào tham số: khó cập nhật tri thức và khó cung cấp nguồn gốc cho câu trả lời. Thay vì buộc mô hình phải “nhớ” mọi thứ, hệ thống truy xuất bằng chứng liên quan rồi đưa bằng chứng đó vào ngữ cảnh để mô hình tổng hợp.

Đây là cách tôi ánh xạ định hướng dữ liệu quốc gia vào một hệ thống Tri thức AI:

```text
Nguồn dữ liệu
  → Chuẩn hóa, siêu dữ liệu và quyền truy cập
  → Kho tri thức cùng các chỉ mục
  → Truy xuất kết hợp và xếp hạng lại
  → LLM tổng hợp câu trả lời
  → Trích dẫn, đánh giá và phản hồi
```

RAG phù hợp với hướng đi này vì bốn lý do.

**Thứ nhất, tri thức có thể cập nhật mà không phải huấn luyện lại toàn bộ mô hình.** Văn bản pháp luật thay đổi, quy trình được sửa, dữ liệu vận hành phát sinh hằng ngày. Khi nguồn được cập nhật và đánh chỉ mục lại đúng cách, hệ thống có thể truy xuất phiên bản mới mà không cần chờ một vòng huấn luyện tốn kém.

**Thứ hai, câu trả lời có thể gắn với bằng chứng.** Với các lĩnh vực như pháp luật, hành chính, y tế hay tài chính, “nghe có vẻ đúng” là chưa đủ. Hệ thống cần chỉ ra tài liệu nào, phiên bản nào và đoạn nào hỗ trợ cho từng nhận định.

**Thứ ba, quyền truy cập có thể được áp dụng ngay tại bước truy xuất.** Người dùng chỉ nên lấy được những tài liệu họ có quyền xem. Phân quyền sau khi LLM đã đọc dữ liệu nhạy cảm là hơi muộn, giống như khóa cửa sau khi khách đã ngồi trong phòng khách.

**Thứ tư, lớp tri thức ít phụ thuộc vào một mô hình duy nhất.** Mô hình sinh, embedding hay bộ xếp hạng lại có thể thay đổi; nguồn dữ liệu, siêu dữ liệu, quy tắc truy cập và bộ đánh giá vẫn là tài sản lâu dài của hệ thống.

## Hệ thống Tri thức AI tôi muốn xây không phải chatbot phủ lên PDF

Tôi dùng tên **Tri thức AI** cho một hệ thống biến dữ liệu đã được quản trị thành câu trả lời hoặc hành động có căn cứ. RAG là lõi truy xuất và tổng hợp, nhưng sản phẩm hoàn chỉnh cần nhiều hơn một cơ sở dữ liệu vector.

Hệ thống đó phải có năm đặc tính:

1. **Kiểm soát được nguồn:** biết tài liệu đến từ đâu, ai sở hữu, còn hiệu lực hay không và lần cuối được cập nhật khi nào.
2. **Ưu tiên bằng chứng:** câu trả lời quan trọng phải có trích dẫn; thiếu bằng chứng thì nói rõ chưa đủ thông tin.
3. **Tôn trọng phân quyền:** quyền truy cập đi cùng dữ liệu từ lúc nhập kho, lập chỉ mục đến khi tạo câu trả lời và ghi nhật ký.
4. **Không khóa vào một mô hình:** có thể đổi LLM, embedding, kho vector hoặc chiến lược truy xuất mà không phải xây lại toàn bộ tài sản tri thức.
5. **Đo được chất lượng:** đánh giá riêng retrieval, độ bám nguồn, tính đầy đủ, độ trễ và hiệu quả đối với tác vụ thực tế.

Retrieval trong kiến trúc này cũng không đồng nghĩa với vector search. Dữ liệu có cấu trúc cần SQL, quan hệ nhiều bước có thể cần graph, mã và tên riêng thường cần keyword search, còn dữ liệu thời gian thực có thể đến từ API. RAG chỉ bền khi nó tìm đúng dữ liệu bằng đúng công cụ rồi mới giao cho mô hình sinh câu trả lời.

Vì thế, phần tôi muốn đầu tư lâu dài không phải là một giao diện chat đẹp hay một mô hình đang đứng đầu bảng xếp hạng tuần này. Đó là quy trình nhập liệu, siêu dữ liệu, bản thể dữ liệu (ontology), truy xuất kết hợp, phân quyền, trích dẫn, đánh giá và khả năng quan sát toàn bộ hành trình từ câu hỏi đến bằng chứng.

## Một lộ trình cá nhân đi cùng lộ trình quốc gia

Quyết định 1308 chia việc khai thác Cơ sở dữ liệu tổng hợp quốc gia thành các giai đoạn: ưu tiên dịch vụ công và “dữ liệu thay giấy tờ” trong 2026–2027; tăng phân tích, dự báo và hỗ trợ ra quyết định trong 2027–2028; mở rộng kinh tế dữ liệu và mô hình kinh doanh mới trong 2028–2030; sau năm 2030 phát triển hệ sinh thái dữ liệu phục vụ AI ở quy mô rộng hơn.

Tôi không giả định mình được tiếp cận các cơ sở dữ liệu quốc gia hay đứng trong một dự án của Nhà nước. Nhưng lộ trình đó giúp tôi xác định thứ tự năng lực cần xây:

| Giai đoạn | Trọng tâm của tôi |
|---|---|
| Nền tảng | Nhập liệu đa nguồn, siêu dữ liệu, quản lý phiên bản, phân quyền và truy vết nguồn gốc |
| Chất lượng | Truy xuất kết hợp, xếp hạng lại, bộ câu hỏi đánh giá và kiểm tra ở cấp độ từng nhận định |
| Chuyên ngành | Các gói tri thức cho pháp luật, hành chính, khoa học, giáo dục hoặc lĩnh vực có dữ liệu hợp pháp |
| Sản phẩm hóa | API tri thức, trợ lý chuyên ngành và quy trình hỗ trợ quyết định có nhật ký, trích dẫn, phản hồi |

Tôi sẽ ưu tiên các nguồn công khai, dữ liệu được cấp quyền và những bài toán có người dùng cụ thể. Chính sách tạo ra hướng gió thuận, nhưng không thay thế quyền truy cập dữ liệu, chất lượng triển khai hay nhu cầu thật của khách hàng.

## Quyết định tạo động lực, không tự động tạo ra sản phẩm tốt

Một chiến lược quốc gia mạnh vẫn còn khoảng cách lớn tới một hệ thống AI hoạt động đáng tin cậy.

Trước hết, mục tiêu “đúng, đủ, sạch, sống” rất khó đạt đồng đều. Dữ liệu lịch sử có thể thiếu, trùng lặp, sai định dạng hoặc không rõ đơn vị chịu trách nhiệm. Mô hình có thể đổi vài lần trước khi một kho dữ liệu được làm sạch xong; dữ liệu bẩn thường kiên định hơn công nghệ khá nhiều.

Tiếp theo, kết nối không đồng nghĩa với truy cập tự do. Dữ liệu mở, dữ liệu dùng chung, dữ liệu cá nhân, dữ liệu quan trọng và dữ liệu cốt lõi có chế độ khai thác khác nhau. Cơ chế phí, giấy phép, API, ủy quyền và kiểm toán sẽ quyết định doanh nghiệp thực sự có thể xây gì trên từng nguồn dữ liệu.

Cuối cùng, RAG không chữa được mọi vấn đề. Truy xuất có thể lấy nhầm tài liệu, nguồn có thể đã hết hiệu lực, mô hình có thể bỏ qua bằng chứng hoặc suy diễn quá mức. Hệ thống vẫn cần quản trị dữ liệu, bộ đánh giá chuyên ngành, giám sát vận hành và con người chịu trách nhiệm ở các quyết định có rủi ro cao.

Nói ngắn gọn: Quyết định 1308 là một cam kết định hướng và hạ tầng dài hạn, không phải đơn đặt hàng có sẵn cho bất kỳ sản phẩm RAG nào.

## Tôi chọn xây phần bền hơn mô hình

Điều quan trọng nhất mà Quyết định 1308 mang lại cho tôi là một đường chân trời đủ dài. Văn bản không bảo tôi phải dùng RAG, nhưng xác nhận rằng bài toán biến dữ liệu thành tài nguyên có thể khai thác, kiểm chứng và bảo vệ sẽ còn là ưu tiên đến năm 2045.

Trong khoảng thời gian đó, tên mô hình, cơ sở dữ liệu vector và framework chắc chắn sẽ đổi nhiều lần. Nhu cầu tìm đúng tri thức, hiểu đúng ngữ cảnh, kiểm soát đúng quyền và trả lời có bằng chứng thì không biến mất.

Vì vậy, định hướng của tôi là xây hệ thống Tri thức AI theo nguyên tắc **ưu tiên dữ liệu, ưu tiên bằng chứng và không phụ thuộc một mô hình**. RAG là công nghệ chủ đạo ở thời điểm hiện tại; quản trị dữ liệu, truy xuất, đánh giá và khả năng kiểm chứng mới là năng lực tôi muốn tích lũy lâu dài.

## Tài liệu tham khảo

1. [Quyết định 1308/QĐ-TTg ngày 18/7/2026](https://vanban.chinhphu.vn/?docid=218908&pageid=27160) — Chiến lược dữ liệu quốc gia giai đoạn 2026–2030, tầm nhìn đến năm 2045.
2. [Phụ lục II của Quyết định 1308/QĐ-TTg](https://datafiles.chinhphu.vn/cpp/files/vbpq/2026/7/1308_qd-ttg_18072026_5-signed.pdf) — danh mục nhiệm vụ trọng tâm, cơ quan chủ trì và thời hạn.
3. [Quyết định 804/QĐ-TTg ngày 6/5/2026](https://vanban.chinhphu.vn/?docid=218027&pageid=27160) — danh mục bộ dữ liệu phục vụ phát triển AI trong các lĩnh vực thiết yếu.
4. [Luật Dữ liệu số 60/2024/QH15](https://xaydungchinhsach.chinhphu.vn/toan-van-luat-du-lieu-119250226145839949.htm) — cơ sở pháp lý về phát triển, quản trị, khai thác và bảo vệ dữ liệu.
5. [Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401) — Lewis và cộng sự, NeurIPS 2020.

*Thông tin chính sách trong bài được kiểm chứng ngày 10/8/2026.*
