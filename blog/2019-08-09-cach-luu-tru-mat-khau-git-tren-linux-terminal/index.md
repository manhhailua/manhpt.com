---
title: Cách lưu trữ mật khẩu git trên linux terminal
description: Cách lưu trữ mật khẩu git trên linux terminal. Tự động ghi nhớ mật khẩu git trên Ubuntu và linux. Git Credential Storage. Store và Cache.
authors: [manhpt]
tags: [git, git password, gitlab, remember password]
image: ./5_password-best-practices_unique-passwords_authentication-100768646-large.jpg
---

![](./5_password-best-practices_unique-passwords_authentication-100768646-large.jpg)

## Vấn đề là...

Nếu bạn đã từng sử dụng git trên "cửa sổ dòng lệnh" (terminal) của windows, linux hay macOS, bạn sẽ thấy rằng mật khẩu git của chúng ta được lưu lại tự động. Sau đó, chúng ta chỉ cần fetch - push - pull bình thường. Không cần nhập lại username và password của git nữa. Hơi tiếc là Ubuntu nói riêng và linux nói chung không có tính năng này. Dĩ nhiên chúng ta có thể cài đặt thêm phần mềm bên thứ 3 để có được tính năng tương tự. Mmình chưa thử và cũng ko tin tưởng để thử... lol.

## Giải pháp

Sau đây là một thủ thuật nhỏ và cực kỳ đơn giản để bạn có thể quên đi việc bị hỏi username và password liên tục mỗi khi `git fetch`. Đó là sử dụng [git credential storage](https://git-scm.com/book/en/v2/Git-Tools-Credential-Storage) chỉ với một câu lệnh duy nhất.

```shell
git config --global credential.helper store
```

- `store` mode: chế độ này lưu thông tin đăng nhập của bạn dưới dạng plain-text mặc định trong file `~/.my-credentials`. Bạn sẽ chỉ phải nhập lại mật khẩu khi bạn đã thay đổi mật khẩu trên git server. Cách này không được bảo mật cho lắm vì mật khẩu được lưu cứng dưới dạng không mã hoá. Do đó, ít nhất các bạn cũng nên sử dụng personal access token thay cho mật khẩu, ví dụ: [github personal access token](https://github.com/settings/tokens), [gitlab personal access token](https://gitlab.com/profile/personal_access_tokens)... - lúc nào mà nhỡ có bị lộ thì revoke cái là xong.

```shell
git config --global credential.helper cache
git config --global credential.helper cache '--timeout 30000'
```

- `cache` mode: chế độ này thì an toàn hơn do mật khẩu của bạn sẽ được lưu trong RAM thay vì file cứng và dĩ nhiên là có timeout - mặc định là 15 phút (900 giây). Bạn có thể tuỳ ý thay đổi thời gian timeout sao cho phù hợp với nhu cầu. Mình khuyến cáo nên sử dụng cách này.

## Kết luận

Trong thực tế, việc sử dụng [private key](https://help.github.com/en/articles/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent) vẫn tối ưu và bảo mật hơn so với trực tiếp lưu trữ mật khẩu, nhưng việc setup không đơn giản như trên. Các đồng dâm tuỳ ý chọn lựa nhé.
