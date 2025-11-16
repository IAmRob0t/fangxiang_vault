---
tags:
  - AT
---
# ESP8266-01S详细介绍

| 参数          | ESP-01S                     |
| ----------- | --------------------------- |
| 通信协议        | 完整的 802.11b/g/n WiFi SoC 模块 |
| 工作频段        | 2400~2483.5MHz              |
| 芯片方案        | ESP8266                     |
| 天线形式        | 板载天线                        |
| 封装形式        | DIP-8                       |
| 尺寸(mm)      | `24.4 * 14.4 * 11.2`        |
| 串口速率        | 4Mbps                       |
| 传输距离        | 50米                         |
| 供电电压        | 供电电压 3.0~3.6V, 典型值 3.3V     |
| SPI Flash   | 8Mbit                       |
| IO口数量       | 2个                          |
| 模组认证        | RoHs                        |
| Modem Sleep | 20mA                        |
| Light Sleep | 2mA                         |
| Deep Sleep  | 20μA                        |

# 什么是 AT 指令？

- AT 指令：Attention command set，AT指令集或AT命令集，一般称其为AT指令
- 海斯命令集：Hayes command set

[[AT 指令集_V3.0.1_ESP8266 Non-OS SDK.pdf]]

# 使用AT指令前需要注意的事

- AT 指令需要大写
- AT 指令需要以回车换行符结束，勾选“发送新行”，即 `\r\n`
	- CR （Carriage Return）表示回车
	  LF （Line Feed）表示换行
	- Dos和Windows采用回车+换行（CR+LF）表示下一行
	  而UNIX/Linux采用换行符（LF）表示下一行
	  MAC OS系统采用回车符（CR）表示下一行
	-  Windows下编写的Shell脚本，直接放到linux/unix下执行会报错，就是因为行结束符不一样导致的。

# AT指令的分类和提示信息

AT 指令可以细分为四种类型：

![[AT 指令集_V3.0.1_ESP8266 Non-OS SDK.pdf#page=13&rect=101,523,581,637&color=note|📖]]

## ESP8266 AT 指令中的提示信息说明

![[AT 指令集_V3.0.1_ESP8266 Non-OS SDK.pdf#page=67&rect=99,322,584,639&color=note|📖]]

# AT 指令概叙

## 基础 AT 指令概叙

![[AT 指令集_V3.0.1_ESP8266 Non-OS SDK.pdf#page=14&rect=101,88,582,627&color=note|📖]]

## 基础 Wi-Fi 功能 AT 指令概述

![[AT 指令集_V3.0.1_ESP8266 Non-OS SDK.pdf#page=25&rect=102,71,585,627&color=note|📖]]
![[AT 指令集_V3.0.1_ESP8266 Non-OS SDK.pdf#page=26&rect=100,478,584,722&color=note|📖]]

## TCP/IP 功能 AT 指令概述

![[AT 指令集_V3.0.1_ESP8266 Non-OS SDK.pdf#page=47&rect=101,69,585,627&color=note|📖]]
![[AT 指令集_V3.0.1_ESP8266 Non-OS SDK.pdf#page=48&rect=101,631,585,720&color=note|📖]]

# AT 指令应用示例

[[AT 指令使用示例_V1.3_ESP8266 Non-OS.pdf]]
