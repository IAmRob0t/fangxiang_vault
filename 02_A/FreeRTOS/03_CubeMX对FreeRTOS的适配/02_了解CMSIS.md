---
tags:
  - cubemx
  - freeRTOS
---
![[01_CMSIS下的RTOS接口.png]]

> [!question] 什么是 CMSIS？
> - CMSIS（Common Microcontroller Software Interface Standard，直译过来就是"通用微控制器软件接口标准"）
> - 它是一个用来让微控制器开发者减少学习时间、简化软件移植、加速工程创建仿真和加速应用产品上架的工具集合
> - D:\0_Project\Git\rtos_doc_source - 副本\RTOS培训资料\00_基础资源资料\4_ARM架构通用资料\CMSIS\5.8.0\CMSIS

| 模块名     | 适用内核                   | 组件类型          | 描述（2025-Q2 版）                                 |
| ------- | ---------------------- | ------------- | --------------------------------------------- |
| Core(M) | Cortex-M, SecurCore    | Header-only   | 提供 Cortex-M 内核、NVIC、SysTick 寄存器定义与 SIMD 内部函数。 |
| Core(A) | Cortex-A5/A7/A9        | Header-only   | 提供 Cortex-A 启动模板、PL1/PL2 寄存器头。                |
| Core(R) | Cortex-R52/R82         | Header-only   | 提供 Cortex-R 内核、GIC、MPU 寄存器定义（CMSIS 6 新增）。     |
| Driver  | All Cortex             | Spec + Header | 定义统一外设驱动 API，实现由厂商 PACK 提供。                   |
| DSP     | Cortex-M               | Source/lib    | 63 种定点/单精度浮点 DSP 函数，针对 Helium/MVE 优化。         |
| ML(NN)  | Cortex-M               | Source/lib    | 轻量级神经网络算子库，前身 CMSIS-NN。                       |
| **RTOS V1** | **M0/M0+/M3/M4/M7**        | **Header + RTX5** | **第一代 CMSIS-RTOS API，基于 RTX5 实现。**                |
| **RTOS V2** | **All Cortex-M, A5/A7/A9** | **Header + 多后端**  | **第二代 API，新增 Armv8-M、可选动态对象、多核、二进制兼容。**           |
| PACK    | All Cortex             | Tool + XML 规范 | 软件组件、设备参数、板级描述包，用于 IDE 一键导入。                  |
| Build   | All Cortex             | CLI 工具        | CMSIS-Toolbox 2.0：cbuild/cpackget，CI 自动化构建。   |
| SVD     | All Cortex             | XML 规范        | 外设寄存器描述文件，供调试器与头文件生成器使用。                      |
| DAP     | All Cortex             | Spec + 固件     | CMSIS-DAP 调试探头标准，支持 JTAG/SW 接口。               |
| Zone    | Cortex-M, Cortex-A     | Header + 工具   | 系统资源划分规范，支持 TrustZone 多项目/多执行区。               |

CMSIS 的作用：
1. 提供了接口标准，便于移植和管理
2. 提供了很多第三方固件，便于业务开发
3. 因为统一了接口，使底层硬件和上层应用耦合降低，更换硬件平台时只需开发人员改变底层硬件的驱动即可，上层业务应用程序无需做改动

![[02_CMSIS架构概览.png]]

> [!question] V1 和 V2 又是指什么？

> [!question] V1 和 V2 有什么区别？

