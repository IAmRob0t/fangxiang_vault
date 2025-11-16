---
title: linux下top命令查看系统资源小技巧
source: https://mp.weixin.qq.com/s/9H2kaFudSzo-d1U8iOw0Qw
author:
  - "[[微信公众平台]]"
published: 
created: 2025-04-03
description: 
tags:
  - clippings
  - linux
---
# top命令刷新原理

`top` 命令默认会按照一定的时间间隔（通常是3秒）更新系统资源使用情况的显示内容。它通过读取系统的 `/proc` 文件系统中的相关文件（如 `/proc/stat` 用于CPU信息、 `/proc/meminfo` 用于内存信息等）来获取最新的进程和资源使用数据。这个更新间隔决定了我们看到信息的时效性。

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/mPZJgHsAnGC7icTS547u5rzcsYbEVoLoiczXcaWm3ehOVcWPYwy2jj1qBibbInvfgr2C6OS7FLibYdLLagYpeTP77Q/640?wx_fmt=png&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

# top命令切换与查阅

`进入top命令行界面后按“ H ”键切换进程与线程模式`

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/mPZJgHsAnGC7icTS547u5rzcsYbEVoLoicmkv5oqSOzyIuJeAmJE53sq2L87uxQQgy3FNVuOod6IJJ3yX0ynO4yg/640?wx_fmt=png&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/mPZJgHsAnGC7icTS547u5rzcsYbEVoLoicTMRiaM4EBnxo8mYicQgtNTohdoJK57mXpIFNN6hG10Vu6TkmzRMrDP6w/640?wx_fmt=png&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

这样你就可以看到不同线程的属性和状态了，比如线程的优先级等。

一般现代的linux操作系统任务都比较多，那么我们可以通过在top界面按上下方向键来翻页。

# 提高刷新速度

top命令默认进入是3s刷新一次，如果需要更快的刷新速度进行观察，那么有如下几种方法:  

1、 当 `top` 命令已经在运行时，可以按下键盘上的 `s` 键。此时， `top` 会提示你输入新的刷新间隔时间（以秒为单位）。输入你想要的间隔时间后回车， `top` 就会按照新的速度进行刷新。这种方式比较灵活，方便你在观察过程中根据实际需要调整刷新速度。例如，如果你一开始使用默认的3秒间隔，在发现系统资源变化较快时，可以按下 `s` 键并输入 `0.5` ，让 `top` 以每秒两次的速度刷新。

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/mPZJgHsAnGC7icTS547u5rzcsYbEVoLoiciaQkJlh6rBNWAKWurFqKHibUvKo3wKobzfnIedaZZZP3QBZzCHOxvib2g/640?wx_fmt=png&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

2、 `top -d [秒数]` 。这个参数用于指定 `top` 命令更新显示内容的时间间隔。例如，如果你想让 `top` 命令以每秒一次的速度刷新，可以使用 `top -d 1` 。这样， `top` 就会每隔1秒重新读取系统信息并更新显示，使你能更快地观察到系统资源使用情况的变化。

3、如果你需要在特定的条件下动态调整 `top` 的刷新速度，可以编写一个简单的脚本。例如，以下是一个使用 `bash` 脚本实现的简单功能：当系统的CPU使用率超过80%时，加快 `top` 的刷新速度为每秒一次；当CPU使用率低于40%时，将刷新速度恢复为默认的3秒。因为虽然提高刷新速度可以让你更及时地获取信息，但过快的刷新速度可能会导致系统资源（特别是CPU资源）被大量消耗在 `top` 命令自身的数据读取和显示更新上。对于性能较低的系统，可能会出现系统响应变慢或者 `top` 命令显示卡顿的情况。

使用脚本实现动态调整刷新速度（参考） ：

```
#!/bin/bash
while true; do
  cpu_usage=$(top -bn1 | grep "Cpu(s)" | awk '{print $2 + $4}')
  if (( $(echo "$cpu_usage > 80" | bc -l) )); then
    top -d 1 &
  elif (( $(echo "$cpu_usage < 40" | bc -l) )); then
    pkill -f "top -d 1"
    top -d 3 &
  fi
  sleep 1
done
```