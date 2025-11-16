---
title: 状态机”来解析UART不定长度的协议帧
source: https://mp.weixin.qq.com/s/QFir5mgrFSLZck6JNMqN3Q
author:
  - "[[微信公众平台]]"
published: 
created: 2025-04-03
description: 常用知识点！
tags:
  - clippings
  - uart
---
通信设计中考虑协议的灵活性，经常把协议设计成“不定长度”。一个实例如下图：锐米LoRa终端的通信协议帧。

![图片](https://mmbiz.qpic.cn/mmbiz_jpg/PnO7BjBKUz8P4R5DTrUpsjb7vRQx738WxFY6hjwwPOgT0aHJubMsQqGPsmcyDIcdPa9tbdh6PYKCu7lkT3NxtQ/640?wx_fmt=jpeg&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

如果一个系统接收上述“不定长度”的协议帧，将会有一个挑战-- **如何高效接收与解析。**

为简化系统设计，我们强烈建议您采用“ **状态机** ”来解析UART数据帧，并且把解析工作放在ISR（中断服务程序）完成，仅当接收到最后一个字节（0x0D）时，再将整个数据帧提交给进程处理。

该解析状态机的原理如下图所示：

![图片](https://mmbiz.qpic.cn/mmbiz_jpg/PnO7BjBKUz8P4R5DTrUpsjb7vRQx738W9ibicianw1Odk8mho1pf3f0eibHT9xAEG9AUuO4v1SqEDzXzmMQrMMfRSQ/640?wx_fmt=jpeg&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

那么ISR处理这个状态机来得及吗？答案是：so easy！因为它只有3个动作，运算量十分小：

**比较接收数据 -> 更新状态变量 -> 存储接收数据** ，C语言仅3条语句，翻译成机器指令也不超过10条。

**代码清单如下** ：

```
/**
* @brief  Status of received communication frame
*/
typedef enum
{
    STATUS_IDLE = (uint8_t)0,
    STATUS_HEAD, /* Rx Head=0x3C */
    STATUS_TYPE, /* Rx Type */
    STATUS_DATA, /* Data filed */
    STATUS_TAIL, /* Tail=0x0D */
    STATUS_END, /* End of this frame */
} COMM_TRM_STATUS_TypeDef;

/**
* @brief  Data object for received communication frame
*/
typedef struct
{
    uint8_t    byCnt; /* Count of 1 field */
    uint8_t    byDataLen; /* Length of data field */
    uint8_t    byFrameLen; /* Length of frame */
    COMM_TRM_STATUS_TypeDef    eRxStatus;
    uint8_t    a_byRxBuf[MAX_LEN_COMM_TRM_DATA]; 
} COMM_TRM_DATA;

/**
* @brief  Data object for received communication frame.
* @note  Prevent race condition that accessed by both ISR and process.
*/
static COMM_TRM_DATA    s_stComm2TrmData;

/**
  * @brief  Put a data that received by UART into buffer.
  * @note  Prevent race condition this called by ISR. 
  * @param  uint8_t byData: the data received by UART.
  * @retval  None
  */
void comm2trm_RxUartData(uint8_t byData)
{
    /* Update status according to the received data */
    switch (s_stComm2TrmData.eRxStatus)
    {
        case STATUS_IDLE:
            if (COMM_TRM_HEAD == byData) /* Is Head */
            {
                s_stComm2TrmData.eRxStatus = STATUS_HEAD;
            }
            else
            {
                goto rx_exception;
            }
            break;
        case STATUS_HEAD:
            if (TYPE_INVALID_MIN < byData && byData < TYPE_INVALID_MAX) /* Valid type */
            {
                s_stComm2TrmData.eRxStatus = STATUS_TYPE;
            }
            else
            {
                goto rx_exception;
            }
            break;
        case STATUS_TYPE:
            if (byData <= MAX_LEN_UART_FRAME_DATA) /* Valid data size */
            {
                s_stComm2TrmData.eRxStatus = STATUS_DATA;
                s_stComm2TrmData.byDataLen = byData;
            }
            else
            {
                goto rx_exception;
            }
            break;
        case STATUS_DATA:
            if (s_stComm2TrmData.byCnt < s_stComm2TrmData.byDataLen)
            {
                ++s_stComm2TrmData.byCnt;
            }
            else
            {
                s_stComm2TrmData.eRxStatus = STATUS_TAIL;
            }
            break;
        case STATUS_TAIL:
            if (COMM_TRM_TAIL == byData)
            {
                /* We received a frame of data, now tell process to deal with it! */
                process_poll(&Comm2TrmProcess);
            }
            else
            {
                goto rx_exception;
            }
            break;
        default:
            ASSERT(!"Error: Bad status of comm2trm_RxUartData().\r\n");
            break;
    }

    /* Save the received data */
    s_stComm2TrmData.a_byRxBuf[s_stComm2TrmData.byFrameLen++] = byData;
    return;

rx_exception:
    ClearCommFrame();
    return; 
}
```

  

原文：https://blog.csdn.net/jiangjunjie\_2005/article/details/50619884