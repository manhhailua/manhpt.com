---
title: 'Agent Skills sẽ biến mất, hay co lại thành một layer ổn định?'
slug: agent-skills-transitional-layer
authors: [manhpt]
tags: [openclaw, claude-code, ai-agent, automation, llm, technical]
date: 2026-04-15
description: 'Agent Skills trông giống một lớp quá độ khi LLM có kiến thức nhưng thiếu practical operational knowledge. Nhưng ngay cả khi model hấp thụ dần nhiều workflow, tôi tin skills không biến mất hoàn toàn mà sẽ co lại thành một layer mỏng nhưng rất bền.'
---

*Tôi nghĩ Agent Skills đang ở đúng một điểm rất thú vị của lịch sử AI ứng dụng. Chúng vừa giống một cái nạng tạm thời, vừa giống một lớp hạ tầng lâu dài. Tạm thời, vì model ngày càng giỏi hơn và sẽ hấp thụ dần nhiều thứ hôm nay còn phải viết ra ngoài. Lâu dài, vì có một nhóm tri thức vận hành mà tôi không tin nên bị nhét hết vào base model.*

<!-- truncate -->

## Agent Skills xuất hiện vì model biết nhiều, nhưng làm việc chưa đủ chắc

LLM hiện đại có một nghịch lý rất rõ.

- Chúng biết rất nhiều.
- Chúng giải thích rất tốt.
- Chúng suy luận ngày càng khá.
- Nhưng khi bước vào công việc thật, chúng vẫn thiếu một lớp mà tôi gọi là **practical operational knowledge**.

Đó không chỉ là kiến thức về thế giới. Đó là kiến thức kiểu:

- trong repo này phải đọc file nào trước,
- muốn verify thì chạy lệnh nào,
- khi nào nên dừng để hỏi người dùng,
- format báo cáo cuối ra sao,
- dùng tool nào trước tool nào sau,
- policy nào là hard constraint chứ không phải gợi ý.

Chính khoảng trống đó sinh ra Agent Skills, `AGENTS.md`, custom instructions, hooks, subagents, runbooks, và đủ loại prompt-software nằm ngoài model.

OpenAI mô tả Codex như một coding agent chạy task trong sandbox riêng, có thể làm nhiều task song song, đọc và sửa file, chạy test, và được hướng dẫn bằng `AGENTS.md` trong repo để biết cách navigate codebase, chạy command nào, và bám chuẩn dự án ra sao. Chỉ riêng chuyện `AGENTS.md` tồn tại như một first-class mechanism đã là tín hiệu rất rõ: model mạnh vẫn cần một lớp chỉ dẫn vận hành tách ra khỏi weights của nó.

Anthropic cũng đang đi đúng hướng đó với Claude Code. Tài liệu về subagents cho thấy họ xem việc tách bớt ngữ cảnh, giới hạn tool, và chuyên biệt hóa hành vi là một primitive nghiêm túc chứ không phải mẹo prompt tạm bợ. Nếu model đã tự đủ mọi thứ, sẽ không cần phải đầu tư hẳn vào lớp subagent, tool restriction, và delegation semantics như vậy.

Nói ngắn gọn, Agent Skills xuất hiện không phải vì model ngu. Chúng xuất hiện vì **kiến thức tổng quát** và **tri thức vận hành cục bộ** là hai thứ khác nhau.

## Skills thực chất là externalized procedural knowledge

Tôi thấy cách gọi đúng nhất cho skills là:

- **externalized procedural knowledge**,
- **operational memory**,
- hoặc **workflow packaging**.

Tức là ta lấy phần tri thức thủ tục, thứ tự hành động, guardrail, kinh nghiệm thực chiến, và đóng gói nó ra ngoài model dưới dạng có thể sửa nhanh, đọc nhanh, audit được.

Đây là giá trị thật của skills.

Một skill tốt không chỉ nói “hãy làm X”. Nó encode những thứ model rất khó tự suy ra ổn định:

1. **Entry point**: bắt đầu ở đâu.
2. **Decision policy**: khi nào chọn nhánh A, khi nào chọn nhánh B.
3. **Verification loop**: phải kiểm chứng bằng gì trước khi báo xong.
4. **Failure handling**: lỗi kiểu này thì retry, kiểu kia thì dừng.
5. **Output contract**: trả lời theo format nào để downstream dùng tiếp được.

Đó là lý do nhiều hệ agent ngày nay trông ngày càng giống phần mềm hơn là prompt đơn lẻ. Skills không chỉ thêm “thông tin”. Chúng thêm **cấu trúc thực thi**.

Và vì nằm ngoài model, skills có vài lợi thế mà weights không có:

- sửa trong vài phút,
- review bằng git diff,
- áp dụng theo từng repo hoặc từng team,
- rollback khi viết sai,
- audit được ai đã đổi policy vận hành.

