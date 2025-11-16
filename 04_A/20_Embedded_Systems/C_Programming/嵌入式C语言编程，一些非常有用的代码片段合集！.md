---
title: 嵌入式C语言编程，一些非常有用的代码片段合集！
source: https://mp.weixin.qq.com/s/qY6AkpHH502qH8Mvhf_zfQ
author:
  - "[[微信公众平台]]"
published: 
created: 2025-03-25
description: 你平时用到哪些？
tags:
  - clippings
  - c
---
*2025年03月25日 08:00* *广东*

我是老温，一名热爱学习的嵌入式工程师  

**关注我** ，一起变得更加优秀！

嵌入式软件开发过程中，为了提升工作效率，避免重复造轮子浪费时间，经常会复用一些C语言代码片段。

以下是一些利剑级别的C语言工具代码示例，以及它们的简要讲解，分享给各位老铁，大家按需使用。

1、循环队列（Circular Buffer）

```
typedef struct {
    int buffer[SIZE];
    int head;
    int tail;
    int count;
} CircularBuffer;

void push(CircularBuffer *cb, int data) {
    if (cb->count < SIZE) {
        cb->buffer[cb->head] = data;
        cb->head = (cb->head +1) % SIZE;
        cb->count++;
    }
}

int pop(CircularBuffer *cb) {
    if (cb->count >0) {
        int data = cb->buffer[cb->tail];
        cb->tail = (cb->tail +1) % SIZE;
        cb->count--;
        return data;
    }
    return-1; // Buffer is empty
}
```

循环队列是一种高效的数据结构，适用于缓冲区和数据流应用，例如串口通信接收缓冲。

2、断言 （Assertion）

```
#define assert(expression) ((void)0)
#ifndef NDEBUG
#undef assert
#define assert(expression) ((expression) ? (void)0 : assert_failed(__FILE__, __LINE__))
#endif

void assert_failed(const char *file, int line) {
    printf("Assertion failed at %s:%d\n", file, line);
    // Additional error handling or logging can be added here
}
```

断言用于在程序中检查特定条件是否满足，如果条件为假，会触发断言失败，并输出相关信息

3、位域反转 （Bit Reversal）

```
unsigned int reverse_bits(unsignedint num) {
    unsignedint numOfBits =sizeof(num) *8;
    unsignedint reverseNum =0;

    for (unsignedint i =0; i < numOfBits; i++) {
        if (num & (1<< i)) {
            reverseNum |= (1<< ((numOfBits -1) - i));
        }
    }
    return reverseNum;
}
```

该函数将给定的无符号整数的位进行反转，可以用于某些嵌入式系统中的位级操作需求 。

4、固定点数运算 （Fixed-Poin Arithmetic）

```
typedef int16_t fixed_t;

#define FIXED_SHIFT 8
#define FLOAT_TO_FIXED(f) ((fixed_t)((f) * (1 << FIXED_SHIFT)))
#define FIXED_TO_FLOAT(f) ((float)(f) / (1 << FIXED_SHIFT))

fixed_t fixed_multiply(fixed_t a, fixed_t b) {
    return (fixed_t)(((int32_t)a * (int32_t)b) >> FIXED_SHIFT);
}
```

在某些嵌入式系统中，浮点运算会较慢或不被支持。因此，使用固定点数运算可以提供一种有效的浮点数近似解决方案。

5、字节序转换 （Endianness Conversion）

```
uint16_t swap_bytes(uint16_t value) { return (value >> 8) | (value << 8); }
```

用于在大端（Big-Endian）和小端（Little-Endian）字节序之间进行转换的函数。

6、位掩码 （Bit Masks）

```
#define BIT_MASK(bit) (1 << (bit))
```

用于创建一个只有指定位被置位的位掩码，可用于位操作。

7、计数器计数 （Timer Counting）

```
#include <avr/io.h>

void setup_timer() {
    // Configure timer settings
}

uint16_t read_timer() {
    return TCNT1;
}
```

在AVR嵌入式系统中，使用计时器（Timer）来实现时间测量和定时任务。

8、二进制查找 （Binary Search）

```
int binary_search(int arr[], int size, int target) {
    int left =0, right = size -1;

    while (left <= right) {
        int mid = left + (right - left) /2;
        if (arr[mid] == target) {
            return mid;
        } elseif (arr[mid] < target) {
            left = mid +1;
        } else {
            right = mid -1;
        }
    }
    return-1; // Not found
}
```

用于在已排序的数组中执行二进制查找的函数。

9、位集合 （Bitset）

```
#include <stdint.h>

typedefstruct {
    uint32_t bits;
} Bitset;

void set_bit(Bitset *bitset, int bit) {
    bitset->bits |= (1U<< bit);
}

int get_bit(Bitset *bitset, int bit) {
    return (bitset->bits >> bit) &1U;
}
```

实现简单的位集合数据结构，用于管理一组位的状态。

这些代码示例代表了嵌入式开发中常用的一些利剑级别的C语言工具代码。它们在嵌入式系统开发中具有广泛的应用，有助于优化性能、节省资源并提高代码的可维护性。

来源 | 知乎-晓亮Albert

  

****\-END-****