# 共享编程(Pair Programming)的环境搭建：Atom的Teletype与VSCode的Live Share

2021.07.11

## 简介

实时共享编程叫Pair Programming，组队写Project的行为就叫pair programming。CS61A的Lab00里推荐了两个在text editor里进行[Pair programming](https://cs61a.org/lab/lab00/#pair-programming)的方法：

- [VS Code](https://cs61a.org/articles/vscode#pair-programming)
- [Atom](https://cs61a.org/articles/atom#pair-programming)

其中VSCode是用[Live Share extension](https://marketplace.visualstudio.com/items?itemName=MS-vsliveshare.vsliveshare&ssr=false)，Atom是用 [TeleType package](https://teletype.atom.io/)。

## 安装尝试

之前虽然有partner，但是project1都独立完成之后才互相询问project如何pair programming的，没机会尝试如何pair。直到今天才在project2里尝试如何pair programming，先是在VS Code上用Live Share，然后又用了Atom的TeleType。但是和partner摸索了好久，两个小白就一边网上查找指南一边瞎jb点，很希望有一份小白入门的文档来帮我们降低使用门槛，但是发现并没有。最后花了一个小时摸索完两个工具的安装和使用，我打算把这个经历记录下来，方便后来的小白能少走一些弯路。

> PS：笔者申请了[Berkeley Summer Sessions](https://summer.berkeley.edu/)，然后在Session C选的CS61A这门课，（小白走美国CS课程路线转码。
>
> 这门课的网站是 [CS 61A Summer 2021](https://cs61a.org/)，主要讲Python和OOP的入门。

最后发现Atom可以即使把文件同步到个人的Git repositories。下面介绍一下这俩工具的安装和使用，降低小白的使用门槛。

## VS Code的Live Share

Live Share的话，[Live Share extension](https://marketplace.visualstudio.com/items?itemName=MS-vsliveshare.vsliveshare&ssr=false)里面会有插件的Overview，介绍安装和共享，按照哪个Overview的步骤来就可以了。不过有一个细节就是Quickstart (Joining)中别人给你分享的链接，不是直接在浏览器里打开。链接格式为：https://prod.liveshare.vsengsaas.visualstudio.com/join?(many-numbers#@%&￥@*#) ，这个直接点进去之后没有反应。

正确的输入链接步骤为：

1、点击VS Code最下方蓝色栏的Live Share左边哪个个人账号（如下图红色方框）

![](https://pic1.zhimg.com/80/v2-0b0e65179741e057f89697c7eee8a664_720w.png)
  
2、VS Code会弹出一个框，点击那个Join Collaboration Session

3、之后会弹出一个填空一样的空行，别人给你分享的链接prod-liveshare格式的是输入在这里之后点击回车。这样才会进入共享编辑的状态。（直接在浏览器里打开那个链接，无法进入共享编辑）

![](https://pic1.zhimg.com/80/v2-2f7ea6b9f5af052ad4365918e887c7ba_720w.png)


## Atom的Teletype

### 安装Teletype

Atom我没用过，更是不知道在Atom的哪里安装插件，甚至不知道Atom里的插件叫做package。好在partner用过Atom，指出在Settings里安装package。

安装的时候，在主页左上角找到File，然后File->Settings->Install，然后页面右边会有一个搜索框，输入teletype即可出现如下的结果，然后点击Install即可安装。

![](https://pic1.zhimg.com/80/v2-f1cb811f2de2d376ef8ec67a9ec27cd9_720w.png)



### Teletype的分享和加入

> PS: 初次使用的话，需要在Atom里进行Github登录授权。

安装完成后的启动是在工具栏里的Packages完成的，点击Packages->Teletype->Share/Join，如下图。

![](https://pica.zhimg.com/80/v2-5b6079c25eccc8c779c4b045f106fe78_720w.png)

先测试Share功能，点击一下Share Portal，页面左下角会出现一个弹窗，哪里有一个Atom://格式的链接，把这个链接分享给partner即可。

partner收到链接后，点击Packages->Teletype->Join Portal，输入那个Atom链接即可，如下图：

![](https://pic1.zhimg.com/80/v2-c78769fa79cab88d50a03dbf0f9ed912_720w.png)



而且Teletype还有一个快捷启动的logo，就是界面右下角那个信号塔一样的icon，它可以替代Packages->Teletype->Share/Join的一大串点击启动模式。

![](https://pic1.zhimg.com/80/v2-1c49b3b7b205bdcfb58556ec200a7163_720w.png)
