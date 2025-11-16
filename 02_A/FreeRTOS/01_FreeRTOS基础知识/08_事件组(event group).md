---
tags:
  - freeRTOS
---
# 事件组概念与操作

## 事件组的概念

![[FreeRTOS完全开发手册之上册_快速入门.pdf#page=124&rect=73,530,523,636|FreeRTOS完全开发手册之上册_快速入门, p.124]]

## 事件组的操作

# 事件组函数

`EventGroupHandle_t`  结构体如下：

```c
typedef struct EventGroupDef_t
{
    EventBits_t uxEventBits;	//整数，每一 bit 代表一个事件
    List_t xTasksWaitingForBits; /*< List of tasks waiting for a bit to be set. */

    #if ( configUSE_TRACE_FACILITY == 1 )
        UBaseType_t uxEventGroupNumber;
    #endif

    #if ( ( configSUPPORT_STATIC_ALLOCATION == 1 ) && ( configSUPPORT_DYNAMIC_ALLOCATION == 1 ) )
        uint8_t ucStaticallyAllocated; /*< Set to pdTRUE if the event group is statically allocated to ensure no attempt is made to free the memory. */
    #endif
} EventGroup_t;
```

## 创建

有两种创建方法：动态分配内存、静态分配内存。函数原型如下：

```c
/* 创建一个事件组，返回它的句柄。
 * 此函数内部会分配事件组结构体
 * 返回值: 返回句柄，非NULL表示成功
 */
EventGroupHandle_t xEventGroupCreate( void );

/* 创建一个事件组，返回它的句柄。
 * 此函数无需动态分配内存，所以需要先有一个StaticEventGroup_t结构体，并传入它的指针
 * 返回值: 返回句柄，非NULL表示成功
 */ 
EventGroupHandle_t xEventGroupCreateStatic( StaticEventGroup_t * pxEventGroupBuffer );
```

## 删除

`vEventGroupDelete` 可以用来删除事件组，函数原型如下：

```c
/*
 * xEventGroup: 事件组句柄，你要删除哪个事件组
 */
void vEventGroupDelete( EventGroupHandle_t xEventGroup )
```

## 设置事件

( [[FreeRTOS完全开发手册之上册_快速入门.pdf#page=125&selection=24,0,35,27&color=note|📖]])
可以设置事件组的某个位、某些位，使用的函数有2个： 
- 在任务中使用 `xEventGroupSetBits()`
- 在ISR中使用 `xEventGroupSetBitsFromISR()`
	- `xEventGroupSetBitsFromISR()` **不会直接修改事件组的值**；
	- 它通过发送命令给 **Timer Service（守护任务）**；
	- 真正的修改和任务唤醒在 **任务上下文中** 完成；
	- 这样做的原因：
	    - 避免 ISR 中访问等待链表；
	    - 保证中断快速；
	    - 允许安全的任务调度。

## 等待事件

使用 `xEventGroupWaitBits` 来等待事件，可以等待某一位、某些位中的任意一个，也可以等待多位； 等到期望的事件后，还可以清除某些位。

( [[FreeRTOS完全开发手册之上册_快速入门.pdf#page=126&selection=55,0,55,7&color=note|📖]])
函数原型如下：

```c
EventBits_t xEventGroupWaitBits (
		EventGroupHandle_t xEventGroup,
		const EventBits_t uxBitsToWaitFor,
		const BaseType_t xClearOnExit,
		const BaseType_t xWaitForAllBits,
		TickType_t xTicksToWait
		);
```

|参数名称|作用|可选值示例|
|---|---|---|
| `xEventGroup` |​**​指定你要监听哪一块白板​**​。就像你要等朋友留言，得先确定是教室里的哪块白板。|通过 `xEventGroupCreate()` 创建的句柄|
| `uxBitsToWaitFor` |​**​指定你关心白板上的哪些特定位置​**​（哪些位）。可以用 `\|` 同时关注多个位。|例如 `BIT_0 \| BIT_4` 表示同时关注位 0 和位4|
| `xClearOnExit` |​**​决定看完留言后是否把这些留言擦掉​**​。| `pdTRUE`: 自动擦掉（避免重复处理）  <br>`pdFALSE`: 不擦（需手动调用 `xEventGroupClearBits`）|
| `xWaitForAllBits` |​**​决定等待的方式​**​：是要求所有关心的位置都有留言才行，还是只要有一个有留言就满足。| `pdTRUE`: 等待所有指定的位被设置（逻辑与）  <br>`pdFALSE`: 等待任意一个指定的位被设置（逻辑或）|
| `xTicksToWait` |​**​设定最多愿意等待多长时间​**​。单位是系统节拍 (ticks)，可以用 `pdMS_TO_TICKS()` 将毫秒转换为 ticks。| `0`: 不等待，立即返回  <br>`portMAX_DELAY`: 无限期等待（需配置 `INCLUDE_vTaskSuspend=1`）|

每个事件组 (`EventGroup_t`) 都维护着自己的等待任务链表 `xTasksWaitingForBits`，  
各事件组之间完全独立，互不干扰。

## 同步点

有一个事情需要多个任务协同，比如： 
- 任务 A：炒菜
- 任务 B：买酒
- 任务 C：摆台
- A、B、C 做好自己的事后，还要等别人做完；大家一起做完，才可开饭

使用 `xEventGroupSync ()` 函数可以同步多个任务：
- 可以设置某位、某些位，表示自己做了什么事
- 可以等待某位、某些位，表示要等等其他任务
- 期望的时间发生后， `xEventGroupSync ()` 才会成功返回。 
- `xEventGroupSync` **成功返回后，会清除事件**

( [[FreeRTOS完全开发手册之上册_快速入门.pdf#page=128&selection=98,0,100,7&color=note|📖]])
`xEventGroupSync` 函数原型如下：

```c
EventBits_t xEventGroupSync(
					EventGroupHandle_t xEventGroup,
					const EventBits_t uxBitsToSet,
					const EventBits_t uxBitsToWaitFor,
					TickType_t xTicksToWait
					);
```

---

> [!NOTE]
> ​​与 `xEventGroupWaitBits`的区别：​​ 另一个函数 `xEventGroupWaitBits`也有等待事件位的功能，但它是否清除等待的位是由你通过一个参数 (`xClearOnExit`) ​​手动选择​​的。而 `xEventGroupSync`​​强制​​在成功返回时清除等待的位，这是它实现“一次性同步”语义的关键。

# 示例 20: 等待多个事件

# 示例 21: 任务同步


本节程序：
* `21_freertos_example_event_group_task_sync`
* 就是参考书配套源码 `FreeRTOS_21_event_group_task_sync`

假设 ABC 三人要吃饭，各司其职：
* A：炒菜
* B：买酒
* C：摆台

三人都做完后，才可以开饭。  

`main` 函数代码如下，它创建了 3 个任务：

```c
int main( void )
{
	prvSetupHardware();
	
    /* 创建递归锁 */
    xEventGroup = xEventGroupCreate( );

	if( xEventGroup != NULL )
	{
		/* 创建3个任务: 洗菜/生火/炒菜
		 */
		xTaskCreate( vCookingTask, "task1", 1000, "A", 1, NULL );
		xTaskCreate( vBuyingTask,  "task2", 1000, "B", 2, NULL );
		xTaskCreate( vTableTask,   "task3", 1000, "C", 3, NULL );

		/* 启动调度器 */
		vTaskStartScheduler();
	}
	else
	{
		/* 无法创建事件组 */
	}

	/* 如果程序运行到了这里就表示出错了, 一般是内存不足 */
	return 0;
}
```

被创建的 3 个任务，代码都很类似，以任务 1 为例：

```c
static void vCookingTask( void *pvParameters )
{
	const TickType_t xTicksToWait = pdMS_TO_TICKS( 100UL );		
	int i = 0;
	
	/* 无限循环 */
	for( ;; )
	{
		/* 做自己的事 */
		printf("%s is cooking %d time....\r\n", (char *)pvParameters, i);
		
		/* 表示我做好了, 还要等别人都做好 */
		xEventGroupSync(xEventGroup, COOKING, ALL, portMAX_DELAY);
	
		/* 别人也做好了, 开饭 */
		printf("%s is eating %d time....\r\n", (char *)pvParameters, i++);
		vTaskDelay(xTicksToWait);
	}
}
```

要点在于 `xEventGroupSync` 函数，它有 3 个功能：
- 设置事件：表示自己完成了某个、某些事件
- 等待事件：跟别的任务同步
- 成功返回后，清除"等待的事件"

# 事件组的内部实现

> [!question] 为什么只需要关闭调度器，不需要关中断？
> 队列是因为在 ISR 中可以进行调用所以才进行关中断的操作，而事件组不会在 ISR 中使用，所以不需要关中断
