---
title: "GPIO功能配置，一次性给你讲清楚！"
source: "https://mp.weixin.qq.com/s/VpRY2FmImU6nU6QDZ1ovyw"
author:
  - "[[微信公众平台]]"
published:
created: 2025-04-03
description: "01引言\x26amp;nbsp; \x26amp;nbsp; \x26amp;nbsp;刚进入嵌入式行业的小伙伴，基本上做的第一个实验就是：点亮一颗"
tags:
  - "clippings"
---

刚进入嵌入式行业的小伙伴，基本上做的第一个实验就是： **点亮一颗LED** 。点亮led基本使用的都是GPIO外设，去驱动LED，但很多小伙伴在学习这个外设的时候，总是搞不明白输入、输出、开漏、推挽等配置含义和影响，这一篇文章将使用stm32F4的库函数， **以《stm32参考手册》为准，讲解下这个外设的具体内容** ，体会一下驱动工程师的日常工作。

# STM32的GPIO简介

GPIO（英语：General-purpose input/output）， **通用型之输入输出的简称** ，功能类似8051的P0—P3，其接脚可以供使用者由程控自由使用，PIN脚依现实考量可作为通用输入（GPI）或通用输出（GPO）或通用输入与输出（GPIO）。 ---摘自维基百科

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/PYpVp1yVeibeu0XGbUgg55Re47emPF8d03JyWtdtbSTVgYPibVpib58eLEsSqrpqENw62Aa6DB24smswnpC3feLfw/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

由图得：

GPIO 最基本的功能就是输入、输出了 。图1的结构也表明了输入、输出信号的流动。红色的线表示GPIO输出电信号怎么走的，绿色表示输入。

## 1. **PIN**

在讲解GPIO之前，需要明确一个概念：PIN（引脚）和GPIO是两个不同的物理实体。 PIN是我们在芯片上面看到的引脚 ，如图2标注所示。

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/PYpVp1yVeibeu0XGbUgg55Re47emPF8d0EoPsytkyTdLua46Sy7ia0cfjl5DBgFWxP6jsBqJjmibFQCmYFf5fJibng/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

PIN是一个 **物理实体** ，我们使用芯片上的PIN连接到其他的电路上。

## 2. **复用**

GPIO **是芯片内部的一个外设** ，在图3中，画出了STM32芯片内部的结构框架。

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/PYpVp1yVeibeu0XGbUgg55Re47emPF8d0OTjUCVy3AHe9Jic7yLR6jWb1JnYsVX920fz9icmTU590LZFyndmr0lQg/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

从图3中可以看到，GPIO只是一个数字电路，和UART、TIMER、I2C这些外设并无区别，均属于外设。 **同一个PIN上面，可以连接多个外设，这个叫做复用。** 不同的外设通过MUX（多路复用器）这个部件，连接到同一个PIN。如图4所示

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/PYpVp1yVeibeu0XGbUgg55Re47emPF8d0fQicC0k7XnLhI8aeDlppWPkA1U7dLSHO7yBlBWcnWibSMoMnR516hJMQ/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

  

PA0就是我们在芯片上面看到的引脚了。不同的外设通过MUX，在同一时刻，选择连接到PA0引脚上。到这里，我们对复用这个概念有了一个更深入的理解， **它其实是为了解决不同的外设连接到同一个引脚上面从而被设计出来的。** 所以，配置外设的时候，如UART，在GPIO的配置结构体里面，需要配置复用这个选项。

复用这个，我们本文里面不会过多涉及，本文只讲解GPIO外设部分。

## 3. **输出**

**输出，** 是CPU让GPIO将某个引脚拉高或拉低（在已经配置GPIO连接到PIN之后），将CPU的信息通过PIN表现出来。在实际的应用场景中，PIN上面连接的外部电路，各种各样的情况都可能发生，因此，对于输出功能，有强输出（推挽）、弱输出（开漏）。推挽的含义是：PIN推、拉（挽）电平，可以强制将这个PIN推拉到芯片想要的电平。 **开漏的含义是：PIN输出电平，至于能不能输出到高/低** （主要是输出高电平场景时，会不确定引脚一定能拉高），看具体的情况（PS：这种解释很不专业，简单的理解下吧）。


