---
tags:
  - freeRTOS
---
# 软件定时器的特性

定时器三要素：
* 超时时间
* 函数
* 单次触发还是周期性触发

# 软件定时器的上下文

## 守护任务

我们自己编写的任务函数要使用定时器时，是通过"定时器命令队列" (timer command queue) 和守护任务交互，如下图所示：

![[FreeRTOS完全开发手册之上册_快速入门.pdf#page=148&rect=74,318,520,471&color=note|📖]]

## 守护任务的调度

## 回调函数

# 软件定时器的函数

根据定时器的状态转换图，就可以知道所涉及的函数：

![[FreeRTOS完全开发手册之上册_快速入门.pdf#page=151&rect=75,328,528,750&color=note|📖]]

## 创建

( [[FreeRTOS完全开发手册之上册_快速入门.pdf#page=151&selection=11,0,11,32&color=note|📖]])
有两种方法创建定时器：动态分配内存、静态分配内存。函数原型如下：

## 删除

## 启动 / 停止

( [[FreeRTOS完全开发手册之上册_快速入门.pdf#page=152&selection=38,0,38,10&color=note|📖]])
涉及的函数原型如下：

## 复位

## 修改周期

## 定时器 ID

# 示例 24: 一般使用

本节视频参考的源码是 `25_freertos_example_timer`，从 `05_freertos_example_createtask` 复制得到。

( [[FreeRTOS完全开发手册之上册_快速入门.pdf#page=156&selection=12,0,12,16&color=note|📖]])
要使用定时器，需要做些准备工作：


# 示例 25: 消除抖动

视频对应的源码为：`26_freertos_example_readkey`

怎么读到确定的按键状态？
- 连续读很多次，知道数值稳定：浪费 CPU 资源
- **使用定时器**：要结合中断来使用

![[FreeRTOS完全开发手册之上册_快速入门.pdf#page=159&rect=72,255,526,563&color=note|📖]]

# 定时器（timer）的内部机制

## 硬件定时器与软件定时器关系

- 硬件定时器（Timer Peripheral）提供一个基础时基（通常是 SysTick 或者其他硬件定时器），周期性地产生中断（Tick 中断）。
- 在此基础上，系统可以构建**多个软件定时器（SoftTimer）**，即在软件层利用 Tick 计数实现多个独立的超时管理。

## 软件定时器结构体（SoftTimer）

一个典型的软件定时器结构体中包含：
- `callback`：定时器回调函数指针（`func`）
- `timeout`：超时周期（单位为 Tick）
- `expire_time`：下次超时时间点（通常是 `xTickCount + timeout`）
- `autoReload`：是否为周期性定时器
- `state`：当前状态（运行/停止）

这些软件定时器会被放在一个 **定时器链表（SoftTimerList）** 中，链表通常会 **按剩余超时时间排序** 。

## `SoftTimer` 的执行机制

- 每当发生 SysTick 中断（即系统 Tick 增加），系统会检查 SoftTimerList：
    - 若有定时器到期（`xTickCount >= expire_time`），则触发对应的 `callback`（`func`）。
    - 如果是周期性定时器，则更新它的下次 `expire_time` 并重新插入链表。
- 这种机制可以在中断中直接执行，也可以交由一个任务延迟执行（取决于系统设计）。

## FreeRTOS 的特殊机制

FreeRTOS 的软件定时器 **不在中断中直接执行**，而是通过一个专用任务 **Timer Service Task（又叫 `TimerTask`）** 来处理：
1. **SysTick 中断中（`xTaskIncrementTick`）**
    - 仅仅增加 `xTickCount`，并检查是否有定时器到期。
    - 如果有到期的定时器，会往 **定时器命令队列（Timer Command Queue）** 发送一个命令，通知 Timer Task 有定时器需要处理。
2. **Timer Task（定时器任务）**
    - 优先级通常较低，由用户创建时配置。
    - 主循环中不断执行以下逻辑：
		1. 调用 `vQueueWaitForMessageRestricted()` 等待消息队列中的事件（即定时器命令），或者等待**下一次定时器超时点**。
		2. 一旦队列中有消息，或有定时器到期：
		    - 处理 Timer 命令（启动/停止/修改/重载等）
		    - 调用对应定时器的回调函数（`callback`）

---

✳️补充：`vQueueWaitForMessageRestricted()` 的作用

- 该函数是 FreeRTOS 内部为 **Timer Service Task 和 Daemon Task** 特制的“受限等待函数”。
- **主要作用：**
    1. 让 Timer Task 在“队列有消息”或“下一个定时器到期”之间**二选一地唤醒**；
    2. 避免频繁调用 `vTaskDelayUntil()` 或长时间阻塞；
    3. 保证即使没有新的命令消息，也能在定时器到期的正确时间点被唤醒执行。

🔹 **通俗理解：**

> 它让 Timer Task“睡到该醒的时候自动醒”，  
> 要么因为有人发来了新的定时器命令，要么因为有定时器时间到了。

🔹 **区别于普通队列等待函数（例如 `xQueueReceive()`）：**

> `vQueueWaitForMessageRestricted()` 不会无限阻塞；  
> 它带有超时唤醒机制，由最近的定时器超时点决定。

## 这种设计的意义

- 避免在中断中执行耗时或未知的用户代码（callback）。
- 确保中断轻量，响应高效。
- Timer Task 的等待机制保证了**实时性与任务调度平衡**：
  即使没有新的命令，也能在**正确的 Tick 时间**处理超时定时器。

## 代码分析

( [[FreeRTOS完全开发手册之上册_快速入门 1.pdf#page=170&selection=8,0,11,1&color=note|📖]])
本节程序为 `FreeRTOS_24_software_timer`
