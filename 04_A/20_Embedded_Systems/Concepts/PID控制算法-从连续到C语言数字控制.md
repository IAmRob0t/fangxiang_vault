---
title: PID控制算法-从连续到C语言数字控制
source: https://mp.weixin.qq.com/s/Pq3IJJkH5hwenErY0DFeoA
author:
  - "[[情报小哥]]"
published: 
created: 2025-03-25
description: 
tags:
  - clippings
  - c
  - PID
---
原创 情报小哥 *2025年03月09日 21:01* *广东*

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/mPZJgHsAnGAWeoz41JuwKXNhqm4CVcxbORco6KPnoTSqJul1Zo7icH8Yyib4FgWrnCBhpbQ2tYOUUf1gUg82Ig0Q/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

大家好，我是情报小哥~

今天总结了一下PID算法，从连续算法公式到离散数字化~

四周无人机悬停，平衡车保持直立姿态，热水器精准维持设定温度，背后都离不开 **PID控制算法这位大佬** 。

作为嵌入式开发中最经典的控制算法，PID凭借其简洁的结构和强大的适应性，成为工程师手中的“万能控制器”，小哥记得之前有个调查统计基本上PID能够解决90%的控制问题。那么本文将 **从数学原理到代码实现** ，带你彻底搞定PID的数字化实现方法，并玩起来。

---

### 0.1. 一、PID控制原理剖析

**PID = 比例（P） + 积分（I） + 微分（D）**  
• **比例项（P）** ：实时偏差的快速响应  
`输出 ∝ 当前误差` ，快速缩小偏差但可能引起震荡  
**公式** ： `P_out = Kp * e(t)`

• **积分项（I）** ：消除静态误差  
`输出 ∝ 误差累积量` ，消除系统稳态误差但可能引发超调  
**公式** ： `I_out = Ki * ∫e(t)dt`

• **微分项（D）** ：预测未来趋势  
`输出 ∝ 误差变化率` ，抑制超调但放大噪声  
**公式** ： `D_out = Kd * de(t)/dt`

**连续域公式** ：  
`u(t) = Kp*e(t) + Ki*∫e(t)dt + Kd*(de(t)/dt)`

---

### 0.2. 二、数字化改造：从连续到离散

在数字系统中，我们需将连续公式离散化。设采样周期为 **T** ，采用 **反向差分法** ：

1. **积分项离散化** ：  
	`∫e(t)dt ≈ T * Σe(k)`  
	累加历史误差： `sum_error += e(k)`
2. **微分项离散化** ：  
	`de(t)/dt ≈ [e(k) - e(k-1)] / T`

**离散PID公式（位置式）** ：  
`u(k) = Kp*e(k) + Ki*T*sum_error + Kd*[e(k)-e(k-1)]/T`

---

### 0.3. 三、C语言实现（基于STM32）

```
typedef struct {
    float Kp, Ki, Kd;   // PID参数
    float T;            // 采样周期
    float max_output;   // 输出限幅
    float integral;     // 积分累加量
    float last_error;   // 上次误差
} PID_Controller;

void PID_Init(PID_Controller *pid, float Kp, float Ki, float Kd, float T, float max_out) {
    pid->Kp = Kp;
    pid->Ki = Ki * T;  // 预乘采样周期
    pid->Kd = Kd / T;  // 预除采样周期
    pid->T = T;
    pid->max_output = max_out;
    pid->integral = 0;
    pid->last_error = 0;
}

float PID_Calculate(PID_Controller *pid, float setpoint, float feedback) {
    float error = setpoint - feedback;
    
    // 积分项（带限幅防饱和）
    pid->integral += error;
    if(pid->integral > pid->max_output) pid->integral = pid->max_output;
    elseif(pid->integral < -pid->max_output) pid->integral = -pid->max_output;

    // 微分项（可选：对微分项做低通滤波）
    float d_error = error - pid->last_error;
    
    // 计算输出
    float output = pid->Kp * error 
                 + pid->Ki * pid->integral 
                 + pid->Kd * d_error;
    
    // 输出限幅
    if(output > pid->max_output) output = pid->max_output;
    elseif(output < -pid->max_output) output = -pid->max_output;
    
    pid->last_error = error;
    return output;
}
```

---

### 0.4. 四、PID参数调试方法

**大部分盲调参口诀** ： **先调P，再调I，最后加D**

1. **试凑法** （适合简单系统,经验丰富一些的工程师直接上手调，基本能够调节到满意的效果)  
	• **P** ：从小到大增加，直到系统出现等幅振荡  
	• **I** ：适当加入，消除稳态误差  
	• **D** ：抑制超调，增强稳定性
2. **临界比例度法（Ziegler-Nichols，专业一点的会比较推荐这个方法）**  
	• 先置Ki=0, Kd=0，逐渐增大Kp至临界振荡点  
	• 记录临界增益Ku和振荡周期Tu  
	• 根据下表设置参数：
	| 控制类型 | Kp | Ki | Kd |
	| --- | --- | --- | --- |
	| P | 0.5\*Ku | 0 | 0 |
	| PI | 0.45\*Ku | 0.54\*Ku/Tu | 0 |
	| PID | 0.6\*Ku | 1.2\*Ku/Tu | 0.075 *Ku* Tu |
3. **经验参数范围** （对于大部分系统很多的参数比较比较相似）  
	• 温度控制：P(2-15), I(0.05-0.5), D(2-15)  
	• 电机控制：P(0.1-1), I(0.01-0.1), D(0-0.1)

**调试技巧** ：  
• 出现震荡：减小Kp或Kd  
• 响应慢：增大Kp  
• 稳态误差：增大Ki  
• 噪声敏感：减小Kd或加低通滤波

---

### 0.5. 五、需要注意的问题

1. **积分饱和** ：当误差持续存在时积分项过大  
	**解决方案** ：  
	• 积分限幅  
	• 积分分离（误差较大时停止积分）
2. **微分噪声** ：测量噪声导致控制量抖动  
	**解决方案** ：  
	• 对微分项做低通滤波
	```
	// 一阶低通滤波示例
	d_filter = 0.2*d_error + 0.8*d_filter;
	```

PID算法犹如控制领域的"乐高积木"，通过三个参数的巧妙组合即可应对大多数控制需求，非常的巧妙~

## 1. 最 后

小哥搜集了一些嵌入式学习资料，公众号内回复 **【 **1024** 】** 即可找到下载链接！

```
推荐好文  点击蓝色字体即可跳转☞ 专辑|Linux应用程序编程大全☞ 专辑|学点网络知识☞ 专辑|手撕C语言
☞ 专辑|手撕C++语言☞ 专辑|经验分享☞ 专辑|从单片机到Linux☞ 专辑|电能控制技术☞ 专辑|嵌入式必备数学知识 ☞  MCU进阶专辑 ☞  嵌入式C语言进阶专辑 ☞  经验分享
```

继续滑动看下一个

向上滑动看下一个 [知道了](https://mp.weixin.qq.com/s/) ： ， ， ， ， ， ， ， ， ， ， ， ， 。 视频 小程序 赞 ，轻点两下取消赞 在看 ，轻点两下取消在看 分享 留言 收藏 听过