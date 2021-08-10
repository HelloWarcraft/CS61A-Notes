# 2021-08-09 Project4 Scheme problem 16~18做题笔记



problem16~18是在`questions.scm`文件里写scheme代码，



Problem16算是简单重复一下scheme里的递归，从而逐个访问scheme list里的内容。



Problem17是merge_sort的scheme版本，如果做过final review里python版本的merge problem，这个题目就是简单转化一下。



Problem18有个题意理解上的难点：

```scheme
(define (let-to-lambda expr)
  (cond ((atom?   expr) <rewrite atoms>)
        ;expr是boolean number symbol string nil的时候，都算atom，都会进入这个case
        ((quoted? expr) <rewrite quoted expressions>)
        ;expr是(quote content)的时候才进入这个case，而传入的expr为'(quote content)。因为'之后的expr	就是里面的内容。例如''hello才会进入这个case，而且expr是(quote hello)；而‘(1 2)就不会进入这个case，因为(car expr)是1，所以进入atom那个case。
        ((lambda? expr) <rewrite lambda expressions>)
        ((define? expr) <rewrite define expressions>)
        ;lambda和define的expr本来应该来什么输出什么，直来直去，但是这俩的表达式里面可能会含有let statement，所以要拆开来处理，把里面的内容再递归一次。
        ((let?    expr) <rewrite let expressions>)
        ;按照提示里的zip函数把let给处理成为lambda
        (else           <rewrite other expressions>)))
		;这时(car expr)非上述情况的case，(car expr)为+、- * /之类的，反正不会在内部出现let statement
```





做到一半发现要先完善`zip`函数，实现下面的输入输出，才能再let里面进行zip 的操作。

```scheme
scm> (zip '((1 2) (3 4) (5 6)))
((1 3 5) (2 4 6))
scm> (zip '((1 2)))
((1) (2))
scm> (zip '())
(() ())
```

进入具体的`(let？ expr)` case，题目给了两个例子：

```scheme
scm> (let-to-lambda '(let ((a 1) (b 2)) (+ a b)))
((lambda (a b) (+ a b)) 1 2)
;'(let ((a 1) (b 2)) (+ a b))
;(car (zip values)) is (a b), call it first
;(cadr (zip values)) is (1 2), call it last
; body is (+ a b) (let-to-lambda body)
```



```scheme
scm> (let-to-lambda '(let ((a 1)) (let ((b a)) b)))
((lambda (a) ((lambda (b) b) a)) 1)
;'(let ((a 1)) (let ((b a)) b))
;(car (zip values)) is (a), call it first
;(cadr (zip values)) is (1), call it last
;body is (let ((b a)) b), (let-to-lambda body)
; so do (let-to-lambda body) to get ((lambda (b) b) a)

; In the end, so I need to make a list of ((lambda first body) last_value)
; make a pair list of (lambda first body), then (append pair_list last)
;(lambda->first->body) should be as below:
;(cons 'lambda (cons first (cons (let-to-lambda body) nil))) 
; Error! Error! Because  (let-to-lambda body) is a scheme list, not a value, so it's ok to simply (cons first body)
;(cons 'lambda (cons first (let-to-lambda body) )
```

基于上面的例子，得到的结果为：`((lambda->first->body)->last_element)`
```scheme

;(lambda->first->body) is (cons 'lambda (cons (car (zip values))  (let-to-lambda (cadr (zip values))) )
; Set last is list2, (lambda->first->body) is list1. Then (append '(list1) list2) will get the result of (list1 list2_element)
(append
'(cons lambda 
  (cons (car (zip values))
    (let-to-lambda body) ))
(cadr (zip values))
)
```

但是上面的这个有个bug，`(cons lambda  (cons (car (zip values)) (let-to-lambda body) ))`是`(lambda (a b) (+ a b))`，同时`(cadr (zip values))`就是`(1 2)`，但是在`first`之前加一个`'`把它变成list，会保留后面的`cons`之类的东西。所以要用`(list element)`来创建list。



然后是`(or (lambda? expr (define? expr))`的case:

```scheme
        ((or (lambda? expr)
             (define? expr))
         (let ((form   (car expr))
               (params (cadr expr))
               (body   (cddr expr)))
           ; BEGIN PROBLEM 18
           ;'replace-this-line
           ; END PROBLEM 18
          )
        )
```



遇到下面这个情况，人傻了，不知道为啥会这样。。。`(lambda (x) a (let ((a x)) a))`的话，`form`是`'lambda`，`params`是`(x)`，`body`是`Pair(a, Pair(..., nil))`。

body应该只能是一个表达式啊，这怎么出了`a`和`(let ((a x)) a))`两个？

结果简单地对body进行`let-to-lambda`操作竟然不行，没法`(cons form (cons params (let-to-lambda body)))`了。

```scheme
scm> (let-to-lambda '(lambda (x) a (let ((a x)) a)))
(lambda (x) a (let ((a x)) a))

# Error: expected
#     (lambda (x) a ((lambda (a) a) x))
# but got
#     (lambda (x) a (let ((a x)) a))
```
ps: 上面的问题会进入在于`else`的case里，而不是进入let

```scheme
 (cons (let-to-lambda (car expr)) (let-to-lambda (cdr expr)))
          ;((lambda (a) a) x), (lambda (a) a) suits this case
```


