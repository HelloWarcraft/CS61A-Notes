# Lab08 Q6 Add leaves的反思

<font color='rainbow'>尝试了很多个version，对于找到tree的每一个node，和keep track of depth的方法我很陌生，代码写来写去，写出来的还有问题，debug之后才改正。</font>

究其原因，估计是之前作业练习的少，而且练习的作业都是对照slides里的模板写相应recursive的statement，没意识到如果statement错了一个位置会有什么结果。到了这次自己懒得参考了，直接凭空写代码，就变成了首先不知道在哪里用recursion，然后不知道recursion的格式是什么样子的。最后在hint video提示下写出了接近答案的recursion又有一些小bug，无法根除，要一遍一遍捋思路才能发觉逻辑漏洞。

### Q6: Add Leaves

Implement `add_d_leaves`, a function that takes in a `Tree` instance `t` and mutates it so that at each depth `d` in the tree, `d` leaves with labels `v` are added to each node at that depth. For example, we want to add 1 leaf with `v` in it to each node at depth 1, 2 leaves to each node at depth 2, and so on.

Recall that the depth of a node is the number of edges from that node to the root, so the depth of the root is 0. The leaves should be added to the end of the list of branches.

> **Hint:** Use a helper function to keep track of the depth!

```python
def add_d_leaves(t, v):
    """Add d leaves containing v to each node at every depth d.

    >>> t_one_to_four = Tree(1, [Tree(2), Tree(3, [Tree(4)])])
    >>> print(t_one_to_four)
    1
      2
      3
        4
    >>> add_d_leaves(t_one_to_four, 5)
    >>> print(t_one_to_four)
    1
      2
        5
      3
        4
          5
          5
        5

    >>> t1 = Tree(1, [Tree(3)])
    >>> add_d_leaves(t1, 4)
    >>> t1
    Tree(1, [Tree(3, [Tree(4)])])
    >>> t2 = Tree(2, [Tree(5), Tree(6)])
    >>> t3 = Tree(3, [t1, Tree(0), t2])
    >>> print(t3)
    3
      1
        3
          4
      0
      2
        5
        6
    >>> add_d_leaves(t3, 10)
    >>> print(t3)
    3
      1
        3
          4
            10
            10
            10
          10
          10
        10
      0
        10
      2
        5
          10
          10
        6
          10
          10
        10
    """
    "*** YOUR CODE HERE ***"
    def helper(t,v,depth=0):
        if t.is_leaf():
            pass #helper里面return一下，问题不大。
        else:#写个if-else主要是因为t是leaf的时候，没法for b in t.branches
            if len(t.branches)>=1: #竟然还有branches里三个nodes的，就不用len==2 or len==1了
                depth+=1
            for b in t.branches:#每个t的子树b都要附加depth个new_leaf
                #debug 2. b不进入循环则depth不变，进入循环则不能直接在for里depth+=1
                #len(t.branches)是2或者1的时候直接在for之前depth+1即可
                print("DEBUG:", depth) 
                helper(b,v,depth)#debug 1. t的下属b完成了添加，b的下属branch则交给helper
                # 应该是先往下递归到最底下，最后到b是leaf了，再一层一层回收
                for _ in range(depth):#depth=1的时候range(1)仍然是
                    new_leaf=Tree(v,[])
                    b.branches+=[new_leaf]
                
            # 不需要再 for branch in b.branches。helper传入b则自动到else有for b in t.branches
    helper(t,v,0)
```

这个题反思一下，关键在于`for b in t.branches`里的recursion怎么写，然后base case是啥，之后如何keep track of depth。至于添加新leaf，则有了depth就比较简单。

`for b in t.branches`之后，b是t的一个子树(或两个子树之一)，b肯定要继续helper递归才能把寻找b的子树这个动作继续下去。问题在于recursion里是`return helper(t,v,depth)`还是`return 1+helper(t,v,depth)`，还是不用`return`?

这个helper函数的目的是修改t树的内容，不需要return，所以直接`helper(t,v,depth)`，一直`for b in t.branches: f(b,v,depth)`不断找子树的子树，直到找到leaf，这就是base case，这时候depth统计完毕，才开始从leaf到root进行添加depth个new_leaf。

先调用recursive function，之后再做操作，不能在recusion之前做操作。（这个跟Lecture: Tree Recursion里面那个cascade的例子有些相似之处。都是recusive function has no return value，在recursion之后再进行某些操作，cascade是print操作，本题是add_leaf操作。）



这题回想一下，很简单，但是昨日卡了2h的bug，今天又花1h才搞定。真是Tree recursion和Trees的课堂练习没有白板推导，打下扎实基础的原因呐！



> 后面的留白，就是练习其他tree recursion和trees 相关problems留用吧，把这块基础打牢。
