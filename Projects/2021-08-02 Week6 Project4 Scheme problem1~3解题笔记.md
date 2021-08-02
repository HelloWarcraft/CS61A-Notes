# Project4 Scheme做题过程

Interpreter当时第一遍听课就卡壳了，以至于当天失去了学习的欲望。第二天强行闷着头给听完，遇到不懂的地方，花个把小时去啃，最后等到pair programming做project4之前我仍然感觉学的毫无头绪，project4没法下手。等跟partner一起聊的时候，才知道他也是一样的感觉。我恍然发觉原来不是太难了，而是老师不能讲得太明白，不然project4让你去实现一个scheme就等于重复课堂内容了。

可见学习到难关之处，有partner共享体验多么重要，此外pair programming真的能规范时间使用，并且解决思路或者代码上的bug。（problem1就在unlock上卡了 bug，想了3分钟没懂，问了partner才懂。另外problem1还有一个疑惑，我给他描述了一遍，结果两人都没搞懂，所以打算先放置一边，做完project再说）

## Problem1: Implement `scheme_read` and `read_tail`

Scheme_reader.py的代码实现要复习REPL里的read部分，

`Scheme_read()`函数就是实现传入一个Buffer类的instance，输出一个Pair类的instance。Buffer类的主要内容是一个字符串列表，Pair类的主要内容是一个链表。



首先通读description，顺便复习video的interpreter实现的讲解。（interpreter的lecture其实就是对scheme的实现的具体讲解，而且里面的demo也有`scheme_read()`和`scheme_eval()`，感觉当时讲课听的就很糊涂，原因在于没有剖开细讲，没有具体分析如何一步一步去实现功能，然后每一步对应什么代码。的部分代码之后再做unlock

```python
Problem 1 > Suite 1 > Case 2
(cases remaining: 7)

>>> from scheme_reader import *
>>> tokens = tokenize_lines(["(+ 1 ", "(23 4)) ("])     
>>> src = Buffer(tokens)
>>> src.current()
'('
>>> src.current()
'+'
>>> src.pop_first()
'+'
>>> src.pop_first()
1
>>> scheme_read(src)  # Removes the next complete expression in src and returns it as a Pair
? Pair('+',Pair(1,Pair(Pair(23,Pair(4,nil)),nil))))
-- Not quite. Try again! --

? Pair('+',Pair(1,Pair(Pair(23,Pair(4,nil)),nil)))
-- Not quite. Try again! --

? Pair('+', Pair(1, Pair(Pair(23, Pair(4, nil)), nil)))
-- Not quite. Try again! --

? Pair('+', Pair(1, Pair( Pair(23, Pair(4, nil)), nil) ))
-- Not quite. Try again! --

? Pair('+', Pair(1, Pair(Pair(23, Pair(4, nil)), nil)))
-- Not quite. Try again! --

? Pair('+', Pair(1, Pair(Pair(23, Pair(4, nil)), nil)))
-- Not quite. Try again! --
```

这个unlock part的问题一直卡住，后来发觉是src因为pop过了，所以src不再对应原来的 `+ 1 (23 4))(`了。而是`(23 4))(`，所以对它转化为Pair。即为`Pair(23, Pair(4, nil))`



唯一一个疑点在于`>>> scheme_read(src)`之后再`src.current()`为什么是`'('`而不是`')'`，毕竟return nil的时候，`'))('`只pop了一个元素，之后就是一直返回，不再进行pop了。

此外本题在`scheme_read`和`read_tail`的填空全不可见上一个笔记：2021-08-01 Week6 Interpreter的重新复习。

## Problem 2: Implement the `define` and `lookup` methods of the `Frame` class

做完发觉不难，就是问题的描述有些抽象，仅仅看描述的话不知道对方在说什么东西，导致看完一遍之后仍然脑子里很多问号，看text editor里的部分代码和描述也不太懂。

这时候做unlock，跟着unlock才知道`difine()`就是把`symbol`作为字典`bindings`的key，`value`作为字典`bindings`的value，极其简单。另外`lookup()`其实就是找self或者self.parent或者self.parent.parent里的`bindings.keys()`。

对于`lookup()`，description里有一个三种情况的解释，unlock里也有例子帮助理解。具体逻辑就是：如果keys的list里有传入的参数`symbol`，那么返回`symbol`着key对应的value，否则就是`SchemeError`（这个Error的语法已经提供了，不需要自己去查阅）。



## Problem3:  complete the `apply` method in the class `BuiltinProcedure`.

Problem3的细节有四点，其实最重要就是第一点：把`args`这个Pair的instance转化为真正的python list。

读题外加做unlock的时候，遇到了下面的这个问题：

```python
    def apply(self, args, env):
        """Apply SELF to ARGS in Frame ENV, where ARGS is a Scheme list (a Pair instance).

        >>> env = create_global_frame()
        >>> plus = env.bindings['+'] #plus应该是一个Buildtin的instance，直接给一个字典里的加是什么意思？
        >>> twos = Pair(2, Pair(2, nil))
        >>> plus.apply(twos, env)
        4
```

这时doctest里的例子，我无法理解plus直接给个`+`号，怎么能创建一个BuiltinProcedure的instance，而下面这个的unlock题目里，plus是`BuiltinProcedure(scheme_add)`创建出来的，因此就是apply的self。但doctest里的plus为何能替换self呢？实在费解。

```python
Problem 3 > Suite 1 > Case 1
(cases remaining: 9)

>>> from scheme import *
>>> env = create_global_frame()
>>> twos = Pair(2, Pair(2, nil))
>>> plus = BuiltinProcedure(scheme_add) # + procedure
>>> scheme_apply(plus, twos, env) # Type SchemeError if you think this errors errors
? 4
```

下面这两点是`apply` method of `BuiltinProcedure`的关键部分：

- Convert the Scheme list to a Python list of arguments. *Hint:* `args` is a Pair, which has a `.first` and `.rest` similar to a Linked List. Think about how you would put the values of a Linked List into a list.
- If `self.expect_env` is `True`, then add the current environment `env` as the last argument to this Python list.

把Pair的instance转为list，可以参考scheme_reader.py里面`Pair`类的`__str__(self)`method，迭代一下，取`.first`放入`argumentlist`即可。

至于那个`self.expect_env`，我反复读了那段`expect_env`的描述，始终没看懂为什么要把env作为最后一个argument，无奈只能按照提示说得来，直接add `env` to the list完事儿。
