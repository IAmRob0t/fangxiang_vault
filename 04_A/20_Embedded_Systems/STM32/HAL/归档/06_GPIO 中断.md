---
tags:
  - hal
deadline: 2025-03-28
---
# 中断概念的引入

## 1. 按键的丢失

![[HAL快速入门与项目实战.pdf#page=58&rect=160,602,445,673]]

如果通过死循环的方式读取 GPIO 引脚判断按键的状态，容易丢失按键。比如，上图中如果能在①②③处读取引脚状态，就能判断出引脚被按下、松开。如果第 4 次读取按键时，刚好位于上图④处，就丢失了 2 个按键动作。

## 2. 日常生活中断示例

你在看书，门铃响了：这就是一个中断。你会插入书签（保存现场），开门取快递（处理中断），回来从书签位置处继续看书（恢复现场）。

## 3. 嵌入系统中也有类似的情况

![[HAL快速入门与项目实战.pdf#page=59&rect=149,644,448,747&color=note]]

- CPU 在运行的过程中，也会被各种“异常”打断。这些“异常”有：
	- 指令未定义
	- 指令、数据访问有问题
	- SWI (软中断) 
	- **中断** - 中断也属于一种“异常”，导致中断发生的情况有很多，比如：
		- 按键
		- 定时器
		- ADC 转换完成
		- UART 发送完数据、收到数据等等

这些众多的“中断源”，汇集到“中断控制器”，由“中断控制器”选择优先级最高的中断并通知 CPU。

## 4. 中断的处理流程

[[Arm 芯片对异常 (中断) 处理过程]]：
1. 初始化
	- **设置中断源，让它可以产生中断**
	- **设置中断控制器(可以屏蔽某个中断，优先级)**
	- **设置 CPU 总开关(使能中断)**
2. 然后就可以执行其他程序了，比如 main 函数
3. 产生中断：比如按下按键--->中断控制器--->CPU
4. CPU 每执行完一条指令都会检查有无中断/异常产生
5. CPU 发现有中断/异常产生，开始处理。
6. 发生中断后，对于不同的异常，跳去不同的地址执行程序。

这地址上，只是一条跳转指令，跳去执行某个函数 (地址)，这个就是异常向量。③④⑤都是硬件做的。

---

这些函数做什么事情？ 
1. 保存现场 (保存被中断瞬间的各个寄存器的值)
2. 处理异常 (中断): 分辨中断源，再调用不同的处理函数
3. 恢复现场（就是从被中断的地方继续运行）

如下图所示：

![[HAL快速入门与项目实战.pdf#page=59&rect=103,84,449,186]]

# STM32 中断体系结构

参考资料：

[[../../../../../01_P/ARM 架构/attachments1/Cortex-M3权威指南(中文参考).pdf]]

## 1. 中断结构图

结构图如下：

![[HAL快速入门与项目实战.pdf#page=60&rect=159,550,461,660]]

沿着中断信号从源头（比如某个 GPIO 引脚），如何一路发给 CPU，简述各个部件的功能：
- **GPIO：可以配置某个引脚能否发出中断信号**
	- 如下图，PA0~PG0 这多个 0 号引脚中，同一时间只能有一个连接到 EXTI0，即**它们中同一时间只能有一个被用作中断引脚**，可以在 AFIO_EXTICR1 寄存器中选择某个引脚。 ![[STM32F103xx参考手册(英文原版).pdf#page=210&rect=232,280,392,738]]
	- 外部中断共有 20 条中断线
		- 外部中断线 EXTI16连接到PVD输出；
		- 外部中断线 EXTI17连接到RTC警告事件；
		- 外部中断线 EXTI17连接到RTC警告事件；
		- 外部中断线 EXTI19连接到ETH唤醒事件；（只有在内部有ETH模块的设备才会有这条线，F103 没有）
		- 112个引脚被分成了16个外部中断线，不同组的同一个引脚号连接到同一个外部中断线上。
	- 如果要同时用到 PA0 和 PB0 作为外部中断引脚怎么办？
	  不允许。不要让相同引脚号的引脚被设计为外部中断使用。
		- STM32F103 的复用功能 IO 的寄存器
			- AFIO_EXTICR1 -> EXTI 0~3
			- AFIO_EXTICR2 -> EXTI 4~7 
			- AFIO_EXTICR3 -> EXTI 8~11
			- AFIO_EXTICR4 ->  EXTI 12~15
	- 芯片手册中有 AFIO_EXTICR1 寄存器的描述： 
		- ![[STM32F103xx参考手册(英文原版).pdf#page=191&rect=60,488,534,756]]
		1. AFIO_EXTICR1有32位，只有低16位可以设置值，高16位是保留位；
		2. 它可以配置4跟外部中断线，每4位控制一根外部中断线；
		3. 对于某一根外部中断线，同一时刻只能选择一组GPIO的引脚作为外部中断输入引脚；
	- 如果同时用到PA0和PB0作为外部中断引脚了会发生什么？
	  如果先将PA0初始化作EXTI0的外部中断输入引脚，再将PB0初始化作EXTI0的输入引脚，那么最终EXTI0的输入引脚是PB0；反过来的话则是PA0。
- **EXTI：对外部中断进行更详细的配置(触发方式、使能、读取当前的状态)**
	- EXTI 内部框图如下：![[STM32F103xx参考手册(英文原版).pdf#page=207&rect=123,144,531,494&color=yellow]]
	- 还是以 EXTI0 为例，在 EXTI 内部，可以**配置** EXTI0 的中断**触发方式**（上升沿触发、下降沿触发、双边沿触发、软件触发）、**使能**（是否允许 EXTI0 传输到 NVIC）、**读取它的当前状态**（是否有待处理的中断）。
	- 寄存器如下：![[HAL快速入门与项目实战.pdf#page=61&rect=164,191,453,304&color=yellow]]
- **NVIC：管理多个中断源（使能/屏蔽、优先级），提供“[[#2. 异常向量表|异常向量表]]”**
	- 在 NVIC 里，每一个异常、中断，都有一个编号：![[HAL快速入门与项目实战.pdf#page=62&rect=176,441,443,744&color=yellow]]
	- 对于这些中断，都可以单独设置：
		1. **使能/屏蔽**：是否允许它传输到 CPU
		2. **优先级**
	- 当各类中断进入 NVIC 后，NVIC 里还有开关，这些中断能否发给 CPU？假设有些中断是同时发生的，哪一个能优先传给 CPU？
	- 在 NVIC 里，可以设置中断优先级、中断向量表（当发生中断时，去这个表里找到、调用对应的处理函数）。
	- NVIC 里使能中断的寄存器如下（优先级相关寄存器看后面）：![[HAL快速入门与项目实战.pdf#page=63&rect=151,499,470,769&color=yellow]]
- **CPU：CPU内部也有一个开关，是否使能CPU处理中断**
	- CPU 内部，有一个“PRIMASK”寄存器，“Priority mask”，往它写入 1 可以禁止所有中断；往它写入 0，可以使能中断 [[#2.3. 设置 CPU]]。代码如下：
	- ![[HAL快速入门与项目实战.pdf#page=63&rect=138,337,459,455]]
	- 如果还想精确地禁止“优先级低于某个数值”的那些中断，可以使用“BASEPRI”。比如想禁止“优先级数值大于等于 0x60 的所有异常”，可以把 0x60 写入 BASEPRI 寄存器。代码如下：
		```
		: 屏蔽优先级为0x60~0xFF的异常
		MOVS R0, #0x60
		MSR BASEPRI, R0
		
		: 取消屏蔽
		MOVS R0, #0
		MSR BASEPRI, R0
		```

当①②③④各部件都设置、使能好了之后，某个中断发生了，比如 PA0 的电平从高变低了，就会触发中断。CPU 接收到中断后，就会跳转到 NVIC 中设置的“异常向量表”，根据 EXTI0 的 ID 找到表里对应的函数，执行它。

## 2. 异常向量表

在中 `startup_stm32f103xe.s`，可以看到如下代码：

![[HAL快速入门与项目实战.pdf#page=64&rect=154,456,450,726&color=yellow]]

需要把这个表格的基地址即 `__Vectors` 告诉 NVIC，这样：当 CPU 检测到发生异常时，才会根据异常 ID 在这个表格里找到并执行对应函数。 

## 3. 中断优先级

在 NVIC 里，对于每一个中断，都有一个 8 位的寄存器被用来表示它的优先级。这个 8 位的寄存器，被分为 2 部分，分别表示：分组优先级（也叫抢占优先级）、子优先级。

![[HAL快速入门与项目实战.pdf#page=64&rect=103,240,503,340]]

- **分组优先级（抢占优先级）** 被用来判断：当前正在处理的中断，**能否被打断**。比如当前正在处理 EXT0 中断，它的分组优先级为 3；如果这时候发生了 EXT1 中断，它的分组优先级为 4（数值越高，优先级越低），那么 EXT1 的中断就无法打断 EXT0，等 EXT0 的中断处理完毕，EXT1 的中断才能被处理。但是，如果 EXT1 的分组优先级为 2，那么当前的 EXT0 中断就被“抢占”，先执行 EXT1 的中断处理函数，再继续执行“被抢占的 EXT0”中断函数。
- **子优先级** 被用来判断：两个中断同时发生时，**谁先被处理**。还是以 EXT0、EXT1 为例，如果它们同时发生了，那么分组优先级高的中断先被处理；如果分组优先级相同，那么子优先级高的先被处理；如果连子优先级也相同，那么编号小的 EXT0 先被处理。

> [!warning] 注意
> 如果 EXT0、EXT1 的分组优先级相同，是不会发生“抢占”的”。比如 EXT0 中断正在被处理，EXT1 紧接着被触发了，即使 EXT1 的子优先级高于 EXT0，EXT1 也不会抢占 EXI0。当 EXT0 被处理完毕，才轮到 EXT1 被处理。

那么，在每个中断的 8 位优先级状态寄存器里，有 2 个问题：

> [!question] 这 8 位都实现了吗？
> 不一定，比如 STM32F103 系列芯片里只实现了 4 位。实现越多位数，硬件设计越复杂， 功耗越高。实现多少位，这是由芯片公司决定的。

> [!question] 这 8 位里，哪几位表示分组优先级（剩下的就表示子优先级）？
> 这是可配置的，NVIC 内部有一个“优先级分组的配置寄存器”，通过它可以设置所有中断的“8 位优先级寄存器里，哪几位表示分组优先级”。如下图所示：
> ![[HAL快速入门与项目实战.pdf#page=65&rect=114,531,495,662]]

# GPIO 中断编程

## 1. 编程示例

[[04_A/STM32/原理图/DshanMCU-F103_baseboard.pdf|原理图]]

## 2. HAL 库代码解析

解读源码：“0601_key_isr”

### 2.1. 设置 GPIO 和 EXTI

在 `Core\Src\gpio. C` 的“MX_GPIO_Init”函数中，有如下代码：

```c
/*Configure GPIO pin : PB14 */
GPIO_InitStruct.Pin = GPIO_PIN_14;
GPIO_InitStruct.Mode = GPIO_MODE_IT_RISING_FALLING;
GPIO_InitStruct.Pull = GPIO_NOPULL;
HAL_GPIO_Init(GPIOB, &GPIO_InitStruct);
```

虽然 `HAL_GPIO_Init` 以 GPIO 命名，但是在上述代码里，还是会设置“GPIO”模块选择把 PB14 连接到 EXTI14，设置 EXTI14 的中断触发方式为“双边沿”。

![[STM32F103xx参考手册(英文原版).pdf#page=192&rect=61,220,531,484]]

### 2.2. 设置 NVIC

```c
/* EXTI interrupt init*/
HAL_NVIC_SetPriority(EXTI15_10_IRQn, 0, 0);
HAL_NVIC_EnableIRQ(EXTI15_10_IRQn);
```

```c
HAL_StatusTypeDef HAL_Init(void)
{
  /* Configure Flash prefetch */
#if (PREFETCH_ENABLE != 0)
#if defined(STM32F101x6) || defined(STM32F101xB) || defined(STM32F101xE) || defined(STM32F101xG) || \
    defined(STM32F102x6) || defined(STM32F102xB) || \
    defined(STM32F103x6) || defined(STM32F103xB) || defined(STM32F103xE) || defined(STM32F103xG) || \
    defined(STM32F105xC) || defined(STM32F107xC)

  /* Prefetch buffer is not available on value line devices */
  __HAL_FLASH_PREFETCH_BUFFER_ENABLE();
#endif
#endif /* PREFETCH_ENABLE */

  /* Set Interrupt Group Priority */
  HAL_NVIC_SetPriorityGrouping(NVIC_PRIORITYGROUP_4);
```

对于前面的 EXTI0... 可以直接发给 CPU ，为了节约硬件资源，将 EXTI10~EXTI15 共 6 个中断合并为一个，发给 NVIC。

所以上述代设置的中断为  `EXTI15_10_IRQn` ：设置它的优先级、使能它（能够发给 CPU）。

向量表则是使用默认的值

### 2.3. 设置 CPU

无需配置 CPU，可以使用调试工具查看 CPU 寄存器，发现它默认使能了中断处理：

![[HAL快速入门与项目实战.pdf#page=66&rect=236,207,384,440]]

# 使用 OLED 进行调试

本节程序源码为“0602_key_isr_oled”，在“0601_key_isr”的基础上修改得来。

![[04_A/STM32/原理图/DshanMCU-F103_baseboard.pdf#page=1&rect=38,243,192,321]]

## 1. STM32CuMX 配置

OLED 屏幕使用 I2C1 通道，I2C1 使用 PB6、PB7 作为 SCL、SDA 引脚，配置如下：

![[HAL快速入门与项目实战.pdf#page=68&rect=110,514,487,733]]

## 2. 上机测试

这里使用到的驱动以及测试代码位于 `Drivers/DShanMCU-F103/driver_oled. C` 和 “Drivers/DShanMCU-F103/driver_oled. H” 中。把“DShanMCU-F103 开发板资料\5_程序源码\01_单片机程序\03_参考的源码\DshanMCU-F103\01_nwatch_game. 7z”解压开，把里面 `Drivers/DShanMCU-F103/driver_oled. C` 和 `Drivers/DShanMCU-F103/driver_oled. H` 加入工程。

其中，OLED_Test 函数完成了 OLED 屏幕的初始化与测试工作。

## 3. 函数说明

OLED 的分辨率是 `128*64`，要显示 `8*16` 点阵字符时，每行最多可以显示 16 个字符，所以下面罗列的函数里，**X 坐标的取值为 0~15**。最多同时能显示 4 行字符，按理说 Y 坐标取值应该为 0~3，但是为了更细致地调整字符的 Y 坐标，我们把 **Y 坐标的取值范围设定为 0~7**。

下图里，分别在坐标 (0, 0)、(0,1) 位置显示了字符“A”；在坐标()显示了字符“B”；在坐标（0,4）、（0,5）显示了字符“C”；在坐标（0,6）显示了字符“D”。

![[HAL快速入门与项目实战.pdf#page=68&rect=202,80,414,270]]

---

OLED 初始化：

```c
void OLED_Init(void);
```

清除屏幕（把屏幕全部显示为黑色）：

```c
 void OLED_Clear(void);
```

在屏幕上指定位置显示 ASCII 字符：

```c
/*
 * 输入参数：x --> x坐标(0~15)
 * y --> y坐标(0~7)
 * c --> 显示的字符
*/
void OLED_PutChar(uint8_t x, uint8_t y, char c);
```

在屏幕上指定位置显示字符串：

```c
/*
 * 输入参数：x --> x坐标(0~15)
 * y --> y坐标(0~7)
 * str --> 显示的字符
*/
int OLED_PrintString(uint8_t x, uint8_t y, const char *str);
```

从屏幕上指定位置清除一行：

```c
/*
 * 输入参数：x - 从这里开始
 * y - 清除这行
*/
void OLED_ClearLine(uint8_t x, uint8_t y);
```

[[HAL快速入门与项目实战.pdf#page=70&selection=42,0,47,7&color=note]]

# 按键驱动程序改进

## 1. 使用定时器消除抖动

> 本节程序源码为“0603_key_timer”，在“0602_key_isr_oled”的基础上修改得来。

![[HAL快速入门与项目实战.pdf#page=72&rect=152,453,443,681]]

在实际的按键操作中，可能会有机械抖动。按下或松开一个按键，它的 GPIO 电平会反复变化，最后才稳定。一般是 5~10 毫秒才会稳定。

> [!question] 如果不处理抖动的话，用户只操作一次按键，中断程序可能会上报多个数据。怎么处理？
> 1. 在按键中断程序中，可以循环判断几十亳秒，发现电平稳定之后再上报
> 2. 使用定时器

显然第 1 种方法太耗时，违背“中断要尽快处理”的原则，你的系统会很卡。怎么使用定时器？看下图：

![[HAL快速入门与项目实战.pdf#page=72&rect=117,131,480,343]]

> [!NOTE] 核心在于：
> 在 GPIO 中断中并不立刻记录按键值，而是修改定时器超时时间，10ms 后再处理。如果 10ms 内又发生了 GPIO 中断，那就认为是抖动，这时再次修改超时时间为 10ms。

只有 10ms 之内再无 GPIO 中断发生，那么定时器的函数才会被调用。在定时器函数中记录按键值。

---

### 1.1. 使用定时器消除抖动程序流程

#### 1.1.1.  系统闹钟

- ​作用：每毫秒响一次，提醒主厨该检查所有正在倒计时的任务了。
- ​代码对应：
    ```c
    // 系统定时器中断函数（在 stm32f1xx_it.c）
    void SysTick_Handler(void) {
        HAL_IncTick();                // 更新系统时间（类似厨房的时钟往前走）
        check_timer();                // 检查所有软件定时器是否超时
    }
    ```

#### 1.1.2. 软件定时器

这是一个虚拟的倒计时器，用来记录某个任务需要多久后执行。比如：“10毫秒后提醒主厨关火”。
- ​结构体定义：
    ```c
    struct soft_timer {
        uint32_t timeout;  // 定时器超时时间（例如：当前时间 + 10毫秒）
        void *args;        // 任务参数（比如要关哪个灶台）
        void (*func)(void *); // 超时后要执行的任务（比如关火函数）
    };
    ```

#### 1.1.3. 门铃按键（GPIO中断）​

- ​作用：当有人按门铃（比如按下按键），触发一个中断，主厨立刻停下手头工作去处理。
- ​代码对应：
    ```c
    // 按键中断回调函数（在 main.c）
    void HAL_GPIO_EXTI_Callback(uint16_t GPIO_Pin) {
        if (GPIO_Pin == GPIO_PIN_14) {
            mod_timer(&key_timer, 10); // 启动一个10毫秒的定时器
        }
    }
    ```

#### 1.1.4. 定时器如何工作？

##### 1.1.4.1. 启动定时器

按下按键后，调用 `mod_timer` 设置定时器的超时时间：

```c
void mod_timer(struct soft_timer *pTimer, uint32_t timeout) {
    pTimer->timeout = HAL_GetTick() + timeout; // 当前时间 + 10ms
}
```

##### 1.1.4.2. 检查定时器

系统闹钟每毫秒检查一次定时器是否超时：

```c
void check_timer(void) {
    if (key_timer.timeout <= HAL_GetTick()) {
        key_timer.func(key_timer.args); // 超时后执行任务（比如g_key_cnt++）
    }
}
```

##### 1.1.4.3. ​执行任务

超时后，主厨执行 `key_timerout_func`：

```c
void key_timerout_func(void *args) {
    g_key_cnt++;       // 记录按键按下的次数
    key_timer.timeout = ~0; // 重置定时器（~0表示停止）
}
```

#### 1.1.5. ​显示结果：OLED屏幕

主厨每次执行完任务后，会在小黑板上更新按键按下的次数：

```c
// 主循环（在 main.c）
while (1) {
    OLED_PrintSignedVal(0, 6, g_key_cnt); // 显示按键次数
}
```

## 2. 环形缓冲区的概念

即使使用中断函数或者定时器函数记录按键，如果只能记录一个键值的话，不能及时读出来，再次发生中断时新值就会覆盖旧值。要解决数据被覆盖的问题，可以使用一个稍微大点的缓冲区，这就涉及数据的写入、读出。可以使用环形缓冲区。

环形缓冲区特别适合这种场景：
- 一方写 buffer
- 另一方读 buffer

环形缓冲区实际上还是一维数组，假设有 N 个数组项，从第 0 个数组项开始遍历，访问完第 N-1 个数组项后，再从 0 开始——这就是“环形”的含义，如下图所示：

![[HAL快速入门与项目实战.pdf#page=73&rect=234,509,359,608]]

环形缓冲区的工作原理如下图所示：

![[HAL快速入门与项目实战.pdf#page=73&rect=145,181,447,497]]

1. 有读位置、写位置：r、w，它们表示“下一个要读的位置”、“下一个要写的位置”。初始值都是 0。
2. 写数据时：把数据写入 `buffer[w]` ，然后调整 w 指向下一个位置（当 w 越界后要从 0 开始）。
3. 读数据时：从 `buffer[r]` 读出数据，然后调整 r 指向下一个位置（当 r 越界后要从 0 开始）。
4. **判断 buffer 为空：r 等于 w 时表示空**，所以程序可以写成当 `buffer[r] != buffer[w]` 时，buffer 不为空，可以读数据
5. **判断 buffer 为满：“下一个写位置”等于当前读位置**，，所以程序可以写成

## 3. 环形缓冲区的编程

本节程序源码为“0604_key_circle_buffer”，在“0603_key_timer”的基础上修改得来。

```c
/* ------  circle_buffer.h  ------ */

#ifndef _CIRCLE_BUF_H
#define _CIRCLE_BUF_H

#include <stdint.h>

typedef struct circle_buf {
	uint32_t r;
	uint32_t w;
	uint32_t len;
	uint8_t *buf;
} circle_buf, *p_circle_buf;

void circle_buf_init(p_circle_buf pCircleBuf, uint32_t len, uint8_t *buf);

int circle_buf_read(p_circle_buf pCircleBuf, uint8_t *pVal);

int circle_buf_write(p_circle_buf pCircleBuf, uint8_t val);

#endif /* _CIRCLE_BUF_H */

```

```c
/* ------  circle_buffer.c  ------ */

#include "circle_buffer.h"

void circle_buf_init(p_circle_buf pCircleBuf, uint32_t len, uint8_t *buf)
{
	pCircleBuf->r = pCircleBuf->w = 0;
	pCircleBuf->len = len;
	pCircleBuf->buf = buf;
}

int circle_buf_read(p_circle_buf pCircleBuf, uint8_t *pVal)
{
	if(pCircleBuf->w != pCircleBuf->r)
	{
		*pVal = pCircleBuf->buf[pCircleBuf->r];
		
		pCircleBuf->r++;
		
		if (pCircleBuf->r == pCircleBuf->len)
			pCircleBuf->r = 0;
		return 0;
	}
	else
	{
		return -1;
	}
}

int circle_buf_write(p_circle_buf pCircleBuf, uint8_t val)
{
	uint32_t next_w;
	
	next_w = pCircleBuf->w + 1;
	if (next_w == pCircleBuf->len)
		next_w = 0;
	
	if (next_w != pCircleBuf->r)
	{
		pCircleBuf->buf[pCircleBuf->w] = val;
		pCircleBuf->w = next_w;
		return 0;
	}
	else
	{
		return -1;
	}
}

```

## 4. 使用环形缓冲区防止按键丢失

修改后的 `key_timeout_func`

```c
static uint8_t g_data_buf[100];
static circle_buf g_key_bufs;

void key_timeout_func(void *args)
{
	uint8_t key_val; //按下是 0x1，松开是 0x81
	g_key_cnt++;
	key_timer.timeout = ~0;
	
	/* read gpio */
	if (HAL_GPIO_ReadPin(GPIOB, GPIO_PIN_14) == GPIO_PIN_RESET)
		key_val = 0x1;
	else
		key_val = 0x81;
	
	/* put key val into circle buf */
	circle_buf_write(&g_key_bufs, key_val);
}

void mod_timer(struct soft_timer *pTimer, uint32_t timeout)
{
	pTimer->timeout = HAL_GetTick() + timeout;
}

void check_timer(void)
{
	if (key_timer.timeout <= HAL_GetTick())
	{
		key_timer.func(key_timer.args);
	}
}

void HAL_GPIO_EXTI_Callback(uint16_t GPIO_Pin)
{
	if (GPIO_Pin == GPIO_PIN_14)
	{
		mod_timer(&key_timer, 10);
	}
}
```

`while (1)` 中的函数

```c
while (1)
{
	OLED_PrintSignedVal(len, 0, g_key_cnt);
	uint8_t key_val = 0;
	if (0 == circle_buf_read(&g_key_bufs, &key_val))
	{
		OLED_ClearLine(len, 2);
		OLED_PrintHex(len, 2, key_val, 1);
	}
}
```