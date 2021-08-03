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
        >>> plus = env.bindings['+'] 
        #plus应该是一个Buildtin的instance，直接给一个字典里的加是什么意思？
        #检索全局的create_global_frame()函数之后，发现它创建了一个symbol-procedure的字典
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

## Problem 4: Implement the missing part of `scheme_eval`

读完problem description和Code之后大致得到如下结论：

> expr是一个combination，读完scheme_apply()和BuitinProcedure感觉应该把expr拆成Procedure和args
>
> 根据operator创建一个procedure，把operands做成Pair类，当作args传入`scheme_apply(Procedure,args,env)`即可

How to handle combinations? lecture slides里介绍的有：`if` `lambda` `define` or `operator`，用`do_?_form`的方法，这也是project里面后面的problem要实现的功能。至于普通call expression，这里就给实现。

对combination的拆分，提供的code如下，分析得出else应该是普通的call expression，格式为：`(<operator> <operand 0> ... <operand k>)`

```python
	first, rest = expr.first, expr.rest
	if scheme_symbolp(first) and first in SPECIAL_FORMS:
        # 这里是special forms，first如果不是special forms就是普通call expression
        # 检索了一下SPECIAL_FORMS ，发现它是一个字典，除了存if lambda define还有and or cond begin等
        	return SPECIAL_FORMS[first](rest, env)
        # 处理if lambda和define，其他情况是普通的call expression
	else:
        # BEGIN PROBLEM 4
        "*** YOUR CODE HERE ***"
        # scheme_eval的代码在John的video里就有，但是else里的一点也没有出现
        # 实现scheme_eval的思路仅在lecture里提了一下，指望不了lecture了
        
        #既然first是普通的call expression，那就first如果是
```

接着回顾problem description里三个要点：

> 1. Evaluate the operator (which should evaluate to an instance of `Procedure`)
> 2. Evaluate all of the operands
> 3. Apply the procedure on the evaluated operands, and return the result

这三点就是我理解的这句：

> 根据operator创建一个Procedure，把operands做成Pair类，当作args传入`scheme_apply(Procedure,args,env)`即可

然后是前两步需要递归调用`scheme_eval(expr,env)`，如何递归调用这个函数？`scheme_eval(expr,env)`显然把`first`和`rest`当作`expr`传入函数，传入之后会有什么结果？

​	如果传入`first`: `first`是`symbol`的话，返回一个`env.lookup(first)`; `first`是数字的话，返回该数字。

​	如果传入`rest`: 则`rest`是新的Pair，再次评估其first。



之外还会用到的函数：

> - The `validate_procedure` function raises an error if the provided argument is not a Scheme procedure. You can use this to validate that your operator indeed evaluates to a procedure.
> - The `map` method of `Pair` returns a new Scheme list constructed by applying a *one-argument function* to every item in a Scheme list.
> - The `scheme_apply` function applies a Scheme procedure to a Scheme list of arguments. **Make sure to use this function rather than the** `apply` **method of a specific procedure**, as not all procedures have their own `apply` methods.

- `validate_procedure` function

  检索了一下，发现他的用法是`validate_procedure(procedure)`，确保一个`procedure`是valid。而valid的意思其实要继续找`scheme_procedurep(procedure)`，检索之后发觉这个`scheme_procedurep(x)`就是`return isinstance(x, Procedure)`，表明如果`procedure`是`Procedure`的instance即是valid。

- The `map` method of `Pair` 

  去Scheme_reader.py里找Pair的map方法，明白它的用法是`expr.map(fn)`，功能是把pair这个scheme list转为每个元素都`fn(element)`之后的scheme list。

- The `scheme_apply` function

  这里就是说不要用`procedure.apply(args, env)`，因为有的`procedure`是没有`apply`method的，要用`scheme_apply`代替`procedure.apply()`。

做unlock，得到一个要注意的点：

```scheme
scm> (1 (print 0)) ; validate_procedure should be called before operands are evaluated
? SchemeError
```



然后怎么做？各种复杂的概念与用法检索和理解了好久，最后如何实现这个eval？没有太明确的概念啊，题目说是要 recursively call `scheme_eval(expr,env)`，那具体是什么思路呢？我无法凭空想出来一个啊。去看一下lecture里的`calc_eval()`吧，模仿一下思路。

​	

> 卧槽啊，一个半小时看完description，每个新概念或者新函数都要去查一下输入的参数是什么样子的，输出的结果是什么类型的，结果整理完了却发现eval的思路lecture里完全没讲，或者讲得遮遮掩掩。你他妈的介绍一个scheme就老老实实从白板介绍，基础概念讲清楚再出练习题啊。lecture故意留着东西不讲明白透彻，让人自己写作业去悟，这种教学贼几把坑。
>
> lecture里遮遮掩掩不讲清楚，导致我听lecture都极其费力。没有讲清楚各种使用情况，如何一步步实现的，作业里就让人给梳理出来，属实无猫画虎。



要把`scheme_eval(expr,env)`的参数、返回值和作用都记下来，之后再去理解其他概念。然后发现这个作用是

