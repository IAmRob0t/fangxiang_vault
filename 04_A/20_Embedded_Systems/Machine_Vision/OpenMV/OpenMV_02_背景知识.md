---
tags:
  - OpenMV
---

# 图像处理背景知识



# Python 背景知识

-  [[01_Python基础#2. 变量|变量]]
- [[01_Python基础#`list` 和 `tuple`|list列表 和 tuple元组]]
- [[01_Python基础#条件判断|条件判断]]
- [[01_Python基础#循环|循环]]
- [[02_函数|函数]]

- 

# REPL和串口

OpenMV的IDE自带一个串口助手，用于连接OpenMV，也可以连接其他的串口，比如Arduino，pyboard，esp8266。

首先，断开OpenMV与IDE的连接，否则串口会冲突！

打开OpenMV 中的 工具 → Open Terminal → New Terminal

![](https://book.openmv.cc/assets/04-001.jpg)

![](https://book.openmv.cc/assets/04-002.jpg)

![](https://book.openmv.cc/assets/04-003.jpg)

![](https://book.openmv.cc/assets/04-004.jpg)

在终端里输入

```
print("hello OpenMV!")
```

会显示

```
hello OpenMV!
```