---
title: "OpenClaw tự host gặp cửa sổ rủi ro từ Axios: lúc này cần kiểm tra forensic ngay"
description: "Hướng dẫn kiểm tra forensic, IOC và các bước xử lý cho operator OpenClaw tự host nếu hệ thống từng install, update hoặc rebuild trong cửa sổ sự cố axios@1.14.1 và axios@0.30.4."
authors: [manhpt]
tags: [openclaw, security, npm, supply-chain, javascript, incident, vietnamese]
date: 2026-04-02
---

Nếu bạn đang chạy **OpenClaw** theo kiểu tự host và có bật **auto-update** hoặc một cơ chế cập nhật định kỳ tương tự, bạn nên **kiểm tra máy ngay lập tức**.

Với tôi, đây cũng không phải một rủi ro "của người khác": chính setup OpenClaw self-hosted của tôi cũng nằm trong nhóm cần audit và rà lại lịch sử cài đặt trong cửa sổ sự cố. Điều đó không tự động chứng minh máy của tôi đã bị compromise, nhưng đủ để biến việc này thành một cuộc kiểm tra bắt buộc chứ không còn là cảnh báo mang tính lý thuyết.

Bài này **không khẳng định official `openclaw` package đã được công khai xác nhận là độc hại**. Điểm cần quan tâm là khác: trong cửa sổ sự cố **Axios compromise** cuối tháng 3/2026, các hệ thống tự động cập nhật dependency có thể đã kéo phải package độc hại trong chuỗi phụ thuộc. Với một agent stack giữ nhiều secret và integration, đó là tình huống cần điều tra theo hướng forensic chứ không nên nhìn current state rồi kết luận vội.

<!-- truncate -->

## Điều gì đã xảy ra với Axios?

Theo issue công khai của dự án Axios và các phân tích kỹ thuật từ StepSecurity, JFrog, Snyk:

- Hai version độc hại được báo cáo là **`axios@1.14.1`** và **`axios@0.30.4`**
- **Không phải `1.14.0`**
- Hai version này kéo thêm **`plain-crypto-js@4.2.1`**
- Payload sử dụng `postinstall` để thả mã độc đa nền tảng cho macOS, Linux và Windows

Khung thời gian công khai hiện có cho thấy:

- `axios@1.14.1` được publish khoảng **00:21 UTC ngày 2026-03-31**
- `axios@0.30.4` được publish khoảng **01:00 UTC**
- các version độc hại bị gỡ khoảng **03:29 UTC**

Với operator, đây nên được xem là **cửa sổ forensic chính** để rà lại mọi lần `install`, `update`, `rebuild`, `deploy` hoặc recreate container: khoảng **00:21-03:29 UTC ngày 2026-03-31**.

Nếu một máy đã cài đúng các version đó trong cửa sổ này, bạn nên **xếp nó vào nhóm likely compromise / high risk** cho đến khi chứng minh được điều ngược lại.

## Khi nào nên coi là rủi ro cao ngay lập tức?

Hãy chuyển sang chế độ **high risk** ngay nếu có một trong các dấu hiệu sau:

- host, runner hoặc workstation đã `install` / `update` / `rebuild` trong khoảng **00:21-03:29 UTC ngày 2026-03-31**
- lockfile, log hoặc lịch sử cài đặt có **`axios@1.14.1`**, **`axios@0.30.4`** hoặc **`plain-crypto-js@4.2.1`**
- xuất hiện IOC trên filesystem hoặc network như bài liệt kê bên dưới
- máy giữ secret quan trọng: cloud credentials, bot tokens, SSH keys, CI secrets, `.env`

Nếu khớp các điều kiện trên, hướng xử lý thực tế là: **cô lập máy, điều tra, và rotate secrets**; đừng chờ đủ mọi xác nhận hoàn hảo mới hành động.

## Vì sao người dùng OpenClaw nên quan tâm ngay?

Tôi muốn tách rõ ba mệnh đề sau:

1. **Sự cố Axios là có thật**, với hai version bị nêu đích danh là `1.14.1` và `0.30.4`.
2. **Các package/advisory công khai có nhắc tới** `@shadanai/openclaw` và `@qqbrowser/openclaw-qbot`.
3. **Điều đó không tự động chứng minh official `openclaw` package bị xác nhận là độc hại.**

Vẫn có một lý do rất thực tế để các operator OpenClaw phải điều tra ngay:

- Trong source tree OpenClaw hiện tại, package chính phụ thuộc `@line/bot-sdk`
- Trong một manifest phát hành của `@line/bot-sdk` mà tôi kiểm tra, `axios` xuất hiện dưới `optionalDependencies` với dải version `^1.7.4`
- Trong một cây cài đặt OpenClaw mà tôi kiểm tra, `axios` hiện diện ở version **`1.14.0`**

