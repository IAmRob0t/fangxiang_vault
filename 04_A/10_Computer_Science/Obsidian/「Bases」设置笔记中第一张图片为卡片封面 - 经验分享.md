---
source: "https://forum-zh.obsidian.md/t/topic/53093"
author:
  - "[[Obsidian 中文论坛]]"
published: 2025-08-19
created: 2025-09-06
description: "一句话总结利用自定义公式获取第一张图片，设置为卡片封面 效果如图：   实现方法创建卡片视图的bases点击右上角属性，添加自定义公式 粘贴公式并命名（例如命名为first_image） 设置封面属性为刚创建的属性 …"
tags:
  - "clippings"
---
[Azona77](https://forum-zh.obsidian.md/u/Azona77) 活跃用户

[17 天](https://forum-zh.obsidian.md/t/topic/53093?u=robot "发布日期")

## 一句话总结

利用自定义公式获取第一张图片，设置为卡片封面

效果如图：  

[![image](https://forum-zh.obsidian.md/uploads/default/optimized/3X/4/2/4280c9986bdac78204c51c6b8910b99cefbbff9f_2_212x249.jpeg)](https://forum-zh.obsidian.md/uploads/default/original/3X/4/2/4280c9986bdac78204c51c6b8910b99cefbbff9f.jpeg "image")

## 实现方法

1. 创建卡片视图的bases
2. 点击右上角属性，添加自定义公式  
	[![image](https://forum-zh.obsidian.md/uploads/default/optimized/3X/3/e/3e94a0c3bebed18fcc4058a513c41cccda418c85_2_130x250.png)](https://forum-zh.obsidian.md/uploads/default/original/3X/3/e/3e94a0c3bebed18fcc4058a513c41cccda418c85.png "image")
3. 粘贴公式并命名（例如命名为first\_image）  
	![image](https://forum-zh.obsidian.md/uploads/default/original/3X/6/9/695308223741a18a8fffb4c9ba4ed40924821594.png)
4. 设置封面属性为刚创建的属性  
	[![image](https://forum-zh.obsidian.md/uploads/default/optimized/3X/5/2/52cb864781c34dc3de4a33fd64bf7de1efbaca25_2_248x250.png)](https://forum-zh.obsidian.md/uploads/default/original/3X/5/2/52cb864781c34dc3de4a33fd64bf7de1efbaca25.png "image")

## 公式

```python
file.embeds.filter(value.containsAny("png","jpg","webp","svg","jpeg"))[0]
```

## 相关

- file.embeds可以替换为file.links，file.links包含属性和正文中的 `[[内容]]` ，以及嵌入的`![[内容]]` ，且顺序不是前后顺序，是先 `[[]]` 后`![[]]` 各自排序
- 如果希望第二张图作为封面，可以将公式后的 `[0]` 改为 `[1]` ，以此类推
- 使用文件后缀筛选，可能不是最优的方案，如果有其他方法，欢迎楼下补充
- **表格视图** 可以用类似的方法提取，额外套一个image函数即可显示： `image(上述公式)`
- 相关文档
	- [Functions - Obsidian Help 5](https://help.obsidian.md/bases/functions)
	- [Bases syntax - Obsidian Help 9](https://help.obsidian.md/bases/syntax#File+properties)

- [「Bases」极简卡片视图（美化css小合集，不定期更新） 6](https://forum-zh.obsidian.md/t/topic/53118)

上次访问

这是 Reese 首次发帖 - 让我们欢迎他/她加入社区吧！

[trentswd](https://forum-zh.obsidian.md/u/trentswd)

[16 天](https://forum-zh.obsidian.md/t/topic/53093/9?u=robot "发布日期")

感谢楼主！  
这个bases我有两个疑惑就是  
1 如何选取第一张图片 （感谢楼主）  
2 如何截取一部分正文作为预览

请问第二个问题有办法吗？

[Azona77](https://forum-zh.obsidian.md/u/Azona77) 活跃用户

[16 天](https://forum-zh.obsidian.md/t/topic/53093/10?u=robot "发布日期")

官方文档里暂时没有检索内容的方法： [Bases syntax - Obsidian Help 3](https://help.obsidian.md/bases/syntax#File+properties)

不过我记得 [Page Gallery 3](https://github.com/tokenshift/obsidian-page-gallery) 插件是有 content mode 可以预览开头内容的，如果刚需的话可以考虑一下插件或者自己用dataview折腾

我们已经有一段时间没有看到 yuno 了 — 他/她上次发帖是 10 个月前。

[@yuno](https://forum-zh.obsidian.md/u/yuno) [@jsye](https://forum-zh.obsidian.md/u/jsye)

表格视图显示图片、外链显示图片的问题，测试了一下可以用 [image函数 6](https://help.obsidian.md/bases/functions#%60image\(\)%60) 实现：

如图中的ob图标为外链图片，公式为 `image(外链属性)` 、红色图标为内链图片 `image(first_image)` ；

但外链需要填写到属性里，暂没有提取文中外链的方法

表格视图：  

[![image](https://forum-zh.obsidian.md/uploads/default/optimized/3X/b/5/b514fabfe1ba732486e657e1e787817be7f2241e_2_517x43.png)](https://forum-zh.obsidian.md/uploads/default/original/3X/b/5/b514fabfe1ba732486e657e1e787817be7f2241e.png "image")

  
卡片视图：  
![image](https://forum-zh.obsidian.md/uploads/default/original/3X/2/7/27fab3abf686021041e01c0e1d3f47e0540f9811.png)

  

[由 Discourse 提供技术支持](https://discourse.org/powered-by)