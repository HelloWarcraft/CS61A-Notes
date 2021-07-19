# 关于Generator和Iterator的理解

## Iterator

### iterator的作用

虽然iter(List)+next(iterator)可以实现List[index]功能

但是iterator的next，是一个一个输出iterator里的内容，而且next(iterator)每调用一次，iterator就变化一次。



### 对于object的理解

Iterator和generator都是一个object，不用管它是什么，就记住它有四个特点即可：

> ①配合next(iterator or generator)使用来输出内部element
>
> ②可以用list(iterator or generator)或tuple(iterator or generator) 来输出这个object内部的全部内容【dict()不能用】
>
> ③iterator or generator是动态的。next( )每访问一次，它都往右移动一次；list( )或者tuple( )访问一次则往右移动到底。
>
> ④>>>a = [1,2,3,4] >>>iter(a)则list(iter(a)) 又恢复成[1,2,3,4]了，iterator和list可以互相转换



## Generator

### yield

```python
def gen_naturals():
    i = 0
    while True:
        yield i # i is the return value of next(g)
        i += 1
>>>g=gen_naturals()
>>>next(g)
0
>>>next(g)
1
.
.
.
#可以一直到无穷大，而list无法实现逐个输出无穷个数字
```

遇到`yield i` 的时候，只要记住”yield的值就是next(generator)的返回值“就可以了。

运行到yield之后，可以继续往下execute。

`yield x`的话，应该是把x传入iterator或者generator这个object里面了，当next()调用这个object，会动态输出每个传入的`x`，如果不调用，那么x就一直在这个object里面。

```python
def a_then_b(a, b):
    for x in a:
        yield x
    for x in b:
        yield x
>>> a_then_b([3, 4], [5, 6])
<generator object> #不调用这个object，发现f()是一个object
>>> list(a_then_b([3, 4], [5, 6]))
[3, 4, 5, 6] #调用了这个object，才会以调用函数的输出方式来输出这个object的内容
```


### no evaluation

```python
def funny_generator():
    yield 1
    yield 2
    yield 1 / 0
    yield 3
```

g=funny_generator()不会出现Error，第三个next(g)才会Error。

而`[1, 2, 1/0, 3]`直接Error，因为输入一个list之后，computer会先evaluate这个list，遇到1/0的时候发现Error，list直接接收失败。