Ba điểm trên **chỉ đủ để chứng minh dependency path là có thật**: `openclaw -> @line/bot-sdk -> axios`. Nó **không chứng minh** máy của bạn đã từng kéo `axios@1.14.1` trong quá khứ.

Nói ngắn gọn:

> OpenClaw có một đường phụ thuộc hợp lý dẫn tới Axios. Nếu hệ thống của bạn auto-update đúng vào cửa sổ sự cố, đó là một đường phơi nhiễm cần điều tra. Nhưng trạng thái filesystem hiện tại có thể không đủ để chứng minh lịch sử phơi nhiễm trong cửa sổ đó.

## Vì sao auto-update và self-hosted agent stack đặc biệt nguy hiểm?

Một web app thông thường bị ảnh hưởng bởi supply-chain attack đã tệ. Một **self-hosted agent stack** còn tệ hơn vì nó thường có:

- API keys của nhiều dịch vụ
- SSH keys hoặc cloud credentials
- token bot cho Telegram, Slack, Discord, LINE, v.v.
- quyền truy cập CI runner, cron host, home directory, workspace nội bộ
- automation chạy nền nên rất ít người quan sát trực tiếp lúc cài đặt

Nếu cơ chế auto-update của bạn có lúc chạy `npm install`, `pnpm install`, `npm update`, pull lại package mới, rebuild container, hoặc recreate một service mà không khóa dependency thật chặt, bạn có thể đã nhận payload chỉ vì một lần cập nhật định kỳ.

Đó là lý do nên nghiêng về hướng **assume breach** với các host đã cài package độc hại trong cửa sổ bị ảnh hưởng, thay vì tự trấn an bằng việc hiện tại `node_modules` trông có vẻ sạch.

## Vì sao lifecycle script nguy hiểm đến vậy?

Vấn đề không nằm ở việc app của bạn có `import axios` hay không. Vấn đề là **package manager lifecycle scripts** như `preinstall`, `install`, `postinstall` chạy **ngay khi package được cài**.

Trong sự cố này, phân tích công khai cho thấy payload được kích hoạt qua `postinstall` của `plain-crypto-js@4.2.1`. Tức là:

- bạn không cần chạy code của ứng dụng
- bạn không cần `require()` package đó
- chỉ cần quá trình cài dependency xảy ra là đủ để mã độc chạy

Với auto-update, đây là mô hình rủi ro cực xấu: compromise xảy ra ở thời điểm "bảo trì bình thường", thường là lúc không ai đang nhìn log.

## Bạn nên kiểm tra gì ngay bây giờ?

### 1. Rà lại lockfile và install logs

Ưu tiên kiểm tra:

- `package-lock.json`
- `pnpm-lock.yaml`
- `yarn.lock`
- log CI/CD
- shell history
- log auto-update service, cron, systemd timer, container rebuild pipeline

Các chuỗi cần tìm:

```bash
axios@1.14.1
axios@0.30.4
plain-crypto-js@4.2.1
```

Ví dụ:

```bash
grep -R -nE 'axios@1\\.14\\.1|axios@0\\.30\\.4|plain-crypto-js@4\\.2\\.1' .
grep -R -nE 'axios.*1\\.14\\.1|axios.*0\\.30\\.4|plain-crypto-js.*4\\.2\\.1' /var/log 2>/dev/null
```

Nếu bạn dùng npm:

```bash
npm ls axios 2>/dev/null
```

Nếu bạn dùng pnpm:

```bash
pnpm why axios
```

Nếu bạn dùng yarn:

```bash
yarn why axios
```

### 2. Kiểm tra IOC trên filesystem

#### Linux

```bash
ls -la /tmp/ld.py
find /tmp -maxdepth 2 -name 'ld.py' 2>/dev/null
```

#### macOS

```bash
ls -la /Library/Caches/com.apple.act.mond
```

#### Windows

```powershell
Test-Path "$env:PROGRAMDATA\wt.exe"
Test-Path "$env:PROGRAMDATA\system.bat"
Get-ItemProperty "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run" | Format-List
```

Trên Windows, hãy tìm đặc biệt:

- `%PROGRAMDATA%\wt.exe`
- `%PROGRAMDATA%\system.bat`
- `HKCU\Software\Microsoft\Windows\CurrentVersion\Run`

Nếu thấy key khả nghi như `MicrosoftUpdate` hoặc giá trị gọi tới batch/script lạ, hãy coi đó là tín hiệu mạnh của compromise.

### 3. Kiểm tra IOC ở lớp network

Tìm outbound connections, DNS queries, proxy logs, firewall logs liên quan tới:

