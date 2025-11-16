---
tags:
  - freeRTOS
---

FreeRTOS的中断管理就是教你如何在中断函数里，使用一套名为 `FromISR` 的专用API来安全地通知任务，从而把耗时的操作交给任务去处理。

# 两套 API 函数

本节视频参考的源码是 `27_freertos_example_fromisr`，从 `26_freertos_example_readkey` 复制得到。

## 为什么需要两套 API

- 很多 API 函数会导致任务计入阻塞状态：
	- 运行这个函数的任务进入阻塞状态
	- 比如写队列时，如果队列已满，可以进入阻塞状态等待一会
- ISR 调用 API 函数时，ISR 不是"任务"，ISR 不能进入阻塞状态
- 所以，在任务中、在 ISR 中，这些函数的功能是有差别的

## 两套 API 函数列表

| 类型                                         | 在任务中                 | 在 ISR 中                     |
| ------------------------------------------ | -------------------- | --------------------------- |
| [[05_队列 (queue)\|队列 (queue)]]              | `xQueueSendToBack`   | `xQueueSendToBackFromISR`   |
|                                            | `xQueueSendToFront`  | `xQueueSendToFrontFromISR`  |
|                                            | `xQueueReceive`      | `xQueueReceiveFromISR`      |
|                                            | `xQueueOverwrite`    | `xQueueOverwriteFromISR`    |
|                                            | `xQueuePeek`         | `xQueuePeekFromISR`         |
| [[06_信号量(semaphore)\|信号量 (semaphore)]]     | `xSemaphoreGive`     | `xSemaphoreGiveFromISR`     |
|                                            | `xSemaphoreTake`     | `xSemaphoreTakeFromISR`     |
| [[08_事件组(event group)\|事件组 (event group)]] | `xEventGroupSetBits` | `xEventGroupSetBitsFromISR` |

### `xQueueSendToBackFromISR()` 和 `xQueueSendToBack()` 这两个函数的内部实现机制的异同点

| 特性            | `xQueueSendToBack()` （任务） | `xQueueSendToBackFromISR()` （中断）                    |
| ------------- | ------------------------- | --------------------------------------------------- |
| **调用上下文**     | 任务中                       | 中断服务程序（ISR）中                                        |
| **核心操作逻辑**    | **完全相同**                  | **完全相同**                                            |
| **队列满时的行为**   | **可以阻塞**等待                | **立即返回错误**，绝不等待                                     |
| **能否导致任务切换**  | **能**，直接触发调度              | **不能直接切换**，但通过`pxHigherPriorityTaskWoken`参数**建议**切换 |
| **保护共享资源的方式** | 锁任务调度器                    | **关中断**（或操作中断优先级掩码）                                 |
| **设计哲学**      | 协作式，可阻塞，功能完整              | 非阻塞，极速，安全第一                                         |

- `xQueueSendToBack()` 就像邮局职员：他可以耐心等待你把包裹包装好（阻塞），并且一旦包裹寄出，他会立刻打电话通知收件人（切换任务）。
- `xQueueSendToBackFromISR()` 就像投进邮筒的紧急信件：邮筒（ISR）只能接受信，如果邮筒满了就塞不进去。投递者（中断）无法通知邮局职员，但投递行为本身会点亮邮筒上的一个红灯（设置 `pxHigherPriorityTaskWoken`）。邮差下次来取件时（中断退出后），看到红灯就知道有紧急信件，需要立刻处理（触发任务切换）。

## `xHigherPriorityTaskWoken` 参数

## 怎么切换任务

FreeRTOS 的 ISR 函数中，使用两个宏进行任务切换：

```c
portEND_SWITCHING_ISR( xHigherPriorityTaskWoken ); // 或
portYIELD_FROM_ISR( xHigherPriorityTaskWoken );
```

( [[FreeRTOS完全开发手册之上册_快速入门.pdf#page=167&selection=34,0,34,7&color=note|📖]])
使用示例如下：

## 优先级

> [!question] 为什么 FromISR API 不直接调度？
> 在 FreeRTOS 中， **中断的首要目标是快速响应** 。因此，FromISR 函数只会标记“有高优先级任务已就绪”，真正的任务切换会在 **中断退出时** 或 **下一个调度点** 统一完成。 这样既保持了中断响应的实时性，也避免了中断嵌套时的上下文混乱。

![[../../../01_P/ARM 架构/attachments1/ARM Cortex-M3与Cortex-M4权威指南.pdf#page=188&rect=102,43,378,365|ARM Cortex-M3与Cortex-M4权威指南, p.161]]

FreeRTOS 中
- 中断优先级 数值越小，优先级越高（0x00 最高，0xFF 最低）。
- FreeRTOS 将可编程中断优先级划分为 两个逻辑区域：A 区（高优先级） 和 B 区（低优先级）。
	- A 部分：高优先级中断（数值小），不受 FreeRTOS 临界区影响，用于硬实时任务。
	- B 部分：低优先级中断（数值大），在 FreeRTOS 关中断时被屏蔽，防止破坏内核数据结构。（`SysTick` 也属于）
	- 不要在 A 区中断中调用 FreeRTOS API（如 `xQueueSendFromISR`），因为这些中断不会被屏蔽，可能导致竞态。

---



# 中断的延迟处理

> [!question] 为什么程序不设计成在 `xTimerResetFromISR` 中直接启用调度，而是在 `portYIELD_FROM_ISR` 中启用调度
> - 保证中断响应速度（中断函数本身非常快）。
> - 遵循“查询与执行分离”的优秀设计原则。
> - 提供灵活性，让程序员决定是否以及何时调度。
> - 提供一个统一、高效、安全的调度触发点（`portYIELD_FROM_ISR`）。

# 中断与任务间的通信

# `pendSV`

**PendSV（Pendable Service Call）** 是 ARM Cortex-M 架构中一个**系统异常**，专为**操作系统上下文切换**而设计。在 FreeRTOS、RT-Thread、Zephyr 等 RTOS 中，PendSV 被用作**任务切换的“安全通道”**。

