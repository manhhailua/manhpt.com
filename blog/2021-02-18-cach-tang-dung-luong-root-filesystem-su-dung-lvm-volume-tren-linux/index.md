---
title: Cách tăng dung lượng root filesystem sử dụng LVM volume trên linux
description: LVM tự động tăng dung lượng sau khi sizing nên ta phải thực hiện thêm dung lượng cho LVM từ phân vùng (partition).
authors: [manhpt]
tags: [disk, drive, logical volume manager, lvm, lvm volume, partition, volume]
image: ./istock-1061856176.jpg
---

![](./istock-1061856176.jpg)

Mình đã có một bài viết về cách [tăng dung lượng phân vùng ổ cứng trên linux](../2020-12-12-tang-dung-luong-phan-vung-o-cung-tren-linux/index.md). Nhưng có một trường hợp mà bài viết chưa nói đến là khi bạn sử dụng LVM. LVM cho phép bạn tạo, thay đổi dung lượng hoặc xóa phân vùng trong hệ thống mà không cần phải khởi động lại. Để tăng dung lượng cho LVM volume thì bạn có thể làm theo các bước sau:

## 1. Xác định phân vùng đĩa cứng chứa LVM volume

Trước tiên cần sử dụng lệnh `lsblk` để xem cấu trúc các phân vùng và ổ đĩa hiện tại.

```shell
$ lsblk
NAME          MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
sr0            11:0    1 1024M  0 rom
vda           252:0    0   30G  0 disk
├─vda1        252:1    0    1G  0 part /boot
└─vda2        252:2    0   29G  0 part
  ├─rhel-root 253:0    0 26.9G  0 lvm  /
  └─rhel-swap 253:1    0  2.1G  0 lvm  [SWAP]
```

Có thể thấy là ta có một `lvm volume` là `rhel-root` trong phân vùng `/dev/vda2`.

```shell
$ sudo pvs
PV VG Fmt Attr PSize PFree
/dev/vda2 rhel lvm2 a-- <29.00g 0
```

## 2. Mở rộng ổ đĩa vật lý (disk) và phân vùng (partition)

Bạn có thể bỏ qua bước này để đến thẳng 3 nếu phân vùng chứa ổ LVM của bạn đã được tự động tăng dung lượng (tự động hoặc ai đó đã tăng hộ bạn).

Như ở step 1, câu lệnh `lsblk` cho thấy `rhel-root` nằm trong ổ đĩa vật lý `vda` có dung lượng 30G. Mình sẽ tăng dung lượng của ổ đĩa này lên 40G (ổ đĩa cứng ảo - cách tăng dung lượng của một ổ đĩa cứng ảo sẽ tùy thuộc vào IaaS provider hoặc công cụ ảo hóa).

```shell
$ lsblk
 NAME          MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
 sr0            11:0    1 1024M  0 rom
 vda           252:0    0   40G  0 disk
 ├─vda1        252:1    0    1G  0 part /boot
 └─vda2        252:2    0   29G  0 part
   ├─rhel-root 253:0    0 26.9G  0 lvm  /
   └─rhel-swap 253:1    0  2.1G  0 lvm  [SWAP]
```

Sau khi sử dụng lệnh `lsblk` một lần nữa thì ta thấy dung lượng của `vda` đã tăng lên thành 40G. Tiếp tục sử dụng lệnh `growpart` để mở rộng dung lượng cho phân vùng `vda2` đang chứa `rhel-root`.

```shell
$ sudo growpart /dev/vda 2
CHANGED: partition=2 start=2099200 old: size=18872320 end=20971520 new: size=60815327,end=62914527
```

Sau khi `growpart` thì dung lượng của `vda2` sẽ tăng lên xấp xỉ dung lượng của `vda`. Do có 1 phân vùng boot là `vda1` đã chiếm 1G nên dung lượng còn lại thuộc về `vda2` là 39G.

