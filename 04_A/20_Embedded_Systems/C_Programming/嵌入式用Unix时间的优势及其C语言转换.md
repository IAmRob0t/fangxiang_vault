---
title: 嵌入式用Unix时间的优势及其C语言转换
source: https://mp.weixin.qq.com/s/w6FsYNXMECT82Vqv4KmE2A
author:
  - "[[Mr.Deng]]"
published: 
created: 2025-04-03
description: 以“数值化时间”的设计哲学，解决了计算机系统中最本质的需求
tags:
  - clippings
  - c
---

今天跟大家聊的主题是Unix时间，在计算机世界中，时间记录是日志追踪、缓存过期、事务排序等场景的核心需求。Unix时间凭借其简洁高效的设计，成为跨系统、跨语言的时间标准。本文将深入聊聊Unix时间，并通过C语言代码演示其与日常时间的转换技巧。

---

# 一、什么是Unix时间？

**1.1 核心定义**  
Unix时间（Unix Time/Epoch Time）是一个从 **1970年1月1日00:00:00 UTC** （协调世界时）起计算的 **连续秒数** 。它忽略闰秒，用整数差值表示时间流逝。

**1.2 表现形式**  
• **秒级时间戳** ：10位整数（如 `1687250000` ）  
• **毫秒级时间戳** ：13位整数（如 `1687250000000` ，多用于JavaScript）

**1.3 设计初衷**  
• **简化计算** ：时间差=两个整数相减，无需处理日期格式。  
• **全球统一** ：基于UTC时区，消除地域时差歧义。

---

# 二、为什么采用Unix时间？

**2.1 系统兼容性**  
所有主流操作系统（Linux、Windows、macOS）和编程语言（Python、Java、C/C++）均支持Unix时间，实现 跨平台无缝对接 。

**2.2 计算高效**  
• **比较时间** ：直接对比两个整数即可判断先后。  
• **设置过期时间** ：缓存过期时间= `当前时间戳 + 有效期秒数` 。

**2.3 时区无感**  
统一使用UTC，避免时区转换的复杂性。例如，北京时间只需在显示时+8小时。

**2.4 存储节省**  
1个 `time_t` 类型（通常4字节）即可存储时间，相比字符串（如 `"2023-10-01 12:00:00"` ）节省空间。

  

---

# 三、Unix时间与日常时间的转换方法

**3.1 数据结构： `struct tm`**  
C语言中，日期时间通过 `tm` 结构体表示：

```
struct tm {
    int tm_sec;   // 秒 [0-59]
    int tm_min;   // 分 [0-59]
    int tm_hour;  // 时 [0-23]
    int tm_mday;  // 日 [1-31]
    int tm_mon;   // 月 [0-11]，0代表1月
    int tm_year;  // 年，实际年份=1900 + tm_year
    int tm_wday;  // 星期 [0-6]，0代表周日
    int tm_yday;  // 一年中的第几天 [0-365]
    int tm_isdst; // 夏令时标志（负数表示未知）
};
```

**3.2 关键函数**  
• **`gmtime()`** ：将时间戳转换为UTC时间的 `tm` 结构体。  
• **`localtime()`** ：转换为本地时区时间（依赖系统时区设置）。  
• **`strftime()`** ：将 `tm` 结构格式化为字符串。  
• **`mktime()`** ：将本地时间的 `tm` 结构转换为时间戳。

---

#  四、C语言实战：时间转换代码

**4.1 时间戳转日期**

```
#include <stdio.h>
#include <time.h>

void print_time(time_t timestamp) {
    struct tm *tm_utc = gmtime(&timestamp);// 转换为UTC时间
    char buffer[80];
    
    // 格式化为字符串
    strftime(buffer, sizeof(buffer), "%Y-%m-%d %H:%M:%S UTC", tm_utc);
    printf("UTC时间: %s\n", buffer);

    // 转换为本地时间
    struct tm *tm_local = localtime(&timestamp);
    strftime(buffer, sizeof(buffer), "%Y-%m-%d %H:%M:%S %Z", tm_local);
    printf("本地时间: %s\n", buffer);
}

int main() {
    time_t now = time(NULL);  // 获取当前时间戳
    print_time(now);
    return0;
}
```

**4.2 日期转时间戳**

```
#include <stdio.h>
#include <time.h>

time_t convert_to_timestamp(int year, int month, int day, int hour, int min, int sec) {
    struct tm tm_time = {0};
    tm_time.tm_year = year - 1900;  // 年份从1900起算
    tm_time.tm_mon = month - 1;     // 月份0-11
    tm_time.tm_mday = day;
    tm_time.tm_hour = hour;
    tm_time.tm_min = min;
    tm_time.tm_sec = sec;
    tm_time.tm_isdst = -1;  // 自动判断夏令时
    
    return mktime(&tm_time);  // 转换为时间戳（本地时区）
}

int main() {
    // 示例：北京时间2023-10-01 12:00:00（UTC+8）
    time_t timestamp = convert_to_timestamp(2023, 10, 1, 12, 0, 0);
    printf("时间戳: %ld\n", timestamp);
    return0;
}
```

---

# 五、Unix时间的“坑”

**5.1 2038年问题**  
• **原因** ：32位系统的 `time_t` 类型将在2038年1月19日溢出（最大值为 `2^31-1` ）。  
• **解决方案** ：迁移到64位系统， `time_t` 可支持到约2900亿年。

**5.2 闰秒问题**  
• **现象** ：Unix时间忽略闰秒调整，可能与实际时间存在±1秒偏差。  
• **应对** ：高精度场景需通过NTP协议同步网络时间。

整体来说在嵌入式领域Unix时间是非常重要和方便的，以“数值化时间”的设计哲学，解决了计算机系统中最本质的需求—— **用最小代价实现时间的记录与计算** 。