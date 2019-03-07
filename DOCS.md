# xmpaint 使用技巧

## 邻接表

邻接表的格式是 `FROM TO` 或 `FROM TO TEXT`，表示有一条从 FROM 到 TO 的边，边上有文字 TEXT。

TEXT 可以包含空格，FROM 和 TO 不能包含空格。

如果你一定要空格，请用 `\` 代替：它会被自动替换成空格。

例如：

```
1\2 3 4,5 6
1\2 3
```

表示两条从 `1 2` 指向 `3` 的边，其中一条边上面有文字 `4,5 6`。

## 高亮

输入一个点的名称来高亮这个节点；输入两个点的名称来高亮它们之间的边。

如果出现重边，你无法单独高亮其中的一个。这是设计缺陷。

例如：

```
1\2
1\2 3
```

表示高亮点 `1 2`，以及 `1 2` 指向 `3` 的所有边。

## 别名

有的时候你想给点或者边起个别名。在 Splay、线段树等每个节点上记录了很多信息的图中，这个功能十分有用。

`BEFORE AFTER` 表示将点 `BEFORE` 显示成 `AFTER`；`|BEFORE AFTER` 表示将文字是 `BEFORE` 的边显示成 `AFTER`。

例如：

```
1\2 foo
|4,5\6 bar
```

分别设置了一个点的别名和一条边的别名。

在邻接表里，你可以使用本名或别名来表示一个节点。例如，当设置了 `1\2 foo` 别名后，这两条边是等价的：

```
1\2 3
foo 3
```

## 快捷键

- 按 <kbd>Alt+1</kbd>、<kbd>Alt+2</kbd>、<kbd>Alt+3</kbd> 可以切换“邻接表”、“高亮”、“别名” 三个窗口。
- 按 <kbd>Alt+`</kbd> 或 中键双击 或 右键双击可以隐藏侧边栏。
- 按 <kbd>Alt+Q</kbd> 可以清空所有输入。
- 按 <kbd>Alt+W</kbd> 可以手动应用剪贴板的控制命令（详见“控制命令”一节）。

## 控制命令

xmpaint 支持下列格式的控制命令：

- `$$! TEXT` 表示在“邻接表”窗口中插入一行内容。
- `$$@ TEXT` 表示在“高亮”窗口中插入一行内容。 
- `$$# TEXT` 表示在“别名”窗口中插入一行内容。
- `$$!clear`、`$$@clear`、`$$#clear` 表示清除对应窗口中的内容（注意大小写）。
- `$$clear` 表示清除三个窗口中的所有内容。
- `$$!block`、`$$@block`、`$$#block` 可以插入多行内容（进入代码块模式），`$$end` 可以退出代码块模式。

其他内容会被忽略。

选中“监视剪贴板”选项后，当 xmpaint 窗口获得焦点时，如果剪贴板内容有变化，xmpaint 将会自动运行剪贴板里的命令。

例如：

```
C:\Users\example\Desktop>dijkstra_example.exe
please input node count: 3
please input edge count: 3
$$clear
please input edge: 1 2 10
$$! 1 2 10
please input edge: 1 3 10
$$! 1 3 10
please input edge: 2 3 10
$$! 2 3 10
$$# 1 S
$$# 3 T
$$@ S
$$@ T
dijkstra begin
point 1 dis 0
  relax 2 dis 99999 -> 10
  relax 3 dis 99999 -> 10
point 2 dis 10
point 3 dis 10
dijkstra end
$$@ 1 3
The shortest path is 10

C:\Users\example\Desktop>
```

你应该已经想到了，设计这一功能的目的是方便你把调试信息导入 xmpaint。
上面那个例子是一个 Dijkstra 程序的控制台输出。你只需要全选、复制它们，再打开 xmpaint，直接按 F5 就能看到结果。
即使这些内容夹杂在很多其他调试信息之间也毫无问题。

你可以通过 [一些例子](http://uoj.ac/submission/164508) 来感受 xmpaint 的控制命令是如何无缝嵌入到你的代码里的。

## 豆知识

- <kbd>Shift+1</kbd> = `!`；<kbd>Shift+2</kbd> = `@`；<kbd>Shift+3</kbd> = `#`。
- 取消选中“清理临时文件”后，将会在 `output` 目录保留生成的 GraphViz 文件和图片文件。
- `dot` 引擎适合 Splay、自动机、特意建图之后的网络流、搜索树等有明显父子关系的图。`fdp` 和 `sfdp` 适合那些看着就像图的图（比如杂乱无章的网络流和最短路等）。`circo` 适合边数远多于点数的图。
