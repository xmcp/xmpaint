# xmpaint
**OI 业界良心系列 之 秒杀mspaint的画图工具**


基于 graphviz 二次开发，直接以邻接表的形式输入一张图就能把它画出来：

![image](https://cloud.githubusercontent.com/assets/6646473/24803987/8fc90a36-1bdf-11e7-8473-f146663af91e.png)

有向/无向图，边权什么的都是嗞磁的：

![image](https://cloud.githubusercontent.com/assets/6646473/24803519/1532d366-1bde-11e7-8275-49365395435c.png)

可以给一些点和边高亮：

![image](https://cloud.githubusercontent.com/assets/6646473/24803579/41699398-1bde-11e7-8df5-5b7b2d96037f.png)

还可以给点和边设置别名，特别适用于需要离散化、splay、AC自动机、层次图等节点编号不直观的图：

![image](https://cloud.githubusercontent.com/assets/6646473/24803695/98382770-1bde-11e7-8d4d-2fe14af93f07.png)

总之，下文所述都可以用 xmpaint 来画，你只需要在调试的时候把邻接表输出出来，再粘贴进去就行了：
- 题目里直接输入的图
- 最短路
- 网络流
- 各种自动机
- Splay
- 并查集
- 线段树
- 树分治
- 记忆化搜索（调用顺序为邻接表）
……

[→ Windows 打包版本下载](http://s.xmcp.ml/xmpaint.7z)

[→ 详细的使用说明](DOCS.md)