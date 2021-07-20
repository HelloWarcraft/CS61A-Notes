# CS61A/hw04/#Q3: Generators generator思路重新整理 

自己对iterator和generator的理解还是不够深刻，所以做完重新花半小时回顾一遍，加深记忆与理解，题目链接：[Homework 4 | CS 61A Summer 2021](https://cs61a.org/hw/hw04/#q3)

## 先概览题目

### Q3: Generators generator

Write the generator function `make_generators_generator`, which takes a zero-argument generator function `g` and returns a generator that yields generators. The behavior of each of these generators is as follows:

Since `g` is a generator function, calling `g()` will return a generator object that yields elements when `next` is called on it. For each element `e` that is yielded when `next` is called on the generator object returned by `g()`, your generator should yield a corresponding generator function that generates the first values, up until `e`, that are yielded by the generator returned by calling `g()`. See the doctests for examples.

```
def make_generators_generator(g):
    """Generates all the "sub"-generators of the generator returned by
    the generator function g.

    >>> def every_m_ints_to(n, m):
    ...     i = 0
    ...     while (i <= n):
    ...         yield i
    ...         i += m
    ...
    >>> def every_3_ints_to_10():
    ...     for item in every_m_ints_to(10, 3):
    ...         yield item
    ...
    >>> for gen in make_generators_generator(every_3_ints_to_10):
    ...     print("Next Generator:")
    ...     for item in gen:
    ...         print(item)
    ...
    Next Generator:
    0
    Next Generator:
    0
    3
    Next Generator:
    0
    3
    6
    Next Generator:
    0
    3
    6
    9
    """
    def gener(x):
        for e in ___________:
            ______________________________
            if _________________________:
                ______________________________
    for e in ___________:
        ______________________________
```

Use Ok to test your code:

```
python3 ok -q make_generators_generator
```

## 题目doctest的分析


```python
    # 读题之后会感觉很费解，要再结合doctest里面那个0 3 6 9的例子来思考，先搞清楚g()会yield 0 3 6 9的sequence
    # 然后通过for gen in make_generators_generator(every_3_ints_to_10)这一段代码发现next generation输出结果是嵌套的sequence
    # 进一步分析发现make()内部有多个sub sequence，而gen是一次等于这些sub sequence，每个gen的内容是一个在g()基础上递增的sequence。
    # 比如第一个gen是 0,第二个gen是0 3，第三个gen是0 3 6。为了方便写代码，把sequence换成list再提交系统，先在逻辑上成功之后再把list改掉
```

## make()结果对代码的启发

```python
    # 既然已知 make()最后会产生多个gen，那么最后的 for e in ___ 的句子就可以想明白应该是返回多个gen的功能，而且每一个gen其实会进一步调用上面定义好的gener函数(HOF的常见操作了)
    # 因此每个gener(x)会产生 [0]  [0,3]  [0,3,6]  [0，3，6，9]  的效果，第一个gen就是gener(0)，第二个gen就是gener(1)。
    # 考虑到for e in __的内容显然应该是跟g()相关，所以gener(x)里的x就不用下标了，而是g()的具体值，比如0 3 6 9。 gener(0)就是 [0] gener(3)就是[0,3]
    # 所以 for e in list(g()): yield gener(e)
```

## gener(x)函数的书写

```python
    # 对于gener(x)的具体函数，则x=0时输出 [0]， x=3时输出[0,3]，显然需要一个new_list来装这个列表，而且new_list在0之前初始化为[]，然后new_list+=[x]即可
    # 在def gener(x)之外 令new_list=[]，然后为了在gener(x)内部使用，必须要nonlocal一下，然后就是 nwe_list+=[x] 
    # 再yield new_list就实现了gener(0)输出[0]，gener(3)输出[0,3]的操作
    #     Next Generator:  [0]
    #     Next Generator:  [0, 3]
    #     Next Generator:  [0, 3, 6]
    #     Next Generator:  [0, 3, 6, 9]
    # 需要把new_list里的值单独yield出来
    # 不直接yield new_list，而是对new_list里的每一个元素进行yield即可，或者说yield from new_list即可
    # for e in new_list:
    #     yield e
```

> PS：由于不是自学而是上课，所以写完的代码会受Academic Honesty约束，无法把代码公布出来，只能放出自己的思路。 

