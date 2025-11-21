---
tags:
---
# 使用按键控制 LED
## 1. 先看原理图

* 100ASK STM32F103 按键原理图

![](attachments/12_使用按键控制LED/001_stm32f103_key_sch.png)

* 我们使用 KEY1 来控制红色 LED：按下 KEY1 则灯亮，松开后灯灭

* KEY1 用的是 PA0 引脚

  ![](attachments/12_使用按键控制LED/002_key1_pin.png)



## 2. 再看芯片手册

### 2.1 使能 GPIOA 模块

**RCC_APB2ENR 地址：0x40021000 + 0x18**


![](attachments/12_使用按键控制LED/003_enable_gpioa.png)


### 2.2 设置引脚 GPIO 输入

**GPIOA_CRL 地址：0x40010800 + 0x00**

![](attachments/12_使用按键控制LED/004_config_gpioa.png)

### 2.3 读取引脚值

**GPIOA_IDR 地址：0x40010800 + 0x08**

![](attachments/12_使用按键控制LED/005_read_gpio_data.png)

## 3. 现场写程序

写好的源码：`doc_and_source_for_mcu_mpu\STM32MF103\source\02_录制视频时现场编写的源码\04_key_led`