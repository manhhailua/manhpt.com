---
title: 'Vì sao tôi không còn dùng Claude làm backend delegate cho OpenClaw'
description: 'Sau khi bị khóa 2 tài khoản Claude vì dùng OpenClaw để delegate task cho Claude Code, tôi đọc lại chính sách và điều khoản của Anthropic/OpenAI và đi đến một kết luận vận hành khá rõ: Claude mạnh, nhưng hợp hơn để dùng trực tiếp; còn nếu muốn dựng harness hay agent runtime, OpenClaw + Codex/OpenCode hiện thực dụng hơn nhiều, nhất là khi xét tới chi phí flat-rate của ChatGPT Plus.'
authors: [manhpt]
tags: [claude-code, openclaw, ai-agent, automation, llm, technical]
image: ./claude-vs-codex-harness.webp
date: 2026-03-27
---

![Claude, Codex và bài học thực chiến khi dùng harness](./claude-vs-codex-harness.webp)

*Đây không phải một bài so benchmark giữa Claude và Codex. Đây là một bài học vận hành. Sau khi bị khóa 2 tài khoản Claude — một Pro và một Max X20 — vì dùng OpenClaw để delegate task cho Claude Code, tôi phải đọc lại chính sách, điều khoản và cách mỗi bên đang productize coding agent của họ. Kết luận rút ra khá rõ: Claude vẫn rất mạnh, nhưng không còn là lựa chọn tôi muốn đặt sau một lớp harness. Nếu muốn làm việc theo kiểu agent runtime, tôi tin OpenClaw + Codex/OpenCode thực dụng hơn ở thời điểm hiện tại.*

<!-- truncate -->

## Bắt đầu từ một vấn đề rất thực tế

Trong một thời gian, tôi dùng OpenClaw như một lớp orchestration để giao việc cho nhiều mô hình coding khác nhau. Về mặt kỹ thuật, điều này rất hấp dẫn: agent nhận task, delegate xuống backend phù hợp, lấy kết quả về, tiếp tục loop, rồi ghép thành workflow thực tế.

Trên lý thuyết, Claude Code có vẻ là ứng viên sáng giá cho việc đó. Nó mạnh, hiểu code tốt, chất lượng đầu ra cao, và khi dùng trực tiếp thì trải nghiệm nhìn chung rất ổn.

Nhưng sau một thời gian dùng **OpenClaw để delegate task cho Claude Code**, tôi bị khóa **2 tài khoản Claude**:

- **1 tài khoản Claude Pro**
- **1 tài khoản Claude Max X20**

Từ đó, tôi buộc phải nhìn câu chuyện này theo một góc khác:

> Một mô hình rất mạnh chưa chắc là một backend tốt cho harness.

Đây là điểm mà nhiều người làm agent dễ bỏ qua. Họ thường nhìn vào capability trước, rồi mới nghĩ đến policy, distribution, và operational fit. Nhưng thực tế vận hành thường không tha cho thứ tự ưu tiên đó.

## Anthropic đang gửi tín hiệu gì?

Điều quan trọng ở đây là tôi không chỉ dựa vào cảm giác “họ khó tính hơn”. Khi đọc lại **chính sách và điều khoản công khai** của Anthropic, có thể thấy một pattern khá rõ: họ đang **rất cẩn thận với cách Claude và Claude Code được dùng trong môi trường agentic**.

### 1. Anthropic có chính sách riêng cho chuyện dùng agent

Help Center của Claude có bài **“Using Agents According to Our Usage Policy”**. Chỉ riêng việc có một bài riêng cho chủ đề này đã là một tín hiệu: Anthropic không xem “agent” như một biến thể nhỏ của chatbot, mà là một lớp sử dụng cần policy riêng.

Trong bài đó, Anthropic nhấn mạnh rằng mọi use case agent và agentic features vẫn phải tuân thủ Usage Policy, đồng thời liệt kê nhiều vùng cấm rõ ràng như:

- scaled abuse
- tạo hoặc quản lý nhiều account để né safeguards
- tự động hóa các hành vi gây hại, lừa đảo hoặc thao túng
- truy cập hay chỉnh sửa hệ thống, tài khoản hoặc dữ liệu mà không được phép

