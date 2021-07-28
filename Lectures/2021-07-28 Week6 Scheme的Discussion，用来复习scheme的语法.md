# Scheme的Discussion，用来复习scheme的语法

记录笔记之前，先瞎说几句题外话：之前都是挂着zoom，没参加具体讨论的，今天很早完成lab了，就参加了discussion，发现还是有收获的。

> people seldom particapate in the discussion
>
> One reason is the lab hasn't been finished
>
> Another reasion is that the time for grouped discussion is too limited. 
>
> ​	Suggestion for TA：easy problem provides 1 minute; hard problem provides 5minutes

## 细节记录

###  `=` `euqal`和`eqv`的区别

`=`只能用在数字上，`equal`用来表示是否相等，`eqv`则是表明是否相同，就类似python里的`==`和`is`。

### Higher order functions用在scheme里

```python
# python
def f(x):
   def g(y):
      return x + y
   return g
```



```scheme
;scheme
(define (f x) 
  (lambda (g y) (+ x y))
)
```



之后就是复习`if`，`cond`和`define`的综合使用

## problems的解决，python里的递归转化为scheme语法

### 一般递归

用factorial来计算x的阶乘，python里`factorial(5)`是120，scheme里`(factorial 5)`的结果是120：

```python
# python
def factorial(x):
    if x==0:
        return 1
    else:
        return x*factorial(x-1)
```



```scheme
;scheme
(define (factorial x)
  		(if (= x 0) 
             1
             (* x  (factorial (- x 1)
                    )
             )
         )
  )
(except (factorial 5) 120) ; (factorial 5)应该是120

```

Fibonacci number，`fib(n)`写完后，转化为scheme的`(fib n)`，结果如下：

```python
# python
def fib(n):
    if n=1 or n==2:
        return 1
    else
    	return fib(n-1)+fib(n-2)
```



```scheme
; scheme
(define (fib n)
        (if (or (= n 1) (= n 0) )
            n ;(fib 1)和(fib 0)是1和0，所以可以return n
            (+ (fib (- n 1))  (fib (- n 2))
             )
        )    
)

(define (f n)
    (if (or (= n 1) (= n 2)
        ) 
        1 ;(fib 1)是1，(fib 2)是1，所以return 1，严格来说base case要是上面那个，不然会漏一个(fib 0)的value
        (+ (f (- n 1)) (f ( - n 2))
        )
    )
)
```



### 关于list的递归调用

先回忆scheme里的list的一些关键字用法


|                | Scheme                  | Python                    |
| -------------- | ----------------------- | ------------------------- |
| Create         | (cons first rest)       | Link(first, rest)         |
| Get label      | (car lst)               | lst.first                 |
| Get rest       | (cdr lst)               | lst.rest                  |
| Empty          | nil, ‘()                |                           |
| Make long list | (list 1 2 3)或 ‘(1 2 3) | Link(1, Link(2, Link(3))) |

之后是两道题目

### Q5: List Concatenation

Write a function which takes two lists and concatenates them.

Notice that simply calling `(cons a b)` would not work because it will create a deep list. Do not call the builtin procedure `append`, since it does the same thing as `list-concat` should do.

```scheme
(define (list-concat a b)
    'YOUR-CODE-HERE
)

(expect (list-concat '(1 2 3) '(2 3 4)) (1 2 3 2 3 4))
(expect (list-concat '(3) '(2 1 0)) (3 2 1 0))

```

就是做一个拼接a和b的函数，用python写的话，直接就a+b了。用scheme写的话，必须要递归调用，这样才能访问到a的每一个元素。（因为a是一个list的话，访问a中每一个元素的方法就是递归里有两个case，用if语句，base case是car a，recursive case是 cdr a。

如果`(list-concat a b)`是把a和b拼接，那么`(car a)`+`(list-concat （cdr a) b)`就是recursive case。当`(cdr a)`也就是传入的参数`a`是`null`的时候，直接返回`b`即可把`b`和每一个`(cdr a)`的`(car dynamic_a)`给`cons`起来。

梳理代码的思路如下


```scheme
;scheme
(if (null ? a)
    b
    (cons (car a)
          (list-concat (cdr a) b)
    )
)
```



> 最后还是要刷一刷Discussion里的Exam Prep啊，关于Tree Recusrion和Tree的Exam Prep完全没做，导致没习惯Exam的题型，所以期中铩羽。

