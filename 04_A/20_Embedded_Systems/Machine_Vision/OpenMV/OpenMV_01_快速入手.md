---
tags:
  - OpenMV
---

[OpenMV详细参数](https://singtown.com/cn/store/openmv4-h7-plus)
[OpenMV官方文档（中文）](https://docs.singtown.com/micropython/zh/latest/openmvcam/index.html)
[OpenMV中文入门教程](https://book.openmv.cc/)

## 1. 安装驱动

将 OpenMV 插到电脑。  
正常情况下，会**自动**安装驱动，一切不需要手动安装。在**设备管理器**中会看到：

![](https://book.openmv.cc/assets/02-003.jpg)

但是可能在一些电脑，驱动不会自动安装。  
这时在设备管理器中会出现一个叹号，表示没有正常安装驱动。

![](https://book.openmv.cc/assets/02-004.jpg)

这时就需要自己手动安装。  
首先下载驱动： [https://dl.singtown.com/openmv/openmv\_windows驱动.zip](https://dl.singtown.com/openmv/openmv_windows%E9%A9%B1%E5%8A%A8.zip)

解压到桌面，然后右键设备管理器中的这个设备，然后点升级驱动：

![](https://book.openmv.cc/assets/02-005.jpg)

![](https://book.openmv.cc/assets/02-006.jpg)

![](https://book.openmv.cc/assets/02-007.jpg)

![](https://book.openmv.cc/assets/02-008.jpg)

![](https://book.openmv.cc/assets/02-009.jpg)

## 2. Windows 驱动安装故障

如果出现下面的情况（此处极少发生，属于电脑故障）：  
![](https://book.openmv.cc/assets/02-010.jpg)

OpenMV 驱动安装失败，90%的情况都是电脑的问题，精简版操作系统和使用了一些优化软件通常是引起此类问题的原因。OpenMV 驱动解决办法跟 arduino 类似。

这是因为精简版的 window 系统删掉了一些不常用的驱动信息引起的。

故障参考资料：  
[https://forum.singtown.com/topic/230](https://forum.singtown.com/topic/230)

## 3. 运行 hello world！

将 OpenMV 通过 USB 线插入电脑，此时会有一个 U 盘出现

![](https://book.openmv.cc/assets/02-016.jpg)

打开 OpenMV IDE。

![](https://book.openmv.cc/assets/02-017.jpg)

重点看这张图。

- 点击 `连接`
- 再点击 `运行`

在右上角的图像窗里就正确显示图像了。  
点击最下方的 Serial Terminal，会弹出终端窗口。  
同时，在 Serial Terminal 里会一直打印数据，这个是帧率。是在代码中第 17 行 `print(clock.fps())` 执行的结果。

## 4. 追踪小球

将编辑框内的内容全部删掉，换成以下代码：

```python
# 色块监测 例子
#
# 这个例子展示了如何通过find_blobs()函数来查找图像中的色块
# 这个例子查找的颜色是深绿色

import sensor, image, time

# 颜色追踪的例子，一定要控制环境的光，保持光线是稳定的。
green_threshold   = (   0,   80,  -70,   -10,   -0,   30)
#设置绿色的阈值，括号里面的数值分别是L A B 的最大值和最小值（minL, maxL, minA,
# maxA, minB, maxB），LAB的值在图像左侧三个坐标图中选取。如果是灰度图，则只需
#设置（min, max）两个数字即可。

sensor.reset() # 初始化摄像头
sensor.set_pixformat(sensor.RGB565) # 格式为 RGB565.
sensor.set_framesize(sensor.QQVGA) # 使用 QQVGA 速度快一些
sensor.skip_frames(time = 2000) # 跳过2000s，使新设置生效,并自动调节白平衡
sensor.set_auto_gain(False) # 关闭自动自动增益。默认开启的，在颜色识别中，一定要关闭白平衡。
sensor.set_auto_whitebal(False)
#关闭白平衡。白平衡是默认开启的，在颜色识别中，一定要关闭白平衡。
clock = time.clock() # 追踪帧率

while(True):
    clock.tick() # Track elapsed milliseconds between snapshots().
    img = sensor.snapshot() # 从感光芯片获得一张图像

    blobs = img.find_blobs([green_threshold])
    #find_blobs(thresholds, invert=False, roi=Auto),thresholds为颜色阈值，
    #是一个元组，需要用括号［ ］括起来。invert=1,反转颜色阈值，invert=False默认
    #不反转。roi设置颜色识别的视野区域，roi是一个元组， roi = (x, y, w, h)，代表
    #从左上顶点(x,y)开始的宽为w高为h的矩形区域，roi不设置的话默认为整个图像视野。
    #这个函数返回一个列表，[0]代表识别到的目标颜色区域左上顶点的x坐标，［1］代表
    #左上顶点y坐标，［2］代表目标区域的宽，［3］代表目标区域的高，［4］代表目标
    #区域像素点的个数，［5］代表目标区域的中心点x坐标，［6］代表目标区域中心点y坐标，
    #［7］代表目标颜色区域的旋转角度（是弧度值，浮点型，列表其他元素是整型），
    #［8］代表与此目标区域交叉的目标个数，［9］代表颜色的编号（它可以用来分辨这个
    #区域是用哪个颜色阈值threshold识别出来的）。
    if blobs:
    #如果找到了目标颜色
        for b in blobs:
        #迭代找到的目标颜色区域
            # Draw a rect around the blob.
            img.draw_rectangle(b[0:4]) # rect
            #用矩形标记出目标颜色区域
            img.draw_cross(b[5], b[6]) # cx, cy
            #在目标颜色区域的中心画十字形标记

    print(clock.fps()) # 注意: 你的OpenMV连到电脑后帧率大概为原来的一半
    #如果断开电脑，帧率会增加
```

运行程序后

![](https://book.openmv.cc/assets/02-018.jpg)

这个程序会根据 `green_threshold` 的阈值，进行色块查找。

## 5. 更改阈值

那么如何自己更改这个阈值呢？我们怎么知道我们的物体的颜色阈值呢？

- 数字列表项目首先在摄像头中找到目标颜色，在 framebuffer 中的目标颜色上左击圈出一个矩形
- 在 framebuffer 下面的坐标图中，选择 LAB Color Space。

![](https://book.openmv.cc/assets/02-019.jpg)

- 三个坐标图分别表示圈出的矩形区域内的颜色的 LAB 值，选取三个坐标图的最大最小值，即 ( 0, 60, -70, -10, -0, 30)

![](https://book.openmv.cc/assets/02-020.jpg)

## 6. 文件系统

文件系统是 OpenMV（或者说 MicroPython）特别优秀的特点。什么是文件系统呢？简单来说，就是各种文件夹和文件以树形结构排列，简单来说，就是你的 U 盘啦。而且在代码中可以使用路径来进行读入文件，创建文件等操作。

![](https://book.openmv.cc/assets/02-021.jpg)

## 7. 脱机运行

那么问题来了？OpenMV 支持文件系统有什么用呢？

答案是，相当方便!  
OpenMV 把内置 Flash 虚拟成一个文件系统，当你插入 OpenMV 到电脑上的时候，电脑会弹出一个 U 盘！里面就是 OpenMV 的文件系统。当你想烧录固件的时候，直接把脚本文件复制到这个“U 盘”的 `main.py` 中。每次上电的时候，OpenMV 会自动运行里面的 `main.py`，这样就实现了脱机运行。

## 8. 一键下载

在工具栏里，点击 `将打开的脚本保存到OpenMV Cam（作为main.py）`, IDE 就会自动将当前文件保存到 main. Py，很方便。

![](https://book.openmv.cc/assets/02-022.jpg)

## 9. 供电

OpenMV 有两个电源**输入端**：

- VIN (有时也会标识为 VCC)
- USB 输入

VIN 输入为 3.6V~5V，推荐 5V。  
USB 和 VIN 可以同时供电。

![](https://book.openmv.cc/assets/02-023.jpg)

OpenMV 有一个电源**输出端**：

- 3.3V，这个电压是 OpenMV 的稳压器输出的，用于给其他传感器供电。注意：不要给 3.3V 直接供电，没有内部芯片的保护，很容易烧毁。

## 10. SD 卡

那如果我的代码有 10 万行，内置的 flash 不够用怎么办？我想保存图片怎么办？

答案是，可以使用 SD 卡！

![](https://book.openmv.cc/assets/02-024.jpg)

那么 SD 卡怎么用呢？SD 卡也是一个文件系统，当上电的时候，如果插入 SD 卡，那么 SD 卡的文件系统就会自动取代内置的 Flash 文件系统，每次上电，就会运行 SD卡中的 `main.py` 啦，是不是很直观，很方便。SD 卡最大支持 32G 的容量。