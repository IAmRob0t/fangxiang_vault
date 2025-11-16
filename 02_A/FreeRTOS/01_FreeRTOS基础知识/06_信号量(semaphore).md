---
tags:
  - freeRTOS
---
前面介绍的 [[05_队列 (queue)|队列 (queue)]] 可以用于传输数据：在任务之间、任务和中断之间。

有时候我们只需要传递状态，并不需要传递具体的信息，比如： 
- 我的事做完了，通知一下你
- 卖包子了、卖包子了，做好了 1 个包子！做好了 2 个包子！做好了 3 个包子！
- 这个停车位我占了，你们只能等着在这种情况下我们可以使用信号量 (semaphore)，它更节省内存。

# 信号量的特性

## 信号量的常规操作

本节源码：`15_freertos_example_semaphore`，在 `12_freertos_example_sync_exclusion` 上修改。

![[FreeRTOS完全开发手册之上册_快速入门.pdf#page=94&rect=66,226,526,347|FreeRTOS完全开发手册之上册_快速入门, p.94]]

## 信号量跟队列的对比

## 两种信号量的对比

信号量的计数值都有限制：限定了最大值。如果最大值被限定为1，那么它就是二进制信号量；如果最大值不是1，它就是计数型信号量。

| 二进制信号量     | 计数型信号量      |
| ---------- | ----------- |
| 被创建时初始值为 0 | 被创建时初始值可以设定 |
| 其他操作是一样的   | 其他操作是一样的    |

# 信号量函数

## 创建

|      | 二进制信号量                                      | 计数型信号量                           |
| ---- | ------------------------------------------- | -------------------------------- |
| 动态创建 | `xSemaphoreCreateBinary`<br>计数值初始值为 0       | `xSemaphoreCreateCounting`       |
|      | `vSemaphoreCreateBinary` (过时了)<br>计数值初始值为 1 |                                  |
| 静态创建 | `xSemaphoreCreateBinaryStatic `             | `xSemaphoreCreateCountingStatic` |

( [[FreeRTOS完全开发手册之上册_快速入门.pdf#page=96&selection=38,2,38,16&color=note|📖]])
二进制信号量的函数原型如下：

( [[FreeRTOS完全开发手册之上册_快速入门.pdf#page=96&selection=40,2,40,16&color=note|📖]])
计数型信号量的函数原型如下：

## 删除

## give / take

`xSemaphoreGive` 的函数原型如下：

( [[FreeRTOS完全开发手册之上册_快速入门.pdf#page=97&selection=116,0,124,3&color=note|📖]])

```c
BaseType_t xSemaphoreGive( SemaphoreHandle_t xSemaphore );
```

`xSemaphoreTake` 的函数原型如下：

( [[FreeRTOS完全开发手册之上册_快速入门.pdf#page=98&selection=89,0,98,2&color=note|📖]])

```c
BaseType_t xSemaphoreTake(
					SemaphoreHandle_t xSemaphore,
					TickType_t xTicksToWait
				);
```

# 示例 12: 使用二进制信号量来同步

# 示例 13: 防止数据丢失

# 示例 14: 使用计数型信号量