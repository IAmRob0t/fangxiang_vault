---
tags:
  - ARM
  - 汇编
  - 指令集
---

VisUAL是一款ARM汇编模拟器，
下载地址：https://salmanarif.bitbucket.io/visual/downloads.html
如果无法下载，可以使用我们预先下载的，下载GIT资料后，位于这个目录：
“STM32F103\开发板配套资料\软件\ARM汇编模拟器”
使用方法：https://salmanarif.bitbucket.io/visual/user_guide/index.html

VisUAL模拟的ARM板子如下图所示，
它没有模拟外设，
仅仅模拟了CPU、ROM、RAM。
红色区域是ROM，不能读不能写，只能运行其中的程序；
ROM区域本来可以读的，这是VisUAL的局限；
RAM区域可读可写。
![图片描述](attachments/04_ARM汇编模拟器VisUAL/幻灯片1的图片1.png)

---

注意：右图中的DCD、FILL、END等是ARM汇编器语法
GCC汇编语法稍有不同，后面会介绍。
![图片描述](attachments/04_ARM汇编模拟器VisUAL/幻灯片2的图片1.png)

---

基本不需要设置，我也就设置字体大小而已：设置大小后，必须回车才其效果
![图片描述](attachments/04_ARM汇编模拟器VisUAL/幻灯片3的图片1.png)

---

![图片描述](attachments/04_ARM汇编模拟器VisUAL/幻灯片4的图片1.png)

---

![图片描述](attachments/04_ARM汇编模拟器VisUAL/幻灯片5的图片1.png)

---

点击“Reset”后修改为：
MOV R0, #0x20000
MOV R1, #0x1234
![图片描述](attachments/04_ARM汇编模拟器VisUAL/幻灯片6的图片1.png)

---

点击“Reset”后，才能修改：
![图片描述](attachments/04_ARM汇编模拟器VisUAL/点击Reset后才能修改.png)

---

![图片描述](attachments/04_ARM汇编模拟器VisUAL/幻灯片8的图片1.png)

---

![图片描述](attachments/04_ARM汇编模拟器VisUAL/幻灯片9的图片1.png)

---

![图片描述](attachments/04_ARM汇编模拟器VisUAL/幻灯片10的图片1.png)
