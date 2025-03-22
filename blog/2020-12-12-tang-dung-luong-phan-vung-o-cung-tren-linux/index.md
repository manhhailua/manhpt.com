---
title: Tăng dung lượng phân vùng ổ cứng trên linux
description: Phân vùng không tự động tăng dung lượng sau khi sizing ổ đĩa ảo (volume) nên ta phải thực hiện thêm dung lượng cho phân vùng (partition).
authors: [manhpt]
tags: [cloud, linux, partition, sizing, virtual machine, volume]
image: ./istock-1061856176.jpg
---

![](./istock-1061856176.jpg)

Trên các hệ thống hạ tầng cloud, sau khi sizing (bổ sung dung lượng) ổ đĩa ảo (volume), ta cần phải thực hiện thêm một vài lệnh đặc thù trên từng [phân vùng](/tags/partition/) ổ đĩa (partition) để hệ thống thực sự nhận diện được dung lượng mới thêm.

Chú ý: Trước khi cập nhật dụng lượng trên ổ đĩa có chứa dữ liệu quan trọng thì ta nên backup dữ liệu hoặc tạo snapshot cho ổ đĩa đó trên các hệ thống cloud mà có hỗ trợ tính năng snapshot.

<!-- truncate -->

## Các bước cơ bản

Sau đó, thực hiện cập nhật dung lượng phân vùng theo các bước sau:

1.  Việc tăng thêm dung lượng cho ổ đĩa ảo không đồng thời tăng dung lượng cho phân vùng bên trong nó. Do đó, ta cần phải kiểm tra xem phân vùng cần tăng thêm dung lượng có nằm bên trong ổ đĩa vừa được bổ sung dung lượng hay không.
2.  Thực hiện các câu lệnh đặc thù để tăng dung lượng cho các phân vùng dựa trên định dạng của phân vùng đó.

Nội dung bài viết hiện tại chỉ hướng dẫn cách tăng dung lượng phân vùng cho các sử dụng định dạng: xfs, ext4 trên các máy chủ ảo của AWS, GCP, Azure hoặc VMWare.

## Các bước chi tiết

Trong ví dụ sau, giả sử bạn đã tăng dung lượng ổ đĩa...

### 1. Kiểm tra định dạng của phân vùng cần tăng bằng câu lệnh `df -hT`

```shell
$ df -hT
```

Sau đây là kết quả mà bạn sẽ nhận được

```shell
$ df -hT
Filesystem      Type  Size  Used Avail Use% Mounted on
/dev/xvda1      ext4  8.0G  1.9G  6.2G  24% /
/dev/xvdf1      xfs   8.0G   45M  8.0G   1% /data
```

### 2. Kiểm tra phân vùng cần tăng dung lượng có nằm trong ổ đĩa đã được bổ sung dung lượng không bằng lệnh `lsblk`

```shell
$ lsblk
NAME    MAJ:MIN RM SIZE RO TYPE MOUNTPOINT
xvda    202:0    0  16G  0 disk
└─xvda1 202:1    0   8G  0 part /
xvdf    202:80   0  30G  0 disk
└─xvdf1 202:81   0   8G  0 part /data
```

Từ kết quả trên ta thấy:
- Ổ đĩa `/dev/xvda` có 1 phân vùng là `/dev/xvda1`. Trong khi dung lượng ổ đĩa là 16G thì dung lượng phân vùng chỉ có 8G nên có thể tăng dung lượng cho phân vùng `/dev/xvda1`.
- Ổ đĩa `/dev/xvdf` có 1 phân vùng là `/dev/xvdf1`. Trong khi dung lượng ổ đĩa là 30G thì dung lượng phân vùng chỉ có 8G nên có thể tăng dung lượng cho phân vùng `/dev/xvdf1`.

### 3. Thực hiện tăng dung lượng phân vùng bằng lệnh `growpart`

```shell
ubuntu@ip-172-31-13-xxx:~$ sudo growpart /dev/xvda 1
ubuntu@ip-172-31-13-xxx:~$ sudo growpart /dev/xvdf 1
```

#### Nếu phân vùng có định dạng `xfs`, dùng lệnh xfs_growfs:

```shell
ubuntu@ip-172-31-13-xxx:~$ sudo xfs_growfs -d /
ubuntu@ip-172-31-13-xxx:~$ sudo xfs_growfs -d /data
```

Nếu xfs_growfs chưa tồn tại thì cài đặt bằng cách:

```shell title="for debian/ubuntu-based"
ubuntu@ip-172-31-13-xxx:~$ sudo apt-get install xfs_growfs
```

```shell title="for centos/rehl-based"
ubuntu@ip-172-31-13-xxx:~$ sudo yum install xfs_growfs
```

#### Nếu phân vùng có định dạng `ext4`, dùng lệnh resize2fs:

```shell
ubuntu@ip-172-31-13-xxx:~$ sudo resize2fs /dev/xvda1
ubuntu@ip-172-31-13-xxx:~$ sudo resize2fs /dev/xvdf1
```

### Kiểm tra lại kết quả thay đổi với `df -h`

```shell
$ df -h
Filesystem       Size  Used Avail Use% Mounted on
/dev/xvda1        16G  1.9G  14G  12% /
/dev/xvdf1        30G   45M  30G   1% /data
```

Bài viết có tham khảo và dịch lại từ: [Extending a Linux file system after resizing a volume - Amazon Elastic Compute Cloud](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/recognize-expanded-volume-linux.html#extend-file-system)
