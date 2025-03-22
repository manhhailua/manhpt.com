---
title: Thay đổi IP/DNS trên Ubuntu Desktop sử dụng Terminal
description: Để thay đổi IP/DNS của máy trạm chỉ có thể thao tác qua Terminal sau khi forward và kết nối đến SSH port của máy trạm từ máy làm việc.
authors: [manhpt]
tags: [dns, linux, network, ubuntu, workstation]
image: ./dns-concept-domain-name-system-decentralized-naming-system-computers-devices-services-other-resources-dns-concept-domain-109460557.jpg
---

![](./dns-concept-domain-name-system-decentralized-naming-system-computers-devices-services-other-resources-dns-concept-domain-109460557.jpg)

## Vấn đề là...

Ubuntu là một trong những distro phổ biến nhất của Linux. Ngoài Ubuntu Server thì Ubuntu Desktop cũng được anh em developer sử dụng rất nhiều. Do tính chất dễ sử dụng và ổn định nên team dự án của mình hiện tại đang sử dụng Ubuntu Desktop cho những máy trạm (workstation) đặt tại địa điểm, văn phòng của đối tác.

Thực trạng này đôi khi phát sinh yêu cầu phải thay đổi local IP và DNS của máy trạm cho phù hợp với địa điểm triển khai. Tuy nhiên, các máy trạm này lại không được kết nối màn hình mà chỉ được duy trì kết nối internet và kết nối từ xa qua Anydesk.

Để thực hiện yêu cầu thay đổi IP/DNS của máy trạm, team phát triển chỉ có thể thao tác thông qua Terminal sau khi forward và kết nối đến SSH port của máy trạm từ máy làm việc. Việc forward và kết nối SSH đến máy trạm qua Anydesk sẽ nằm trong bài viết khác.

<!-- truncate -->

## Để thay đổi IP

```shell
nmcli connection modify "Wired Connection 1" ipv4.addresses 192.168.1.101
```

## Để thay đổi DNS

```shell
nmcli connection modify "Wired Connection 1" ipv4.dns 8.8.8.8,8.8.4.4
```

## Để cập nhật thay đổi

```shell
systemctl restart NetworkManager.service
```

Trong bài viết có sử dụng `nmcli` để thực hiện thay đổi cấu hình của các network connection của NetworkManager. Tham khảo [nmcli reference](https://developer.gnome.org/NetworkManager/stable/nmcli.html) và [nmcli examples](https://developer.gnome.org/NetworkManager/stable/nmcli-examples.html).
