---
title: Linux的起源：从一个故事说起
source: https://mp.weixin.qq.com/s/XMoEvX0pCwDzYfBGb7D6XQ
author:
  - "[[微信公众平台]]"
published: 
created: 2025-04-03
description: 
tags:
  - clippings
  - linux
---
# Multics计划

上个世纪六十年代，那个计算机还没有很普及，只有少数人才能使用，而且当时的计算机系统都是批处理的，就是把一批任务一次性提交给计算机，然后就等待结果。并且中途不能和计算机交互。往往准备作业都需要花费很长时间，并且这个时候别人也不能用，导致了计算机资源的浪费。

![图片](https://mmbiz.qpic.cn/sz_mmbiz_jpg/mPZJgHsAnGCYHlSgicy7j4yfsseaPIGSRsz8vuGPTOjbHaibVicg3c7rLnrpaXuP7Clgqpia87ia615NNERWTFG2RwA/640?wx_fmt=jpeg&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

  

为了改变这种情况，在1965年前后，贝尔实验室（Bell）、麻省理工学院（MIT）以及通用电气（GE）联合起来准备研发一个分时多任务处理系统，简单来说就是实现多人同时使用计算机的梦想，并把计算机取名为Multics（多路信息计算系统），但是由于项目太复杂，加上其他原因导致了项目进展缓慢，1969年贝尔实验室觉得这个项目可能不会成功，于是就退出不玩了。

# Unix的诞生

Bell退出Multics计划之后，Bell实验室的那批科学家就没有什么事做了，其中一个叫做Ken Thompson的人在研发Multics的时候，写了一个叫做太空大战（Space Travel）的游戏，大概就是一个很简单的打飞机的游戏，但是这个游戏运行在Multics上。当Bell退出了Multics后，Thompson就没有了Multics的使用环境了，为了能够继续游戏，于是他花了一个月的时间写了一个小型的操作系统，用于运行Space Travel，当完成之后，Thompson怀着激动的心情把身边同事叫过来，让他们来玩他的游戏，大家玩过之后纷纷表示对他的游戏不感兴趣，但是对他的系统很感兴趣。

因为MULTICS是“Multiplexed informtion and Computing Service”的缩写（多路信息计算系统），于是他们命名这个系统为：“UNiplexed Information and Computing Service”，缩写为“UNICS”(每路信息计算系统，与Multics相反)。后来大家取其谐音，就称其为“UNIX”了。

![图片](https://mmbiz.qpic.cn/sz_mmbiz_jpg/mPZJgHsAnGCYHlSgicy7j4yfsseaPIGSRTdqJMefUw1j8KwNiaEDWk8kxhzJ1CQVIHr5ujnibrAl7B0UoFV1khm9Q/640?wx_fmt=jpeg&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

**这个时候已经是1970年了，于是就将1970年定为Unix元年，因此计算机上的时间就是从这一年开始计算的。**

后来Unix这个小操作系统就在Bell实验室内部流行开，并经过不断地改良最终在1974年7月Unix发展到第5个版本，Bell实验室公开了Unix，结果引起了学术界的广泛兴趣并对其源码索取。所以，Unix第五个版本就以“仅用于教育目的”的协议，提供给各大学作为教学之用，成为当时操作系统课程的范例教材。各大学公司开始通过Unix源码对Unix进行了各种各样的改进和拓展。1978年学术界的老大伯克利大学，推出了一份以第六版为基础，加上一些改进和新功能而成的Unix。并命名为BSD（Berkeley Software Distribution伯克利分发版），开创了Unix的另一分支： **BSD系列** 。

于是乎Unix就有了两个分支，一个就是BSD系列的分支，一个就是Bell本身发放的分支，当时因为Bell属于AT&T，AT&T受到了美国《谢尔曼反托拉斯法》的影响，不能销售除了电话机电报机等之外的商品，后来AT&T分解，Bell可以卖Unix了，Unix走向了商业化，如果想继续使用就需要购买授权，一份授权4万美元。

# 1. Minix及Linux的诞生

在Unix昂贵的授权费用下，很多大学不得不停止对其研究，老师导致上课也不知道讲什么了。在1987年荷兰有个大学教授安德鲁写了一个Minix，类似于Unix，专用于教学。当Minix流传开来之后，世界各地的黑客们纷纷开始使用并改进，希望把改进的东西合并到Minix中，但是安德鲁觉得他的系统是用于教学的，不能破坏纯净性，于是拒绝了。

在1991年9y月17日，Linus Torvalds(林纳斯.托瓦兹)在互联网上公布了自己写的Linux，可能是表达对安德鲁的不满吧（为什么不接受大家的好意呢？你让大家的满腔热情往哪放呢？），于是Linus发布了一个帖子，大概就是说：我写了一个操作系统的内核，但是还不够完善，你们以任何姿势使用不收费，也可以帮助我一起修改。帖子发出后引起了强烈的反响。在大家的努力下，于1994年Linux的1.0版本正式发布。

![图片](https://mmbiz.qpic.cn/sz_mmbiz_jpg/mPZJgHsAnGCYHlSgicy7j4yfsseaPIGSR1ibxPThibS3OtozOv5HM07KPszep7UN5zKE6kiaVTa3wj0BzlgXWUDXpQ/640?wx_fmt=jpeg&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

**为什么会引起这么强烈的反应呢？** 这就要从了另一个人说起，那就是Richard Stallman(自由软件之父)。Stallman是一个非常“激进”的人，因为Unix商业化的影响，他认为软件是全人类的智慧结晶，不应该为某一家公司服务。在八十年代，他发起了自由软件运动，吹起了共产主义的号角（发起了GNU运动），并发布了软件界的共产主义宣言（GPL协议），并且这一运动得到了很多人的认同。

所谓\*\*\*自由软件自由就是指： **自由使用、自由学习和修改、自由分发、自由创建衍生版。**

GNU的定义是一个递归缩写，就是GNU IS NOT UNIX。就是说Unix是流氓，我不是。有意思的是，GNU运动是上个世纪八十年代开始的，而那个时候Linux还没有诞生呢 ，所以Stallman宝宝心里苦啊，就在大家逐渐失去信心的时候，1991年Linus Torvalds带着他的Linux闪亮登场了，给GNU运动画了一个完美的句号。

Linux为什么会引起如此强烈的反响呢？因为Unix有版权，爱好编程的狂热分子在研究Unix的时候很容易吃上官司 ，而Linux是遵循GPL协议的，可以免费使用，让黑客们尽情的施展（这里的黑客指那些技术大牛，不是指那些利用计算机干坏事的人）。于是Linux提供内核（kernel），GNU提供外围软件，就这样GNU/Linux诞生了。

**从Unix到Linux的发展关系：**

![图片](https://mmbiz.qpic.cn/sz_mmbiz_jpg/mPZJgHsAnGCYHlSgicy7j4yfsseaPIGSRU0WzgZgI2hDxgQLuyg0YBHRSzkoEuNuMIlkWRogDMgIbmibGCKsA71w/640?wx_fmt=jpeg&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

所以，看到这里你就会了解到Unix是1970年出现的，Linux是1991年发布的，但Linux是不同于Unix的操作系统。

# 操作系统的基本概念

上面主要介绍了Linux以及Unix的一些历史故事，下面则介绍操作系统方面的知识。在进入正题之前，我们先简单了解一下操作系统。

我们都知道，CPU是由运算器和控制器组成的，程序在运行的时候就是调用CPU的指令进行一些运算操作，例如加减乘除。CPU能够调用的指令集合，就是指令集。但是不幸的是CPU的生产厂家不止一家，例如Intel、AMD等。即便是同一家厂商生产CPU，不同平台之间的指令集也不一样。那么程序员在编写程序的时候会遇到一个尴尬的局面，就是当你在某一个平台编码的时候，如果想将程序移到另外一个平台上，就需要重新编码，重新编码还不是最可怕的，可怕的是你得学习对应的新平台的指令集。

一般而言，我们称直接在硬件层面上进行编程是硬件规格层的编程（hardware spaceifiacation），例如调用CPU提供的指令等。你需要知道的是，不同硬件提供的API是个不相同的。如果程序员要编程还得精通硬件那得多难，所以我们需要一个通用软件来提供统一接口，以屏蔽硬件的差异化。这个通用软件就是操作系统。

**操作系统将底层硬件提供的接口进行封装，程序员直接调用由操作系统提供的接口，也称为系统调用。**

但是系统封装的接口会很多吗？显然不会很多，因为如果操作系统提过

几万个接口，程序员还不累的学出血。一般而言，系统提供的接口都是短小精悍，我们需要像搭积木一样，将其组装起来提供更为丰富的功能，并且将组装好的代码做成库，供别人使用。这样一来，就是库调用。在Windows上库一般都是dll（Dynamic Link Library），而在Linux或者Unix上我们一般称之为so（shared object），就是共享的代码，大家都可以调用。

现在我们知道了，操作系统的一个重要功能就是将硬件提供的功能进行封装，我们调用操作系统提供的接口就是系统调用（system call）。然后将系统提供的接口组合后形成更丰富的库。当然操作系统还有其他的功能，例如CPU的时间分片、安全保证等。

# Linux的发行版本

我们知道Linux或者Unix是一个操作系统，1991年的Linus Torvalds公布的是Linux的内核（kernel）。但是要注意的是，公布的是源码，并不是编译好的直接可安装的操作系统，我们如何安装一个操作系统呢？很简单啊，就是先下载一份源码，然后进行编译安装，但是编译的时候程序需要运行在操作系统上啊，操作系统呢？还没有编译呢。于是就陷入了一个死循环中，就是我们要安装操作系统，就需要编译，编译的时候需要操作系统，这样就是鸡生蛋，蛋生鸡。

这里就需要引入交叉编译了，具体做法： **假设我们要在电脑上安装Linux，我们把A的硬盘拆下来，放到已经安装了操作系统的电脑B上，然后编译，将编译好的操作系统放到硬盘上，再把硬盘装回去，开机启动，这就是交叉编译安装系统。**

这得有多难啊，入门难度实在太高了，所以我们迫切需要一种简单的方式来安装。于是就出现了这么一种公司，他们将已经公开好的Kernel（内核）再加上一些开源的周边软件收集起来编译成二级制文件放到网上供别人使用，其中Red Hat（红帽）就是其中著名的一家。我们知道Linux是遵循GPL协议的，也就是公开免费的，那么他们怎么盈利呢？既然不能卖软件，那么就卖服务呗，比如说，发现了Linux漏洞，然后Red Hat修复，如果你买了我们的服务，我们就将补丁程序给你，并指导你安装，所有问题都帮你解决。

世界上总是不缺好事者，RedHat既然可以这么做，为什么就不能有好心人免费做呢？是的，有这样一个社区，他们把RedHat的源码拿过来，然后编译成操作系统放出去，这就是CentOS，就是社区版的RedHat，所以基本RedHat的补丁包出来一个月之后，CentOS就出现对应的补丁包了。这对于Red Hat是好事还是坏事呢？这恐怕只有当事人知道了，不过在2014年年初传来消息，RedHat收编了CentOS的团队。就像MSDN I TELL YOU 上面都是微软的正版软件，可以随便下载，但是这不也是为微软做了免费宣传吗。

当别人说Linux的版本时，一般来说有两个版本，一个是内核的版本，一个是发行的版本。例如登录到终端执行命令：

```ruby
root@localhost:/home/Superman# uname -aLinux localhost.localdomain 4.6.0-040600-generic #201606100558 SMP Fri Jun 10 10:01:15 UTC 2016 x86_64 x86_64 x86_64 GNU/Linuxroot@localhost:/home/Superman# more /etc/issueUbuntu 16.04.2 LTS \n \l
```

从上面可以看出，uname -a 查看了内核的版本，是4.6.0的版本，而 more /etc/issue就是 查看发行版的版本，表示了我安装的是Ubuntu的16.04.2的发行版。

内核更新的信息可以到官网查看： https://www.kernel.org/

# Linux的哲学思想

**A.**一切皆文件，把几乎所有的资源都组织成文件的格式，我们只需要一个文本编辑工具，就可以修改工作的特性了，很方便。

**B.**组合小程序，完成复杂任务，例如将系统调用组合形成库（在Linux就是so结尾的文件）。

**C.**尽量避免和用户交互，Windows上就是弹框，让你点确定。在Linux上，如果执行一个程序之后没有任何提示，那就是最后的提示。

**D.**使用纯文本文件保存配置信息，这个在第一点就可以看出来。