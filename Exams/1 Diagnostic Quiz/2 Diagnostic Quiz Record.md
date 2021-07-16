# Diagnostic Quiz Record

2021.07.03 16:00 CST

## Problem**1. Catch that Bug!**

You may assume that digit_counter will only be passed a positive integer for its second parameter. 

### Problem1 debug1

```python
 def digit_counter(f, item):
     counter = 0
     while item >= 0:
         if f(item % 10):
             counter += 1
         item = item // 10
     return counter
```

### Problem1 debug2

```python
 def digit_counter(f, item):
     if item < 10 and f(item):
         return item
     if f(item % 10):
         return 1 + digit_counter(f, item // 10)
     return digit_counter(f, item // 10)
```

### Problem1 debug3

```python
 def digit_counter(f, item):
     def helper(x, sofar):
         if x > item:
             return sofar
         last = (item // x) % 10
         return helper(x * 10, sofar + f(last))
     return helper(0, 0)
```

> solution

debug1的`item>=0`去掉`=`

debug2的`return item`改为`return 1`

debug3的`helper(0,0)`改为`helper(1,0)`



## Problem**2. Applications are Closed**

You may assume that x is always less than the second argument of the function.



## Problem3. Camel Sequence

```python
def is_camel_sequence(n):
    """
    >>> is_camel_sequence(15263) # 1 < 5, 5 > 2, 2 < 6, 6 > 3
    True
    >>> is_camel_sequence(98989) 
    True
    >>> is_camel_sequence(123) # 1 < 2, but 2 is not greater than 3.
    False
    >>> is_camel_sequence(4114) # 1 is not strictly less than 1
    False
    >>> is_camel_sequence(1)
    True
    >>> is_camel_sequence(12)
    True
    >>> is_camel_sequence(11)
    False
    >>> is_camel_sequence(11910986)
    False
    """
    def helper(n, thank):
        if _____________:
        #      (a)
            return True
        elif thank:
            return _______________ and helper(_____________)
            #            (b)                       (c)
        else:
            return _______________ and helper(_____________)
            #            (d)                       (e)
    return ____________ or _____________
```

> Problem2 soluton

```python
def is_camel_sequence(n):

    def helper(n, thank):
        if n//10==0:
        #      (a)
            return True
        elif thank:
            return n % 10 < n // 10 % 10 and helper(n//10,False)
            #            (b)                       (c)
        else:
            return n % 10 > n // 10 % 10 and helper(n//10,True)
            #            (d)                       (e)
    return helper(n,True) or helper(n,False)
```

