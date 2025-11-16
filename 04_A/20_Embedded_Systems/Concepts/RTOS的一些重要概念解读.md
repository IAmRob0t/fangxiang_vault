---
title: RTOS的一些重要概念解读
source: https://mp.weixin.qq.com/s/uGH0Y8SBk6nXOFpq7i6cvg
author:
  - "[[微信公众平台]]"
published: 
created: 2025-04-03
description: 裸机还是RTOS？
tags:
  - clippings
  - rtos
---

# RTOS基础知识

![图片](https://mmbiz.qpic.cn/mmbiz_png/zcVcDoKYUnaFLC9f63Heb61F0lBic1aRLnPjO9yibCHDblOqia6PMg9kuyfibwI5iay00rhZIwgYueWEFYyQKwRYNwA/640?wx_fmt=png&from=appmsg&random=0.5663448757269351&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

![图片](https://mmbiz.qpic.cn/mmbiz_jpg/zcVcDoKYUnaFLC9f63Heb61F0lBic1aRL6WBic0iabNGMcYiaHmjnVnrYrDeLCdaJ1tQz43GwS1QbgSuWnmGckf6wQ/640?wx_fmt=jpeg&from=appmsg&random=0.2784912995901403&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

实时操作系统（RTOS）是一种操作系统（OS），旨在提供实时应用进程数据，通常没有缓冲延迟。

RTOS中的关键因素是最小的中断延迟和最小的线程切换延迟。RTOS的价值在于它的响应速度或可预测性，而不是它在给定时间段内可以执行的工作量。

对于嵌入式设备，一般规则是当应用进程需要执行多个简单操作时使用RTOS。

实时操作系统具有以下目标：

- 低延迟。
- 决定论：需要知道处理事情需要多长时间才能确保满足最后期限。
- 结构化软件：使用RTOS，可以以结构化的方式分而治之。直接向应用进程添加其他组件。
- 可扩展性：RTOS必须能够从简单的应用进程扩展到具有堆栈、驱动进程、文档系统等的复杂应用进程。
- 卸载开发：RTOS管理系统的许多方面，例如，RTOS与调度一起，通常处理电源管理，中断表管理，内存管理，异常处理等。

## 1. 线程

基于RTOS的应用进程中的典型线程：

- 中断服务例程（ISR）：由硬件中断启动的线程。ISR运行直至完成。ISR都共享同一堆栈。
- 任务：在等待事件发生时可以阻塞的线程。传统上，任务是长寿命线程（与运行直至完成的ISR相反）。每个任务都有自己的堆栈，可以让它长寿。
- Idle：优先级最低的线程，仅在没有其他线程准备好执行时运行。通常，空闲只是具有尽可能低优先级的特殊任务。

## 2. 调度进程

每个RTOS的核心都有一个调度进程。调度进程负责管理系统中线程的执行。调度进程有两种主要管理方式：抢占式调度和时间片调度。

抢占式调度是最常见的RTOS调度进程类型。TI-RTOS和FreeRTOS都有抢占式调度进程。使用抢占式调度进程，正在运行的线程将一直持续到

- 完成（例如，ISR完成）。
- 较高优先级的线程准备就绪（在这种情况下，优先级较高的线程会抢占优先级较低的线程）。
- 线程在等待资源时放弃处理器（例如，任务调用sleep()）。

时间片调度保证每个线程都有一个要执行的槽。这种类型的调度通常不利于实时应用。如果需要，TI-RTOS内核支持使用任务进行时间切片调度。

## 3. 其他关键术语

线程安全：如果一段代码以保证多个线程同时正确访问（读取、写入）的方式操作共享数据结构，则该代码段是线程安全的。

Blocked：如果任务正在等待资源且未消耗任何CPU，则阻止该任务。例如，如果任务调用Task\_sleep()或Semaphore\_pend()（非零超时且信号量不可用），则该任务将被阻止，并允许另一个线程运行。

裸机：不适用RTOS的应用进程的公用名。

## 4. 裸机与实时操作系统

典型的裸机应用进程通常可分为三个关键部分：

- 初始化：初始化main()中的硬件和软件组件。
- 超级循环状态机：用于管理应用进程的代码。这些操作基于中断（例如，收到SPI数据包或计时器过期）或轮询的结果。
- ISR：由外围设备（例如UART）、定时器或其他特定于设备的项目（例如异常或多核通信）的中断执行的代码。

![图片](https://mmbiz.qpic.cn/mmbiz_jpg/zcVcDoKYUnaFLC9f63Heb61F0lBic1aRLsib6zxHXvOFuVNibI1SQvGSC2BxNbgVrNJbWmicJN17LS3Hic15cyMibGGA/640?wx_fmt=jpeg&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

裸机应用进程有其一席之地。它们通常很小，速度快，并且通过简单的应用进程相对容易理解。一旦需要更复杂的逻辑，RTOS就开始大放异彩。

![图片](https://mmbiz.qpic.cn/mmbiz_jpg/zcVcDoKYUnaFLC9f63Heb61F0lBic1aRLIJjfJ6yBGzNZnw3oibzoVTtc5RvkMH6rJpAias5D6DrniasgyyIOmplEQ/640?wx_fmt=jpeg&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

实时操作系统组件

- 计划进程：保证最高优先级线程正在运行的抢占式计划进程。
- 通信机制：信号量、消息队列、队列等。
- 关键区域机制：互斥体、门、锁等。
- 计时服务：时钟、定时器等。
- 电源管理：对于低功耗设备，电源管理通常是RTOS的一部分，因为它知道设备的状态。
- 内存管理：可变大小的堆、固定大小的堆等。
- 外设驱动器：UART、SPI、I2C等。
- 协议栈：蓝牙、无线网络等。
- 文档系统：FatFs等。
- 设备管理：异常处理、启动等。

## 5. POSIX

POSIX（Portable Operating System Interface）：可移植操作系统接口

SimpleLink SDK在TI-RTOS和FreeRTOS之上提供POSIX支持。这允许应用进程独立于底层RTOS。

POSIX API是底层实时操作系统之上的一个小填充码。创建POSIX线程时，将创建基础TI-RTOS（或FreeRTOS）任务。同样，在创建POSIX线程信号量时，将创建TI-RTOS（或FreeRTOS）信号量。

POSIX支持的一个很好的功能是能够从网络上获取基于POSIX的代码并快速使其正常工作。

POSIX不是实时操作系统。它是一个操作系统兼容性层，允许应用进程在操作系统之间轻松移植。


# RTOS线程通信

所有RTOS都提供标准的通信机制，如信号量、互斥锁、消息队列、链表等。

## 1. 信号量

信号量允许资源管理。任务可以在sem\_wait()上阻塞，直到资源变得可用（通过sem\_post()）。一个常见的用例是Hwi接收数据并发布信号量，以便任务可以处理它。

这是可取的，因为它可以最大限度地减少中断的持续时间。大多数RTOS都支持二进制和计数信号量。

![图片](https://mmbiz.qpic.cn/mmbiz_jpg/zcVcDoKYUnaFLC9f63Heb61F0lBic1aRLRJVZEFCe0MWEib9GRzEl5gPN0HZYZOS7aTZzevjdnPCJKK8ssiadt0SQ/640?wx_fmt=jpeg&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

## 2. 消息队列

消息队列对于在线程之间发送数据非常有用。消息队列可以配置为发送/接收任何大小的用户定义的消息。在这里，一个任务正在向另一个任务发送消息：

![图片](https://mmbiz.qpic.cn/mmbiz_jpg/zcVcDoKYUnaFLC9f63Heb61F0lBic1aRLZWeys9WgwHo20Lr9ePX8iaoQDFIuQVKzWkNgLOv4CrZtE1zELuJ6LaA/640?wx_fmt=jpeg&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

当希望将特定功能集中到单个任务中时，消息队列非常有用。所有其他线程都可以将消息发送到集中式任务进行处理。消息队列以线程安全的方式处理消息。

POSIX支持层中的消息队列是创建在TI-RTOS中的Mailboxes和FreeRTOS中的队列之上的。

执行

一个抢占式的调度进程在运行。假设以下线程是在main()中创建的：

`ISRX` ：中断服务例程

`MidA` ：在main()中创建第一个优先级为4

`MidB` ：在main()中创建第二个优先级为4

`High` ：在main()中创建最后一个优先级为8

![图片](https://mmbiz.qpic.cn/mmbiz_jpg/zcVcDoKYUnaFLC9f63Heb61F0lBic1aRL7TDiamjrEZkghxguuZHTX2rUvV6hxrvIeuuicb8riagUlAXqTcmkbkSLg/640?wx_fmt=jpeg&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

一旦内核的调度进程启动（在本例中为main()中的BIOS\_start()），所有任务都已准备好运行，首先运行的是High，因为它具有最高优先级。

1.`ISRX` 断言，因为它会抢占所有任务。 `High` 现在处于抢占状态。

2.`ISRX` 完成后，High将再次开始运行，直到它在 `Task_sleep()` （或某些阻塞 `API` ）上阻塞。现在， `MidA` 可以运行了。

3.`MidA` 一直运行，直到它遇到阻塞调用（比如Semaphore\_pend()）。现在， `MidB` 可以运行了。

4.`MidB` 一直运行到High取消阻塞（假设Task\_sleep()已过期）。 `MidB` 现在被抢占了。

5.`High` 将一直运行，直到 `ISRX` 被断言并抢占High。注意：现在有两个任务被抢占。

6.`MidA` 准备就绪（假设 `ISRX` 发布了它被阻止的信号量）。 `MidA` 不会运行，因为有更高优先级的线程正在运行。

7.`ISRX` 完成，因此 `High` 再次运行，然后再次阻塞，因此 `MidB` 再次运行，直到它阻塞。现在 `MidA` 可以运行，因为没有更高优先级的任务正在运行。注意： `MidA` 必须等到 `MidB` 完成后，因为当 `MidA` 准备就绪时， `MidB` 正在运行。

8.`MidA` 阻塞，现在没有线程正在运行或准备运行，因此Idle运行。

9.`MidB` 取消阻塞并运行。