Tất nhiên, các điều khoản này không trực tiếp ghi câu “không được dùng OpenClaw để delegate task cho Claude Code”. Nhưng vấn đề là ở **stance vận hành**: Anthropic đang nhìn agentic use với mức độ cảnh giác cao, và có vẻ đánh giá rất gắt các pattern có mùi harness, automation layer, hoặc bypass product boundary.

### 2. Claude Code đang được thiết kế theo hướng autonomy có kiểm soát — nhưng trong sân của Anthropic

Anthropic gần đây liên tục đẩy các tính năng như:

- auto mode
- sandboxing
- admin controls
- managed policy settings
- compliance API cho business plans

Điều này cho thấy họ không phản đối autonomy. Ngược lại, họ đang đầu tư mạnh vào nó.

Nhưng autonomy mà Anthropic muốn là kiểu:

- autonomy trong sandbox của họ
- autonomy trong policy framework của họ
- autonomy trong product boundary mà họ kiểm soát được

Đây là khác biệt rất quan trọng.

Một vendor có thể hoàn toàn ủng hộ agent, nhưng lại **không muốn agent đó chạy qua một harness do bên thứ ba điều phối** theo cách làm mờ ranh giới giữa interactive use, subscription use, scripting, và delegated automation.

### 3. Tín hiệu thực chiến của tôi khớp với hướng policy đó

Tôi không có bằng chứng để khẳng định Anthropic “ban tất cả harness”. Nhưng tôi có một bằng chứng thực chiến đủ mạnh để đổi cách vận hành của mình:

- Tôi đã bị khóa **2 tài khoản Claude**
- Cả hai đều xảy ra sau khi dùng **OpenClaw để delegate task cho Claude Code**

Khi một pattern vừa **không được product page khuyến khích rõ ràng**, vừa **đi ngược với tín hiệu chính sách ngày càng chặt**, lại vừa **đã khiến mình trả giá thật**, thì với tôi, đó không còn là vùng xám đáng để tiếp tục thử vận may nữa.

## OpenAI đang productize Codex theo hướng hoàn toàn khác

Nếu đọc các **chính sách, điều khoản và trang sản phẩm chính thức** của OpenAI về Codex, cảm giác gần như ngược hẳn.

### 1. OpenAI mô tả rất rõ Codex là coding agent để pair, delegate và automate

Trong bài **“Using Codex with your ChatGPT plan”**, OpenAI viết rất thẳng:

- Codex là **AI coding agent**
- có thể **pair** trong terminal, IDE hoặc app
- có thể **delegate work for it to complete in the cloud**
- có thể **run in the background**
- hỗ trợ **automatic code review**
- có app với **multiple codex agents in parallel**, worktree support, skills, automations, và git functionality

Đây không còn là cách nói “assistant giúp code”. Đây là mô tả của một **agent runtime chính danh**.

### 2. OpenAI công khai support subscription-based access cho Codex

Chính trang chính thức của OpenAI về Codex và bài Help Center **“Using Codex with your ChatGPT plan”** cũng ghi khá rõ rằng **Codex được include trong ChatGPT Plus, Pro, Business, Enterprise/Edu**. Nghĩa là Codex không chỉ là sản phẩm API trả theo token, mà đã được đưa vào lớp subscription product thật sự.

Ở trang **Authentication – Codex**, OpenAI còn mô tả rõ:

- **sign in with ChatGPT** cho subscription access
- **sign in with API key** cho usage-based access
- **Codex cloud requires signing in with ChatGPT**
- CLI và IDE extension hỗ trợ cả hai đường đăng nhập

Quan trọng hơn, docs còn nêu rõ rằng API key authentication được **recommend cho programmatic Codex CLI workflows**, ví dụ **CI/CD jobs**.

Nói ngắn gọn: OpenAI không chỉ “chịu đựng” harness hay automation. Họ đang **productize nó công khai**.

### 3. Stance này hợp với OpenClaw hơn rất nhiều

OpenClaw là một agent runtime. Một khi đã chấp nhận logic của OpenClaw, bạn gần như chắc chắn sẽ muốn những thứ sau:

