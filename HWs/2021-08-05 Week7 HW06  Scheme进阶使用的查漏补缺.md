# HW06 Scheme进阶使用的查漏补缺



## 错误用法1

```scheme
scm> (define lst cons(3, nil))
;cons(3, nil)外面再套一层括号，表明这是一个完整的list
;而且cons(3, nil)就有问题，应该是(cons 3 nil)
;(define lst (cons 3 nil))，而且也没有逗号，如果cons嵌套则为expr=(cons 3 nil)之后外面再嵌套 (cons 2 expr)
;不要写成(cons expr 2)了，cons的第二个元素要么是一个scheme list要么是一个nil，只有cons的第一个元素才是放数字的。
```

[pair-and-list-manipulation | Discussion 9 | CS 61A Summer 2021](https://cs61a.org/disc/disc09/#pairs-and-lists)里有嵌套的cons。

我已经短时间内三次使用 cons(3 nil)类似的用法了，特别是3和nil不是单纯的value，而是复杂的expression的时候，更容易忘记`(cons A B)`

HW6 Q3 filter-lst 的一个关键recursive case就是这个`(cons (car lst) (filter-lst func (cdr lst)) )`，而我写成了`(cons ((car lst) (filter-lst func (cdr lst))) )`即`(cons(A B))`，导致出现`# Error: int is not callable: A`，而且潜意识以为自己写的是对的，肉眼看了好久没看出来，又因为scheme没法`print(J"DEBUG:")`来缩小范围，所以很耗时。



## 错误用法2


```scheme
scm> (cond
 (phase 1) (expression 1)
 (phase 2) (expression 2)
 else (else_expression) ;else也可以不要
 )
;phase1和expression1本身外面一层括号之外，phase1和expression1的外层也有一层括号
```

## 错误用法3

没有`nil?`，而是`null?`

```
(null? <arg>)
```

Returns true if `arg` is `nil` (the empty list); false otherwise.



## quasiquote

为什么quasiquote和quote的用法那么奇怪易混淆？Macros没听lecture啊，话说听那个真的太费解，有空去听听。

```scheme
scm> `(x ,(* y x) y)
? (2 6 3)
-- Not quite. Try again! --

? (x ,(* y x) y)
-- Not quite. Try again! --

? (x 6 y)
-- OK! --
;总结一下，没有加逗号的情况下，`和'的区别就是'无脑当作字符串转化，`()则把括号里的单个元素保留字符串格式，expression元素计算出结果。
;加逗号的情况下，‘(expr)，则变为(unquote (expr))，而`(expr)变成该expr的计算值
```



## Tail Recursion再复习

HW06的Q7就是练习这个的（听lecture学不会Tail Recursion，只有需要自己上手操作与实践的时候才学的会这个）



下面是一个常见的factorial的递归方法，如何把结果不当作return value而是存在另一个参数里？这就需要新建立一个`helper()`函数，多增加一个result的argument（python常用套路），那么下面的代码如何改呢？

```scheme
(define (factorial n)
  (if (= n 0)
      1
      (* n (factorial (- n 1)))))
```



```scheme
(define (fac-tail n)
    (define (helper n result)
        (if (= n 0)
            result; base case, return the product.(product is calculated in every call)
            ; Why  (* n (factorial (- n 1))) will cause the rest half return calls?
            ; Because every returned value need to times other value.
            ; If no n*f(n-1) but only f(n-1), then no the rest half return calls.
            (helper (- n 1) (* n result))
            )
        )
    (helper n n)
    )
```

走到Base Case的时候，因为每一个递归调用都跟随着计算了result，所以到出口了不需要`n*f(n-1)`这样的`1*f(0)` `2*f(1)` `3*f(2)`这样在返回的途中逐个计算`*`的结果。

```c
(factorial 6)
(fact-tail 6 1)
(fact-tail 5 6)
(fact-tail 4 30)
(fact-tail 3 120)
(fact-tail 2 360)
(fact-tail 1 720)
(fact-tail 0 720)
720
```

而回到最初的factorial的计算过程，会发现多了一半的计算量：

```c
(factorial 6)
(* 6 (factorial 5))
(* 6 (* 5 (factorial 4)))
(* 6 (* 5 (* 4 (factorial 3))))
(* 6 (* 5 (* 4 (* 3 (factorial 2)))))
(* 6 (* 5 (* 4 (* 3 (* 2 (factorial 1))))))
(* 6 (* 5 (* 4 (* 3 (* 2 1)))))
(* 6 (* 5 (* 4 (* 3 2))))
(* 6 (* 5 (* 4 6)))
(* 6 (* 5 24))
(* 6 120)
720
```

所以关键在于把`n*result`传入新的helper的最后一个参数里，而且新的helper外面不要放杂七杂八的计算，光棍一个`helper((n-1), n*result)`。

他的实质是把`helper()`外面的计算，挪到了参数里，这样本来应该抵达base case之后在每次回归时做的计算早早地在递进的时候就做了。到了base case由于f(n)和f(n-1)的关系是一一对应，没有其他计算公式，所以一溜烟从`helper(0,result)`跳到了`helper(6,1)`。

有了这个思路再去做Q7就很简单了。





## Without Duplicates: Unique list

这个是HW06的Question 5，有点类似SU19的Unique 问题：[Homework 6 Q2: Unique | CS 61A Summer 2019 (berkeley.edu)](https://inst.eecs.berkeley.edu/~cs61a/su19/hw/hw06/#q2)

> Implement `unique`, which takes in a list `s` and returns a new list containing the same elements as `s` with duplicates removed.
>
> ```
> scm> (unique '(1 2 1 3 2 3 1))
> (1 2 3)
> scm> (unique '(a b c a a b b c))
> (a b c)
> ```
>
> > Hint: you may find it useful to use the built-in `filter` procedure. See the [built-in procedure reference](https://inst.eecs.berkeley.edu/~cs61a/su19/articles/scheme-builtins.html) for more information.
>
> ```
> (define (unique s)
>   'YOUR-CODE-HERE
> )
> ```

当然，要实现的是下面这个问题：

```scheme
; Question 5
;
(define (without-duplicates lst)
  'YOUR-CODE-HERE
)
```

理解上很简单一个list，把里面重复的元素剔除掉，剩下的独一无二(unique)的元素保留为一个list，然后返回这个list。

我潜意识筛选出unique的逻辑思路为迭代：list[index]，如果list[index]在list里有重复，则把重复的pop掉。显然这个思路很难在scheme里实现。

要实现的话，经过hint video的提示，我想到了`cons (car lst) (without-duplicates (cdr lst))`。即函数本身的返回值作为一个result-lst，先把list的first value拿出来，如果first value在result-lst里存在，则不把first value放入result-lst，first value在result-lst里不存在，则把first value放入result-lst，first value取完之后list自然迭代为`(cdr list)`。因此可以创建一个`(exist x list)`的函数，用来迭代。(当然了，既然用`cons (car lst) (without-duplicates (cdr lst))`的递归，Base Case就是lst为nil的时候，这时候返回nil即可。若 `(cdr lst)`是`nil`，则返回`nil`之后就是 `(cons (car lst) nil)`)

```scheme
; Question 5 solution (no filter, not standard solution)
;

(define (without-duplicates lst)
  (define (exit x lst)
    	(if (null? lst)
            #f ;x doesn't exits in null
            (if(= x (car lst))
               #t ;once one (car lst) is equal to x, return #t
               (exit x (cdr lst));else, iterate to (cdr lst)
               )
          )
    );end the exit function
  ;the judgement should be "if (exit (car lst) result-list)", but no result-list here
  ;so there needs a helper function, which has an argument to store the result-list.
  ;And the initail value of result-lst is nil
    (define (helper lst result-lst)
          (if (null? lst)
              result-lst ;base case
              (;recursive case
               if (exit (car lst) result-lst)
                  (helper (cdr lst)  result-lst) ; do exit, so result-lst does nothing and iterate to (cdr lst)
                  (helper (cdr lst) (cons (car lst) result-lst));do not exit, result-lst updates and iterate
                  )
            )
     ) 
     (helper lst nil)
)
;Chinese comment is banned in Scheme
;no result_lst, because the expression of 'name_name' is banned
```

最后能跑的通过，不过结果和标准的有些顺序差异：

```scheme
scm> (without-duplicates (list 5 4 5 4 2 2))
(2 4 5)
```



这个思路就是逐个拿`(cdr lst)`里的first value去跟result-lst去对比，如果不存在就放到里面。但是有两个难点，一个是`(exit x lst)`要自己去写，另一个是`rsult-lst`需要用Tail recursion。其中把Q5的顺序放到Q7之后的原因就是这里要用tail recursion。(如果tail recursion不熟悉的话，下面放的那一堆代码会没有概念，只能推理出`(helper (cdr lst)  result-lst)`和`(helper (cdr lst) (cons (car lst) result-lst))`这俩代码，然而不完整)

```scheme
(define (helper lst result-lst)
          (if (null? lst)
              result-lst ;base case
```



后来又想了想，题目提示要用`filter`，我的思路从`recursive-func (car lst) (cdr lst)`变成了`recursive-func (car lst) (filter-lst fn lst)`，因为`(filter-lst fn lst)`返回的是一个所有元素都满足`fn`的list，`fn(element)`是`#t`的元素都会被挑出来。

如果这个`(fn element)`是`（not (= element (car lst)))`（即element与`(car lst)`不相等），那么`(filter-lst fn lst)`的结果就是比`(cdr lst)`范围更小的一个list。

而且这个新的list里，没有与`(car lst)`相等的element，因此可以把`null? lst`的else结果中的`recursive-func (car lst) (cdr lst) `换成`(cons (car lst) recursive-func (car lst) (filter-lst fn (cdr lst)))`。

具体代码就不放了，上面那个非标准答案，顺序是反的，可以放。这个solution的话由于是有效的solution需要遵守Academic Honesty