Đây là một điểm tôi nghĩ nhiều người đánh giá thấp. Một phần lớn giá trị của skills không nằm ở chuyện model “không biết”, mà nằm ở chuyện **tổ chức cần một nơi để ghi tri thức vận hành dưới dạng có thể quản trị**.

## Phần nào sẽ bị model hấp thụ dần theo thời gian?

Tôi tin khá nhiều thứ trong Agent Skills sẽ bị model hấp thụ.

Cụ thể là các phần có tính lặp cao, phổ quát cao, và ít phụ thuộc local state.

### 1. Workflow phổ biến sẽ bị nén vào model

Ví dụ:

- đọc repo trước khi sửa,
- chạy test trước khi kết luận,
- tách research khỏi implementation,
- ưu tiên diff nhỏ,
- báo blocker rõ ràng thay vì nói chung chung.

Những pattern này lặp đi lặp lại trên rất nhiều codebase và toolchain. Một khi các model được train bằng nhiều trajectory agentic hơn, reinforcement learning tốt hơn, và được fine-tune trên dữ liệu vận hành thực tế, chúng sẽ nội hóa ngày càng nhiều best practice kiểu đó.

Nói cách khác, phần “generic craftsmanship” của skills rất dễ bị hút ngược vào model.

### 2. Prompt boilerplate sẽ chết dần

Rất nhiều skill hiện nay thực ra chỉ là prompt glue viết dài dòng cho các điều gần như ai cũng muốn:

- đừng bịa fact,
- đọc context trước,
- verify rồi hãy báo xong,
- giữ output gọn,
- ưu tiên an toàn.

Những thứ này về lâu dài khó có lý do để tồn tại thành cả một file riêng nếu model đã được productize đủ tốt. Nó sẽ giống evolution tự nhiên của compiler hay framework, những thứ từng phải viết tay rất nhiều rồi sau đó thành default behavior.

### 3. Một phần kỹ năng tool use sẽ trở thành mặc định

Nếu vendor tiếp tục productize agent theo kiểu OpenAI đang làm với Codex, tức là task chạy trong environment tách biệt, có logs, có verification, có support cho repo guidance, thì một phần skill “cách làm việc với tool” cũng sẽ được absorb.

Model tương lai nhiều khả năng không cần được nhắc lại mỗi lần rằng phải:

- đọc terminal logs,
- kiểm tra test,
- commit rõ nghĩa,
- hoặc tôn trọng một số convention phổ biến.

## Nhưng phần nào sẽ rất khó biến mất?

Đây là chỗ tôi không đồng ý với luận điểm “skills chỉ là lớp quá độ rồi sẽ chết sạch”.

Tôi nghĩ chỉ phần generic mới chết bớt. Phần gắn với hệ thống thật thì rất khó mất hoàn toàn.

### 1. Skills gắn với tool và environment cục bộ

Base model không thể luôn biết:

- repo của bạn tổ chức thế nào hôm nay,
- script nào mới đổi sáng nay,
- lệnh build nào đang broken ở branch hiện tại,
- service nội bộ nào đang bắt buộc qua VPN,
- convention review của team bạn tuần này là gì.

Đó là tri thức động, cục bộ, và sống cùng environment. Nếu nhét hết vào weights thì đến lúc deploy model nó đã cũ.

Nơi phù hợp nhất cho loại tri thức này vẫn là file, config, runbook, skill, hoặc một lớp memory ngoài model.

### 2. Skills gắn với policy và trust boundary

Đây là phần rất bền.

Một tổ chức không chỉ muốn model “giỏi”. Họ muốn model hành xử đúng trong boundary của họ:

- được phép gửi email hay không,
- được phép push thẳng vào `main` hay không,
- khi nào phải xin phê duyệt,
- dữ liệu nào không được đụng,
- tool nào bị deny ở môi trường production.

Những thứ này không nên train vào base model như một chân lý chung, vì nó khác nhau giữa từng tổ chức, từng repo, từng thời điểm.

Ví dụ rất đời là có team cho agent mở pull request nhưng cấm push thẳng vào `main`, có team cho đọc log production nhưng cấm chạm dữ liệu khách hàng, và có team bắt buộc mọi hành động như gửi email hay chạy lệnh nhạy cảm đều phải qua một bước approval riêng. Những boundary kiểu đó không phải tri thức phổ quát, mà là policy cục bộ.

Nói cách khác, **policy không phải là kiến thức phổ quát**. Nó là cấu hình vận hành. Và cấu hình vận hành thì hợp sống ngoài model hơn nhiều.

### 3. Skills gắn với organizational memory

Mỗi team đều có những bài học đắt giá kiểu:

- bug class nào hay lặp lại,
- migration nào rất dễ phá dữ liệu,
- thư mục nào “nhìn vô hại nhưng không được sửa bừa”,
- checklist release nào bắt buộc phải đi đủ.

Đây là loại tri thức có giá trị cực cao nhưng quá đặc thù để kỳ vọng base model nào cũng biết.

Nếu có bị hấp thụ, nó cũng chỉ hấp thụ được các pattern trừu tượng. Còn bản thể cụ thể của nó vẫn phải được externalize.

### 4. Skills là lớp quản trị được, còn model thì không

Đây là điểm thực dụng nhất.

Nếu một skill sai, bạn sửa một file.
Nếu một skill nguy hiểm, bạn diff, review, revert.
Nếu một policy đổi, bạn commit mới.

Còn nếu cùng logic đó nằm trong weights của model, bạn gần như không có cấp độ kiểm soát tương đương.

Với đội ngũ làm việc nghiêm túc, khả năng quản trị, audit, và rollback thường quan trọng không kém raw intelligence. Vì thế tôi không tin enterprises sẽ tự nguyện bỏ lớp skill/config/rule ngoài model chỉ để “mọi thứ magical hơn”. Magical thì vui, nhưng không ai muốn magical trong pipeline release hoặc trong production incident.

## Vậy Agent Skills sẽ chết, co lại, hay ổn định thành một layer?

Quan điểm của tôi là:

> **Agent Skills sẽ không chết hẳn. Chúng sẽ co lại, mỏng đi, nhưng trở thành một layer ổn định trong agent stack.**

Tôi kỳ vọng ba chuyển động xảy ra cùng lúc.

### Chuyển động 1: skill phình to kiểu prompt dump sẽ chết bớt

Các file dài hàng trăm dòng chỉ để dạy model những điều phổ quát sẽ dần bị thay thế bởi model tốt hơn, product semantics tốt hơn, và default behavior tốt hơn.

### Chuyển động 2: skill tốt sẽ dịch từ “nhắc model” sang “khai báo hệ thống”

Skill tương lai sẽ ít giống motivational prompt hơn, và giống:

- policy file,
- workflow contract,
- environment guide,
- task router,
- org memory capsule,
- approval boundary.

Tức là nó sẽ bớt mang tính mẹo, và mang tính hạ tầng hơn.

### Chuyển động 3: ranh giới giữa skill, config, memory và code sẽ mờ dần

Thứ hôm nay gọi là “Agent Skill” có thể ngày mai tách thành nhiều lớp:

- một ít nằm trong model behavior,
- một ít nằm trong tool metadata,
- một ít nằm trong repo instruction files như `AGENTS.md`,
- một ít nằm trong memory store,
- một ít nằm trong workflow engine hoặc hook.

Tên gọi có thể thay đổi. Nhưng nhu cầu externalize tri thức vận hành thì vẫn còn.

## Kết luận

Nếu nhìn Agent Skills chỉ như một mánh prompt để vá chỗ yếu của LLM hiện tại, bạn sẽ kết luận vòng đời của nó ngắn.

Nếu nhìn kỹ hơn, bạn sẽ thấy skills đang gánh hai vai trò khác nhau:

1. **bù cho phần model chưa đủ trưởng thành**, và
2. **làm lớp mang tri thức cục bộ, policy, memory, và workflow có thể quản trị**.

Vai trò thứ nhất sẽ co lại rất mạnh.
Vai trò thứ hai thì tôi tin là còn rất lâu.

Vì thế, câu trả lời của tôi là:

- **Agent Skills không bất tử dưới dạng hiện tại.**
- **Nhưng chúng cũng không phải công nghệ một lần rồi bỏ.**
- **Chúng sẽ tiến hóa từ prompt wrapper thành một lớp operational interface ổn định giữa model và thế giới thật.**

Và thành thật mà nói, đó mới là tương lai hợp lý.

Model nên học phần phổ quát.
Còn phần cục bộ, rủi ro, thay đổi liên tục, và cần audit, tốt hơn hết là cứ để nó sống ở ngoài.

## Nguồn tham khảo

- OpenAI, *Introducing Codex*: [https://openai.com/index/introducing-codex/](https://openai.com/index/introducing-codex/)
- OpenAI Developers, *Delegate to Codex in the cloud*: [https://developers.openai.com/codex/cloud](https://developers.openai.com/codex/cloud)
- Anthropic, *Claude Code Subagents*: [https://code.claude.com/docs/en/sub-agents](https://code.claude.com/docs/en/sub-agents)
- OpenClaw docs, *Standing orders*: [https://docs.openclaw.ai/automation/standing-orders](https://docs.openclaw.ai/automation/standing-orders)
- OpenClaw docs, *Hooks*: [https://docs.openclaw.ai/automation/hooks](https://docs.openclaw.ai/automation/hooks)
