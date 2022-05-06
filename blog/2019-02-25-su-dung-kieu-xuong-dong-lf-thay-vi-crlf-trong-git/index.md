---
title: Sử dụng kiểu xuống dòng LF thay vì CRLF trong Git
description: Loại bỏ sự đau đầu khi làm việc với git auto CRLF. Sử dụng LF làm mặc định thay vì CRLF và ngăn cản tự động chuyển LF thành CRLF.
authors: [manhpt]
tags: [git, crlf, lf]
image: ./crlf.png
---

![](./crlf.png)

## Vấn đề là...

Không ít lần project có cấu hình eslint gặp lỗi `Expected linebreaks to be 'LF' but found 'CRLF'`. Lỗi này thực sự dẫn đến sự bế tắc khi lần đầu gặp phải. Tại sao lập trình trên windows cứ hay gặp mấy vấn đề dễ gây bối rối như vậy? Shit… chê tí thôi chứ dùng MacOS hay Linux thì đừng mơ chơi đc PUBG Mobile giả lập.

```
git config --global core.autocrlf false
git config --global core.eol lf
```

Gõ 2 dòng lệnh trên vào bất cứ CLI tool nào bạn có (powershell, cmd, terminal…). Done!

## Giải ngố 1 chút

- `core.autocrlf` là để tự động sử dụng CRLF cho các file mới được tạo hoặc sau khi `git add`
- `core.eol` là để set mặc định kiểu xuống dòng cho Git
- `--global` thì bạn sẽ setup cấu hình Git trên toàn hệ thống
- Còn nếu muốn apply setting đặc dị này cho từng project thì có thể dùng file `.gitattributes`

## Tham khảo

1. https://help.github.com/en/articles/dealing-with-line-endings
1. https://stackoverflow.com/questions/37826449/expected-linebreaks-to-be-lf-but-found-crlf-linebreak-style
1. https://stackoverflow.com/questions/1552749/difference-between-cr-lf-lf-and-cr-line-break-types