- `sfrclak[.]com`
- `142.11.206.73`
- `142.11.206.73:8000`

Ví dụ:

```bash
grep -R -nE 'sfrclak\\.com|142\\.11\\.206\\.73' /var/log 2>/dev/null
```

Trên các môi trường có egress logs hoặc DNS logs tập trung, đây thường là nơi đáng tin hơn filesystem hiện tại.

## Một lưu ý quan trọng: trạng thái hiện tại có thể đánh lừa bạn

Ngay cả khi hôm nay bạn thấy:

- `axios` đang ở `1.14.0`
- không còn `plain-crypto-js` trong `node_modules`
- app vẫn chạy bình thường

thì điều đó **không đủ để kết luận máy an toàn**.

Lý do là các phân tích công khai đều nhấn mạnh payload có hành vi tự xóa và che giấu dấu vết. Thêm nữa, về mặt vận hành, một máy có thể đã:

- auto-update trong cửa sổ rủi ro
- chạy `postinstall`
- bị payload thực thi
- sau đó lại được update tiếp về version sạch hơn

Nên **current state không nhất thiết phản ánh historical exposure**. Đó là lý do log cài đặt, lockfile, CI log và network telemetry thường đáng tin hơn ảnh chụp filesystem hiện tại.

## Nên làm gì nếu host OpenClaw có khả năng nằm trong cửa sổ bị ảnh hưởng?

Tôi sẽ làm theo thứ tự này:

1. Cô lập host hoặc runner nghi ngờ bị ảnh hưởng.
2. Ưu tiên rà mọi `install` / `update` / `rebuild` diễn ra trong khoảng **00:21-03:29 UTC ngày 2026-03-31**.
3. Rà lockfile, install log, CI log để xác định có từng kéo `axios@1.14.1`, `axios@0.30.4`, hoặc `plain-crypto-js@4.2.1` hay không.
4. Kiểm tra IOC filesystem và network nêu trên.
5. Rotate toàn bộ secrets có thể đã từng hiện diện trên máy:
   - npm tokens
   - GitHub/GitLab tokens
   - cloud credentials
   - SSH keys
   - `.env` secrets
   - bot tokens cho các channel mà OpenClaw đang kết nối
6. Audit tất cả CI runners, builder, cron host, dev workstation nào có thể đã rebuild hoặc reinstall dependency trong cửa sổ sự cố.
7. Nếu có dấu hiệu rõ ràng, **rebuild máy từ known-good state**, không cố "lau sạch tại chỗ".

Với các OpenClaw deployment thực chiến, tôi nghĩ **CI runners và máy cá nhân của operator** mới là nơi đáng lo nhất, vì đó là nơi thường giữ nhiều quyền nhất.

## Tôi khuyên gì cho operator OpenClaw sau sự cố này?

Ngoài việc điều tra ngay, tôi nghĩ đây là lúc siết lại quy trình:

- khóa dependency bằng lockfile thực sự được kiểm soát
- hạn chế hoặc tắt auto-update mù
- dùng `--ignore-scripts` ở nơi phù hợp khi audit/reinstall
- tách bot tokens và cloud credentials khỏi máy build càng nhiều càng tốt
- chạy egress filtering cho CI runners
- coi mọi package mới publish trong vài giờ đầu là vùng rủi ro cao

Supply-chain attack khó ở chỗ nó lợi dụng đúng thứ chúng ta gọi là "bảo trì bình thường". Với những hệ như OpenClaw, nơi automation, background job và secret tập trung về cùng một host, mức độ nguy hiểm còn lớn hơn nhiều so với một app Node.js thông thường.

Vì vậy, kết luận của tôi khá thẳng:

> Nếu bạn đã cấu hình OpenClaw tự cập nhật, đừng chờ thêm xác nhận hoàn hảo mới hành động. Hãy điều tra ngay. Điều tra sớm rồi hóa ra an toàn vẫn tốt hơn là bỏ lỡ một compromise thật.

## Nguồn tham khảo

- [axios/axios issue #10604: axios@1.14.1 and axios@0.30.4 are compromised](https://github.com/axios/axios/issues/10604)
- [StepSecurity: axios Compromised on npm - Malicious Versions Drop Remote Access Trojan](https://www.stepsecurity.io/blog/axios-compromised-on-npm-malicious-versions-drop-remote-access-trojan)
- [JFrog Security Research: Cross-Platform Threat - Axios Package Compromise](https://research.jfrog.com/post/axios-compromise/)
- [Snyk advisory: Embedded Malicious Code in axios](https://security.snyk.io/vuln/SNYK-JS-AXIOS-15850650)
- [npm package `@line/bot-sdk` version `9.2.2`](https://www.npmjs.com/package/%40line/bot-sdk/v/9.2.2)
