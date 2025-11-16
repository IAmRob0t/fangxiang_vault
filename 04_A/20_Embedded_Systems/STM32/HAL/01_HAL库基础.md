---
tags:
  - hal
---
# LED_KEY

- MCU： [[开发板原理图_100ASK_STM32F103_V12原理图.pdf]]
- 扩展板接口： [[扩展板原理图_F103_Extend_V2.pdf]]
- LED 和按键：
	- ![[扩展板原理图_F103_Extend_V2.pdf#page=1&rect=178,597,337,743|扩展板原理图_F103_Extend_V2, p.1|172]]
	- ![[扩展板原理图_F103_Extend_V2.pdf#page=1&rect=347,596,480,738|扩展板原理图_F103_Extend_V2, p.1|177]]

> [!NOTE] 控制原理
> 1. 选择引脚：MCU 要知道想要蓝灯亮是需要控制哪一个引脚
> 2. 引脚方向（输入/输出）：MCU 需要给这个引脚输出一个电平才能让灯亮或者灭
> 3. 控制逻辑： 引脚低电平的时候灯亮，高电平的时候灯灭

## 使用HAL库初始化 LED 和按键的 GPIO 的步骤

```c
void MX_GPIO_Init(void)
{

// 将硬件对象使用结构体具象，这里使用GPIO_InitTypeDef具象GPIO这个硬件
  GPIO_InitTypeDef GPIO_InitStruct = {0};

  /* GPIO Ports Clock Enable */
// 使能外设的时钟，这里是使能按键的GPIO组GPIOE的时钟，调用的函数是__HAL_RCC_GPIOE_CLK_ENABLE()
  __HAL_RCC_GPIOE_CLK_ENABLE();
  __HAL_RCC_GPIOC_CLK_ENABLE();

// 使能外设的时钟，这里是使能LED的GPIO组GPIOF的时钟，调用的函数是__HAL_RCC_GPIOF_CLK_ENABLE()
  __HAL_RCC_GPIOF_CLK_ENABLE();
  __HAL_RCC_GPIOD_CLK_ENABLE();
  __HAL_RCC_GPIOA_CLK_ENABLE();

  /*Configure GPIO pin Output Level */
  HAL_GPIO_WritePin(INA_GPIO_Port, INA_Pin, GPIO_PIN_SET);

  /*Configure GPIO pin Output Level */
  HAL_GPIO_WritePin(GPIOF, WHITE_Pin|BLUE_Pin|GREEN_Pin|SCL_Pin
                          |SDA_Pin, GPIO_PIN_SET);

  /*Configure GPIO pin Output Level */
  HAL_GPIO_WritePin(INB_GPIO_Port, INB_Pin, GPIO_PIN_SET);

  /*Configure GPIO pin : PtPin */
  GPIO_InitStruct.Pin = INA_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_PULLUP;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_HIGH;
  HAL_GPIO_Init(INA_GPIO_Port, &GPIO_InitStruct);

  /*Configure GPIO pins : PFPin PFPin PFPin PFPin
                           PFPin */
//配置硬件属性，将描述硬件对象的结构体中的成员，按照需求的功能配置
  GPIO_InitStruct.Pin = WHITE_Pin|BLUE_Pin|GREEN_Pin|SCL_Pin
                          |SDA_Pin;			// 比如GPIO这里的选择引脚；
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;	// 配置输入输出方向；
  GPIO_InitStruct.Pull = GPIO_PULLUP;			// 选择上拉或者下拉；
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_HIGH;	// 选择相应速率；
  
// 调用库函数初始化结构体，比如GPIO这里的HAL_GPIO_Init
  HAL_GPIO_Init(GPIOF, &GPIO_InitStruct);

  /*Configure GPIO pins : PEPin PEPin */
// 配置硬件属性，将描述硬件对象的结构体中的成员，按照需求的功能配置
  GPIO_InitStruct.Pin = K1_Pin|K2_Pin;		// 比如GPIO这里的选择引脚；
  GPIO_InitStruct.Mode = GPIO_MODE_INPUT;	// 配置输入输出方向；
  GPIO_InitStruct.Pull = GPIO_PULLUP;		// 选择上拉或者下拉；
  HAL_GPIO_Init(GPIOE, &GPIO_InitStruct);	// 调用库函数初始化结构体，比如GPIO这里的HAL_GPIO_Init

  /*Configure GPIO pin : PtPin */
  GPIO_InitStruct.Pin = INB_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_PULLUP;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_HIGH;
  HAL_GPIO_Init(INB_GPIO_Port, &GPIO_InitStruct);

}
```

## GPIO的两个输出HAL库函数

( [[STM32F1HAL库和LL库用户手册.pdf#page=227&selection=59,13,60,88&color=note|📖]])
`void HAL_GPIO_WritePin (GPIO_TypeDef * GPIOx, uint16_t GPIO_Pin, GPIO_PinState PinState)`
控制一个GPIO引脚输出高或者低电平

( [[STM32F1HAL库和LL库用户手册.pdf#page=228&selection=3,0,3,65&color=note|📖]])
`void HAL_GPIO_TogglePin (GPIO_TypeDef * GPIOx, uint16_t GPIO_Pin)`
控制一个GPIO引脚电平翻转，调用一次电平翻转一次

## 封装功能函数的两种方法

1. 宏定义：`#define`
	* 简洁直观，但仅适用于封装功能简单的函数
2. 定义函数：`void function(void)`
	* 功能复杂的时候需要定义一个函数来实现

## 按键的抖动和消除

- 按键按下的瞬间引脚的电平不是马上从高电平变为低电平或者从低电平变成高电平；而是有一个抖动；
- 可以使用加延时判断的办法消除这个抖动；
- 缺点：延时时间不好掌握，容易让程序对按键的反应过于灵敏或者迟钝；

## GPIO的输入HAL库函数

( [[STM32F1HAL库和LL库用户手册.pdf#page=227&selection=30,13,31,72&color=note|📖]])
`GPIO_PinState HAL_GPIO_ReadPin (GPIO_TypeDef * GPIOx, uint16_t GPIO_Pin)`
读取一个GPIO引脚的电平

# I2C_OLED

## 扩展板接口原理图

![[扩展板原理图_F103_Extend_V2.pdf#page=1&rect=345,388,433,480|扩展板原理图_F103_Extend_V2, p.1]]

## [[I2C 协议]]

## I2C 总线的 GPIO

( [[I2C总线协议手册.pdf#page=8&selection=34,0,37,49&color=note|📖]])
Both SDA and SCL are bidirectional lines, connected to a positive supply voltage via a current-source or pull-up resistor (see Figure 3). 
- SDA 和 SCL 是两条连接到一个正电压的双向信号线，这个电压由一个电源或者上拉电阻提供；

When the bus is free, both lines are HIGH. 
- 当总线空闲时，两条信号线的电平是高电平；

The output stages of devices connected to the bus must have an open-drain or open-collector to perform the wired-AND function.
- 当总线上有多个设备时，应该将信号线设置为开漏模式，让这个结构是一个与功能结构；

( [[I2C总线协议手册.pdf#page=8&selection=43,0,44,65&color=note|📖]])
For a single master application, the master’s SCL output can be a push-pull driver design if there are no devices on the bus which would stretch the clock.
- 对于单主机的应用，如果总线上没有设备需要钳制时钟线，我们可以将时钟线 SCL 设置为推挽模式

> [!NOTE] 所以在我们的实际应用中，为了兼容，我们将 SCL 和 SDA 均设置为开漏模式。

[[04_A/STM32/GPIO的工作模式#再探 STM32F103 的 GPIO]]

![[2_0.96OLED-IIC-原理图.pdf]]

SCL -> PF10 -> 开漏输出 -> 
- 往 PF10 的输出数据寄存器写 1 -> 
	- 因为有 OLED 内部上拉，所以可以输出一个高电平给 OLED
	- 也可以被 OLED 钳位拉低
- 往 PF10 的输出数据寄存器写 0 -> 向 OLED 输出低电平

SDA  -> PF11 -> 开漏输出 -> 
- 往 PF11 的输出数据寄存器写 1 -> 因为有 OLED 内部上拉，所以可以输出一个高电平给 OLED
- 往 PF11 的输出数据寄存器写 0 -> 也可以被 OLED 钳位拉低，主机读 OLED 应答时就可以使 SDA 输出高电平，然后去读 SDA 的状态

>  1-3-7 完成 I2C 底层驱动

## [[SSD1306]]

## OLED 显示要思考的几个问题

### OLED 是怎么显示像素的？

MCU通过I2C等接口向OLED控制器（如SSD1306）发送指令和数据，数据被写入控制器内部的GDDRAM（图形显示数据RAM）。GDDRAM中的每一位对应屏幕上的一个物理像素点，控制器根据这些位的状态（0或1）来驱动对应的有机发光二极管点亮或熄灭，从而显示出图像。

- 数据字节内部的位映射到像素行 ：在一个数据字节中， 最低位（LSB, D0）对应的是当前列 PAGE 中最上面一行的像素（低位在前），而最高位（MSB, D7）对应的是当前列 PAGE 中最下面一行的像素 4 1 。
	- 例如，如果发送的数据字节是 0x01 (二进制 00000001 )，那么在当前选定的列和页（page，通常包含 8 行）中，只有最上面一行的那个像素点会被点亮。
	- 如果发送的数据字节是 0x80 (二进制 10000000 )，那么只有最下面一行的那个像素点会被点亮。
	- 如果发送的数据字节是 0xFF (二进制 11111111 )，那么这一列的 8 个像素点都会被点亮。

- 数据传输的顺序（I2C/SPI 层面） ：在通过 I2C 或 SPI 总线发送这一个字节的数据时，通信协议本身通常规定了是 MSB 优先还是 LSB 优先发送。例如，标准的 I2C 和 SPI 协议通常是先发送字节的最高位（MSB first）。但这指的是 字节在传输过程中的位顺序 ，而不是字节内的位如何映射到 OLED 屏幕的物理像素行。

### OLED 是怎么确定要在哪一行哪一列显示像素的？

- 需要设置地址：列地址和页地址
- 需要先选择内存地址模式
	- 选择页地址模式 -> 设置页起始地址和列起始地址
	- 选择水平/竖直地址模式 -> 设置页起始地址和结束地址 -> 设置列起始地址和结束地址
- 填充 GDDRAM 数据
- 显示像素

### 字符是怎么在 OLED 上显示的？

- 方法一（直接生成数据）：将要显示的字符使用取模软件生成对应的像素数据，然后填充到 GDDRAM
	- 优点：直接、简单、节省内存空间
	- 缺点：只能显示指定的字符
- 方法二（字库）：生成 ASCII 码字模文件，根据简单算法查询要显示的字符的像素数据，然后再填充到 GDDRAM 中
	- 优点：可以显示任意 ASCII 字符
	- 缺点：
		- 需要占用比较大的内存空间
		- 需要使用简单计算查找字符对应的像素数据

#### 取字模软件（Pctolcd）的使用方法

1. 选择字符模式
2. 设置阴码/阳码，更具屏幕特性或设计需求选择（选择低位在前、列行式）
3. 设置显示方向，这个需要根据屏幕特性决定
4. 设置生成数据的格式
5. 输入要显示的字符
6. 生成字模数据

#### OLED 显示的美化

```c
OLED_SetComConfig(COM_PIN_ALT, COM_NOREMAP);
// 使字体变得更小更圆润
```

#### 功耗与休眠

1. 合理配置 OLED 的参数
2. 合理分配显示时间，考虑是否需要移植显示；考虑设计熄灭和显示的周期
3. 模块的休眠与 MCU 的休眠

# 串口通信

## 通信的基本概念

- 串行通信
	- 数据通过一根线路一位接一位地顺序传输。
	- 优点：数据线少，成本低
	- 缺点：速度比并行通信慢
- 并行通信
	- 数据通过多根线路在同一时刻同时传输多位
	- 优点：速度快
	- 缺点：需要数据线多，成本高

---

- 全双工
	- 同一时刻双方可以互相发送数据、接收数据
	- 电话
- 半双工
	- 同一时刻只能有一方可以给另一方发送数据，即此发彼收、此收彼发
	- 对讲机
- 单工
	- 只能由发送方将数据发送给接收方
	- 收音机

---

> [!warning] 注意！
> 同步通信和异步通信都是针对串行通信而言。

- 异步通信
	- 数据是以字符为单位组成字符帧传输的。
	- 字符帧由发送端一帧一帧的发送，每帧数据可能是低位在前高位在后也可能是高位在前低位在后，通过传输线被接收端一帧一帧的接收。
	- 发送端和接收端可以有各自独立的时钟来控制数据的发送和接收，这两个时钟各自独立，互不同步。
	- 接收端依靠字符帧格式来判断发送端是何时开始和结束发送的。
	- 字符帧也叫数据帧，由起始位，数据位，奇偶校验位，停止位等部分组成，是异步通信的一个重要指标。
- 同步通信
	- 同步是指在约定的通信速率下，发送端和接收端的时钟信号和相位始终保持一致，保证通信双方在发送和接收数据时具有完全一致的定时关系。
	- 同步通信把许多字符组成一个信息帧，每帧的开始用同步字符来表示。
	- 在绝大多数场合下发送端和接收端采用的都是同一个时钟，所以在传送数据的同时还要发送时钟信号，以便接收端可以使用时钟信号来确定每一个信息位。
	- 同步通信一次通信只能传送一帧信息。

---

- 通信速率
	- 对于同步通信，通信速率由时钟信号决定，时钟信号越快，传输速度就越快。
	- 对于异步通信，需要收发双方提前统一通信速率，这也就是我们串口调试时，波特率不对显示乱码的原因。

- 比特率: 系统在单位时间内传输的比特位（二进制0或1）个数，通常用 $R_b$ 表示，单位是比特/秒（bit/s），缩写为bps；
- 波特率:系统在单位时间内传输的码元个数，通常用 $R_B$ 表示，单位是波特（Bd）;
- 码元有N个状态时，比特率与波特率的关系式：$R_b=R_B×log_2⁡N$

---

1. 开发板上的调试串口使用的是USART1，是一个异步串行全双工的通信接口，常用波特率是115200；
2. 通过USB转串口芯片将开发板和PC连接起来进行通信；
3. 通常使用串口调试工具查看打印信息以及输入信息到开发板；

## 分析原理图和UART收发流程

### 原理图分析：调试串口

![[开发板原理图_100ASK_STM32F103_V12原理图.pdf#page=7&rect=287,8,592,834|开发板原理图_100ASK_STM32F103_V12原理图, p.7]]

### 原理图分析：和 Wi-Fi 模块通信的串口

![[扩展板原理图_F103_Extend_V2.pdf#page=1&rect=74,359,170,521|扩展板原理图_F103_Extend_V2, p.1]]

### STM32F103 的 USART 资源概览

| USART 模式       | UASRT1/2/3 | UART4 | UART5 |
| -------------- | ---------- | ----- | ----- |
| 异步模式           | 支持         | 支持    | 支持    |
| 硬件流控制（CTS/RTS） | 支持         | 不支持   | 不支持   |
| 多缓存通信（DMA）     | 支持         | 支持    | 不支持   |
| 多处理器通信         | 支持         | 支持    | 支持    |
| 同步通信           | 支持         | 不支持   | 不支持   |
| 智能卡（Smartcard） | 支持         | 不支持   | 不支持   |
| 半双工（单线模式）      | 支持         | 支持    | 支持    |
| IrDA（红外线）      | 支持         | 支持    | 支持    |
| LIN（域互联网络）     | 支持         | 支持    | 支持    |

> [!NOTE] STM32F103 有 3 个通用同步异步收发器 USART，2 个通用异步收发器 UART， USART 也可以当作 UART 使用

### STM32F103 的 USART 收发控制

### STM32F103 的 USART 的发送流程


Procedure:
1. Enable the USART by writing the UE bit in USART_CR1 register to 1
2. Program the M bit in USART_CR1 to define the word length.
3. Program the number of stop bits in USART_CR2.
4. Select DMA enable (DMAT) in USART_CR3 if Multi buffer Communication is to take place. Configure the DMA register as explained in multibuffer communication.
5. Select the desired baud rate using the USART_BRR register.
6. Set the TE bit in USART_CR1 to send an idle frame as first transmission.
7. Write the data to send in the USART_DR register (this clears the TXE bit). Repeat this for each data to be transmitted in case of single buffer.
8. After writing the last data into the USART_DR register, wait until TC=1. This indicates that the transmission of the last frame is complete. This is required for instance when the USART is disabled or enters the Halt mode to avoid corrupting the last transmission.

( [[STM32F103xx参考手册(英文原版).pdf#page=792&selection=10,0,39,13&color=note|📖]])

1. 将USART_CR1寄存器的UE位写1使能USART；
2. 配置USART_CR1寄存器的M位来设置数据位；
3. 配置USART_CR2寄存器来设置停止位；
4. 如果是多缓冲通讯的话，可以选择使用DMA，在USART_CR3寄存器中使能DMA；
5. 配置USART_BRR寄存器来设置波特率；
6. 通过置位USART_CR1寄存器的TE位来发送第一个空闲帧；
7. 将要发送的数据写入到USART_DR寄存器中，如果是单缓冲区就重复此动作直到整个缓冲区发送完成；
8. 当写入数据到USART_DR寄存器后，判断TC位，如果被置1就表明最新一帧的数据被发送完成了。

### STM32F103 的 USART 的接收流程

Procedure:
1. Enable the USART by writing the UE bit in USART_CR1 register to 1
2. Program the M bit in USART_CR1 to define the word length.
3. Program the number of stop bits in USART_CR2.
4. Select DMA enable (DMAR) in USART_CR3 if multibuffer communication is to take place. Configure the DMA register as explained in multibuffer communication. STEP 3
5. Select the desired baud rate using the baud rate register USART_BRR
6. Set the RE bit USART_CR1. This enables the receiver which begins searching for a start bit.

( [[STM32F103xx参考手册(英文原版).pdf#page=795&selection=15,0,35,10&color=note|📖]])

1. 通过将 USART_CR1 的 UE 位写 1 使能 USART；
2. 通过写 USART_CR1 的 M 位配置数据位；
3. 通过配置 USART_CR2 寄存器来配置停止位；
4. 如果是多缓冲区通信的话可以使能 DMA；
5. 通过配置 USART_BRR 寄存器配置波特率
6. 通过置位 USART_CR1 的 RE 位使能接收；

---

When a character is received
- The RXNE bit is set. It indicates that the content of the shift register is transferred to the RDR. In other words, data has been received and can be read (as well as its associated error flags).
- An interrupt is generated if the RXNEIE bit is set.
- The error flags can be set if a frame error, noise or an overrun error has been detected during reception.
- In multibuffer, RXNE is set after every byte received and is cleared by the DMA read to the Data Register.
- In single buffer mode, clearing the RXNE bit is performed by a software read to the USART_DR register. The RXNE flag can also be cleared by writing a zero to it. The RXNE bit must be cleared before the end of the reception of the next character to avoid an overrun error.

( [[STM32F103xx参考手册(英文原版).pdf#page=795&selection=36,0,63,17&color=note|📖]])

当接收到一个字符后：
* **RXNE 位会被写 1**，表明数据已经被接收到了，可以通过 DR 寄存器来读了；
* 如果 RXNEIE 位被置位的话，接收到一个字符后会产生一个接收中断；
* 如果检测到了噪声或者 overrun 错误，会将错误标志置位；
* 在多缓冲去通信中，RXNE 直到缓冲区中所有的数据都接收到了才会被置位，然后通过 DMA 读取完之后又会被复位；
* 在单缓冲区应用中，RXNE 可以通过软件读取 DR 寄存器来清零。RXNE 位也可以通过直接向其写 0 来清零。

## STM32F103 的 USART 字符描述

1. 起始位
2. **数据位**
	- 8bits
	- 9bits
3. **停止位**
	- 1bit ---> 默认值
	- 2bits --> 适用于通用 USART、单总线和 modem 模式
	- 0.5bit -> 适用于 Smartcard 模式的接收数据情况下
	- 1.5bit -> 适用于 Smartcard 模式下的接收和发送
4. **校验位**
	- 无校验位
	- 奇校验
	- 偶校验

## USART的HAL库函数(仅以异步通信UART为例)

描述UART外设的结构体：

```c
typedef struct

{

  __IO uint32_t SR;         /*!< USART Status register,                   Address offset: 0x00 */

  __IO uint32_t DR;         /*!< USART Data register,                     Address offset: 0x04 */

  __IO uint32_t BRR;        /*!< USART Baud rate register,                Address offset: 0x08 */

  __IO uint32_t CR1;        /*!< USART Control register 1,                Address offset: 0x0C */

  __IO uint32_t CR2;        /*!< USART Control register 2,                Address offset: 0x10 */

  __IO uint32_t CR3;        /*!< USART Control register 3,                Address offset: 0x14 */

  __IO uint32_t GTPR;       /*!< USART Guard time and prescaler register, Address offset: 0x18 */

} USART_TypeDef;
```

具象化：使用结构体定义变量，通过对结构体成员的值的配置来指向我们使用的串口、设置需要的串口参数

## UART 常用 HAL 库函数

![[UART 常用 HAL 库函数.png|640]]

- `HAL_UART_Init()` / `HAL_UART_DeInit()`
- `HAL_UART_MspInit()` / `HAL_UART_MspDeInit()`
- `__HAL_UART_ENABLE_IT()` / `__HAL_UART_DISABLE_IT()`
- `HAL_UART_Transmit()` / `HAL_UART_Receive()`
- `HAL_UART_Transmit_IT()` / `HAL_UART_Receive_IT()`
- `HAL_UART_Transmit_DMA()` / `HAL_UART_Receive_DMA()`
- `HAL_UART_TxCpltCallback()` / `HAL_UART_RxCpltCallback()`

## 使用 HAL 库对 USART 的初始化流程

1. 使用 `UART_HandleTypeDef` 定义变量具象 USART 对象；
2. 在 `HAL_UART_MspInit()` 函数中完成对时钟的使能和 GPIO/DMA 等的配置；
3. 配置 `UART_HandleTypeDef` 结构体成员变量，配置设备号、数据位、停止位和校验位等；
4. 使用 `HAL_UART_Init()` 初始化结构体变量，完成对该 USART 外设的初始化；
5. 如果要使用中断，则使用 `__HAL_UART_ENABLE_IT()` 使能某个中断；
6. 开始收发数据；

## C 库输入输出函数的重定向

- `putchar()` / `getchar()`
- `printf()` / `scanf()`

```c
void DebugPrint(const char *str)
{
	uint16_t len = strlen(str);
	
	HAL_UART_Transmit(&huart1, (uint8_t*)str, len, 3000);
}

void DebugGet(char *str, uint16_t len)
{
	while(HAL_UART_Receive(&huart1, (uint8_t*)str, len, 3000) != HAL_OK);
}

/* ----------------------------------------------------------------------------- */

int fputc(int ch, FILE *f)
{
	while(HAL_UART_Transmit(&huart1, (uint8_t*)&ch, 1, 3000) != HAL_OK);
}

int fgetc(FILE *f)
{
	volatile char c = 0;
	while(HAL_UART_Receive(&huart1, (uint8_t*)str, len, 1) != HAL_OK);
	
	return c;
}
```

# 中断收发

## STM32F103 中断系统概述

根据图示架构，​**​STM32F103中断系统是以Cortex-M3内核机制为核心、外设事件为触发源的多级响应体系​**​：外部引脚边沿中断（如GPIO）、外设功能中断（如UART收发）等事件首先转化为​**​中断挂起请求​**​，由Cortex-M3内核通过​**​中断向量表​**​自动跳转执行对应的​**​中断服务例程（ISR）​**​；在此过程中，​**​中断优先级控制​**​模块动态管理请求的响应顺序（支持抢占式嵌套），而​**​事件​**​通道则提供无需CPU干预的硬件级响应（如HAL_Delay()的时序控制），最终实现从硬件触发到软件处理的低延迟高可靠调度。

## 中断优先级

- 优先级
	- **抢占优先级** —— 抢占优先级可以实现中断嵌套，抢占优先级级数低的可抢占级数高的
	- **子优先级** —— 子优先级无法实现中断嵌套，同一时刻两个子优先级不同的中断来临则先处理优先级高的即优先级级数低的中断，弱先后发生则先处理上一个中断，再处理后面的中断；

> [!NOTE] 一旦确定了优先级组别，抢占优先级和子优先级的范围就确定下来了且除非复位否则无法更改

## HAL库下的USART中断使用

- 在 `HAL_Init()` 中设置中断优先级组

1. 使用 `HAL_NVIC_SetPriority()` 设置中断优先级，比如将 `USART1` 的中断设置为次高级优先级： `HAL_NVIC_SetPriority(USART1_IRQn, 0, 1);`
2. 使用 `HAL_NVIC_EnableIRQ()` 使能中断；
3. 使用 `__HAL_UART_ENABLE_IT()` 使能 `UART` 的某个中断，比如发送、接收或者错误等；
	- 有使能就应该有失能中断
4. 使用 `HAL_UART_Transmit_IT()` / `HAL_UART_Receive_IT()` 进行中断收发（重定向 `fputc()` / `fgetc()`）；
5. 在中断回调函数 `USART1_IRQHandler()` 中进行中断处理，可以调用 `HAL_UART_IRQHandler()` 函数进行中断处理，也可以自己写处理语句；
6. 如果使用 `HAL_UART_IRQHandler()` 进行中断处理，则用户就要重定向 `HAL_UART_RxCpltCallback()` 或 `HAL_UART_TxCpltCallback()` 函数进行进一步数据或者任务处理；

使用常规方式进行收发可能会将我们发送过来的数据在接受的时候漏掉一些字符或数据，不能保证收到的数据是正确的，所以我们需要使用**环形缓冲区**

## 环形缓冲区

- 概念上的缓冲区 —— 一个线性的、无起始地址也无结束地址的环形内存
- 实际上的内存 —— 一片线性的、有起始地址有结束地址的内存

- 环形缓冲区基本操作
	- 申请内存空间
	- 写数据 —— 判断缓冲区是否为空
	- 读数据 —— 判断缓冲区是否写满

### 环形缓冲区：申请内存空间

```c
#define BUFFER_SIZE 8
char ring_buf[BUFFER_SIZE];
```

### 环形缓冲区：写数据

```c
int pW = 0;
ring_buf[pW] = data0;

//pW = pW + 1;
//pW + 1 = 8;	ring_buf[8]越界！

pW = (pW + 1) % BUFFER_SIZE
//(pW + 1)% BUFFER_SIZE = 0;
```

### 环形缓冲区：读数据

```c
int pR = 0;
Data = ring_buf[pR];

//pR = pR + 1;
pR = (pR + 1) % BUFFER_SIZE;
```

### 环形缓冲区：小结

- 缓冲区长度 `#define BUFFER_SIZE`
- 缓冲区内存申请 `char ring_buf[BUFFER_SIZE];`
- 写地址 `int pW;`
- 读地址 `int pR;`

```c
#define BUFFER_SIZE 1024

typedef struct
{
  unsigned char buffer[BUFFER_SIZE];
  volatile unsigned int pW;
  volatile unsigned int pR;
} ring_buffer;
```

### 环形缓冲区：判断缓冲区没有数据

- `pR == pW;`

### 环形缓冲区：判断缓冲区写满数据

- `(pW+1) % BUFFER_SIZE == pR;`

## HAL库下的串口中断接收

1. Data -> MCU - USART
2. USART1_IRQHandler
3. `HAL_UART_IRQHandler`
4. 判断状态寄存器后调用 `UART_Receive_IT`
5. 判断结构体变量的接收状态 `huart->RxState` 是否处于接收忙状态
	- 所谓接收忙，意思是程序处于接收状态，但是还没有收到数据或者说还没从数据寄存器将数据读取出来
6. 如果处于接收忙状态，则去处理数据和状态寄存器
7. 调用接收完成回调函数 `HAL_UART_RxCpltCallback` 做进一步数据处理

### RxState的变化流程

`HAL_UART_Init` -> `huart->RxState = HAL_UART_STATE_READY;`
`HAL_UART_Receive_IT` -> `UART_Start_Receive_IT` -> `huart->RxState = HAL_UART_STATE_BUSY_RX;`
`USART1_IRQHandler` -> `HAL_UART_IRQHandler` -> `UART_Receive_IT` -> `huart->RxState = HAL_UART_STATE_READY;`

## STM32F103的外部中断

[[06_GPIO 中断#STM32 中断体系结构]]

### STM32F103的外部中断在程序中的定义

1. 在 `startup_stm32xxx.s` 中查看定义的中断服务函数；
2. 在 `stm32xxx.h` 中查看定义的中断号名称；

- 以 STM32F103ZE 举例：
	1. 在 `startup_stm32f103xe.s` 中查看定义的中断服务函数:
		- ![[外部中断0~4的中断服务函数.png]]
	2. 在 `stm32f103xe.h` 中查看定义的中断号名称；
		-  ![[外部中断的中断号定义.png]]

> [!NOTE] 不是每个外部中断线都有一个中断号，有个中断线共用一个中断号

### 使用ST的HAL库完成外部中断的程序设计

1. 使用 `HAL_NVIC_SetPriority` 设置外部中断的优先级：
   `HAL_NVIC_SetPriority(中断号, 抢占优先级, 子优先级);`
   `HAL_NVIC_SetPriority(EXTI15_10_IRQn, 0, 2);`
2. 使用HAL_NVIC_EnableIRQ使能外部中断：
   `HAL_NVIC_EnableIRQ(中断号);`
   `HAL_NVIC_EnableIRQ(EXTI15_10_IRQn);`
3. 重定向中断服务函数：
   `void 中断_IRQHandler(void){;};`
   `void EXTI15_10_IRQHandler(void){;};`
4. (可选项)直接在中断服务函数中读取EXTI的PR寄存器判断是发生的哪个外部中断：

```c
void EXTI15_10_IRQHandler(void)
{
    if(EXTI->PR &(1<<0))
    {
      ;
    }
}
```

5. (可选项)也可以在中断服务函数中调用 `HAL_GPIO_EXTI_IRQHandler(uint16_t GPIO_Pin)` 然后重定向回调函数 `void HAL_GPIO_EXTI_Callback(uint16_t GPIO_Pin)` 做最后的中断处理

```c
void EXTI15_10_IRQHandler(void)
{
    HAL_GPIO_EXTI_IRQHandler(GPIO_PIN_10);
}
```

```c
void HAL_GPIO_EXTI_Callback(uint16_t GPIO_Pin)
{
    if(GPIO_PIN_10== GPIO_Pin)
    {
        ;
    }
}
```