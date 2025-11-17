---
tags:
  - ARM
  - 汇编
  - 指令集
  - VisUAL
  - 教程
---

# VisUAL 模拟器入门教程

本教程将引导您完成 VisUAL ARM 汇编模拟器的基本使用，从安装、编写代码到执行和调试，帮助您快速上手。

## 1. 引言与准备

VisUAL 是一款轻量级的 ARM 汇编模拟器，非常适合学习和测试 ARM 指令。它提供了一个可视化的界面，可以清晰地看到代码执行过程中寄存器和内存的变化。

- **模拟范围**：VisUAL 仅模拟了 CPU 核心（包括寄存器）和一块内存空间，并未模拟中断、GPIO 等外设。
- **内存模型**：如下图所示，VisUAL 将内存分为指令区（Instruction Memory）和数据区（Data Memory）。
- **官方链接**：
    - **下载地址**: [https://salmanarif.bitbucket.io/visual/downloads.html](https://salmanarif.bitbucket.io/visual/downloads.html)
    - **使用指南**: [https://salmanarif.bitbucket.io/visual/user_guide/index.html](https://salmanarif.bitbucket.io/visual/user_guide/index.html)

![VisUAL模拟的CPU与内存模型](attachments/04_ARM汇编模拟器VisUAL/file-20251117221304132.png)

---

## 2. 界面导览与基本设置

VisUAL 的界面主要分为三个区域：左侧的代码编辑区，右侧的寄存器状态区，以及顶部的执行控制区。

对于初学者，基本无需额外设置。如果需要调整字体大小以便观察，可以按以下步骤操作：
1.  点击菜单栏的 `Settings`。
2.  在 `Code editor font size` 处输入合适的字号（例如 40），然后按回车键即可生效。

![设置字体大小](attachments/04_ARM汇编模拟器VisUAL/file-20251117221304136.png)

---

## 3. 第一个汇编程序：从编写到执行

让我们通过一个将数值 `0x1234` 存入地址 `0x20000` 的简单程序来学习核心操作。

### 步骤 1：编写代码

在左侧的代码编辑区，我们可以直接编写汇编代码。

![编写第一个汇编程序](attachments/04_ARM汇编模拟器VisUAL/file-20251117221304137.png)

### 步骤 2：常见错误与修正

在编写 `MOV R1, #0x1234` 时，VisUAL 会提示一个运行时错误：“Invalid immediate operand value”。

这是因为在 ARM 指令中，`MOV` 指令的立即数（immediate）有范围限制，`0x1234` 超出了这个限制。

**修正方法**：使用 `LDR` 伪指令。汇编器会自动将 `LDR R1, =0x1234` 转换为一条或多条合法的 ARM 指令，以将这个较大的数值加载到寄存器 `R1` 中。

| 错误代码 | 错误提示 | 修正后代码 |
| :--- | :--- | :--- |
| `MOV R1, #0x1234` | ![无效立即数错误](attachments/04_ARM汇编模拟器VisUAL/file-20251117221304137%201.png) | `LDR R1, =0x1234` |

修正后的完整代码如下：

```arm
MOV R0, #0x20000  // 将内存地址 0x20000 加载到 R0
LDR R1, =0x1234   // 将数值 0x1234 加载到 R1
STR R1, [R0]     // 将 R1 中的值存储到 R0 指向的内存地址
```

![使用LDR伪指令修正](attachments/04_ARM汇编模拟器VisUAL/file-20251117221304138.png)

### 步骤 3：执行与调试

VisUAL 提供了多种执行方式，最常用的是：
- **Execute (F5)**: 全速执行，直到程序结束或遇到断点。
- **Step Forwards (F10)**: 单步执行，即每次只执行一条指令，便于观察每一步的变化。

![执行与单步调试按钮](attachments/04_ARM汇编模拟器VisUAL/file-20251117221304138%201.png)

---

## 4. 观察与验证

代码执行后，我们需要验证其结果是否符合预期。

### 步骤 1：观察寄存器

通过单步执行，我们可以看到每条指令执行后，右侧寄存器状态区的变化。执行前两条指令后，`R0` 和 `R1` 的值会变为我们代码中设定的值。

![单步执行后观察寄存器变化](attachments/04_ARM汇编模拟器VisUAL/file-20251117221304139.png)

### 步骤 2：观察内存

执行完 `STR R1, [R0]` 指令后，数据 `0x1234` 应该被写入了地址 `0x20000`。验证步骤如下：
1.  点击菜单栏的 `Tools` -> `View memory contents`。
2.  在弹出的 `View Memory Contents` 窗口中，输入起始地址 `0x20000`。
3.  可以看到地址 `0x20000` 处的值已经变成了 `0x1234`，验证成功。

![查看内存写入结果](attachments/04_ARM汇编模拟器VisUAL/file-20251117221304140.png)

---

## 5. 进阶示例：条件执行

VisUAL 同样支持带有条件的指令。例如，下面的代码比较 `R1` 和 `R2` 的大小，并根据结果将较大的值存入 `R0` 指向的内存地址。

- `CMP R1, R2`: 比较 `R1` 和 `R2`，结果影响 `CPSR` 状态寄存器。
- `STRLE R1, [R0]`: 如果 `R1 <= R2` (LE: Less or Equal)，则执行存储。
- `STRGT R2, [R0]`: 如果 `R1 > R2` (GT: Greater Than)，则执行存储。

![条件执行指令示例](attachments/04_ARM汇编模拟器VisUAL/file-20251117221304142.png)

---

## 附录：ARM 指令集速查表

下图列出了一些常用的 ARM 指令，以供快速参考。

![ARM指令集速查表](attachments/04_ARM汇编模拟器VisUAL/file-20251117221304135.png)