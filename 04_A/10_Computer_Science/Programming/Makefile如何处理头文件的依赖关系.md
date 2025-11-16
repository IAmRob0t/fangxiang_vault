---
title: Makefile如何处理头文件的依赖关系
source: https://mp.weixin.qq.com/s/WSJqhHrzgOkPw6ovT7B59Q
author:
  - "[[情报小哥]]"
published: 
created: 2025-03-25
description: 
tags:
  - clippings
  - linux
---
原创 情报小哥 *2025年03月06日 21:02* *广东*

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/mPZJgHsAnGAWeoz41JuwKXNhqm4CVcxbORco6KPnoTSqJul1Zo7icH8Yyib4FgWrnCBhpbQ2tYOUUf1gUg82Ig0Q/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

#### 一、背景

在编译C/C++项目的时候，有时候会看到.d文件，但不太清楚具体是怎么产生的。

首先Makefile是如何处理头文件的依赖关系？通常，在Makefile中，我们需要指定目标文件（比如.o）依赖于哪些源文件（.c或.cpp）和头文件（.h）。但是，如果每次修改头文件后，Makefile不能自动检测到这些变化，可能会导致编译结果不正确，因为没有重新编译依赖该头文件的源文件。

所以，为了正确管理这些依赖关系，Makefile需要知道每个源文件都包含了哪些头文件。手动维护这些依赖关系会很麻烦，尤其是当项目很大，头文件很多的时候。这时候，自动生成依赖关系就显得很重要了。

##### 二. 生成.d 文件的编译器选项

这时候，GCC编译器支持生成依赖关系的功能。比如，gcc的-M系列选项，如-M、-MM、-MD、-MMD等。这些选项可以生成依赖规则，然后把这些规则包含到Makefile中。例如，使用-MMD选项，编译器在编译源文件的同时会生成一个.d文件，里面记录了该源文件生成的目标文件所依赖的所有头文件。

• **`-MMD`** ：生成依赖文件，忽略系统头文件（如 `<stdio.h>` ）。 • **`-MD`** ：生成依赖文件，包含所有头文件。 • **`-MP`** （推荐）：为每个头文件生成一个伪目标，避免删除头文件时报错。

**示例编译命令：**

```
gcc -MMD -MP -c main.c -o main.o
```

这会生成 `main.d` ，内容如下：

```
main.o: main.c utils.h
utils.h:  # 伪目标，防止删除头文件时报错
```

---

#### 三、一个 Makefile 的完整步骤

##### 1\. 基础 Makefile

```
CC = gcc
CFLAGS = -MMD -MP  # 启用依赖生成
SRCS = main.c utils.c
OBJS = $(SRCS:.c=.o)
TARGET = app

all: $(TARGET)

$(TARGET): $(OBJS)
$(CC)$^ -o $@

%.o: %.c
$(CC)$(CFLAGS) -c $< -o $@

clean:
 rm -f $(OBJS)$(TARGET) *.d

# 包含所有 .d 文件
-include $(SRCS:.c=.d)
```

##### 2\. 关键解释

• **`-include $(SRCS:.c=.d)`** ：  
自动包含所有 `.d` 文件， `-` 表示忽略文件不存在的错误（首次编译时无 `.d` 文件）。 • **`CFLAGS` 中的 `-MMD -MP`** ：  
编译时生成 `.d` 文件，并添加伪目标。

  

---

#### 四、验证

1. **首次编译** ：  
	执行 `make` ，生成 `main.o` 、 `utils.o` 和 `main.d` 、 `utils.d` 。
	```
	$ make
	gcc -MMD -MP -c main.c -o main.o
	gcc -MMD -MP -c utils.c -o utils.o
	gcc main.o utils.o -o app
	```
2. **修改头文件触发重新编译** ：  
	修改 `utils.h` 后再次执行 `make` ，观察 `main.o` 和 `utils.o` 是否重新编译。
	```
	$ touch utils.h
	$ make
	gcc -MMD -MP -c main.c -o main.o   # main.o 因依赖 utils.h 被重新编译
	gcc -MMD -MP -c utils.c -o utils.o
	gcc main.o utils.o -o app
	```

---

#### 五、优化与常见问题

##### 1\. 处理多级目录

如果项目文件分布在多个目录中，可以指定 `.d` 文件的输出路径：

```
OBJDIR = build
OBJS = $(addprefix $(OBJDIR)/, $(SRCS:.c=.o))
DEPFILES = $(addprefix $(OBJDIR)/, $(SRCS:.c=.d))

%.o: %.c | $(OBJDIR)
$(CC)$(CFLAGS) -c $< -o $@

$(OBJDIR)/%.d: %.c | $(OBJDIR)
 @touch $@

$(OBJDIR):
 @mkdir -p $@

-include$(DEPFILES)
```

##### 2\. 性能优化

• **快速查找 `.d` 文件** ：  
使用 `find` 命令替代递归函数：

```
DEPFILES := $(shell find $(OBJDIR) -name '*.d')
-include $(DEPFILES)
```

##### 3\. 常见问题

• **问题：删除头文件后报错**  
**解决** ：添加 `-MP` 选项生成伪目标。 • **问题：首次编译报错 `.d` 不存在**  
**解决** ：使用 `-include` 忽略错误。

## 最 后

小哥搜集了一些嵌入式学习资料，公众号内回复 **【 **1024** 】** 即可找到下载链接！

  

```
推荐好文  点击蓝色字体即可跳转☞专辑|Linux应用程序编程大全☞ 专辑|学点网络知识☞ 专辑|手撕C语言
☞ 专辑|手撕C++语言☞ 专辑|经验分享☞ 专辑|从单片机到Linux☞ 专辑|电能控制技术☞ 专辑|嵌入式必备数学知识☞  MCU进阶专辑
☞  嵌入式C语言进阶专辑
☞  经验分享
```

继续滑动看下一个

向上滑动看下一个 [知道了](https://mp.weixin.qq.com/s/) ： ， ， ， ， ， ， ， ， ， ， ， ， 。 视频 小程序 赞 ，轻点两下取消赞 在看 ，轻点两下取消在看 分享 留言 收藏 听过