- delegate task
- spawn sub-agents
- chạy background jobs
- giữ memory và state qua thời gian
- ghép workflow thành nhiều lớp
- điều phối giữa model lớn và model nhỏ

Với một vendor đang công khai nói về:

- cloud delegation
- automations
- background execution
- parallel agents
- ChatGPT subscription access cho Codex

thì rõ ràng **độ khớp vận hành** sẽ cao hơn nhiều.

## Khác biệt lớn nhất không phải capability, mà là product boundary

Đây là điểm tôi thấy nhiều người vẫn chưa nhìn ra đủ rõ.

Claude vs Codex không chỉ là so:

- model nào code tốt hơn
- model nào reasoning ổn hơn
- output nào đẹp hơn

Câu hỏi thực tế hơn là:

> Vendor này muốn sản phẩm của họ được dùng theo kiểu nào?

### Với Anthropic
Tín hiệu hiện tại cho tôi cảm giác là:

- Claude / Claude Code rất mạnh
- nhưng product boundary được giữ rất chặt
- đặc biệt với các pattern giống harness hoặc delegated worker đứng sau một orchestration layer

### Với OpenAI
Tín hiệu hiện tại lại là:

- Codex được thiết kế để trở thành coding agent chính danh
- pair được
- delegate được
- chạy cloud được
- tự động hóa được
- có docs auth, SDK, app server, app, CLI, IDE path khá rõ

Vì thế, nếu mục tiêu của bạn là **dùng AI trực tiếp**, Claude vẫn rất đáng dùng.

Nhưng nếu mục tiêu của bạn là **dựng một hệ thống agent có orchestration, delegation và background execution**, thì câu hỏi nên là:

> mô hình nào hợp với workflow này về mặt product boundary và policy hơn?

Ở thời điểm hiện tại, câu trả lời của tôi là: **Codex/OpenCode hợp hơn Claude.**

## Vì sao tôi khuyên: Claude dùng trực tiếp, còn OpenClaw nên ghép với Codex/OpenCode

### Claude nên dùng trực tiếp khi:

- bạn muốn pair programming tương tác
- bạn đang ngồi trong loop trực tiếp với model
- bạn muốn tận dụng chất lượng reasoning và code generation của Claude trong một product boundary do Anthropic kiểm soát
- bạn không cần biến nó thành worker phía sau một runtime khác

Nói đơn giản: Claude hợp làm **đối tác trực tiếp**, không phải **backend delegate mặc định**.

### OpenClaw + Codex/OpenCode hợp hơn khi:

- bạn muốn delegate task
- bạn muốn orchestration nhiều agent
- bạn muốn background execution
- bạn muốn automation layer bền hơn về policy fit
- bạn muốn một đường đi rõ hơn giữa local tool, cloud task, app, CLI và subscription access

Về mặt thực dụng, đây là combo tôi thấy hợp lý hơn nhiều cho một agent runtime sống cùng công việc thật.

## Lợi thế bị đánh giá thấp: chi phí flat-rate của ChatGPT Plus

Một điểm nữa mà tôi thấy nhiều người bỏ qua là **chi phí**.

Khi dùng OpenClaw với hệ OpenAI/Codex theo đường **ChatGPT Plus trở lên**, bạn có một lợi thế rất thực tế: **chi phí gần với flat-rate hơn và dễ dự đoán hơn** so với việc phải cân từng tác vụ delegated dưới logic mơ hồ của một subscription không thật sự thân thiện với harness.

Điều này quan trọng vì khi đã đi theo hướng agent runtime, usage pattern sẽ rất khác chat thông thường:

- task nhiều hơn
- context dài hơn
- agent gọi qua lại nhiều hơn
- background work xuất hiện thường xuyên hơn
- tổng mức sử dụng không còn giống một người chat tay nữa

Trong bối cảnh đó, một subscription path được productize rõ cho coding agent sẽ tạo ra **predictability** tốt hơn. Với solo builder, indie hacker hoặc team nhỏ, predictability về cost đôi khi còn quan trọng ngang raw capability.

### Nói thẳng hơn
Nếu một hệ thống cho phép bạn:

- dùng OpenClaw để điều phối
- dùng Codex/OpenCode để nhận task delegated
- tận dụng subscription ChatGPT Plus/Pro như một lớp chi phí dễ đoán hơn

