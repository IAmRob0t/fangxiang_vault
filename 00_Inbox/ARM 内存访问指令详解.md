---
tags:
  - ARM
  - 汇编
  - 内存访问
  - LDR
  - STR
  - LDM
  - STM
  - 栈
---

## 1. 概述

ARM 处理器提供了丰富的内存访问指令，用于在寄存器和内存之间传输数据。这些指令是编写高效汇编代码的基础，理解它们对于深入学习 ARM 架构至关重要。本笔记将详细介绍单寄存器和多寄存器内存访问指令，以及栈操作指令。

## 2. 单寄存器内存访问：LDR 与 STR

LDR 和 STR 指令用于在寄存器和内存之间传输单个字（Word）、半字（Halfword）或字节（Byte）数据。

### 2.1 LDR (Load Register) - 从内存加载数据到寄存器

LDR 指令用于将内存中的数据加载到指定的通用寄存器中。

*   **语法**: `LDR{type}{cond} Rt, [Rn {, #offset}]`
    *   `Rt`: 目标寄存器，数据将加载到此寄存器。
    *   `Rn`: 基址寄存器，包含内存地址的基址。
    *   `#offset`: 可选的偏移量，用于计算最终的内存地址。
    *   `type`: 指定加载数据的大小和符号扩展方式。
        *   `B`: 无符号字节 (Zero extend to 32 bits on loads)。
        *   `H`: 无符号半字 (Zero extend to 32 bits on loads)。
        *   `SB`: 有符号字节 (Sign extend to 32 bits)。
        *   `SH`: 有符号半字 (Sign extend to 32 bits)。
        *   省略 `type` 则表示加载一个字 (Word)。

![LDR指令语法](attachments/05_内存访问指令/LDR指令语法.png)

### 2.2 STR (Store Register) - 将寄存器数据存储到内存

STR 指令用于将指定通用寄存器中的数据存储到内存中。

*   **语法**: `STR{type}{cond} Rt, [Rn {, #offset}]`
    *   `Rt`: 源寄存器，其数据将被存储。
    *   `Rn`: 基址寄存器，包含内存地址的基址。
    *   `#offset`: 可选的偏移量，用于计算最终的内存地址。
    *   `type`: 指定存储数据的大小。
        *   `B`: 存储一个字节。
        *   `H`: 存储一个半字。
        *   省略 `type` 则表示存储一个字。

![STR指令语法](attachments/05_内存访问指令/STR指令语法.png)

### 2.3 寻址模式与特殊后缀

LDR 和 STR 指令支持多种寻址模式，以及一些特殊后缀来控制基址寄存器的更新。

*   **基址加偏移量寻址**: `[Rn, #offset]`
    *   例如：`STR R2, [R0, #4]` (将 R2 的值存到 R0+4 所示地址)
*   **基址加变址寻址**: `[Rn, +/-Rm {, shift}]`
    *   例如：`STR R2, [R0, R1, LSL #4]` (R2 的值存到 R0+(R1<<4) 所示地址)
*   **`!` (写回)**: 表示修改后的 `Rn` 值会写入 `Rn` 寄存器。
    *   例如：`STR R2, [R0, #8]!` (R2 的值存到 R0+8 所示地址, 并且 R0 = R0+8)
    *   如果没有 `!`, 指令执行完后 `Rn` 恢复/保持原值。
*   **`^` (CPSR)**: 会影响 `CPSR` (Current Program Status Register)，通常在讲异常处理时会详细说明。

### 2.4 单寄存器内存访问示例

以下代码展示了 `STR` 指令的多种用法：

```arm
MOV		R0, #0x20000            ; R0 = 0x20000 (基址)
MOV		R1, #0x10               ; R1 = 0x10
MOV		R2, #0x12               ; R2 = 0x12

STR		R2, [R0]                ; R2的值存到R0所示地址 (0x20000)
STR		R2, [R0, #4]            ; R2的值存到R0+4所示地址 (0x20004)
STR		R2, [R0, #8]!           ; R2的值存到R0+8所示地址 (0x20008), R0更新为0x20008
STR		R2, [R0, R1]            ; R2的值存到R0+R1所示地址 (0x20008 + 0x10 = 0x20018)
STR		R2, [R0, R1, LSL #4]    ; R2的值存到R0+(R1<<4)所示地址 (0x20008 + (0x10<<4) = 0x20008 + 0x100 = 0x20108)
STR		R2, [R0], #0X20         ; R2的值存到R0所示地址 (0x20108), R0更新为0x20108 + 0x20 = 0x20128
MOV		R2, #0x34               ; R2 = 0x34
STR		R2, [R0]                ; R2的值存到R0所示地址 (0x20128)
LDR		R3, [R0], +R1, LSL #1   ; R3的值等于R0+(R1<<1)所示地址上的值 (0x20128 + (0x10<<1) = 0x20128 + 0x20 = 0x20148)
```

---

## 3. 多寄存器内存访问：LDM 与 STM

LDM 和 STM 指令用于在寄存器列表和内存之间传输多个字数据，这在保存/恢复上下文（如函数调用）时非常有用。

### 3.1 LDM (Load Multiple Register) - 从内存加载多个寄存器

