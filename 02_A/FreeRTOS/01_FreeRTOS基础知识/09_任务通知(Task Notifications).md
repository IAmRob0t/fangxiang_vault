使用队列、信号量、事件组时，我们都要事先创建对应的结构体，双方通过中间的结构体通信：

![[FreeRTOS完全开发手册之上册_快速入门.pdf#page=133&rect=67,615,523,680|FreeRTOS完全开发手册之上册_快速入门, p.133]]

使用任务通知时，任务结构体 TCB 中就包含了内部对象，可以直接接收别人发过来的"通知"：

![[FreeRTOS完全开发手册之上册_快速入门.pdf#page=133&rect=71,514,526,590|FreeRTOS完全开发手册之上册_快速入门, p.133]]

# 任务通知的特性

本节源码：`22_freertos_example_tasknotify_semaphore`，来自 `15_freertos_example_semaphore`，下一节视频才修改。

## 优势及限制

## 通知状态和通知值

理解任务通知的核心在于 TCB 结构体中有这两项：

```c
#if ( configUSE_TASK_NOTIFICATIONS == 1 )
    volatile uint32_t ulNotifiedValue[ configTASK_NOTIFICATION_ARRAY_ENTRIES ];
    volatile uint8_t ucNotifyState[ configTASK_NOTIFICATION_ARRAY_ENTRIES ];
#endif
```

`ucNotifyState` 通知状态有 3 种取值：
* `taskNOT_WAITING_NOTIFICATION`：任务没有在等待通知
* `taskWAITING_NOTIFICATION`：任务在等待通知
* `taskNOTIFICATION_RECEIVED`：任务接收到了通知，也被称为 pending (有数据了，待处理)  

# 任务通知的使用

使用流程：使用 ucNotifyState 来切换任务状态 (阻塞、就绪)，使用 ulNotifiedValue 来传递信息。

* 任务 A 被创建出来时，ucNotifyState 为 `taskNOT_WAITING_NOTIFICATION`
* 它想等待通知的话
	* 调用 `ulTaskNotifyTake ` 或 `xTaskNotifyWait  `，进入 `taskWAITING_NOTIFICATION`
	* 表示在等待通知，任务进入阻塞状态
* 任务 B 可以调用这两个函数来通知 A：`xTaskNotifyGive  ` 或 `xTaskNotify  `
	* 任务 A 的 ucNotifyState 就变为 `taskNOTIFICATION_RECEIVED`
	* 表示收到了通知，待处理
* 任务 A 从阻塞状态变为就绪态，它运行时
	* 从 `ulTaskNotifyTake ` 或 `xTaskNotifyWait  ` 得到数值并返回
	* 返回之前把 ucNotifyState 恢复为 `taskNOT_WAITING_NOTIFICATION`

## 两类函数

## `xTaskNotifyGive` / `ulTaskNotifyTake`

在任务中使用 `xTaskNotifyGive` 函数，在 ISR 中使用 `vTaskNotifyGiveFromISR` 函数，都是直接给其他任务发送通知： 
- 使得通知值加一
- 并使得通知状态变为"pending"，也就是 `taskNOTIFICATION_RECEIVED` ，表示有数据了、待处理

可以使用 `ulTaskNotifyTake` 函数来取出通知值：
- 如果通知值等于 0，则阻塞 (可以指定超时时间) 
- 当通知值大于 0 时，任务从阻塞态进入就绪态
- 在 `ulTaskNotifyTake` 返回之前，还可以做些清理工作：把通知值减一，或者把通知值清零

使用 `ulTaskNotifyTake` 函数可以实现 [[#任务通知实现轻量级 06_信号量(semaphore) 信号量|轻量级的、高效的二进制信号量、计数型信号量]] 。

---

这几个函数的原型如下：

```c
BaseType_t xTaskNotifyGive (TaskHandle_t xTaskToNotify);

uint32_t ulTaskNotifyTake (BaseType_t xClearCountOnExit, TickType_t xTicksToWait);
```

( [[FreeRTOS完全开发手册之上册_快速入门.pdf#page=136&selection=83,0,84,10&color=note|📖]])
`xTaskNotifyGive` 函数的参数说明如下：

( [[FreeRTOS完全开发手册之上册_快速入门.pdf#page=137&selection=105,0,106,10&color=note|📖]])
`ulTaskNotifyTake` 函数的参数说明如下：

## `xTaskNotify` / `xTaskNotifyWait`

`xTaskNotify` 函数功能更强大，可以使用不同参数实现各类功能，比如：
- 让接收任务的通知值加一：这时 `xTaskNotify()` 等同于 `xTaskNotifyGive()`
- 设置接收任务的通知值的某一位、某些位，这就是一个 [[#任务通知实现轻量级 08_事件组(event group) 事件组|轻量级的、更高效的事件组]]
- 把一个新值写入接收任务的通知值：上一次的通知值被读走后，写入才成功。这就是 [[#任务通知实现轻量级 05_队列 (queue) 队列|轻量级的、长度为1的队列]]
- 用一个新值覆盖接收任务的通知值：无论上一次的通知值是否被读走，覆盖都成功。类似 `xQueueOverwrite()` 函数，这就是 [[05_队列 (queue)#示例 11 邮箱 (Mailbox)|轻量级的邮箱]] 。

使用 `xTaskNotifyWait ()` 函数来取出任务通知：
- 可以让任务等待 (可以加上超时时间)，等到任务状态为"pending" (也就是有数据)
- 还可以在函数进入、退出时，清除通知值的指定位

---

这几个函数的原型如下：

```c
BaseType_t xTaskNotify (TaskHandle_t xTaskToNotify, uint32_t ulValue, eNotifyAction eAction);

BaseType_t xTaskNotifyWait	(uint32_t ulBitsToClearOnEntry, 
							uint32_t ulBitsToClearOnExit, 
                        	uint32_t *pulNotificationValue, 
                        	TickType_t xTicksToWait );
```

( [[FreeRTOS完全开发手册之上册_快速入门.pdf#page=138&selection=131,0,132,10&color=note|📖]])
`xTaskNotify` 函数的参数说明如下：

( [[FreeRTOS完全开发手册之上册_快速入门.pdf#page=138&selection=134,0,135,5&color=note|📖]])
`eNotifyAction` 参数说明：

| `eNotifyAction` 取值          | 说明                                                                                  |
| --------------------------- | ----------------------------------------------------------------------------------- |
| `eNoAction`                 | 仅仅是更新通知状态为"pending"，未使用 `ulValue`。这个选项相当于轻量级的、更高效的二进制信号量。                           |
| `eSetBits`                  | 通知值 = 原来的通知值 \| `ulValue`，按位或。相当于轻量级的、更高效的事件组。                                      |
| `eIncrement`                | 通知值 = 原来的通知值 + 1，未使用 ulValue。相当于轻量级的、更高效的二进制信号量、计数型信号量。相当于 xTaskNotifyGive () 函数。   |
| `eSetValueWithoutOverwrite` | 则此次调用 `xTaskNotify` 不做任何事，返回 pdFAIL。如果通知状态不是"pending" (表示没有新数据)， 则：通知值 = `ulValue`。 |
| `eSetValueWithOverwrite`    | 覆盖。<br>无论如何，不管通知状态是否为"pendng"， 通知值 = `ulValue`。                                     |

( [[FreeRTOS完全开发手册之上册_快速入门.pdf#page=139&selection=177,0,178,8&color=note|📖]])
`xTaskNotifyWait` 函数列表如下：

# 示例 22: 传输计数值

# 示例 23: 传输任意值

# 任务通知实现轻量级 [[06_信号量(semaphore)|信号量]]

本节源码：`22_freertos_example_tasknotify_semaphore`，来自 `15_freertos_example_semaphore`。

函数对比：

|      | 信号量                                                                                                 | 使用任务通知实现信号量                                                                          |
| ---- | --------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------ |
| 创建   | `SemaphoreHandle_t xSemaphoreCreateCounting (UBaseType_t uxMaxCount, UBaseType_t uxInitialCount );` | 无                                                                                    |
| Give | `xSemaphoreGive ( SemaphoreHandle_t xSemaphore );`                                                  | `BaseType_t xTaskNotifyGive ( TaskHandle_t xTaskToNotify );`                         |
| Take | `xSemaphoreTake (SemaphoreHandle_t xSemaphore, TickType_t xBlockTime);`                             | `uint32_t ulTaskNotifyTake (BaseType_t xClearCountOnExit, TickType_t xTicksToWait);` |
 
# 任务通知实现轻量级 [[05_队列 (queue)|队列]]

本节源码：`23_freertos_example_tasknotify_queue`，来自 `13_freertos_example_queue`。

函数对比：

|     | 队列                                                                                                  | 使用任务通知实现队列                                                                                                                                           |
| --- | --------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| 创建  | `QueueHandle_t xQueueCreate (UBaseType_t uxQueueLength, UBaseType_t uxItemSize);`                   | 无                                                                                                                                                    |
| 发送  | `BaseType_t xQueueSend QueueHandle_t xQueue, const void * pvItemToQueue, TickType_t xTicksToWait);` | `BaseType_t xTaskNotify (TaskHandle_t xTaskToNotify, uint32_t ulValue, eNotifyAction eAction);`                                                      |
| 接收  | `BaseType_t xQueueReceive ( QueueHandle_t xQueue, void * const pvBuffer, TickType_t xTicksToWait);` | `BaseType_t xTaskNotifyWait (uint32_t ulBitsToClearOnEntry, uint32_t ulBitsToClearOnExit, uint32_t *pulNotificationValue, TickType_t xTicksToWait);` |

# 任务通知实现轻量级 [[08_事件组(event group)|事件组]]

本节源码：`24_freertos_example_tasknotify_event_group`，来自 `20_freertos_example_event_group`。

假设有 3 个任务：
* 任务 1 做事件 1
* 任务 2 做事件 2
* 任务 3 等待事件 1、事件 2 都发生

可以使用事件组来编写程序，也可以使用任务通知来编写程序。

函数对比：

|      | 事件组                                                                                                                                                                                              | 使用任务通知实现事件组                                                                                                                                          |
| ---- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| 创建   | `EventGroupHandle_t xEventGroupCreate (void)`                                                                                                                                                    | 无                                                                                                                                                    |
| 设置事件 | `EventBits_t xEventGroupSetBits (EventGroupHandle_t xEventGroup, const EventBits_t uxBitsToSet);`                                                                                                | `BaseType_t xTaskNotify (TaskHandle_t xTaskToNotify, uint32_t ulValue, eNotifyAction eAction);`                                                      |
| 等待事件 | `EventBits_t xEventGroupWaitBits (EventGroupHandle_t xEventGroup, const EventBits_t uxBitsToWaitFor, const BaseType_t xClearOnExit, const BaseType_t xWaitForAllBits, TickType_t xTicksToWait);` | `BaseType_t xTaskNotifyWait (uint32_t ulBitsToClearOnEntry, uint32_t ulBitsToClearOnExit, uint32_t *pulNotificationValue, TickType_t xTicksToWait);` |

使用任务通知实现轻量级事件组时，无论我设置哪些位，肯定会把目标任务唤醒，而且函数 `xTaskNotifyWait` 也无法指定等待的任务是什么

# 任务通知内部机制

- 发通知
	1. 关中断
	2. 写 value ，wake up
	3. 开中断

- 等通知
	1. 关中断
	2. 判断状态
		- 开中断，休眠
	3. 唤醒后，return

## 通知状态

一个任务的"通知状态"有三种：
* `taskNOT_WAITING_NOTIFICATION`：任务没有在等待通知（空闲状态）
* `taskWAITING_NOTIFICATION`：任务在等待通知（被 `ulTaskNotifyTake()` 或 `xTaskNotifyWait()` 挂起）
* `taskNOTIFICATION_RECEIVED`：任务接收到了通知，也被称为 pending（即 pending，有待处理的通知)  

## 等待通知的过程

当一个任务调用以下函数之一时：
- `ulTaskNotifyTake()`
- `xTaskNotifyWait()`

它的行为如下：
1. 如果任务的通知状态为 `taskNOTIFICATION_RECEIVED`（即之前已经收到通知但尚未取走），函数会**立即返回**，并根据参数清除或减少通知值。
2. 如果通知状态为 `taskNOT_WAITING_NOTIFICATION`（即当前没有待处理的通知），函数会：
    - 将任务的通知状态设置为 `taskWAITING_NOTIFICATION`；
    - 将任务加入阻塞态，等待其他任务或中断通过 `xTaskNotify()` 或 `xTaskNotifyGive()` 发送通知；
    - 若在超时时间内收到通知，则恢复运行并更新通知状态为 `taskNOTIFICATION_RECEIVED` 或清除通知值；
    - 若超时未收到通知，则返回 0（表示超时）。

## 通知值

通知值是每个任务内部维护的一个 **32 位无符号整数**。当调用 `xTaskNotifyGive()` 或 `xTaskNotify()` 时，可以根据不同的参数配置，对这个数值执行不同的操作，例如：
- **仅唤醒任务**，不改变通知值（例如使用 `eNoAction`）
- **将通知值加 1**（例如 `xTaskNotifyGive()` 或 `eIncrement`）
- **将通知值设置为特定数值**（例如 `eSetValueWithOverwrite` 或 `eSetValueWithoutOverwrite`）