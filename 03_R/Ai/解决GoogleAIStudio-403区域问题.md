---
source: https://blog.csdn.net/m0_74916313/article/details/152078469
author:
  - 被巨款砸中
published: 2025-09-25
created: 2025-11-20
description: "解决 Google AI Studio(Gemini) 403 问题，您不在支持的区域，Failed to list models: permission denied.Please try again._如果您在尝试打开 google ai studio 后看到此页面,可能是因为 google ai studio"
tags:
  - clippings
  - AI
  - Google
  - Gemini
  - Troubleshooting
---

# 解决 Google AI Studio 403 “您不在支持的区域”问题

## 1. 问题背景

当访问 Google AI Studio 时，可能会遇到 403 错误，提示“您不在支持的区域” (Failed to list models: permission denied)。

![](https://i-blog.csdnimg.cn/img_convert/391d98e5aa711b8d87838499efd98e10.png)

根据 [Google 官方文档](https://ai.google.dev/gemini-api/docs/troubleshoot-ai-studio?hl=zh-cn#understand-403-errors)，这是因为您的 IP 地址被 Google 标记到了不支持的区域。此时，使用 [Google 地图](https://www.google.com/maps/) 或 [WhereAmI](https://www.where-am-i.co/my-ip-location) 等工具检查定位，可能会发现定位在一个非预期的位置（例如公海）。

![](https://i-blog.csdnimg.cn/img_convert/b3c90ad9bb2cc4695741281065202265.png)

## 2. 核心思路

解决方案的核心是**伪造浏览器地理位置，并同步更新至 Google 账户**。单纯更换代理 IP 地址可能效果不明显。

## 3. 操作步骤

### 第一步：安装浏览器插件和脚本

1.  **安装 Tampermonkey**：这是一个用户脚本管理器，如果您的浏览器尚未安装，请先安装。
    
    ![](https://i-blog.csdnimg.cn/img_convert/e0538ab35f59f20e306f3db5629e1293.png)
    
2.  **安装 Location Guard Ng**：这是一个 Tampermonkey 脚本，用于伪造浏览器地理位置。
    -   **脚本地址**：[SukkaW/location-guard-ng on GitHub](https://github.com/SukkaW/location-guard-ng)
    -   在页面中找到并点击安装。
    
    ![](https://i-blog.csdnimg.cn/img_convert/6646aa82b1b2225c277e11ae15d59ba0.png)

### 第二步：配置固定定位

1.  打开 Location Guard Ng 的配置页面：[options page](https://location-guard-ng.skk.moe/options)。
2.  选择 **Fixed Location**，在地图上将您的位置设置到期望的国家/地区（建议与您的代理工具/VPN 节点位置保持一致，例如美国）。
    
    ![](https://i-blog.csdnimg.cn/img_convert/53cfdac96dcd03877eacbf0427e1751a.png)

### 第三步：检查定位是否生效

使用以下任一工具，检查浏览器报告的地理位置是否已成功修改：

1.  **WhereAmI**：[where-am-i.co](https://www.where-am-i.co/my-ip-location)
    
    ![](https://i-blog.csdnimg.cn/img_convert/1ac8931f4746bb5e653e82976bfd1adb.png)
    
2.  **Google 地图**：[google.com/maps](https://www.google.com/maps/)，在搜索框输入 `where am i`。
    
    ![](https://i-blog.csdnimg.cn/img_convert/b92fb2572f018ca774497bcb99b731e3.png)

### 第四步：更新 Google 搜索位置

1.  在 Google 浏览器中搜索任意内容。
2.  将页面滚动到最底部，检查显示的地区是否已更新。
3.  如果地区不正确，点击 **“更新位置信息”**。

![](https://i-blog.csdnimg.cn/img_convert/97880dda52b9cd706a4c0d6987e03d9c.png)

### 第五步：（可选）向 Google 发送反馈

如果上述步骤未能更新您的位置，可以尝试向 Google 反馈。

1.  在搜索结果页底部，点击 **“发送反馈”**。
    
    ![](https://i-blog.csdnimg.cn/img_convert/6feb5b5af7cc08effbcd1d01a32ce13a.png)
    
2.  用英文说明您的实际所在地（例如，您正在使用位于洛杉矶的服务器），并指出之前的 IP 定位不准确。根据经验，Google 可能会在一到两天内修正。

## 4. 注意事项

-   操作需要您的 **Google 账户已通过年龄验证**（年满18周岁）。
-   您可能需要上传身份证件以完成验证。
    
    ![](https://i-blog.csdnimg.cn/img_convert/91e433dcc00f1428bc0600fc1d645398.png)