LDM 指令用于将内存中的多个字数据加载到指定的寄存器列表中。

*   **语法**: `LDM{addr_mode}{cond} Rn{!}, reglist{^}`
    *   `Rn`: 基址寄存器。
    *   `reglist`: 用花括号 `{}` 括起来的寄存器列表，例如 `{R0-R3, R5}`。
    *   `addr_mode`: 寻址模式，控制内存地址的增减方式。

![LDM指令语法](attachments/05_内存访问指令/LDM指令语法.png)

### 3.2 STM (Store Multiple Register) - 将多个寄存器数据存储到内存

STM 指令用于将指定寄存器列表中的多个字数据存储到内存中。

*   **语法**: `STM{addr_mode}{cond} Rn{!}, reglist{^}`
    *   `Rn`: 基址寄存器。
    *   `reglist`: 用花括号 `{}` 括起来的寄存器列表。
    *   `addr_mode`: 寻址模式，控制内存地址的增减方式。

![STM指令语法](attachments/05_内存访问指令/STM指令语法.png)

### 3.3 寻址模式 (addr_mode) 详解

`addr_mode` 决定了内存地址在每次传输前或传输后递增或递减。

*   **IA (Increment After)**: 每次传输后才增加 `Rn` 的值 (默认，可省略)。
*   **IB (Increment Before)**: 每次传输前就增加 `Rn` 的值 (ARM 指令才能用)。
*   **DA (Decrement After)**: 每次传输后才减小 `Rn` 的值 (ARM 指令才能用)。
*   **DB (Decrement Before)**: 每次传输前就减小 `Rn` 的值。

### 3.4 多寄存器内存访问示例

以下代码展示了 `STMIA` 指令的用法，以及内存布局的变化：

```arm
MOV		R1, #1
MOV		R2, #2
MOV		R3, #3
MOV		R0, #0x20000            ; R0 作为基址寄存器

STMIA	R0,  {R1-R3}            ; R1, R2, R3 分别存入 R0, R0+4, R0+8 地址处
                                ; 内存布局: 0x20000=1, 0x20004=2, 0x20008=3

ADD	R0, R0, #0x10           ; R0 = R0 + 0x10 = 0x20010

STMIA	R0!, {R1-R3}            ; R1, R2, R3 分别存入 R0, R0+4, R0+8 地址处
                                ; 内存布局: 0x20010=1, 0x20014=2, 0x20018=3
                                ; R0 更新为 R0 + 3*4 = 0x20010 + 0xC = 0x2001C
```

![STMIA多寄存器存取示例](attachments/05_内存访问指令/STMIA多寄存器存取示例.png)

---

## 4. 栈操作指令

栈是一种特殊的内存区域，用于临时存储数据，通常用于函数调用时的参数传递和局部变量存储。ARM 处理器通过 LDM/STM 指令的特定寻址模式来高效地实现栈操作。

### 4.1 栈的原理：满/空与增/减

根据栈指针 (SP) 的指向和增长方向，栈可以分为四种类型：

*   **满 (Full) / 空 (Empty)**:
    *   **满栈**: SP 指向最后一个入栈的数据。入栈前需要先修改 SP。
    *   **空栈**: SP 指向下一个空位置。先入栈再修改 SP。
*   **增 (Ascending) / 减 (Descending)**:
    *   **增栈**: SP 的值在入栈时变大。
    *   **减栈**: SP 的值在入栈时变小。

### 4.2 常用的“满减栈”操作

在 ARM 编程中，最常用的是**满减栈 (Full Descending Stack)**。

*   **入栈 (Push)**: 使用 `STMDB` 或 `STMFD` 指令。
    *   `STMDB sp!, {r0-r5}`: 将 `r0-r5` 寄存器的值压入栈中，SP 先递减再存储。
    *   `STMFD sp!, {r0-r5}`: 与 `STMDB` 作用相同，`FD` 表示 Full Descending。
*   **出栈 (Pop)**: 使用 `LDMIA` 或 `LDMFD` 指令。
    *   `LDMIA sp!, {r0-r5}`: 将栈顶数据弹出到 `r0-r5` 寄存器，SP 先加载再递增。
    *   `LDMFD sp!, {r0-r5}`: 与 `LDMIA` 作用相同，`FD` 表示 Full Descending。

### 4.3 栈操作示例

以下代码展示了满减栈的入栈和出栈操作：

```arm
STMFD sp!, {r0-r5} ; Push onto a Full Descending Stack (将r0-r5压入栈)
LDMFD sp!, {r0-r5} ; Pop from a Full Descending Stack (将栈顶数据弹出到r0-r5)
```

![STMFD与LDMFD栈操作示例](attachments/05_内存访问指令/STMFD与LDMFD栈操作示例.png)

---

## 5. 参考资料

*   《DEN0013D_cortex_a_series_PG.pdf》P340、P341、P377、P378
*   源码路径：`source\02_录制视频时现场编写的源码\02_VisUAL\ldr_str.S`
*   源码路径：`source\02_录制视频时现场编写的源码\02_VisUAL\stm.S`
*   源码路径：`source\02_录制视频时现场编写的源码\02_VisUAL\stack.S`