```shell
$ lsblk
 NAME          MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
 sr0            11:0    1 1024M  0 rom
 vda           252:0    0   40G  0 disk
 ├─vda1        252:1    0    1G  0 part /boot
 └─vda2        252:2    0   39G  0 part
   ├─rhel-root 253:0    0 26.9G  0 lvm  /
   └─rhel-swap 253:1    0  2.1G  0 lvm  [SWAP]
```

Bây giờ ta đã đủ điều kiện để có thể tăng dung lượng cho ổ LVM là `rhel-root`.

## 3. Tăng dung lượng cho LVM volume

Resize volume vật lý:

```shell
$ sudo pvresize /dev/vda2
  Physical volume "/dev/vda2" changed
  1 physical volume(s) resized or updated / 0 physical volume(s) not resized

$ sudo pvs
  PV         VG   Fmt  Attr PSize   PFree
  /dev/vda2  rhel lvm2 a--  <39.00g 10.00g
```

Kiểm tra dung lượng được cấu hình cho volume group:

```shell
$ sudo vgs
   VG   #PV #LV #SN Attr   VSize   VFree
   rhel   1   2   0 wz--n- <39.00g 10.00g
```

Bây giờ là lệnh quan trọng nhất, resize ổ LVM với `lvextend`.

```shell
$ sudo lvextend -l +100%FREE /dev/mapper/rhel-root
Size of logical volume rhel/root changed from <26.93 GiB (6893 extents) to <36.93 GiB (9453 extents).
Logical volume rhel/root successfully resized.
```

Bạn có thể thay thế `+100%FREE` bằng giá trị khác để phù hợp với nhu cầu. Ví dụ bạn muốn tăng dung lượng thêm 10GB thì có thể thay thế bằng `+10G`.

## 4. Cập nhật filesystem để nhận diện dung lượng mới

Nếu kiểm tra dung lượng thực tế được sử dụng bởi filesystem thì có thể thấy nó vẫn hiển thị dung lượng cũ.

```shell
$ df -hT | grep mapper
 /dev/mapper/rhel-root xfs        27G  1.9G   26G   8% /
```

Để filesystem có thể nhận diện dung lượng đã thay đổi thì ta chỉ cần sử dụng `resize2fs` đối với `ext4` và `xfs_growfs` đối với `xfs`.

Với `ext4`:

```shell
$ sudo resize2fs /dev/mapper/rhel-root
resize2fs 1.45.5 (07-Jan-2020)
Filesystem at /dev/mapper/rhel-root is mounted on /; on-line resizing required
old_desc_blocks = 60, new_desc_blocks = 121
The filesystem on /dev/mapper/rhel-root is now 253365248 (4k) blocks long.
```

Với `xfs`:

```shell
$ sudo xfs_growfs /
 meta-data=/dev/mapper/rhel-root  isize=512    agcount=4, agsize=1764608 blks
          =                       sectsz=512   attr=2, projid32bit=1
          =                       crc=1        finobt=1, sparse=1, rmapbt=0
          =                       reflink=1
 data     =                       bsize=4096   blocks=7058432, imaxpct=25
          =                       sunit=0      swidth=0 blks
 naming   =version 2              bsize=4096   ascii-ci=0, ftype=1
 log      =internal log           bsize=4096   blocks=3446, version=2
          =                       sectsz=512   sunit=0 blks, lazy-count=1
 realtime =none                   extsz=4096   blocks=0, rtextents=0
 data blocks changed from 7058432 to 9679872
```

Để cho chắc thì bạn có thể kiểm tra lại với câu lệnh `lsblk`.

```shell
$ lsblk
 NAME          MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
 sr0            11:0    1 1024M  0 rom
 vda           252:0    0   40G  0 disk
 ├─vda1        252:1    0    1G  0 part /boot
 └─vda2        252:2    0   39G  0 part
   ├─rhel-root 253:0    0 36.9G  0 lvm  /
   └─rhel-swap 253:1    0  2.1G  0 lvm  [SWAP]
```

Vậy là xong.
