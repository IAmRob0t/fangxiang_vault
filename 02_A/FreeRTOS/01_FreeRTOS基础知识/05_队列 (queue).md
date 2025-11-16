---
tags:
  - freeRTOS
---
**队列 = 环形缓冲 + 发送/接收等待列表**：用于任务间通信，发送到满队列或从空队列接收时任务会阻塞并加入等待列表，满足条件由调度器唤醒。

**要点**：条目为固定大小并被**拷贝**入队；有 `...FromISR` 接口、超时阻塞、队列集合等扩展；**优先级继承由 mutex 提供，队列不负责**。
 
# 队列的特性

本节源码：`13_freertos_example_queue`，基于 `12_freertos_example_sync_exclusion` 修改。

## 常规特性

队列的简化操如入下图所示，从此图可知：
- 队列可以包含若干个数据：队列中有若干项，这被称为"长度"(length)
- 每个数据大小固定
- 创建队列时就要指定长度、数据大小
- 数据的操作采用先进先出的方法 (FIFO, First In First Out)：写数据时放到尾部，读数据时从头部读
- 也可以强制写队列头部：覆盖头部数据

![[FreeRTOS完全开发手册之上册_快速入门.pdf#page=71&rect=63,509,532,625|FreeRTOS完全开发手册之上册_快速入门, p.71]]

![[FreeRTOS完全开发手册之上册_快速入门.pdf#page=72&rect=74,245,522,816|FreeRTOS完全开发手册之上册_快速入门, p.72]]

## 传输数据的两种方法

- 拷贝：把数据、把变量的值复制进队列里
- 引用：把数据、把变量的地址复制进队列里

FreeRTOS 使用拷贝值的方法很简单：
- 局部变量的值可以发送到队列中，后续即使函数退出、局部变量被回收，也不会影响队列中的数据
- 无需分配buffer来保存数据，队列中有buffer
- 局部变量可以马上再次使用
- 发送任务、接收任务解耦：接收任务不需要知道这数据是谁的、也不需要发送任务来释放数据
- 如果数据实在太大，你还是可以使用队列传输它的地址
- 队列的空间有FreeRTOS内核分配，无需任务操心
- 对于有内存保护功能的系统，如果队列使用引用方法，也就是使用地址，必须确保双方任务对这个地址都有访问权限。使用拷贝方法时，则无此限制。

## 队列的阻塞访问

FreeRTOS 中阻塞式读队列让任务进入“休眠/阻塞”状态，相比裸机轮询是一个巨大的优势。

# 队列函数

使用队列的流程：创建队列、写队列、读队列、删除队列。

## 创建

- 动态分配内存：`xQueueCreate`，队列的内存在函数内部动态分配，函数原型如下：

```c
QueueHandle_t xQueueCreate( UBaseType_t uxQueueLength, UBaseType_t uxItemSize );
```

![[FreeRTOS完全开发手册之上册_快速入门.pdf#page=74&rect=78,489,519,602|FreeRTOS完全开发手册之上册_快速入门, p.74]]

---

- 静态分配内存：`xQueueCreateStatic`，队列的内存要事先分配好函数原型如下：

```c
QueueHandle_t xQueueCreateStatic(
							UBaseType_t uxQueueLength, 
							UBaseType_t uxItemSize, 
							uint8_t *pucQueueStorageBuffer, 
							StaticQueue_t *pxQueueBuffer 
						);
```

![[FreeRTOS完全开发手册之上册_快速入门.pdf#page=74&rect=78,106,519,301|FreeRTOS完全开发手册之上册_快速入门, p.74]]

## 复位

( [[FreeRTOS完全开发手册之上册_快速入门.pdf#page=75&selection=4,0,9,5&color=note|📖]])
队列刚被创建时，里面没有数据；使用过程中可以调用 xQueueReset() 把队列恢复为初始状态，此函数原型为：

## 删除

( [[FreeRTOS完全开发手册之上册_快速入门.pdf#page=75&selection=15,0,19,29&color=note|📖]])
删除队列的函数为 vQueueDelete() ，只能删除使用动态方法创建的队列，它会释放内存。原型如下：

## 写队列

可以把数据写到队列头部，也可以写到尾部，这些函数有两个版本：在任务中使用、在ISR中使用。函数原型如下：( [[FreeRTOS完全开发手册之上册_快速入门.pdf#page=75&selection=27,4,28,6&color=note|📖]])

```c
/* 等同于xQueueSendToBack
 * 往队列尾部写入数据，如果没有空间，阻塞时间为xTicksToWait
 */
BaseType_t xQueueSend(
						QueueHandle_t xQueue,
						const void *pvItemToQueue,
						TickType_t xTicksToWait
					 );

/* 往队列尾部写入数据，如果没有空间，阻塞时间为xTicksToWait
 */
BaseType_t  xQueueSendToBack(
								QueueHandle_t xQueue,
								const void *pvItemToQueue,
								TickType_t xTicksToWait
							);
```

这些函数用到的参数是类似的，统一说明如下：

| 参数              | 说明                                                                                                                          |
| --------------- | --------------------------------------------------------------------------------------------------------------------------- |
| `xQueue`        | 队列句柄，要写哪个队列                                                                                                                 |
| `pvItemToQueue` | 数据指针，这个数据的值会被复制进队列，复制多大的数据？在创建队列时已经指定了数据大小                                                                                  |
| `xTicksToWait`  | 如果队列满则无法写入新数据，可以让任务进入阻塞状态， `xTicksToWait` 表示阻塞的最大时间(Tick Count)。如果被设为 0，无法写入数据时函数会立刻返回； 如果被设为 `portMAX_DELAY`，则会一直阻塞直到有空间可写 |
| 返回值             | `pdPASS`：数据成功写入了队列<br>`errQUEUE_FULL`：写入失败，因为队列满了。                                                                          |

写队列的内部操作：
1. 存入数据
2. 唤醒"等待数据的任务"
3. 如果被唤醒的任务优先级比当前更高，**直接调度**

## 读队列

使用 `xQueueReceive()` 函数读队列，读到一个数据后，队列中该数据会被移除。这个函数有两个版本：在任务中使用、在 ISR 中使用。函数原型如下：

```c
BaseType_t xQueueReceive(
						QueueHandle_t xQueue,
						void * const pvBuffer,
						TickType_t xTicksToWait );

BaseType_t xQueueReceiveFromISR(
						QueueHandle_t xQueue,
						void *pvBuffer,
						BaseType_t *pxTaskWoken );

```

参数说明如下：

![[FreeRTOS完全开发手册之上册_快速入门.pdf#page=77&rect=77,133,519,333&color=note|📖]]

---

Task2、Task3 同时调用 `xQueneReceive()` ：会有一个先关中断，所以无法同时执行

两个任务可以同时“要求”从队列取数据，但队列内部“取数据”的这个核心动作是绝对不允许同时进行的。FreeRTOS通过一个叫“临界区”的机制（本质上是短暂地关闭中断或停止任务调度）来保证这一点，让这些操作像排队一样，一个一个地顺序完成，从而确保数据不会出错。​

## 查询

可以查询队列中有多少个数据、有多少空余空间。函数原型如下：

```c
/*
 * 返回队列中可用数据的个数
 */
UBaseType_t uxQueueMessagesWaiting( const QueueHandle_t xQueue );

/*
 * 返回队列中可用空间的个数
 */
UBaseType_t uxQueueSpacesAvailable( const QueueHandle_t xQueue );
```

## 覆盖/偷看

当队列长度为 1 时，可以使用 `xQueueOverwrite()` 或 `xQueueOverwriteFromISR()` 来覆盖数据。注意，队列长度必须为 1。当队列满时，这些函数会覆盖里面的数据，这也以为着这些函数不会被阻塞。

函数原型如下：

( [[FreeRTOS完全开发手册之上册_快速入门.pdf#page=78&selection=21,0,21,7&color=note|📖]])

```c

```

# 示例 8: 队列的基本使用

( [[FreeRTOS完全开发手册之上册_快速入门.pdf#page=80&selection=12,0,16,6&color=note|📖]])
本程序会创建一个队列，然后创建2个发送任务、1个接收任务：

# 示例 9: 分辨数据源

( [[FreeRTOS完全开发手册之上册_快速入门.pdf#page=83&selection=12,0,12,34&color=note|📖]])
当有多个发送任务，通过同一个队列发出数据，接收任务如何分辨数据来源？

# 示例 10: 传输大块数据

( [[FreeRTOS完全开发手册之上册_快速入门.pdf#page=88&selection=24,0,31,7&color=note|📖]])
如果要传输1000字节的结构体呢？写队列时拷贝1000字节，读队列时再拷贝1000字节？不建议这么做，影响效率！

# 示例 11: 邮箱 (Mailbox)

( [[FreeRTOS完全开发手册之上册_快速入门.pdf#page=91&selection=14,0,44,41&color=note|📖]])
FreeRTOS的邮箱概念跟别的RTOS不一样，这里的邮箱称为"橱窗"也许更恰当：
- 它是一个队列，队列长度只有1 
- 写邮箱：新数据覆盖旧数据，在任务中使用 `xQueueOverwrite()` ，在中断中使用 `xQueueOverwriteFromISR()` 。
  既然是覆盖，那么无论邮箱中是否有数据，这些函数总能成功写入数据。
- 读邮箱：读数据时，数据不会被移除；在任务中使用 `xQueuePeek()` ，在中断中使用 `xQueuePeekFromISR()` 。
  这意味着，第一次调用时会因为无数据而阻塞，一旦曾经写入数据，以后读邮箱时总能成功。

# 队列集

本节源码：`14_freertos_example_queue_set`

---

假设你的电脑支持鼠标、键盘、触摸屏，就需要多个队列

1. 创建一个队列集（实质上也是一个队列）
	- 要检测 3 个队列 A、B、C
	- 队列集的长度是：队列 A 的长度 + 队列 B 的长度 + 队列 C 的长度
	- 否则在 A、B、C 都满的情况下，队列集没有空间存放所有的 handle
2. `mouse_Queue_handle`、`key_Queue_handle` 、`touch_Queue_handle` 的某个成员会指向队列集，此时三个 handle 并没有数据，并不会放到队列集中，只不过是建立了一个联系
3. touch => touch Queue => Queue Set
4. Read Queue Set 返回 Queue（一次）
5. Read Queue（一次）
	- 第 4 步和第 5 步时一一对应的，首先要读 Queue Set，返回 Queue ，就要读一次 Queue

```c
xQueueCreateSet()

xQueueAddToSet(xQueueHandle1, xQueueSet);
xQueueAddToSet(xQueueHandle2, xQueueSet);
.
.
.
void Task3Function(void * param)
{
	QueueSetMemberHandle_t handle;
	int i;
	while (1)
	{
		/* 1. read queue set: which queue has data */
		handle = xQueueSelectFromSet(xQueueSet, portMAX_DELAY);

		/* 2. read queue */
		xQueueReceive(handle, &i, 0);	//能执行到这里表明一定有数据，所以无需等待

		/* 3. print */
		printf("get data : %d\r\n", i);
	}
}
```

# FreeRTOS 队列的内部实现

队列主要由三个部分组成，这些部分让它既能存储数据，又能处理等待，还能防止出错。
- **环形缓冲区（Ring Buffer）**
    - 存放实际的数据
    - 用“读指针”和“写指针”来管理数据：写的时候放进去，读的时候取出来。这些指针像时钟一样循环走（到头就从开始重来），确保数据按“先进先出”（FIFO，先放的先取）的顺序处理。
- **等待任务的链表（像一个等候名单）**
    - 当队列空了（没数据），想读数据的任务会在这里“排队等待”。
    - 当队列满了（放不下了），想写数据的任务也会在这里等待。
    - 好消息是：当有人写数据或读数据时，系统会自动“叫醒”这些等待的任务，不需要你手动去管。
- **安全保护机制（像门锁和警卫，防止混乱）**
    - 为了避免多个任务或中断（突发事件）同时乱改数据，FreeRTOS 用“关中断”（暂时停掉突发事件）和“挂起调度器”（暂停任务切换）来保护关键部分。
    - 这确保了在多任务环境下，不会出现“竞态条件”（大家抢着改数据导致出错）。

## 队列怎么存储数据？——环形缓冲区

环形缓冲区是队列的“仓库”，专门用来放数据元素。它的设计像一个圆圈：当指针走到尽头，就跳回起点，继续使用空间。这样就能高效地实现“先进先出”——最早放进去的数据最早被取出来。

队列的总内存占用 = 队列的控制结构（叫 `Queue_t`，像一个管理表格） + 缓冲区的实际大小（取决于你创建队列时设定的容量和每个数据的大小）。

## 队列怎么处理等待？——链表的唤醒机制

FreeRTOS 的队列很聪明，它内置了“同步机制”（让任务协调工作的办法），不需要你额外写代码去管理锁或信号。核心是用链表（像一个列表）来记录等待的任务。

- 当你写数据到队列或从队列读数据时，系统会自动检查并唤醒（激活）那些因为队列满或空而等待的任务。
- 相比“裸机”（没有操作系统的简单程序）里不停轮询（反复检查队列有没有数据），阻塞式（等待模式）读队列有这些好处：
    - 节省 CPU 时间：任务睡着了，不用一直忙着检查。
    - 降低功耗：尤其在电池设备上，CPU 可以休息。
    - 代码更简单：你不用写循环检查，FreeRTOS 帮你处理。

这里有两个重要的链表（列表）：

| 链表名称                  | 它做什么？ |
|---------------------------|------------|
| `xTasksWaitingToSend`    | 当队列满了，记录那些想发送（写）数据但得等待的任务。 |
| `xTasksWaitingToReceive` | 当队列空了，记录那些想接收（读）数据但得等待的任务。 |

这些链表其实是“事件列表”，任务被加进去时，会根据等待时间放到内核的延迟列表或阻塞列表中。当条件满足（比如队列不空了），最高优先级的等待任务会先被唤醒，可能切换到它运行。

## 队列怎么确保安全访问？——关中断和调度器挂起

队列在多任务或有中断的环境下工作，所以需要保护机制，防止数据被乱改。FreeRTOS 用两种办法，像双重保险。

- **挂起调度器**（用 `vTaskSuspendAll` 和 `xTaskResumeAll` 函数）
    - 当任务调用 `xQueueSend()`（发送）或 `xQueueReceive()`（接收）时，如果需要等待（阻塞），FreeRTOS 会暂时挂起调度器。这意味着禁止其他任务切换进来，防止它们干扰队列。
    - 注意：这只在真正需要阻塞的时候用，不是每次操作都挂起。快速操作（队列有空间或数据）就不需要。
- **短时间关中断**（用 `portENTER_CRITICAL` 和 `portEXIT_CRITICAL` 函数）
    - 在更新队列的关键信息（如读写指针或数据计数）时，FreeRTOS 会短暂关闭中断（突发事件处理器）。这创造了一个“临界区”（不能被打断的区域）。
    - 这个关中断的时间超级短——通常就几条指令，更新几个字节而已，不会影响系统响应。

为什么需要两层保护？
- 挂起调度器：只防任务切换，但中断（ISR，中断服务程序）还能发生，可能改动数据。
- 短时间关中断：加一层，彻底保护那些必须一次性完成的微小操作（比如改指针），确保原子性（不可分割）。

这样组合，就能安全处理任务和中断的访问。额外提示：如果从中断里操作队列（用 `FromISR` 函数），就不挂起调度器，只用临界区。

## 读队列流程

![[读、写队列流程.canvas|读、写队列流程]]