![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/MVPvEL7Qg0HJalXIBXGXSBFLMk2TZAqh23iaHwLpprUov8bNQ95dWDVMTq4qGicM3G6cmsZcCF6RsKyn9p8eQA3Q/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

从图1红色的信号流来看，推挽、开漏的配置（黄色框），位于输出控制这个部分。在它的上半部分，是输出的高/低信号配置（数字1和0），这个部分就是我们代码控制GPIO输出高/低电平的地方。还有一个是片上外设的复用功能输出，比如UART的TX，走的就是这个信号流。

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/PYpVp1yVeibeu0XGbUgg55Re47emPF8d0OTjUCVy3AHe9Jic7yLR6jWb1JnYsVX920fz9icmTU590LZFyndmr0lQg/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

从这里也可以看出来，我们使用寄存器配置GPIO **推挽、开漏，和输入部分在物理电路上完全是两个部分。** 因此，引脚配置为输入的时候，实际上就是绿色信号流，哪怕配置了推挽、开漏，这部分电路也不起作用。

注：推挽和开漏的应用场景

**推挽：** 指的是对外部电路强推。因此用到输出能力较强的部分，如驱动LED。

**开漏：** 指的是对外部电路弱推。在I2C协议中，SDA信号线就是开漏输出，这样可以实现“线与”的功能。在I2C中，SDA信号脚输出的时候，还能读取SDA的信号（多主机通信的时候）。

## 4. **输入**

**输出，是CPU通过GPIO外设，将PIN上的电信号读取出来，读取到高电平或者低电平，在图1中是绿色信号流部分。** 除此之外，还有模拟和复用功能输入。模拟和数字部分是两个东西， 二者连接起来需要进行特殊处理（对于这部分，博主就不懂了）。复用功能输入指的是数字电路部分的，比如UART的RX，走的就是这个信号流。

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/PYpVp1yVeibeu0XGbUgg55Re47emPF8d0OTjUCVy3AHe9Jic7yLR6jWb1JnYsVX920fz9icmTU590LZFyndmr0lQg/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

## 5. **上/下拉**

上/下拉部分，在图1中是蓝色部分，可以看出，输出信号流（红色）、输入信号流（绿色），都和蓝色部分有联系，这说明无论GPIO配置为输出还是输入，上/下拉都要进行配置。 **上/下拉部分，是保证PIN，在不接任何电路的情况下，保持高/低电平的能力** （简单解释，不要太在意0^0）。

# 配置GPIO

## 1. 输出配置（点亮LED）

点亮LED程序非常简单，只需要配置好GPIO，将PIN拉低即可。我们先看看 **电路图**

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/PYpVp1yVeibeu0XGbUgg55Re47emPF8d0s441SricTuWWyhAEKeJPtIibDP8D8ClZ9YbIRRtIgqmUiaNlOnqCzAQ7Q/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

从图5、图6可以看出来， **只要将LED对应的引脚拉低，LED就会亮** （一般LED都是一端接VCC，一端接PIN，芯片的输出电流比较弱，输入电流会强很多）。下面是对应的代码。

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/PYpVp1yVeibeu0XGbUgg55Re47emPF8d0O9MVXVDNomE8CvdgrQjA3a5B3LfNcDWfPEQlf74ANWK77MndaTyZOQ/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

先使能时钟，时钟是数字电路的“能源”，数字电路如果没有时钟，将无法工作。配置GPIO的输出模式、推挽模式、上拉模式，都在图1中的红色信号流上面（寄存器就像一个一个开关，控制着数字电路的电信号流动）。

注：寄存器是什么？

若想控制stm32中的GPIO引脚，需要使用到寄存器。寄存器是软件（C语言）控制硬件的接口，也是一块内存。软件想要使用、控制一个硬件功能，只需要向对应的寄存器写入0和1（0和1可以理解为开关，开关硬件功能）。在stm32中，寄存器是32位的（可以理解一个寄存器有32个开关，每个开关对应一个功能。也有可能某些位用不到，空着，称之为保留，英文为reserve）， **我们可以通过向GPIO寄存器中写入1和0来控制GPIO的高、低电平，进而控制LED的灭亮**

## 2. 输入配置（按键）

先看按键连接的 **原理图** 。

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/PYpVp1yVeibeu0XGbUgg55Re47emPF8d0ucxXN3IQLnr5jKUymSVpbxMS8fjRSIWApd1JM1icvaH0knufrenh0lA/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

从上图中可以看出来，按键连接的是PE0/1，另一端连接的是GND， **因此需要将GPIO配置为输入、上拉模式** （默认高电平，按键按下之后，PIN连接到GND，读取GPIO时，就得到低电平信号）。

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/PYpVp1yVeibeu0XGbUgg55Re47emPF8d02w6CyS2icQ7Tx7h3ozSYtBTWCEgpzTibhib5avL7oRPNkOslxx4TeFR4g/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

**输入配置和输出类似** ，配置成输入模式，上拉。这里没有配置推挽/开漏，实际上从图1中可知，配置了推挽/开漏，也不影响输入的功能。

# 总结  

在配置GPIO的时候，心里面要有这个图（不同芯片GPIO设计略微不同，具体以对应芯片的参考手册为准），需要知道配置某个寄存器的时候，哪部分电路会被用到，哪部分电路起作用了。  

这个工作就是芯片驱动工程师日常要做的。只不过GPIO是最简单的外设了，只需要配置一点点就可以用了。从这里也可以看出，驱动工程师是使用软件，使相关的硬件正常工作起来（是正常工作！不是乱配置）。驱动程序本质上是硬件的延申，要做好驱动工程师， **首先要好好研究硬件** ，否则连硬件结构都不懂，谈不上驱动硬件。