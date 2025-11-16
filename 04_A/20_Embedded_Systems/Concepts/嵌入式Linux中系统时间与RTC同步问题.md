---
title: 嵌入式Linux中系统时间与RTC同步问题
source: https://mp.weixin.qq.com/s/aLgiizxYMF7nU2-pAzRS2g
author:
  - "[[Mr.Deng]]"
published: 
created: 2025-04-09
description: 
tags:
  - clippings
  - linux
---
今天主要跟大家分享一下Linux系统时间与RTC的同步问题。

在Linux系统中，硬件实时时钟（RTC）如同一块永不掉电的“机械表”，即使设备关机，它仍能持久记录时间。而系统时间（由内核维护的软件时钟）在长期运行中会因晶振误差、温度变化等因素逐渐漂移，导致时间失准。

**那如何让系统时间始终以RTC为基准，甚至优先信任RTC的精度？**

---

### 一、默认机制：Linux如何与RTC同步时间？

#### 1\. 启动与关机的“一次性同步”

• **启动时** ：系统通过 `hwclock --hctosys` 命令从RTC读取时间，初始化系统时间。  
• **关机时** ：系统通过 `hwclock --systohc` 将当前系统时间回写到RTC。

这种机制仅保障了 **开机时间的准确性** ，但长期运行的服务器或嵌入式设备（如工控机、路由器）可能因系统时钟漂移，逐渐与RTC产生偏差。

#### 2\. 无干预下的时间偏差风险

• **示例** ：某服务器连续运行3个月，系统时钟每秒漂移0.1秒，累计误差将达约 **43分钟** 。  
• **后果** ：日志时间混乱、证书验证失败、定时任务错乱等。

---

### 二、systemd的rtcsync：让RTC与系统时间长期同步

#### 1\. rtcsync的作用

`rtcsync` 是 `systemd-timesyncd` 服务的核心功能之一。启用后，系统会 **定期将当前时间写入RTC** （默认每分钟尝试同步），而非仅在关机时同步。这解决了长期运行中系统时间与RTC的偏差问题，但是这里是以系统时间为基准，而非RTC时间，单向同步系统时间同步到RTC。

防止异常关机导致RTC时间陈旧，在NTP正常时，能立马将准确时间持久化到RTC，避免异常关机导致RTC时间失效。

#### 3\. 配置方法

1. **启用 `rtcsync`** ：
	```
	sudo nano /etc/systemd/timesyncd.conf
	```
	修改为：
	```
	[Time]
	RTCSync=yes
	```
2. **重启服务** ：
	```
	sudo systemctl restart systemd-timesyncd
	```
3. **验证同步** ：
	```
	timedatectl show-timesync | grep RTCTimeUSec  # 查看最近RTC同步时间
	hwclock -r && date                            # 对比RTC与系统时间
	```

---

### 三、让RTC更新系统时间

若RTC本身具有高精度（如温补晶振的工业级RTC），可配置系统 **优先以RTC为时间源** ，甚至完全依赖RTC校准时间。

调整RTC同步频率

• **适用场景** ：需高频同步RTC（如秒级校准）。  
• **通过systemd定时器实现** ：

1. 创建服务文件 `/etc/systemd/system/rtc-sync.service` ：
	```
	[Unit]
	Description=Sync system time from RTC
	[Service]
	Type=oneshot
	ExecStart=/sbin/hwclock --hctosys
	```
2. 创建定时器 `/etc/systemd/system/rtc-sync.timer` ：
	```
	[Unit]
	Description=Sync RTC every 30 seconds
	[Timer]
	OnBootSec=1min
	OnUnitActiveSec=30s
	AccuracySec=1ms
	[Install]
	WantedBy=timers.target
	```
3. 启用定时器：
	```
	sudo systemctl enable --now rtc-sync.timer
	```

**四、adjtimex时间纠正**

`adjtimex` 是一个 Linux 命令行工具，用于 **调整内核时钟的硬件参数** ，从而控制系统时间的频率和偏移。它的核心功能是 **通过微调系统时钟的振荡频率** ，使系统时间逐步趋近于参考时间源（如硬件 RTC 或 NTP 服务器），避免直接修改时间值导致的时间跳跃（Jump）。

adjtimex 源自 Unix 的 `ntp_adjtime` 系统调用，是 Linux 内核时间管理的重要接口。

##### 1\. 时钟漂移的产生

系统时间由内核维护的软件时钟驱动，其基准是硬件时钟源的振荡频率（通常为 11 MHz 或 25 MHz）。由于晶振受温度、电压等因素影响，实际频率与标称值存在微小偏差（如 ±100 ppm），导致系统时间逐渐偏离真实时间。

##### 2\. adjtimex 的修正逻辑

• **频率调整** ：通过修改内核时钟的 `frequency` 参数，直接改变系统时钟的振荡频率。  
• 示例：若系统时钟每天慢 10 秒，可将频率调高 115.74 ppm（ `10秒 / 86400秒 ≈ 115.74 ppm` ）。 **平滑同步** ：通过微调频率，系统时间会以线性速率逼近参考时间，而非直接跳跃。

##### 3\. 内核参数解析

`adjtimex` 操作以下关键参数（通过 `struct timex` 传递）：

• **`frequency`** ：时钟频率偏移量，单位为 **ppm（百万分之一秒）** 。正值加快时钟，负值减慢。

• **`tick`** ：时钟中断周期（单位：微秒），默认 10,000（即 100 Hz）。  
• 修改 `tick` 可间接调整时钟频率，但需谨慎操作。

• **`offset`** ：直接设置时间偏移（单位：微秒），通常由 NTP 服务自动调整。

• **`status`** ：时钟状态标志（如 `STA_PLL` 启用锁相环频率调整）。

如下是自动校准脚本示例，根据 RTC 时间偏差动态调整频率：

```
#!/bin/bash
# 获取系统时间与RTC的时间差（秒）
RTC_TIME=$(hwclock --debug | awk '/Hw clock time/ {print $5}' | tr -d ',')
SYS_TIME=$(date +%s)
DELTA=$(( $(date --date="$RTC_TIME" +%s) - $SYS_TIME ))

# 计算频率修正值（假设每6小时校准一次）
FREQ_CORRECTION=$(( DELTA * 1000000 / (6 * 3600) ))

# 应用修正
sudo adjtimex --frequency $FREQ_CORRECTION
```

## 最 后

小哥搜集了一些嵌入式学习资料，公众号内回复 **【 **1024** 】** 即可找到下载链接！

  

```
推荐好文  点击蓝色字体即可跳转☞专辑|Linux应用程序编程大全☞ 专辑|学点网络知识☞ 专辑|手撕C语言
☞ 专辑|手撕C++语言☞ 专辑|经验分享☞ 专辑|从单片机到Linux☞ 专辑|电能控制技术☞ 专辑|嵌入式必备数学知识☞  MCU进阶专辑
☞  嵌入式C语言进阶专辑
☞  经验分享
```

继续滑动看下一个

向上滑动看下一个 [知道了](https://mp.weixin.qq.com/s/) ： ， ， ， ， ， ， ， ， ， ， ， ， 。 视频 小程序 赞 ，轻点两下取消赞 在看 ，轻点两下取消在看 分享 留言 收藏 听过