# Lecture17 Representation再理解

## 关于repr和str的疑惑

看到`__repr__ `和` __str__`这俩函数的时候，搞不懂为什么要把这俩对比，貌似功能一样，都是输出一个结果啊。

```python
# Implementing generic string functions

class Bear:
    """A Bear."""
    def __init__(self):
        self.__repr__ = lambda: 'oski'
        self.__str__ = lambda: 'oski the bear'

    def __repr__(self):
        return 'Bear()'

    def __str__(self):
        return 'a bear'

def print_bear():
    oski = Bear()
    print(oski)
    print(str(oski))
    print(repr(oski))
    print(oski.__repr__())
    print(oski.__str__())

def repr(x):
    return type(x).__repr__(x)

def str(x):
    t = type(x)
    if hasattr(t, '__str__'):
        return t.__str__(x)
    else:
        return repr(x)
```



下面这个例子让我感觉两者还是有区别的。

```python
    def __repr__(self):
        return 'Bear()'

    def __str__(self):
        return 'a bear'
```

但是不懂这样有什么意义，反正只要输出一个结果不就行了，repr和str二选一。

但是后来到了写linked list的class的时候，我发觉两者不能二选一，各自的作用互相替代。

## 写Link的时候回顾repr和str的区别

对于Link这个类，我自己只写了一个基本功能：

```python
class Link:
    empty=()
    def __init__(self,first,rest=empty):
        assert rest is Link.empty or isinstance(rest,Link)
        self.first=first
        self.rest=rest
```

然后发现`>>> Link(1,Link(2))`之后显示`<__main__.Link object>`，跟我预期的重复一遍`Link(1,Link(2))`不太一样。而且如果想要直接显示Link里面的所有内容，用list的格式来输出，也不能直接`print(Link(1,Link(2)))`。

这时候发觉直接输入类名，返回一个结果的函数就是`__repr__(self)`函数，而`__str__(self)`则在`print(instance)`或者`str(instance)`的时候生效。而且两个函数都要自己去写，才能生效的。

```python
class Link:
    empty=()
    def __init__(self,first,rest=empty):
        assert rest is Link.empty or isinstance(rest,Link)
        self.first=first
        self.rest=rest
    def __repr__(self):
        if self.rest:
            rest_str=','+repr(self.rest)
        else:
            rest_str=''
        return 'Link({0}{1})'.format(self.first,rest_str)
    def __str__(self):
        string='[]'
        while self.rest is not Link.empty:
            string+=str(self.first)+''
            self=self.rest
        return string+str(self.first)+']'
```

上面俩函数直接搬运vitamin08里面的结构了，自己有空再写一个出来。



## 回头对oski例子的repr和str再理解

后来对那个oski和Bear的例子理解更深入了，可以直接摸出这个例子的头绪：

```python
class Bear:
    """A Bear."""
    def __init__(self):
        self.__repr__ = lambda: 'oski'
        self.__str__ = lambda: 'oski the bear'

    def __repr__(self):
        return 'Bear()'

    def __str__(self):
        return 'a bear'

def print_bear():
    oski = Bear()
    print(oski)
    print(str(oski))
    print(repr(oski))
    print(oski.__repr__())
    print(oski.__str__())
    

>>> oski=Bear()
>>> oski
Bear()
>>> str(oski)
'a bear'
#oski这个instance，直接输入的话，得到结果是__repr__(self)的返回值
#str(oski)的话，得到的是__str__(self)的返回值
#而oski.__repr__则__repr__是oski的一个variable，要在constructor里找这个__repr__，然后发现它是一个lambda function，自然oski.__repr__()和oski.__str__()就是两个新的string：'oski'和'oski the bear'了。

#于是直接print_bear()的结果如下：
>>> print_bear()
a bear
a bear
Bear()
oski
oski the bear
# print(oski)和print(str(oski))永远等价
```



## Representation里的Ratio例子有待反思



```python
# Ratio numbers
from fractions import gcd

class Ratio:
    """A mutable ratio.

    >>> f = Ratio(9, 15)
    >>> f
    Ratio(9, 15)
    >>> print(f)
    9/15

    >>> Ratio(1, 3) + Ratio(1, 6)
    Ratio(1, 2)
    >>> f + 1
    Ratio(8, 5)
    >>> 1 + f
    Ratio(8, 5)
    >>> 1.4 + f
    2.0
    """
    def __init__(self, n, d):
        self.numer = n
        self.denom = d

    def __repr__(self):
        return 'Ratio({0}, {1})'.format(self.numer, self.denom)

    def __str__(self):
        return '{0}/{1}'.format(self.numer, self.denom)

    def __add__(self, other):
        if isinstance(other, Ratio):
            n = self.numer * other.denom + self.denom * other.numer
            d = self.denom * other.denom
        elif isinstance(other, int):
            n = self.numer + self.denom * other
            d = self.denom
        else:
            return float(self) + other
        g = gcd(n, d)
        r = Ratio(n // g, d // g)
        return r

    __radd__ = __add__

    def __float__(self):
        return self.numer / self.denom
```