- scheme_eval(rest,env)，输入的是rest，返回的是经历fn的rest，这样rest的所有element，

- 如果expr是symbol则返回scheme_add之类的procedure，如果是数字原样返回，如果是Pair串则返回Pair串的数值

- 只有把第三种情况转为value，这样的rest才可以作为无嵌套的scheme list，从而作为operands

这样`operantor`就用`scheme_eval(first,env)`来搞定，而`scheme_eval(rest,env)`则要把rest里每一个元素都转成`value`，因此用`rest.map(fn)`，`fn`用`lambda`来输入`rest`并输出Pair linked list的`rest_value`。

同时要注意` validate_procedure(operator)`来确保 `operator`确实是`Procedure`的instance(hint提醒要用这个函数)。

​    

## Problem 5: Implement defining names. 

`do_define_form(expressions, env)`实现的功能有两个`scm> (define a (+ 2 3))` 和 `scm> (define (foo x) x)`。即把define这个expressions的rest跟first匹配在一起。

之后阅读代码，要注意的是，`"***YOUR CODE HERE***"`上面有个`validate_form(expressions, 2)`，这个语句的意思是expressions的Pair类型的linked list里面，只有两个元素。（如果print(expressions)只有两个值，虽然某个值可能是一个`(+ 2 3)`之类的表达式）

代码里的doctest里有两个例子。下面的例子对应`scm> (define (foo x) x)`，是problem 9要完善的部分。因此只需要完成`scm> (define a (+ 2 3)) ; Binds the name a to the value`  或者`scm> (define a 3)` 这样的情况即可。

而且传入的`expressions`已经把`Pair('define', ...)`给去掉了，只剩下name和value。



而unlock的前两道题，第一道就点出了`expressions`是`Pair(A, Pair(B, nil))`的格式，不过A是一个name，B可能是一个value，也可能是一个expression。第二道unlock的题目提示要用`Frame`里的`define(self, name, value)`。

把这两道题翻译成Code即可: 直接用`expressions.first`和`expressions.rest`提取出`A`和`B`，然后`env.define(A, B)`即可。 不过`B`需要把value或者expression都过一遍`scheme_eval(expr, env)`。而`expr`如果是一个value则返回本身，如果是一个`(<operator> <operand1> <operand2> ... )`的Pair linked list，就需要返回这expr的数值（正好`scheme_eval(expr, env)`可以实现这个功能）



## Problem 6: Implement quoting in our interpreter

在读description之前，先理解下面这些scheme语句对应的Pair表示：

```scheme
    'hello -> epxr1=Pair('quote',Pair('hello',nil))
    'expr1 -> Pair('quote',Pair(expr1,nil) )
    ''hello -> Pair('quote',Pair('hello,nil) )
    ; return expressions.first得到 'hello, -> scheme_read(src) -> Pair('quote',Pair('hello',nil))
    (quote hello)
    
    ;(cons 'car '('(4 2)))
    '(4 2) -> expr3=Pair('quote', Pair( Pair(4, Pair(2, nil)),nil))
    '('(4 2)) -> Pair('quote',Pair( Pair(expr3, nil),nil))
    '('(4 2)) -> Pair('quote',Pair( Pair(Pair('quote', Pair( Pair(4, Pair(2, nil)),nil)), nil),nil))
```

关于(eval)的用法

```scheme
scm> (eval (list 1 2))
Traceback (most recent call last):
 0	(eval (list 1 2))
 1	(1 2)
Error: int is not callable: 1
;把list的第一个元素变成callable：换成lambda函数名
scm> (eval '((lambda (x) (* x x)) 2) )
4
```

（这个problem6的doctest引导性不是特别强，unlock也不是很有启发，跟着description看才是王道。

之后阅读description，首先要实现如下输入输出的结果：

```scheme
scm> (quote a)
a
scm> (quote (1 2))
(1 2)
```

在Code里有这句： ` validate_form(expressions, 1, 1)`，这个语句的意思，规定了expressions只能是Pair(...,nil)格式。也说明`scm> (quote a)`或者`scm> (quote (1 2))`这样的语句会去掉quote变成expressions，作为参数传入`do_quote_form(expressions, env)`，而且print(expressions)的话只有一个元素，因此直接return expressions.first即可（expressions.rest是nil）

根据后来的description，要在`scheme_reader.py`里`scheme_read()`函数里修改语句，handling the case for `'`。

实现如下输入输出的结果：

```scheme
scm> 'hellohelloscm> '(1 2)(1 2)scm> '(1 (2 three (4 5)))(1 (2 three (4 5)))
```

即，用`'`来表示scheme list，也要保存为 Pair('quote', ...)的格式，当val=="'"的时候，只需要`>>> 'hello -> (quote hello)`即可，如果`val=="'"`，则`src=["hello"]`，因此直接Pair list的第一个元素是'quote'，第二个元素就是"hello"，这个"hello"需要用Pair表示，即`Pair("hello", nil)`，同时它外面套一个`Pair('quote', ...)`。`src=["hello"] - > Pair("hello", nil)`的方法就是用`scheme_reader(src)`。