thì đây là một tổ hợp rất mạnh về mặt vận hành.

Không phải lúc nào nó cũng cho output đẹp nhất. Nhưng rất có thể nó cho ra **hệ thống sống được lâu hơn**.

## Kết luận: đừng chỉ hỏi model nào mạnh hơn

Bài học tôi rút ra sau câu chuyện bị khóa 2 tài khoản Claude là thế này:

> Khi dựng agent runtime, câu hỏi quan trọng không chỉ là model nào mạnh hơn. Câu hỏi quan trọng hơn là vendor nào thực sự muốn sản phẩm của họ được dùng theo cách bạn đang dùng.

Ở thời điểm hiện tại, tôi nhìn thấy:

- **Anthropic**: rất mạnh, nhưng ngày càng rõ là muốn autonomy diễn ra trong boundary họ kiểm soát chặt
- **OpenAI**: đang productize Codex theo đúng hướng pair + delegate + automate + cloud + subscription

Vì vậy, quan điểm vận hành của tôi là:

- **Claude rất tốt, nhưng nên dùng trực tiếp**
- **OpenClaw + Codex/OpenCode phù hợp hơn cho delegate tasks**
- Và nếu xét thêm **chi phí flat-rate / predictable cost**, tổ hợp dùng **OpenClaw với ChatGPT Plus trở lên** lại càng đáng cân nhắc

Nếu mục tiêu là xây một hệ thống AI làm việc thật, chứ không chỉ demo đẹp, thì policy fit và product boundary thường quan trọng hơn benchmark. Tôi đã học bài đó theo cách hơi đắt.

---

## Chính sách và nguồn tham khảo gốc

### Anthropic
- Anthropic Help Center — *Using Agents According to Our Usage Policy*  
  [https://support.claude.com/en/articles/12005017-using-agents-according-to-our-usage-policy](https://support.claude.com/en/articles/12005017-using-agents-according-to-our-usage-policy)
- Anthropic — *Usage Policy Update*  
  [https://www.anthropic.com/news/usage-policy-update](https://www.anthropic.com/news/usage-policy-update)
- Anthropic — *Updates to our Consumer Terms*  
  [https://www.anthropic.com/news/updates-to-our-consumer-terms](https://www.anthropic.com/news/updates-to-our-consumer-terms)
- Anthropic — *Claude Code auto mode: a safer way to skip permissions*  
  [https://www.anthropic.com/engineering/claude-code-auto-mode](https://www.anthropic.com/engineering/claude-code-auto-mode)
- Anthropic — *Making Claude Code more secure and autonomous with sandboxing*  
  [https://www.anthropic.com/engineering/claude-code-sandboxing](https://www.anthropic.com/engineering/claude-code-sandboxing)

### OpenAI
- OpenAI — *Terms of Use*  
  [https://openai.com/policies/row-terms-of-use/](https://openai.com/policies/row-terms-of-use/)
- OpenAI — *Usage Policies*  
  [https://openai.com/policies/usage-policies/](https://openai.com/policies/usage-policies/)
- OpenAI — *Using ChatGPT agent in line with our policies*  
  [https://openai.com/policies/using-chatgpt-agent-in-line-with-our-policies/](https://openai.com/policies/using-chatgpt-agent-in-line-with-our-policies/)
- OpenAI Help Center — *Using Codex with your ChatGPT plan*  
  [https://help.openai.com/en/articles/11369540-using-codex-with-your-chatgpt-plan](https://help.openai.com/en/articles/11369540-using-codex-with-your-chatgpt-plan)
- OpenAI Developers — *Authentication – Codex*  
  [https://developers.openai.com/codex/auth](https://developers.openai.com/codex/auth)

---

*Bài viết này phản ánh quan sát và trải nghiệm vận hành cá nhân của tác giả tại thời điểm viết bài. Policy và product boundary của các nhà cung cấp AI có thể thay đổi theo thời gian; vì vậy nếu bạn định build agent trên bất kỳ dịch vụ nào, hãy đọc kỹ docs và điều khoản hiện hành trước khi đưa nó vào workflow thật.*
