---
title: 用了 Linux 那么久，你知道从开机到第一行内核代码执行的全过程吗？
source: https://mp.weixin.qq.com/s/uY5OAzAsusnN22MAB8Gryg
author:
  - "[[ytcoode]]"
published: 
created: 2025-03-25
description: 
tags:
  - clippings
  - linux
---
**0x01 全景图**

本篇文章会根据下面这张全景图，来讲解从开机到第一行linux内核代码执行，之间的全部过程。

  

![图片](https://mmbiz.qpic.cn/mmbiz_png/z79xARvmm9iax9d94j0H5jCRr1DlmvLTKlhqYczVbtyaAIB91AF5N97zRq14cJwJtuY19F6HRKFCGOiaKdZCj7WQ/640?wx_fmt=png&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

## 1. 0x02 从开机到boot loader

  

电脑开机后，内嵌到主板上的uefi系统固件就会开始执行。  

  

固件的英文是firmware, 它是一种介于软件software和硬件hardware之间的，内嵌到硬件上的软件。  

  

uefi固件开始执行后，会先检测并初始化系统硬件，然后在它内部一个叫做boot manager的组件就开始执行。  

  

uefi boot manager的作用，就是寻找并启动一个uefi应用程序。  

  

所谓uefi应用程序，就是一个以PE32+格式存储的程序文件。  

  

PE32+文件格式，是 uefi规范中指定的，uefi应用程序使用的存储格式，它和Windows程序使用的 存储格式 是一样的。  

  

另外，linux程序使用的存储格式是 ELF，mac程序使用的存储格式是Mach-O。  

  

定义程序的存储格式，是为了在执行程序时，程序的执行者，比如操作系统，可以找到程序的代码在哪里，数据在哪里。  

  

综上我们可知，任何程序只要是以PE32+文件格式存储的，且符合uefi规范的，都可以被uefi直接执行。  

  

linux内核默认也被编译成了PE32+文件格式，所以它也是可以被uefi直接执行的。  

  

不过通常情况下我们不会这么做，我们一般会在uefi和linux内核之间，添加一个boot loader，然后让boot loader启动linux内核。  

  

这样做的好处是，我们可以非常方便的配置要传递给内核的initrd文件，以及各种参数等。  

  

总之，增加一个boot loader层，给我们带来了更多的灵活性。  

  

现在主流的boot loader有两个，一个是grub，一个是systemd-boot。  

  

grub虽然功能更强大些，但它配置方式太复杂了，所以对于日常使用，我更推荐功能足够但配置非常简单的systemd-boot。  

  

而且systemd-boot是被集成到了systemd里的，也就是说，只要你机器上装了systemd，systemd-boot也就自动装好了，是可以直接使用的。  

  

因为现在主流的linux发行版都使用systemd作为init程序，所以默认情况下，systemd都是已经安装了的，所以systemd-boot也是已经安装了的。  

  

另外说一句，systemd真的是一个大而全的重型武器，非常好用。  

  

鉴于systemd-boot的各种优点，本文就以systemd-boot作为boot loader，来讲解启动流程。  

  

systemd-boot作为一个boot loader，是要被uefi启动的，所以它也是以PE32+文件格式存储的，即它也是一个uefi应用程序。  

  

不过对于uefi的boot manager来说，它并不管它要启动的应用程序是什么，它只要求被启动的应用程序，是一个符合uefi规范的应用程序就好。  

  

下面我们来讲下，uefi中boot manager的执行逻辑。  

  

在uefi空间里面，除了有uefi固件代码，还有很多的uefi变量。  

  

每一个uefi变量就是一个类似于硬盘的存储单元，即在断电之后，变量里存储的数据不会丢失。  

  

uefi规范里面定义了 很多用于各种用途的变量。  

  

其中有一个变量，就是和启动相关的，它就是BootOrder。  

  

BootOrder变量里存储的，是一个可执行的uefi程序列表。  

  

uefi的boot manager在运行期间，就是从BootOrder里获取这些uefi程序，然后根据这些程序在BootOrder里的位置，依次尝试执行它们，直到有一个成功。  

  

这其实就是uefi boot manager的主体逻辑。  

  

另外要注意，BootOrder变量里并不是直接存储各uefi程序的文件路径的，它存储的，其实是一些以Boot作为前缀的uefi变量名。  

  

就像文章最开始那张图里展示的，BootOrder变量里存储的其实是 Boot0004, Boot0003, Boot001B, Boot0017 等uefi变量。  

  

而这些以Boot作为前缀的uefi变量，它们里面才存储了要执行的uefi程序的文件路径。  

  

又比如文章最开始那张图里展示的，Boot0004变量里存储的uefi应用程序所在路径为 /boot/EFI/systemd/systemd-bootx64.efi，它指向的其实就是 systemd-boot。  

  

uefi的boot manager在从BootOrder变量里挑选出一个合适的uefi程序后，它就会使用 EFI\_BOOT\_SERVICES.LoadImage() 函数，将这个uefi程序加载到内存， 然后再使用 EFI\_BOOT\_SERVICES.StartImage() 函数，启动这个uefi程序。  

  

如果这两步都没有发生错误，说明这个uefi程序启动成功。  

  

此时，控制流就会跳转到这个uefi程序的入口函数，然后开始执行这个uefi程序里面的相关代码。  

  

至此，uefi中boot manager的生命周期也就结束了。  

  

最后，我们再来实际查看下真实机器上的这些uefi变量。  

  

我们可以使用 efibootmgr 命令，来查看所有和启动相关的uefi变量：  

  

![图片](https://mmbiz.qpic.cn/mmbiz_png/z79xARvmm9iax9d94j0H5jCRr1DlmvLTK7CC48ySR6Iiba3YcicpdR5xFbwUtxMyHzI5XxnWKMk8slLg5fHdvBSsQ/640?wx_fmt=png&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

  

当然，我们也可以使用这个命令，来添加/修改/删除这些uefi变量，其实就是在修改uefi boot manager的启动逻辑。  

  

另外，我们还可以通过 efivar 命令，来查看或修改所有的uefi变量：  

  

![图片](https://mmbiz.qpic.cn/mmbiz_png/z79xARvmm9iax9d94j0H5jCRr1DlmvLTK9G88tAebnGEvyJ394gVKEXlcgCibwcicN5l2WmJwzCOPDpb8DEmPdubg/640?wx_fmt=png&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

  

因为机器上uefi变量非常多，所以这里只展示了前20条，大家如果有兴趣的话，可以在自己机器上试一下。  

  

最后再说一下，uefi boot manager选择要执行的uefi程序这一步，用户是可以介入的。  

  

我们在电脑开机后，先进入到uefi的配置界面：  

  

![图片](https://mp.weixin.qq.com/s/www.w3.org/2000/svg'%20xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg%20stroke='none'%20stroke-width='1'%20fill='none'%20fill-rule='evenodd'%20fill-opacity='0'%3E%3Cg%20transform='translate(-249.000000,%20-126.000000)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

  

然后在这里，就可以选择你想要执行的uefi程序。  

  

比如上图中的第三项，就是启动usb里的uefi程序。  

  

我们一般用usb安装操作系统时，就是通过这种方式，来让uefi启动usb里的iso镜像文件的。  

  

## 2. 0x03 从boot loader到linux内核

  

上文说过，boot loader我们选择的是systemd-boot。  

  

因为systemd-boot是有 源码 的，所以了解它内部的运行机制也相对较容易些。  

  

systemd-boot作为uefi应用程序的入口函数是 efi\_main。  

  

在它的内部，主要做了以下几件事，接下来我们就根据文章最开始的全景图来对照讲解。  

  

它先从 /boot/loader/entries/ 目录里加载所有以.conf 结尾的文件，每个文件是一个启动项。  

  

然后再从 /boot/loader/loader.conf 全局配置里，找到默认启动项。  

  

看全景图，/boot/loader/loader.conf 文件里配置的默认启动项是 nixos-generation-292.conf。  

  

其实在这一步之后，systemd-boot还会显示一个菜单，让用户可以选择其他启动项。  

  

但因为这一过程并不影响对systemd-boot启动流程的理解，所以就不详细讲了。  

  

systemd-boot在获得了一个启动项之后，就开始尝试运行该启动项里配置的linux内核。  

  

但在此之前，它还要做一些准备工作。  

  

比如，它会先把在启动项 nixos-generation-292.conf 里配置的initrd文件加载到内存，然后再把内存里的initrd数据绑定到uefi空间的一个固定设备路径上。  

  

这样后续内核启动时，就可以通过这个uefi设备路径，找到对应的initrd。  

  

initrd是一个打包文件，linux内核在启动时，会把它解压到内存根文件系统里的根目录下。  

  

然后，等linux内核都初始化完毕之后，内核就会开始尝试执行内存根目录下的init程序。  

  

这个init程序其实还不是我们经常说的，真正意义上的init程序。  

  

它只是linux内核执行的第一个用户程序。  

  

该init程序的作用，就是找到并挂载真正的根文件系统，这个一般是在硬盘上，然后再把控制权限转交给真正根文件系统下的init程序。  

  

第一个init程序，也就是initrd里的init程序，一般是shell脚本，当然也可以是systemd。  

  

第二个init程序，也就是真正根文件系统下的init程序，一般是systemd。  

  

至于init程序为什么要分成两个，在这里我们就不展开讲了，等后面讲linux内核启动流程时，再详细讲。  

  

我们再回到systemd-boot的启动流程。  

  

在加载完并初始化好initrd之后，systemd-boot就会使用uefi里的 EFI\_BOOT\_SERVICES.LoadImage() 函数，将启动项 nixos-generation-292.conf 里配置的linux内核加载到内存。  

  

然后再将启动项 nixos-generation-292.conf 里配置的内核参数，赋值到刚加载的内核镜像的对应字段上，这样内核在启动时，就可以通过某些uefi函数，来获取这些内核参数了。  

  

最后，systemd-boot再使用uefi里的 EFI\_BOOT\_SERVICES.StartImage() 函数，启动这个内核镜像。  

  

至此，控制流就会跳转到linux内核作为uefi应用的入口函数，systemd-boot的生命周期也就结束了。  

  

从上文我们可以看到，systemd-boot的启动流程和uefi的启动流程是很类似的，它们都是使用uefi中boot services里的 LoadImage 和 StartImage 函数，来加载并启动uefi应用程序的。  

  

由此我们可以得知，systemd-boot不仅可以用来启动linux内核，还可以用来启动任意的uefi应用程序。  

  

这也是为什么systemd-boot的官方文档，把它称为uefi boot manager，而非 boot loader 的原因。  

  

不过我们主要是用systemd-boot加载linux内核，所以为了便于大家理解，我们还是称之为 boot loader。  

  

另外我们还可以看到，使用uefi直接启动linux内核，和使用systemd-boot间接启动内核，它们之间是没有本质区别的，最终控制流都会跳转到linux内核作为uefi应用的入口函数，然后开始执行linux内核的相关代码。

  

  

\- END -