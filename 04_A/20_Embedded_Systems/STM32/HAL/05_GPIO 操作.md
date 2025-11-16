---
tags:
  - HAL
---

# C 语言基础补充

- [[指针]]
- [[结构体]]
- [[进制]]
- [[字节序]]
- [[位操作]]

# 芯片封装

一个芯片，需要给它供电，必然有电源的正负引脚；还有其他功能，比如用来控制灯、识别按键。所以，根据功能的不同，芯片会有很多引脚。这些引脚如何排列？本称为封装 （Package）。有多种封装，如下：

![[HAL快速入门与项目实战.pdf#page=32&rect=145,212,471,649|HAL快速入门与项目实战, p.32|394]]

基本的芯片封装类型有：
1. SOP (Small outline Package): 零件两面有脚，脚向外张开（一般称为鸥翼型引脚）
2. SOJ (Small outline J-lead Package): 零件两面有脚，脚向零件底部弯曲（J 型引脚）
3. QFP (Quad Flat Package): 零件四边有脚，零件脚向外张开
4. PLCC (Plastic Leadless Chip Carrier): 零件四边有脚，零件脚向零件底部弯曲
5. BGA (Ball Grid Array): 零件表面无脚，其脚成球状矩阵排列于零件底部。

---

![[04_A/STM32/pdf/stm32f103c8.pdf#page=104&rect=121,168,491,697|stm32f103c8, p.104|430]]

根据官方给出的购买信息可得知，STM32C8T6 使用的是 LQFP 封装

![[04_A/STM32/pdf/stm32f103c8.pdf#page=1&rect=308,527,529,651|stm32f103c8, p.1|409]]

在芯片表面有一个圆点，它对应的引脚被称为第 1 个引脚（PIN1），逆时针依次是：PIN2、PIN3、……。这些数值被称为“引脚编号”。但是只根据引脚编号，无法知道引脚的用途，所以在芯片手册里还会有“引脚名”，如下图所示：

![[04_A/STM32/pdf/stm32f103c8.pdf#page=26&rect=123,510,526,755|stm32f103c8, p.26]]

# 芯片内部模块

以 STM32F103C8T6 为例，一个单片机芯片，里面含有 CPU、存储用的 Flash、内存 （RAM）、各类模块，比如引脚模块（GPIO）、I2C 控制器、SPI 控制器、USB 控制器。如下图所示：

![[STM32F103xx参考手册(英文原版).pdf#page=47&rect=123,208,530,530|STM32F103xx参考手册(英文原版), p.47]]

上图过于复杂，我们只需要知道：单片机芯片是一个“SOC”（Sytem On a Chip），是一个系统，里面含有 CPU、Flash、RAM、GPIO、I2C、SPI 等模块

# GPIO 模块

## 1. 点灯原理

LED，就是发光二极管 (light-emitting diode)，实物如下：

![[HAL快速入门与项目实战.pdf#page=35&rect=125,577,416,693|HAL快速入门与项目实战, p.35]]

点亮 LED 需要通电源，同时为了保护 LED，加个电阻减小电流。

常见的 LED 连接方式如下：

![[HAL快速入门与项目实战.pdf#page=36&rect=112,570,431,770|HAL快速入门与项目实战, p.36]]

方式 1：使用引脚输出 3.3V 点亮 LED，输出 0V 熄灭 LED。
方式 2：使用引脚拉低到 0V 点亮 LED，输出 3.3V 熄灭 LED。

有的芯片为了省电等原因，其引脚驱动能力不足，这时可以使用三极管驱动。
方式 3：使用引脚输出 3.3V 点亮 LED，输出 0V 熄灭 LED。
方式 4：使用引脚输出 0V 点亮 LED，输出 3.3V 熄灭 LED。

## 2. STM32 的 GPIO 模块

一般的芯片内部，都有多组 GPIO，每组里有多个引脚。比如 STM32F103 里有：GPIOA、GPIOB、……、 GPIOE 多组 GPIO；GPIOA 里有 PA0、PA1、……、PA15 等 16 条引脚。

要想使用 PC13 来控制 LED，需要做什么？

这需要深入了解芯片内部，在芯片手册 GPIO 章节，可以看到如下结构图：

![[HAL快速入门与项目实战.pdf#page=37&rect=136,549,480,773|HAL快速入门与项目实战, p.37]]

> [!NOTE] 要想使用引脚来控制 LED，需要：
> 1. **使能 GPIO 模块**：我们的这种单片机系统是用电池供电的，非常注重节能，默认是禁止的，我们需要把它打开
> 2. **选择引脚功能**：把引脚配置为 GPIO 功能，连接到芯片内部的 GPIO 模块，而不是连接到其他模块
> 3. **选择方向**：配置 GPIO 模块，把引脚配置为输出引脚
> 4. **配置引脚**：让它输出高电平或低电平

# 使用 HAL 库点灯

## 1. 配置 GPIO

根据原理图把 PC13 配置为输出引脚即可：

![[04_A/STM32/原理图/STM32F103C8T6.pdf#page=1&rect=511,118,575,220|DshanMCU-F103, p.1|134]]

![[STM32F1HAL库和LL库用户手册.pdf#page=227&rect=39,161,546,339|STM32F1HAL库和LL库用户手册, p.227|631]]

---

![[04_A/STM32/pdf/stm32f103c8.pdf#page=11&rect=154,440,251,522|stm32f103c8, p.11|300]]

> 每组 GPIO 都有 16 个引脚，但是我们使用的 STM32C8T6 是较为廉价的版本，只有 48 个引脚

## 2. 编写程序

- Configure pins

```c
void MX_GPIO_Init(void)
{

  GPIO_InitTypeDef GPIO_InitStruct = {0};

  /* GPIO Ports Clock Enable */
  __HAL_RCC_GPIOC_CLK_ENABLE();

  /*Configure GPIO pin Output Level */
  HAL_GPIO_WritePin(GPIOC, GPIO_PIN_13, GPIO_PIN_RESET);

  /*Configure GPIO pin : PC13 */
  GPIO_InitStruct.Pin = GPIO_PIN_13;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
  HAL_GPIO_Init(GPIOC, &GPIO_InitStruct);

}
```

- Infinite loop

```c
/* USER CODE BEGIN WHILE */
while (1)
{
	/* set PC13 output high */
	HAL_GPIO_WritePin(GPIOC, GPIO_PIN_13, GPIO_PIN_SET);
	HAL_Delay(500);
	
	/* set PC13 output low */
	HAL_GPIO_WritePin(GPIOC, GPIO_PIN_13, GPIO_PIN_RESET);
	HAL_Delay(500);
	
	/* USER CODE END WHILE */
	
	/* USER CODE BEGIN 3 */
```

# HAL 库的本质

## 1. **本质是读写寄存器**

HAL 库函数的本质是：帮我们操作寄存器。以 `HAL_GPIO_WritePin` 函数为例，它就是去操作下图中的“Output data register”

![[HAL快速入门与项目实战.pdf#page=39&rect=116,314,483,546|HAL快速入门与项目实战, p.39]]

## 2. 寄存器

> [!question] 什么是寄存器？
> 寄存器是CPU内部的高速临时存储单元，体积小但速度快，用于**暂存**当前正在处理的指令、数据或地址。作为CPU直接操作的"工作台"，它能快速存取中间计算结果，相比内存访问速度提升百倍以上，是保障计算机高效运行的核心组件。

- SoC （System on a Chip，片上系统）
	- RAM
	- GPIOX
	- Flash（读出指令，不能直接写，起长期保存的作用）

---

([[STM32F103xx参考手册(英文原版).pdf#page=51&selection=92,0,94,11&color=yellow|📖]])
GPIO Port C ：0x4001 1000 - 0x4001 13FF

即 GPIOC 的基地址为 `0x4001 1000`

在 STM32F103 的芯片手册中，可以看到下图：

![[STM32F103xx参考手册(英文原版).pdf#page=173&rect=61,539,532,758|STM32F103xx参考手册(英文原版), p.173]]

可以看到地址偏移量 Address offset 为 `0x0C`

则 GPIOC_ODR 的实际地址为 `0x4001 1000 + 0x0C = 0x4001 100c`

只要写 GPIOC_ODR 寄存器，让它的 bit13 为 1 即可让 PC13 输出高电平，让它的 bit13 为 0 即可让 PC13 输出低电平。
操作 GPIOC_ODR 寄存器时，为了**不影响其他数据位**，需要“先读出原理的值，修改 BIT13 后，再写入”，涉及 3 步操作。

---

也可以直接写 GPIOC_BSRR 寄存器，它的定义如下：

![[STM32F103xx参考手册(英文原版).pdf#page=173&rect=64,240,532,525|STM32F103xx参考手册(英文原版), p.173]]

比如要让 PC13 输出高电平，往 GPIOC_BSRR 中写入“1<<13”即可；要让 PC13 输出低电平，往 GPIOC_BSRR 中写入“1<<29”即可。写入 0 的位，不影响 GPIO 引脚。

## 3. 编写程序

操作 GPIOC_ODR 寄存器：

```c
unsigned int *p;

p = (unsigned int *)0x4001100c; /*Port output data register (GPIOC_ODR) (x=A..G) */

/* Infinite loop */
/* USER CODE BEGIN WHILE */
while (1) {
	/* set PC13 output high */
	//HAL_GPIO_WritePin(GPIOC, GPIO_PIN_13, GPIO_PIN_SET);
	unsigned int val = *p;
	val = val | (1<<13);
	*p = val;
	
	HAL_Delay(500);
	
	/* set PC13 output low */
	//HAL_GPIO_WritePin(GPIOC, GPIO_PIN_13, GPIO_PIN_RESET);
	val = *p;
	val = val & ~(1<<13);
	*p = val;
	
	HAL_Delay(500);
	
	/* USER CODE END WHILE */
	
	/* USER CODE BEGIN 3 */ }
```

或者，操作 GPIOC_BSRR 寄存器：

```c
unsigned int *p;
p = (unsigned int *)0x40011010; /* Port bit set/reset register (GPIOC_BSRR) */
while (1)
{
	/* set PC13 output high */
	//HAL_GPIO_WritePin(GPIOC, GPIO_PIN_13, GPIO_PIN_SET);
	*p = (1<<13);
	HAL_Delay(500);
	
	/* set PC13 output low */
	//HAL_GPIO_WritePin(GPIOC, GPIO_PIN_13, GPIO_PIN_RESET);
	
	*p = (1<<29);
	HAL_Delay(500);
	
	/* USER CODE END WHILE */
	
	/* USER CODE BEGIN 3 */
}
```


## 4. [[04_A/STM32/GPIO的工作模式]]

## 5. HAL 库源码解析

> 分析程序 `0501_led. 7z` 。

```c
/** Configure pins
*/
void MX_GPIO_Init(void)
{

  GPIO_InitTypeDef GPIO_InitStruct = {0};
  
  /* GPIO Ports Clock Enable */
  __HAL_RCC_GPIOC_CLK_ENABLE();

  /*Configure GPIO pin Output Level */
  HAL_GPIO_WritePin(GPIOC, GPIO_PIN_13, GPIO_PIN_RESET);
  /*
  为什么在配置输出引脚之前先写了寄存器的值？
  是因为我一旦配置成输出的时候，肯定会输出电平。当我将它配置成输出引脚时，它立马就可以输出预先设置的值
  */

  /*Configure GPIO pin : PC13 */
  GPIO_InitStruct.Pin = GPIO_PIN_13;			//初始化 GPIOC 里面的第 13 个引脚
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;	//推挽输出
  GPIO_InitStruct.Pull = GPIO_NOPULL;			//没有上拉电阻
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;	//低速
  HAL_GPIO_Init(GPIOC, &GPIO_InitStruct);

}
```

```c
/**
  * @brief GPIO Init structure definition
  */
typedef struct
{
  uint32_t Pin; 
  uint32_t Mode;
  uint32_t Pull;
  uint32_t Speed;
} GPIO_InitTypeDef;
```

`HAL_GPIO_Init(GPIOC, &GPIO_InitStruct);` 
-> `#define GPIOC               ((GPIO_TypeDef *)GPIOC_BASE)` 
-> `#define GPIOC_BASE            (APB2PERIPH_BASE + 0x00001000UL)`
-> `#define APB2PERIPH_BASE       (PERIPH_BASE + 0x00010000UL)`
-> `#define PERIPH_BASE           0x40000000UL /*!< Peripheral base address in the alias region */`
-> `0x4001 1000 GPIO Port C` 75421

# GPIO 输入

## 1. 按键原理图

常见的按键电路如下图所示：

![[HAL快速入门与项目实战.pdf#page=54&rect=202,475,413,697|HAL快速入门与项目实战, p.54|500]]

瑞士军刀的按键原理图：

![[04_A/STM32/原理图/DshanMCU-F103_baseboard.pdf#page=1&rect=530,100,659,173&color=red|DshanMCU-F103_baseboard, p.1]]

- 理想情况 - 按下按键 PB14 读取到低电平，松开按键 PB14 读取到高电平

## 2. 编写按键控制 LED 的程序 

目标：使用按键控制 LED，按下按键让 LED 亮，松开按键让 LED 熄灭。
在0501_led. 7z 的基础上编写程序，程序为：
1. “0506_key_led_cubemx”：使用cubemx配置引脚PB14为输入引脚
2. “0507_key_led_manual”：手动调用代码初配置引脚PB14为输入引脚

![[STM32F1HAL库和LL库用户手册.pdf#page=227&rect=40,343,529,514|STM32F1HAL库和LL库用户手册, p.227]]

![[04_A/STM32/原理图/STM32F103C8T6.pdf#page=1&rect=511,117,575,219|DshanMCU-F103, p.1|200]]

- 对于输入引脚，无需配置速率。在结构体里设置速率不会起作用。

## 3. 光敏传感器和蜂鸣器原理图

### 3.1. 光敏电阻

光敏传感器样子如下：

![[HAL快速入门与项目实战.pdf#page=55&rect=197,598,412,722|HAL快速入门与项目实战, p.55|500]]

它的原理图为：

![[HAL快速入门与项目实战.pdf#page=55&rect=129,414,475,583|HAL快速入门与项目实战, p.55]]

LM393 是比较器，它的“+”极接到光敏电阻，“-”极接到可调电阻。当“+”极的电压大于“-”极的电压，DO 输出高电平，LED 被熄灭；当“+”极的电压小于“-”极的电压， DO 输出低电平，LED 被点亮。

当光照比较强烈时，光敏电阻阻值下降，“+”极电压下降低于“-”极电压时，DO 输出低电平，LED 被点亮。当光照比较强烈时，光敏电阻阻值上升，“+”极电压上升大于“-”极电压时，DO 输出高电平，LED 被熄灭。即
- 暗 - DO=1 - LED 灭
- 亮 - DO=0 - LED 亮

光敏电阻跟瑞士军刀的连接图如下，读取 PB11 即可知道光敏电阻的状态：

![[04_A/STM32/原理图/DshanMCU-F103_baseboard.pdf#page=1&rect=379,174,512,233&color=red|DshanMCU-F103_baseboard, p.1|400]]

### 3.2. 有源蜂鸣器

有源蜂鸣器样子如下：

![[HAL快速入门与项目实战.pdf#page=56&rect=208,605,385,739|HAL快速入门与项目实战, p.56|500]]

原理图如下，只要让 I/O 引脚输出低电平，就可以让它发出声音：

![[HAL快速入门与项目实战.pdf#page=56&rect=159,372,448,588|HAL快速入门与项目实战, p.56]]

蜂鸣器跟瑞士军刀的连接图如下，让 PA8 输出低电平即可让蜂鸣器发声：

![[04_A/STM32/原理图/DshanMCU-F103_baseboard.pdf#page=1&rect=65,106,195,174|DshanMCU-F103_baseboard, p.1|400]]

## 4. 使用光敏传感器控制蜂鸣器

程序为：“0508_light_beep”。

```c
/* USER CODE BEGIN PV */
static int isDark(void)
{
	return HAL_GPIO_ReadPin(GPIOB, GPIO_PIN_11);
}

static void BeepContral(int on)
{
	if (on)
		HAL_GPIO_WritePin(GPIOA, GPIO_PIN_8, GPIO_PIN_RESET);
	else
		HAL_GPIO_WritePin(GPIOA, GPIO_PIN_8, GPIO_PIN_SET);
}

static void LEDContral(int on)
{
	if (on)
		HAL_GPIO_WritePin(GPIOC, GPIO_PIN_13, GPIO_PIN_RESET);
	else
		HAL_GPIO_WritePin(GPIOC, GPIO_PIN_13, GPIO_PIN_SET);
}
/* USER CODE END PV */
```

[[存储类说明符|static是什么意思]]