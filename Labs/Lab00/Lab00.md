# Lab00

> 刚看到lab00的时候晕了两天，[Lab 0: Getting Started | CS 61A Summer 2021](https://cs61a.org/lab/lab00/#doing-the-assignment)，对这么长的文档直接崩溃，对python的交互式方式也很诧异。我只会在devC++里面写代码，然后点击run。然后上知乎去b站，翻遍syllabus翻油管。甚至听了几小时的国内python入门，都对做lab00的效果不大。
>
> 后来想到花了一万多块不能浪费，就对着文档的目录逐节往下阅读和操作，而且逐句朗读查单词，最后花了十个小时左右，搞定了这个文档。

##  Follow the YouTube Guidance

I learned how to install and use python, powershell and vscode, from the YouTube guidance. And the summary is as below:

> Do as YouTube does
>
> Windows
>
> - install python 3
> - test PowerShell
> - install vscode
> - test `demo.py` in vscode
>   - how to create py file
>   - how to run a py file
>   - how to open a py file



but the webpage ([Lab 0: Getting Started | CS 61A Summer 2021](https://cs61a.org/lab/lab00/) ) is more than what I have learned form the video: [CS61A Su20: Lab 00 Setup - YouTube](https://www.youtube.com/watch?v=YlothkvwsJo).



I could catch the YouTube video, but cannot do as the tutorial do. because the words are abstract.





##  Learn the tutorial webpage step by step(click the content icons one by one)

 ### Install Live Share extension for Pair Programming
  ### Summary of the commands 

  - cd <directory path>
  - ls (dir)
  - mkdir <directory name>
  - mv <source> <destination>
 ### At here: [Lab 0:  python-basics](https://cs61a.org/lab/lab00/#python-basics), I have a question: What is the differences among interpreter, terminal and editor ？ 

  - refer to: [一文搞懂Python解释器，终端，编辑器区别和联系 - 云+社区 - 腾讯云 (tencent.com)](https://cloud.tencent.com/developer/article/1516833)
  - Terminal
    - Terminal is Shell, which is system of computer
    - Terminal is a place to input command and output results. (Notice: Commands are totally different from Codes)
    - Terminal can be opened by 3 methods
      - cmd
      - Windows PowerShell
      - VsCode
  - Interpreter
    - for primary learning, interpreter can be considered as ">>>"
  - editor
    - code editor, also known as Integrated Development Environment (IDE)
    - IDLE
    - [VsCode](https://code.visualstudio.com/)
    - [Jupyter Notebook](https://jupyter.org/)
    - [Pycharm](https://www.jetbrains.com/pycharm/)
### Then Python expressions

  - primitive expressions
  - arithmetic expressions
    - //	Floor division 整除
    - /     Floating point division 浮点除法
    - %   Modulo 求余



> ![image-20210620222658998](C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20210620222658998.png)
>
> I eventually find the difference between eecs link and cs61a link!
>
> Previously, I thought eecs link is a website of ECE SICP Course. (In fact, ECE College in China will also open Data Structure or Operations Research)
>
> （In Chinese：我以为eecs的cs61a和cs61b是电气学院开的SICP和DS，只有CS61a和CS61b的网站才是计算机学院开的正宗SICP和DS）



 ### Test OK Grading Website

  - run ok(in the lab00) by terminal
  - submit ok file to https://okpy.org by terminal
  - type in `python3 ok -q python-basics -u`  in the terminal to unlock the test (这里要cd到lab00的目录里才行)
  - write code and run the code
    - edit `lab00.py` in vscode and write `return 2021`
    - input `python3 ok`, then the code will run
    - type in `python3 ok --submit`, then the lab00.py will be submitted to https://okpy.org
    - A useful summary: [okpy Command Generator (cs61a.org)](https://ok-help.cs61a.org/)

### Submit and check submission

- drag the `.py`file to the Submission Area: [Submit Assignment | Ok (okpy.org)](https://okpy.org/cal/cs61a/su21/lab00/submit)

- Or submit `.py` file by terminal

  - In the terminal, `cd` to the lab00 directory and type in `python3 ok --submit` 
  - click into [Assignment | Ok (okpy.org)](https://okpy.org/cal/cs61a/su21/lab00/), check the `Recent Submissions` of Lab0

  
