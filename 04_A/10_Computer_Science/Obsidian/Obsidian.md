---
tags:
  - Obsidian
---
# Obsidian 核心插件



# Obsidian 插件

## 1. Dataview

**[[01_Overview]]**

## 2. Keep the Rhythm

用热力图可视化每日字数。

## 3. Note Definitions
## 4. PDF++

原本 `Quote` 选项里的文本如下：

```
> ({{linkWithDisplay}})
> {{selection}}
```

## 5. Keyboard Analyzer

快捷键热点图

## 6. File Tree Alternative Plugin：文件计数
## 7. Hover Editor：浮动式编辑窗格
### 7.1. 编辑器小窗格使用要点
6.  滑鼠游标悬停在内部链接一会（依设定可能要按着〔Ctrl/Cmd〕并悬停）即会弹出编辑器小窗格
7.  将滑鼠游标移到小窗格顶端，当游标变成移动形状时可拖拉窗格到其他位置
8.  拖拉操作可自动钉选(Pin)小窗格在Obsidian上方
9.  也可点击左上角的钉选图示直接钉选窗格在上方
10.  小窗格边框可拖拉变更视窗大小
11.  双击顶端可收合/展开视窗,

> Clipped from [[Obs＃77] 浮动式编辑窗格：Hover Editor – 简睿随笔](http://jdev.tw/blog/7043) at 2025-02-06.

## 8. Lapel：标题等级

当我们能很容易的看到标题等级，可以很轻易的决定新的标题的等级。

最简单的方法是安装并启用Lapel外挂（Live Preview）。点击Lapel显示的H1～H6，能选择变更标题等级。

[# [Obs＃86] 分享与编辑器相关的21个Obsidian插件 - YouTube](https://www.youtube.com/watch?v=Bh46zC5wUQo&list=PLWg9zacwOnwfcpVm5pAKgOHms7PntsgJS&index=86)

## 9. Number Headings：标题编号

安装并启用 Number Headings 外挂，可自动做标题编号。

### 9.1. 外挂选项

以下是常用的选项：

| 选项                            | 说明                                                     |
| ----------------------------- | ------------------------------------------------------ |
| Skip top level heading        | 是否略过一级标题；若一级标题是笔记名称时应勾选                                |
| Style for level 1 heading     | 1或A，一级标题用数字或字母编号                                       |
| Style for lower level heading | 1或A，二级～六级标题用数字或字母编号                                    |
| Automatically numbering       | 自动编号，输入# 后自动编号                                         |
| Seperator style               | 有点(dot)、减号(dash)、冒号(colon)等三种，数字间的分隔符号                 |
| Table of contents Anchor      | 要插入静态目录的定位符号，例如使用「^toc」，在要插入位置上的标题结尾加上定位符号，就能在下一行插入目录。 |

[[Obs＃87] 章节标题自动编号与设定编号形式的Obsidian插件：Number Headings - YouTube](https://www.youtube.com/watch?v=2grpw5KNnqA&list=PLWg9zacwOnwfcpVm5pAKgOHms7PntsgJS&index=87)

## 10. Creases：标题折叠

[[Obs＃94] 关於标题摺叠的大小事：用Creases控制不同级别标题的摺叠状态 - YouTube](https://www.youtube.com/watch?v=Mj2ko8jx5Mg&list=PLWg9zacwOnwfcpVm5pAKgOHms7PntsgJS&index=94)

用不了？

# 浏览器插件
## 1. 搜集资料利器：TabCopy
## 2. 网页撷取工具：Obsidian Web Clipper

### 2.1. 模板设定

撷取的内容可以指定套用需要的模板。预设的Default模板主要设置了6 个Property，本体内容(Note content)是`{{content}}`。  
笔记存放位置在模板的【Note location】栏位设定。

![gh|593](https://raw.githubusercontent.com/emisjerry/upgit/master/2024/173241742700058bnir.png)

因为我的笔记都是用Heading 1当做标题和档名，因此我自订了新的模板，修改了Note content:

![gh](https://raw.githubusercontent.com/emisjerry/upgit/master/2024/173241775900006fsgu.png)

### 2.2. 模板变数

点击扩充右上角的【•••】 就能查看所有模板变数，这些变数能使用在YAML的特性与笔记本体内容。

> 参考: [https://help.obsidian.md/web-clipper/variables](https://help.obsidian.md/web-clipper/variables)

- authhor: 网页作者
- content: 网页内容
- contentHtml: 网页内容(HTML格式)
- fullHtml: 未处理过的网页内容(HTML格式)
- date: 撷取日期
- time: 撷取日期待+时间
- description: 网页描述
- domain: 网页的网域
- image: 分享用的图片网址
- published: 发布日期，应该是Obsidian Publish服务要使用的
- site: 网站名称(似乎就是title 的值)
- title: 网页的标题
- url: 网页的网址
- highlights: 网页标示为高亮的内容
- meta...: 网页head区内的meta data(诠释资料，后设资料，元资料)
- 其他请参考[web-clipper variables](https://help.obsidian.md/web-clipper/variables)

变数里能再使用过滤器（filters），格式是`{{variable|filter}}`，请参考[web-clipper filters](https://help.obsidian.md/web-clipper/filters)。

![gh](https://raw.githubusercontent.com/emisjerry/upgit/master/2024/1731503958000kfkoqq.png)

### 2.3. Highlighter 高亮功能

除了整页的撷取，也可启用高亮功能，启用后撷取的选取文字会变成Note content，Add to Obsidian点击后只存入高亮部份。日后再浏览此网页时，高亮部份会自动呈现。

![gh](https://raw.githubusercontent.com/emisjerry/upgit/master/2024/1732417878000biijo2.png)

![gh|700](https://raw.githubusercontent.com/emisjerry/upgit/master/2024/1731470937000mmkaew.png)

# 功能实现
## 1. Iframe 测试
### 1.1. Google 表格
### 1.2. Youtube 影片
### 1.3. Google 日历
### 1.4. 天气预报
[Windy: 风图及天气预报](https://www.windy.com/?25.040,121.469,5)

# 未看

## 1. 简睿学堂

[[Obs#5] Obsidian(黑曜石) 高亮度显示或变更文字顏色的3种方法 (CC字幕) - YouTube](https://www.youtube.com/watch?v=994nPrmkXIA&list=PLWg9zacwOnwfcpVm5pAKgOHms7PntsgJS&index=5)
[[Obs#13] 快速開啟Obsidian筆記的方法：快速切換對話窗與obsidian:// URI 命令行 - YouTube](https://www.youtube.com/watch?v=uQTC3WWVvX8&list=PLWg9zacwOnwfcpVm5pAKgOHms7PntsgJS&index=13)
==[[Obs#15] 在筆記裡複製、使用obsidian網址與工作空間(Workspace)的使用 - YouTube](https://www.youtube.com/watch?v=Uv6AZNxv12k&list=PLWg9zacwOnwfcpVm5pAKgOHms7PntsgJS&index=15)==
==[[Obs#16] 使用Obsidian區塊代碼以快速跳轉位置的方法 - YouTube](https://www.youtube.com/watch?v=r7WbgQeZnk4&list=PLWg9zacwOnwfcpVm5pAKgOHms7PntsgJS&index=16)==
[[Obs＃23] 更有彈性的Obsidian整合Anki外掛：Obsidian_to_Anki (CC字幕) - YouTube](https://www.youtube.com/watch?v=nUAVySf-2Dk&list=PLWg9zacwOnwfcpVm5pAKgOHms7PntsgJS&index=23)

[[Obs＃42] Obsidian Buttons外掛 0.4.5 新功能 - YouTube](https://www.youtube.com/watch?v=KWDaK9TyFfE&list=PLWg9zacwOnwfcpVm5pAKgOHms7PntsgJS&index=42)
[[Obs＃46] 笔记整理─找出孤儿(Orphans)和缺少标籤的笔记的 4 个方法 - YouTube](https://www.youtube.com/watch?v=xqyx3LGzVEo&list=PLWg9zacwOnwfcpVm5pAKgOHms7PntsgJS&index=46)
[[Obs＃47] 用Command Alias（命令别名）快速操作命令面板 - YouTube](https://www.youtube.com/watch?v=8-WWw7loeQw&list=PLWg9zacwOnwfcpVm5pAKgOHms7PntsgJS&index=47)
[[Obs＃48] 动态目录外挂：快速生成笔记的章节目录 - YouTube](https://www.youtube.com/watch?v=TmTLQ_ec3k4&list=PLWg9zacwOnwfcpVm5pAKgOHms7PntsgJS&index=48)
[[Obs＃50] QuickAdd全攻略(一)：改变工作流程的超强外掛 - YouTube](https://www.youtube.com/watch?v=78pBTF0CObI&list=PLWg9zacwOnwfcpVm5pAKgOHms7PntsgJS&index=51)
[[Obs＃51] QuickAdd全攻略(2)：脚本撰写与宏使用要点 - YouTube](https://www.youtube.com/watch?v=yo_2ZGnv2_Y&list=PLWg9zacwOnwfcpVm5pAKgOHms7PntsgJS&index=51)
[[Obs＃53] 文字运输车：透过书籤在不同笔记之间搬运文字 - YouTube](https://www.youtube.com/watch?v=pxhcXuIV6jM&list=PLWg9zacwOnwfcpVm5pAKgOHms7PntsgJS&index=53)

[[Obs＃55] 建立新笔记的模板设定－Calendar, Templater与QuickAdd - YouTube](https://www.youtube.com/watch?v=-KlpwM9XfGA&list=PLWg9zacwOnwfcpVm5pAKgOHms7PntsgJS&index=55)
[[Obs＃56] 快速新增灵感／闪念笔记(Fleeting Note)的 3 种方法 - YouTube](https://www.youtube.com/watch?v=c69rpaaAyEM&list=PLWg9zacwOnwfcpVm5pAKgOHms7PntsgJS&index=56)
[[Obs＃58] 快速开启常用笔记的方法 - YouTube](https://www.youtube.com/watch?v=fGFqbafNcw0&list=PLWg9zacwOnwfcpVm5pAKgOHms7PntsgJS&index=58)
[[Obs＃59] Obsidian快速开啟常用笔记（2）：不使用外掛的简单方法 - YouTube](https://www.youtube.com/watch?v=idGh3eqQBHY&list=PLWg9zacwOnwfcpVm5pAKgOHms7PntsgJS&index=59)
[[Obs＃60] 用Obsidian管理瀏览器书籤的尝试 - YouTube](https://www.youtube.com/watch?v=TdzrCuW5I9Y&list=PLWg9zacwOnwfcpVm5pAKgOHms7PntsgJS&index=60)
[[Obs＃62] Obsidian搜寻全攻略 - YouTube](https://www.youtube.com/watch?v=NheSnDUZDjM&list=PLWg9zacwOnwfcpVm5pAKgOHms7PntsgJS&index=62)
[[Obs＃63] 将Chrome瀏览器书籤匯出成Markdown的方法 - YouTube](https://www.youtube.com/watch?v=KTT3RR0wGCU&list=PLWg9zacwOnwfcpVm5pAKgOHms7PntsgJS&index=63)
[[Obs＃64] Ebullientworks轻量主题－使用Style Settings设定 - YouTube](https://www.youtube.com/watch?v=AtibeL0tceo&list=PLWg9zacwOnwfcpVm5pAKgOHms7PntsgJS&index=64)
[[Obs＃65] Obsidian exporter：将储存库匯出成标準Markdown格式 - YouTube](https://www.youtube.com/watch?v=LOusoBlYuOc&list=PLWg9zacwOnwfcpVm5pAKgOHms7PntsgJS&index=65)
[[Obs＃66] 自动维护Markdown相容性的外掛：obsidian-consistent-attachments-and-links - YouTube](https://www.youtube.com/watch?v=C06k96_vQbk&list=PLWg9zacwOnwfcpVm5pAKgOHms7PntsgJS&index=66)
[[Obs＃68] 利用QuickAdd巨集由IMDB建立影片档案，用Minimal主题显示成卡片 - YouTube](https://www.youtube.com/watch?v=NkLs97knSjA&list=PLWg9zacwOnwfcpVm5pAKgOHms7PntsgJS&index=68)
[[Obs＃69] 由豆瓣建立Minimal样式主题的阅读书单卡片 - YouTube](https://www.youtube.com/watch?v=1gKMQhxYYlA&list=PLWg9zacwOnwfcpVm5pAKgOHms7PntsgJS&index=69)
[[Obs＃71] 新手适用的多功能模板外掛：From Template - YouTube](https://www.youtube.com/watch?v=pzA66MwozsY&list=PLWg9zacwOnwfcpVm5pAKgOHms7PntsgJS&index=71)
[[Obs＃72] Step by Step 用From Template建立笔记实例操作 - YouTube](https://www.youtube.com/watch?v=CdxABcKYdts&list=PLWg9zacwOnwfcpVm5pAKgOHms7PntsgJS&index=72)
[[Obs＃74] 和外掛相关的外掛─BRAT: 抢先体验未上架外掛；Settings Search: 加速搜寻外掛设定 - YouTube](https://www.youtube.com/watch?v=WjZPA2mq0tk&list=PLWg9zacwOnwfcpVm5pAKgOHms7PntsgJS&index=74)
[[Obs＃76] (Spotlight/Alfred, Launchy)-like：Key Sequence Shortcut, Obsidian的快速命令啟动器 - YouTube](https://www.youtube.com/watch?v=kJg3agf4n2k&list=PLWg9zacwOnwfcpVm5pAKgOHms7PntsgJS&index=76)

==[[Obs＃82] 用Obsidian学会Markdown--Markdown完整解析 - YouTube](https://www.youtube.com/watch?v=lnsQsFCYhNc&list=PLWg9zacwOnwfcpVm5pAKgOHms7PntsgJS&index=82)==
[[Obs＃83] 多栏式Callouts! 直接套用CSS片段变身N栏～ - YouTube](https://www.youtube.com/watch?v=sEogbW4UGYo&list=PLWg9zacwOnwfcpVm5pAKgOHms7PntsgJS&index=83)
[[Obs＃84] 另一个更简便的笔记多栏作法：使用Columns外挂 - YouTube](https://www.youtube.com/watch?v=3w3hpCisw5w&list=PLWg9zacwOnwfcpVm5pAKgOHms7PntsgJS&index=84)
[[Obs＃89] QuickAdd巨集快速开啟设定视窗-Step by step；直接使用window.open - YouTube](https://www.youtube.com/watch?v=g-rtSlHao0g&list=PLWg9zacwOnwfcpVm5pAKgOHms7PntsgJS&index=89)
[[Obs＃90] Callouts扩充：CalloutTypesetting CSS Snippet - YouTube](https://www.youtube.com/watch?v=4cS8-j4iXl4&list=PLWg9zacwOnwfcpVm5pAKgOHms7PntsgJS&index=90)
[[Obs＃91] 用Dashboard++ CSS片段建立Obsidian首页 - YouTube](https://www.youtube.com/watch?v=e_YosZyWbLo&list=PLWg9zacwOnwfcpVm5pAKgOHms7PntsgJS&index=91)
[[Obs＃96] Obsidian分页调整： CSS样式与外掛，让分页操作更简便 - YouTube](https://www.youtube.com/watch?v=BLC6Y_gJ8UY&list=PLWg9zacwOnwfcpVm5pAKgOHms7PntsgJS&index=96)
[[Obs＃98] Obsidian的几个CSS+Markdown小技巧 - YouTube](https://www.youtube.com/watch?v=y4Z7CgV7V4c&list=PLWg9zacwOnwfcpVm5pAKgOHms7PntsgJS&index=98)
[[Obs＃99] Obsidian跳页分隔线的简单作法：使用HR标签（水平线） - YouTube](https://www.youtube.com/watch?v=-6-bO1_8v-I&list=PLWg9zacwOnwfcpVm5pAKgOHms7PntsgJS&index=99)
[[Obs＃105] Local REST API插件：提供Obsidian HTTP调用整合服务 - YouTube](https://www.youtube.com/watch?v=sPqgHcuT_Sw&list=PLWg9zacwOnwfcpVm5pAKgOHms7PntsgJS&index=105)
[[Obs＃106] Strange New Worlds (SNW) 奇异新世界插件—轻松掌握网络状链接；同场加映Relation Pane - YouTube](https://www.youtube.com/watch?v=iDlrV1G79c0&list=PLWg9zacwOnwfcpVm5pAKgOHms7PntsgJS&index=106)
[[Obs＃107] Obsidian全方位搜寻：OmniSearch插件 - YouTube](https://www.youtube.com/watch?v=7SILGFkcZys&list=PLWg9zacwOnwfcpVm5pAKgOHms7PntsgJS&index=107)
[[Obs＃108] 用Obsidian学习英文：Language Learner—事半功倍的Obsidian插件 - YouTube](https://www.youtube.com/watch?v=lK3oFpUg7-o&list=PLWg9zacwOnwfcpVm5pAKgOHms7PntsgJS&index=108)
[[Obs＃110] 用Emo Uploader将GitHub用做图床，方便发佈、分享 - YouTube](https://www.youtube.com/watch?v=ZQspooxvaHc&list=PLWg9zacwOnwfcpVm5pAKgOHms7PntsgJS&index=110)
[[Obs＃112] 用Spaced Repetition外掛强化长期记忆 - YouTube](https://www.youtube.com/watch?v=VYlVFawRgyM&list=PLWg9zacwOnwfcpVm5pAKgOHms7PntsgJS&index=112)
[[Obs＃113] 展示程式码片段的好工具：HK Code block插件 - YouTube](https://www.youtube.com/watch?v=MKd336sGQDA&list=PLWg9zacwOnwfcpVm5pAKgOHms7PntsgJS&index=113)
[[Obs＃114] 取代Obsidian核心插件的替代性插件：Better Command Palette、Another Quick Switcher、File Tree Alternative等 - YouTube](https://www.youtube.com/watch?v=XbPTYrjwBLw&list=PLWg9zacwOnwfcpVm5pAKgOHms7PntsgJS&index=114)
[[Obs＃115] 用Obsidian建立万用的收藏资料库(Collections)；善用Minimal Theme与Dataview - YouTube](https://www.youtube.com/watch?v=204kBqRatiQ&list=PLWg9zacwOnwfcpVm5pAKgOHms7PntsgJS&index=115)
[Obs＃118 | Obsidian超棒的图形处理 Awesome Image - YouTube](https://www.youtube.com/watch?v=d0NC2sQkDVE&list=PLWg9zacwOnwfcpVm5pAKgOHms7PntsgJS&index=118)
[Obs＃120 | Chronology：笔记年表📆一览无遗 - YouTube](https://www.youtube.com/watch?v=bWJYNc6h8rM&list=PLWg9zacwOnwfcpVm5pAKgOHms7PntsgJS&index=120)
 [Obs122 | AI大揭密！探索Obsidian笔记的神秘关联性：Smart Connections - YouTube](https://www.youtube.com/watch?v=2WKgZfYaSzQ&list=PLWg9zacwOnwfcpVm5pAKgOHms7PntsgJS&index=122)
[Obs124｜跳，跳，跳乎伊勇！Obsidian用书签和标签快速在文件间跳转 - YouTube](https://www.youtube.com/watch?v=Kgb_A5ReOxw&list=PLWg9zacwOnwfcpVm5pAKgOHms7PntsgJS&index=124)
[Obs126 | Obsidian 2023/04: 7个新插件的介绍与评析 - YouTube](https://www.youtube.com/watch?v=EQDzgkJXEaU&list=PLWg9zacwOnwfcpVm5pAKgOHms7PntsgJS&index=126)
[Obs127｜用Templater Hotkeys简化Obsidian自动化脚本，详解4个脚本范例 - YouTube](https://www.youtube.com/watch?v=U8HDmoQAwts&list=PLWg9zacwOnwfcpVm5pAKgOHms7PntsgJS&index=127)
[Obs128｜Obsidian DataView进度条与YAML栏位快速输入的方法(Templater Script) - YouTube](https://www.youtube.com/watch?v=c5T-flyo81E&list=PLWg9zacwOnwfcpVm5pAKgOHms7PntsgJS&index=128)
[Obs129｜Obsidian除了CSS片段以外的CSS进阶用法与两个CSS插件(MD Attributes and Stylist) - YouTube](https://www.youtube.com/watch?v=Z6ndLU85Iaw&list=PLWg9zacwOnwfcpVm5pAKgOHms7PntsgJS&index=131)
[Obs130｜用Dataviewjs将Dataview表格產生成Markdown格式并复製到剪贴簿的技巧 - YouTube](https://www.youtube.com/watch?v=7vsVj6sV3Dk&list=PLWg9zacwOnwfcpVm5pAKgOHms7PntsgJS&index=130)
[Obs131｜Obsidian使用Dataviewjs动态查询的尝试 - YouTube](https://www.youtube.com/watch?v=JDPMHoZbjow&list=PLWg9zacwOnwfcpVm5pAKgOHms7PntsgJS&index=131)
[Obs132｜标籤使用汇总与TagFolder：多重＋阶层式标籤资料夹，更妥善使用＃标籤的技巧 - YouTube](https://www.youtube.com/watch?v=L06pi781PeI&list=PLWg9zacwOnwfcpVm5pAKgOHms7PntsgJS&index=132)
[Obs134｜用Dataviewjs製作简单的建档统计图－使用Charts插件 - YouTube](https://www.youtube.com/watch?v=I1I9YeI1jDo&list=PLWg9zacwOnwfcpVm5pAKgOHms7PntsgJS&index=134)
[Obs135｜解锁简易Dataview查询：惊人的SQL技巧，使用Query All The Things(QATT)外掛 - YouTube](https://www.youtube.com/watch?v=-k5y6yhrWTM&list=PLWg9zacwOnwfcpVm5pAKgOHms7PntsgJS&index=135)
[Obs136｜3 个方法让你用Obsidian QATT插件读取外部档案 - YouTube](https://www.youtube.com/watch?v=sw1NiqawWlM&list=PLWg9zacwOnwfcpVm5pAKgOHms7PntsgJS&index=136)
[Obs137｜用Dataviewjs读取CSV资料以绘製统计图表 - YouTube](https://www.youtube.com/watch?v=xe53gjtTO1M&list=PLWg9zacwOnwfcpVm5pAKgOHms7PntsgJS&index=137)
[Obs138｜以标籤為基底，用Dataview形成索引笔记的尝试 - YouTube](https://www.youtube.com/watch?v=53FOyzgn8Hk&list=PLWg9zacwOnwfcpVm5pAKgOHms7PntsgJS&index=138)
[Obs139 | 5款便于维护属性的插件：Linter、TagMany、File Cooker、Tag Wrangler、Templater Hotkeys - YouTube](https://www.youtube.com/watch?v=ftaTh-UZUSA&list=PLWg9zacwOnwfcpVm5pAKgOHms7PntsgJS&index=139)
[Obs140｜Obsidian进阶全文检索与复製结果的插件－Query Control、Better Search View、Float Search、Text Expand、File Cooker - YouTube](https://www.youtube.com/watch?v=bf5vs4bQAZs&list=PLWg9zacwOnwfcpVm5pAKgOHms7PntsgJS&index=140)
[Obs142｜轻鬆烘烤(汇编)出需要的笔记：Easy Bake - YouTube](https://www.youtube.com/watch?v=jN3AdS0T2Es&list=PLWg9zacwOnwfcpVm5pAKgOHms7PntsgJS&index=142)
[Obs143｜分页式介面的应用：HTML Tabs外掛；增加Obsidian呈现的便利性 - YouTube](https://www.youtube.com/watch?v=WF7d7rUnG9Y&list=PLWg9zacwOnwfcpVm5pAKgOHms7PntsgJS&index=143)
[Obs146｜Obsidian汇总常用说明网站的助手：HelpMate - YouTube](https://www.youtube.com/watch?v=YIf0sznCIiU&list=PLWg9zacwOnwfcpVm5pAKgOHms7PntsgJS&index=146)
[Obs147｜Obsidian: 简易试算表外挂：CalcCraft，运算式储存格 - YouTube](https://www.youtube.com/watch?v=Ussk4xnIP2w&list=PLWg9zacwOnwfcpVm5pAKgOHms7PntsgJS&index=147)
[Obs149-左边长笔记，右边卡片的编辑布局：Query Control, Note Gallery - YouTube](https://www.youtube.com/watch?v=ErzEYx8Sto0&list=PLWg9zacwOnwfcpVm5pAKgOHms7PntsgJS&index=149)

[Obs150｜多重笔记标签操作-新增与移除：Multi Tag、TagMany、Notepad++、EmEditor、VS Code - YouTube](https://www.youtube.com/watch?v=-_0hOd87VeQ&list=PLWg9zacwOnwfcpVm5pAKgOHms7PntsgJS&index=150)
[Obs152｜终于能生成书签与页码了！与PDF相关的插件：Better - YouTube](https://www.youtube.com/watch?v=DnghHAcMW_g&list=PLWg9zacwOnwfcpVm5pAKgOHms7PntsgJS&index=152)
[Obs153｜快速开启外挂设定的方法；使用Open Plugin Settings与Advanced URI，通过Templater Hotkeys绑定快捷键 - YouTube](https://www.youtube.com/watch?v=bTYq-_jxIHU&list=PLWg9zacwOnwfcpVm5pAKgOHms7PntsgJS&index=153)
[Obs155｜程設师的编程好友：Codeblock Customizer／Code Styler、Codeblock Tabs、Keyshots - YouTube](https://www.youtube.com/watch?v=S3N6kyTGUoA&list=PLWg9zacwOnwfcpVm5pAKgOHms7PntsgJS&index=155)
[Obs156｜懒人式版本控制＋差异式备份：diffzip－Differential ZIP Backup - YouTube](https://www.youtube.com/watch?v=Mvje4Qn8-Ss&list=PLWg9zacwOnwfcpVm5pAKgOHms7PntsgJS&index=156)
==[Obs157｜使用Copilot插件使用本地AI模型服务-使用Ollama与LM Studio - YouTube](https://www.youtube.com/watch?v=mVP8GwHajv4&list=PLWg9zacwOnwfcpVm5pAKgOHms7PntsgJS&index=157)==
==[Obs158｜Obsidian自定义提示词与命令 - YouTube](https://www.youtube.com/watch?v=EdJRpucVNtg&list=PLWg9zacwOnwfcpVm5pAKgOHms7PntsgJS&index=158)==
[Obs159｜Obsidian术语词汇整合－definitions插件 - YouTube](https://www.youtube.com/watch?v=lKyLVP-3ZCY&list=PLWg9zacwOnwfcpVm5pAKgOHms7PntsgJS&index=159)
[Obs160｜Obsidian 试算表插件2024年新选择：Univer、Sheet Plus - YouTube](https://www.youtube.com/watch?v=rKUZtqeRpPk&list=PLWg9zacwOnwfcpVm5pAKgOHms7PntsgJS&index=160)
[Obs162｜Obsidian简单且容易操作的Anki新插件：Yanki - YouTube](https://www.youtube.com/watch?v=CE6iNxBGBTc&list=PLWg9zacwOnwfcpVm5pAKgOHms7PntsgJS&index=162)
[Obs163｜Yanki插件制作Anki 克漏字(Cloze)闪卡技巧，同场加映翏央填空模板 - YouTube](https://www.youtube.com/watch?v=DQ9DFKPugpQ&list=PLWg9zacwOnwfcpVm5pAKgOHms7PntsgJS&index=163)
[AHK64｜用AutoHotkey V2产生Yanki MD文件，快速建立Anki闪卡 - YouTube](https://www.youtube.com/watch?v=X4c4MItuBS8&list=PLWg9zacwOnwfcpVm5pAKgOHms7PntsgJS&index=164)
[Obs164｜将一篇英文文章制作成Anki闪卡的步骤，使用Yanki、ChatGPT(Copilot)与Note Splitter - YouTube](https://www.youtube.com/watch?v=Gu6B7nqUV9o&list=PLWg9zacwOnwfcpVm5pAKgOHms7PntsgJS&index=165)
[Obs165｜使用Copilot (ChatGPT)和Yanki生成Anki的注音闪卡 - YouTube](https://www.youtube.com/watch?v=Y-CkNWFmGCE&list=PLWg9zacwOnwfcpVm5pAKgOHms7PntsgJS&index=166)
[Obs167｜复制Dataview表格成为Markdown格式的插件：Enhanced Copy与Dataview Serializer - YouTube](https://www.youtube.com/watch?v=HiNdC7Mmnh4&list=PLWg9zacwOnwfcpVm5pAKgOHms7PntsgJS&index=168)
[Obs176｜Obsidian的卡片显示插件：Notes Explorer、GridExplorer与Data Cards，可视化笔记新体验 - YouTube](https://www.youtube.com/watch?v=Ht7dO4jJjq4)

# 正文前页(frontmatter)

- 用来设定该篇笔记的属性
- 为 YAML 格式
- 必须写在笔记最开头，以三个减号开头与结尾
- 设定的格式是 `键: 值`

## 1. Tags

## 2. aliases

- 设置笔记的别名
- 文件名会受到系统的限制，例如 Windows 的文件名不能有冒号、星号等。我们只要将其置于 aliases 里，就不受此限制