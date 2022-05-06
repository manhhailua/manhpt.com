---
title: "[Gitlab] Cài đặt gitlab-runner sử dụng môi trường docker"
description: Cài đặt và cấu hình gitlab-runner trên môi trường docker. Cài đặt gitlab-runner thành công nhưng job không được kích hoạt.
authors: [manhpt]
tags: [gitlab, gitlab-ci, gitlab-runner]
image: ./docker-build-push-gitlab-ci-1200x675.png
---

![](./docker-build-push-gitlab-ci-1200x675.png)

Việc cài đặt `gitlab-runner` sử dụng docker được hướng dẫn khá đầy đủ tại [tài liệu chính thống](https://docs.gitlab.com/runner/install/docker.html). Nhưng thực tế quá trình cài đặt và sử dụng thường không diễn ra suôn sẻ với mình lắm nên mình chắc nhiều bạn cũng gặp vấn đề giống mình. Bài viết này chủ yếu chỉ ra những điều cần chú ý khi bạn cài đặt và sau khi cài thành công mà pipeline có thể vẫn báo tình trạng `stuck` (`job` không thể kích hoạt bởi gitlab-runner).

## Triển khai gitlab-runner

Để cài đặt `gitlab-runner` bạn chỉ cần 2 câu lệnh sau là đủ:

### 1. Cài đặt gitlab-runner   

```shell
sudo docker run -d --name gitlab-runner --restart always \
  -v /srv/gitlab-runner/config:/etc/gitlab-runner \
  -v /var/run/docker.sock:/var/run/docker.sock \
  gitlab/gitlab-runner:latest
```

### 2. Cấu hình gitlab-runner

```shell
sudo docker run --rm -t -i \
  -v /srv/gitlab-runner/config:/etc/gitlab-runner \
  gitlab/gitlab-runner register
```

Để điền thông tin cấu hình bạn chỉ cần theo sát hướng dẫn tại [đây](https://docs.gitlab.com/runner/register/index.html#docker). Vậy là xong rồi!

## Chú ý

- _Cài đặt xong rồi nhưng pipeline của tôi vẫn không được kích hoạt?_ - Rất có thể bạn cần cấu hình thêm một chút để Runners có thể kích hoạt các jobs không được `tags`, việc này có thể làm ngay trên giao diện web gitlab. ([Link tham khảo](https://docs.gitlab.com/ee/ci/runners/#allowing-runners-with-tags-to-pick-jobs-without-tags))
- _Tôi cần build docker image trên CI nhưng khi chạy thì báo không tìm thấy docker?_ - Chắc là quên bật `--privileged` ([link tham khảo](https://docs.gitlab.com/ee/ci/docker/using_docker_build.html#use-docker-in-docker-executor)).
- Nếu bạn muốn sử dụng gitlab-runner cho docker swarm thì có thể tham khải [tại đây](https://manhpt.com/2019/11/30/gitlab-cai-dat-gitlab-runner-tren-moi-truong-docker-swarm/).
