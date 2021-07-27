# Lab08 Q6 Add leaves的反思

## Q1 Combinations的一些固定结果

###  `(or 1 #t)`

<img src=https://pic3.zhimg.com/80/v2-dc5607509e6d976f7c985ba399be1236_720w.jpeg width=350>

 Scheme的or和and也有短路原则， `(or 1 #t)`不会评价完所有的element，再返回一个结果，直接看到1不是False value就返回它了

### `(define x 3)`

<img src=https://pic1.zhimg.com/80/v2-c3c84ba3cfc15646b7f413563f5e5186_720w.jpeg width=350>

`(define symbol value)`之后会显示这个symbol，实际上define的规则是三步走，最后一步就是return symbol的操作：

> The rules to evaluate this expression are
>
> 1. Evaluate the `<expression>`.
> 2. Bind its value to the `<name>` in the current frame.
> 3. Return `<name>`.
>
> from👉[Defining procedures | Lab 9: Scheme | CS 61A Summer 2021](https://cs61a.org/lab/lab09/#defining-procedures)

### `(if (not (print 1)) (print 2) (print 3))`

<img src=https://pic2.zhimg.com/80/v2-826f1562665c3b22fcc7b7cd858e80ec_720w.jpeg width=350>

`(if <predicate> <if-true> [if-false])`，加入print的if else，先调用print 1，然后print 1是一个非False，如果它是False则进入 print 3的语句。

### `((lambda (a) (print 'a)) 100)`

<img src=https://pic1.zhimg.com/80/v2-0330c3b5952f64620c0922130a55b21b_720w.jpeg width=350>

'a 与a的讨论，即使有了 `scm>(define a 10)`，在使用'a，也是只输出a，即使用 '(a, b)，也是输出(a,b)，不去理会a赋值的内容是多少。

## Q2 加强记忆if和cond的语句格式

```scheme
(if (> x 3)
    'x_is_bigger_than_3
    'x_is_not_bigger_than_3
    )
```



```scheme
(cond
 ((phase 1) (expression 1))
 ((phase 2) (expression 2))
 (else (else_expression) ;else也可以不要
 )
```



## Q3 define的symbol和procedure

difine symbol的value很简单

```scheme
(define <name> <expression>)
```

define procedures比较麻烦，很多复杂的功能都靠这个来实现

```scheme
(define (<name> <param1> <param2> ...) ;name后面有几个参数，以后就可以 (name param1 param2 ...)这样来调用函数了
  <body>  ;这个body 一般是 (lambda (x) (f_x))或者一个cond之类的
  )
```

## Q6 list的相关细节

创建一个list的方法

```scheme
'(1 2 3 4)
(list 1 2 3 4)
```

当然了依次`cons`也是可以的， `cons 4 nil`，前面依次1 2 3即可。
