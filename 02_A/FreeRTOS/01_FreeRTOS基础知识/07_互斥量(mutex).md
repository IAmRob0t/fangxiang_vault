---
tags:
  - freeRTOS
---
怎么独享厕所？自己开门上锁，完事了自己开锁。

使用队列、信号量，都可以实现互斥访问，以信号量为例：
- 信号量初始值为 1 任务 A 想上厕所，"take"信号量成功，它进入厕所
- 任务 B 也想上厕所，"take"信号量不成功，等待
- 任务 A 用完厕所，"give"信号量；轮到任务 B 使用

这需要有 2 个前提：
- 任务B很老实，不撬门(一开始不"give"信号量)
- 没有坏人：别的任务不会"give"信号量

可以看到，使用信号量确实也可以实现互斥访问，但是不完美。

使用互斥量可以解决这个问题，它的核心在于：谁上锁，就只能由谁开锁。

很奇怪的是，FreeRTOS 的互斥锁，并没有在代码上实现这点：
- 即使任务A获得了互斥锁，任务B竟然也可以释放互斥锁。
- 谁上锁、谁释放：只是约定。

# 互斥量的使用场合

- 跟二进制信号量的对比：
	- 能解决优先级反转的问题：优先级继承
	- 能解决递归上锁

> [!NOTE] 
> 互斥量本质上是带有**优先级继承**机制的二进制信号量，而二进制信号量不具备此功能。 优先级继承用于避免优先级反转（priority inversion）问题：在高优先级任务等待低优先级任务释放资源时，互斥量会临时提升低优先级任务的优先级，确保高优先级任务尽快获得资源。

# 互斥量函数

* 常规使用：
	* 源码：`16_freertos_example_mutex`
	* 来自视频配套源码：`15_freertos_example_semaphore`

## 创建

( [[FreeRTOS完全开发手册之上册_快速入门.pdf#page=109&selection=10,0,12,23&color=note|📖]])
创建互斥量的函数有2种：动态分配内存，静态分配内存，函数原型如下：

```c
/* 创建一个互斥量，返回它的句柄。
 * 此函数内部会分配互斥量结构体
 * 返回值: 返回句柄，非NULL表示成功
 */
 SemaphoreHandle_t xSemaphoreCreateMutex( void );
 
 /* 创建一个互斥量，返回它的句柄。
  * 此函数无需动态分配内存，所以需要先有一个StaticSemaphore_t结构体，并传入它的指针
 * 返回值: 返回句柄，非NULL表示成功
 */
SemaphoreHandle_t xSemaphoreCreateMutexStatic( StaticSemaphore_t *pxMutexBuffer );
```

## 其他函数

( [[FreeRTOS完全开发手册之上册_快速入门.pdf#page=109&selection=22,0,27,13&color=note|📖]])
要注意的是，互斥量不能在ISR中使用。各类操作函数，比如删除、give/take，跟一般是信号量是一样的。

```c
/*
 * xSemaphore: 信号量句柄，你要删除哪个信号量, 互斥量也是一种信号量
 */
void vSemaphoreDelete (SemaphoreHandle_t xSemaphore);

/* 释放 */
BaseType_t xSemaphoreGive (SemaphoreHandle_t xSemaphore);

/* 释放(ISR版本) */
BaseType_t xSemaphoreGiveFromISR (
				SemaphoreHandle_t xSemaphore,
				BaseType_t *pxHigherPriorityTaskWoken
			);
			
/* 获得 */
BaseType_t xSemaphoreTake (
				SemaphoreHandle_t xSemaphore,
				TickType_t xTicksToWait
			);
			
/* 获得(ISR版本) */
xSemaphoreGiveFromISR (
				SemaphoreHandle_t xSemaphore,
				BaseType_t *pxHigherPriorityTaskWoken
			);
```

# 示例 15: 互斥量基本使用

# 示例 16: 谁上锁就由谁解锁？

# 示例 17: 优先级反转

* 优先级反转的例子: 
	* 源码：`17_freertos_example_mutex_inversion`
	* 来自文档配套的源码 `FreeRTOS_17_mutex_inversion`

简单说：​​ 就是一个中优先级的任务，通过“卡住”一个持有资源（锁）的低优先级任务，​**​间接地阻塞了​**​最高优先级的任务，导致系统响应变慢，违背了优先级设计的初衷。FreeRTOS 提供了“优先级继承”机制（在创建互斥量时设置）来尝试缓解这个问题。

# 示例 18: 优先级继承

* 使用互斥量解决优先级反转
	* 源码：`18_freertos_example_mutex_inheritance`
	* 来自文档配套的源码 `FreeRTOS_18_mutex_inheritance`

当一个低优先级任务持有高优先级任务所需要的互斥量时，系统会临时将这个低优先级任务的优先级提升到和那个等待的高优先级任务一样高，以防止被中间优先级的任务打断，从而保证高优先级任务能够尽快获得资源。​

# 递归锁

本节源码：`19_freertos_example_mutex_recursive`，源自 `16_freertos_example_mutex`

* 对于互斥量，本意是：谁持有，就由谁释放
* 但是FreeRTOS并没有实现这点：A持有，B也可以释放（Linux 也没有，RT-Thread 就实现了）
* 递归锁实现了
	* 谁持有，就由谁释放
	* 递归上锁/解锁

递归锁就像你家的门锁：同一个任务（你）可以多次用同一把钥匙（递归锁）开门和锁门，不会把自己锁在外面，但其他人（其他任务）必须等你彻底归还钥匙（解锁）后才能使用。​

如果同一个任务多次获取同一个普通锁而不释放，就会像自己把自己锁在门外一样，导致任务永远卡死（死锁），无法继续运行。​

( [[FreeRTOS完全开发手册之上册_快速入门.pdf#page=119&selection=24,0,24,3&color=note|📖]])
递归锁

## 死锁的概念



## 自我死锁

## 函数

## 示例 19: 递归锁

# 常见问题