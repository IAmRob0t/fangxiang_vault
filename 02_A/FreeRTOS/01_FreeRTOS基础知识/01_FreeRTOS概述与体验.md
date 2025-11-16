---
tags:
  - freeRTOS
---
[FreeRTOS/FreeRTOS 内核手册](https://github.com/FreeRTOS/FreeRTOS-Kernel-Book/tree/main)

[[00_C语言的本质#ARM 架构与汇编简明教程]]

# FreeRTOS 目录结构

![[FreeRTOS完全开发手册之上册_快速入门 1.pdf#page=5&rect=79,337,512,676|FreeRTOS完全开发手册之上册_快速入门 1, p.5]]

主要涉及 2 个目录：
- Demo
	- Demo目录下是工程文件，以"芯片和编译器"组合成一个名字
	- 比如：CORTEX_STM32F103_Keil
- Source
	- 根目录下是核心文件，这些文件是通用的
	- portable目录下是移植时需要实现的文件
		- 目录名为：`[compiler]/[architecture]`
		- 比如：RVDS/ARM_CM3，这表示cortexM3架构在RVDS工具上的移植文件

# 核心文件

FreeRTOS 的最核心文件只有 2 个：
- `FreeRTOS/Source/tasks.c`
- `FreeRTOS/Source/list.c`

其他文件的作用也一并列出：

| FreeRTOS/Source/下的文件 | 作用                             |
| -------------------- | ------------------------------ |
| `tasks.c`            | 必需，任务操作                        |
| `list.c`             | 必须，列表                          |
| `queue.c`            | 基本必需，提供队列操作、信号量 (semaphore) 操作 |
| `timer.c `           | 可选，software timer              |
| `event_groups.c`     | 可选，提供 event group 功能           |
| `croutine.c`         | 可选，过时了                         |

# 移植时涉及的文件

移植 FreeRTOS 时涉及的文件放在 `FreeRTOS/Source/portable/[compiler]/[architecture]` 目录下， 比如：RVDS/ARM_CM3，这表示 cortexM3 架构在 RVDS 或 Keil 工具上的移植文件。

里面有 2 个文件：
- `port.c`
- `portmacro.h`

# 添加串口打印功能

* 去掉无关的代码：LCD 等
* 增加串口打印功能
	* 初始化串口
	* 实现 `fputc()`
		* ![[STM32F103xx参考手册(英文原版).pdf#page=818&rect=126,355,527,443&color=note|📖]]
		* ( [[STM32F103xx参考手册(英文原版).pdf#page=820&selection=119,0,120,65&color=note|📖]])
		  The Data register performs a double function (read and write) since it is composed of two registers, one for transmission (TDR) and one for reception (RDR)

```c
int fputc(int ch, FILE *f)
{
	USART_TypeDef* USARTx = USART1;
	
	USARTx->DR = ch
	return ch;
}
```


# 头文件相关

## 头文件目录

FreeRTOS 需要 3 个头文件目录：
- FreeRTOS本身的头文件：`FreeRTOS/Source/include`
- 移植时用到的头文件：`FreeRTOS/Source/portable/[compiler]/[architecture]`
- 含有配置文件 `FreeRTOSConfig.h` 的目录

## 头文件

| 头文件                | 作用                                                                                                                        |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------- |
| `FreeRTOSConfig.h` | FreeRTOS 的配置文件，比如选择调度算法：`configUSE_PREEMPTION` 每个 demo 都必定含有 `FreeRTOSConfig.h` 建议去修改 demo 中的 `FreeRTOSConfig.h`，而不是从头写一个 |
| `FreeRTOS.h`       | 使用 FreeRTOS API 函数时，必须包含此文件。在 FreeRTOS. h 之后，再去包含其他头文件，比如： `task.h`、`queue.h`、`semphr.h`、`event_group.h`                  |

# 内存管理

文件在 `FreeRTOS/Source/portable/MemMang` 下，它也是放在 `portable` 目录下，表示你可以提供自己的函数。

源码中默认提供了 5 个文件，对应内存管理的 5 种方法。

后续章节会详细讲解。

| 文件       | 优点                   | 缺点           |
| -------- | -------------------- | ------------ |
| `heap_1.c` | 分配简单，时间确定            | 只分配、不回收      |
| `heap_2.c` | 动态分配、最佳匹配            | 碎片、时间不定      |
| `heap_3.c` | 调用标准库函数              | 速度慢、时间不定     |
| `heap_4.c` | 相邻空闲内存可合并            | 可解决碎片问题、时间不定 |
| `heap_5.c` | 在 heap_4 基础上支持分隔的内存块 | 可解决碎片问题、时间不定 |

# Demo

Demo 目录下是预先配置好的、没有编译错误的工程。目的是让你可以基于它进行修改，以适配你的单板。

这些 Demo 还可以继续精简：
- `Demo/Common` 中的文件可以完全删除
- `main` 函数中只需要保留2个函数：
	- `prvSetupHardware()`
	- `vTaskStartScheduler()`
	- 如下所示

```c
int main (void)
{
	/* Perform any hardware setup necessary. */
	prvSetupHardware ();
	
	/* --- APPLICATION TASKS CAN BE CREATED HERE --- */
	
	/* Start the created tasks running. */
	vTaskStartScheduler ();
	
	/* Execution will only reach here if there was insufficient heap to start the scheduler */
	for ( ; ; );
	return 0;
}
```

# 数据类型和编程规范

## 数据类型

每个移植的版本都含有自己的 `portmacro.h` 头文件，里面定义了 2 个数据类型：
- `TickType_t`
	- FreeRTOS 配置了一个周期性的时钟中断：Tick Interrupt
	- 每发生一次中断，中断次数累加，这被称为 tick count
	- tick count 这个变量的类型就是 `TickType_t`
	- `TickType_t` 可以是16位的，也可以是32位的
	- `FreeRTOSConfig.h` 中定义 `configUSE_16_BIT_TICKS` 时，`TickType_t` 就是 `uint16_t`
	- 否则 `TickType_t` 就是 `uint32_t`
	- 对于 32 位架构，建议把 `TickType_t` 配置为  `uint32_t`
- `BaseType_t`
	- 这是该架构最高效的数据类型
	- 32 位架构中，它就是 `uint32_t`
	- 16 位架构中，它就是 `uint16_t`
	- 8 位架构中，它就是 `uint8_t`
	- `BaseType_t` 通常用作简单的返回值的类型，还有逻辑值，比如 `pdTRUE/pdFALSE`

## 变量名

变量名有前缀：

| 变量名前缀 | 含义                                                      |
| ----- | ------------------------------------------------------- |
| `c`   | `char`                                                  |
| `s`   | `int16_t`, `short`                                      |
| `l`   | `int32_t`, `long`                                       |
| `x`   | `BaseType_t`，其他非标准的类型：结构体、`task handle`、`queue handle`等 |
| `u`   | `unsigned`                                              |
| `p`   | 指针                                                      |
| `uc`  | `uint8_t`, `unsigned char`                              |
| `pc`  | `char`指针                                                |

## 函数名

函数名的前缀有 2 部分：返回值类型、在哪个文件定义。

| 函数名前缀               | 含义                                      |
| ------------------- | --------------------------------------- |
| `vTaskPrioritySet`  | 返回值类型：`void` 在 `task.c` 中定义             |
| `xQueueReceive`     | 返回值类型：`BaseType_t` 在 `queue.c` 中定义      |
| `pvTimerGetTimerID` | 返回值类型：`pointer to void` 在 `timer.c` 中定义 |

## 宏的名

宏的名字是大小，可以添加小写的前缀。前缀是用来表示：宏在哪个文件中定义。

| 宏的前缀                                 | 含义：在哪个文件里定义                  |
| ------------------------------------ | ---------------------------- |
| `port` (比如 `portMAX_DELAY`)          | `portable.h` 或 `portmacro.h` |
| `task` (比如 `taskENTER_CRITICAL()`)   | `task.h`                     |
| `pd` (比如 `pdTRUE`)                   | `projdefs.h`                 |
| `config` (比如 `configUSE_PREEMPTION`) | `FreeRTOSConfig.h`           |
| `err` (比如 `errQUEUE_FULL`)           | `projdefs.h`                 |

通用的宏定义如下：

| 宏         | 值   |
| --------- | --- |
| `pdTRUE`  | 1   |
| `pdFALSE` | 0   |
| `pdPASS`  | 1   |
| `pdFAIL`  | 0   |

# 使用模拟器运行第 1 个程序

( [[FreeRTOS完全开发手册之上册_快速入门 1.pdf#page=19&selection=2,0,6,4&color=note|📖]])

# 使用逻辑分析仪

( [[FreeRTOS完全开发手册之上册_快速入门 1.pdf#page=19&selection=2,0,6,4&color=note|📖]])
