# Project3 Ant完成笔记

7.23 完成Phase 1 

7.24 完成Phase 2

7.25 完成Phase 3

7.26 完成Phase 4

主要难点再Phase 1和Phase 2的入门，一旦对这些class的相互关系和class里面的method熟悉了之后，后面的Phase3和Phase4就不会出现没有头绪或者看不下去的情况，顶多会卡bug。



## Phase 1: problem1~3 

<p align=left><font=宋体>2021-07-23</font></align>


刚学完Class Object和Inheritance，完成了两个练习的lab。然后听了linked list和mutable tree作为class的练习例子。然后就要做project了，估计还是我题目做的太少不熟练，lab的optional也应该做一做的，现在看着Ants这800行的原始代码，还有8000字的阅读材料，就定神按照problem的顺序一个一个往下啃。

但是发觉上来就给我Colony、Places、The Hive、Ants和Bees，又给了GameState、Place、Hive、Insect、Ant和Bee六个class，全是文字描述。看的我都不知道这游戏到底如何操作了，应接不暇。

还是用了`python3 gui.py`，实际玩了一下游戏才知道一些概念。原来就类似植物大战僵尸，Bees类似僵尸，HarvesterAnt类似向日葵，food类似阳光，ThrowerAnt就是攻击型植物。Bees从右边向左边移动，遇到Ant就攻击，没遇到就左移一格，一旦有一个Bee接触左边边界，Bees就赢了，玩家就输了。

> 问题在于我可以无限放置Ants，但是ThrowerAnt貌似不会扔leaf，导致几乎无法杀伤Bees，总是被Bees攻入Home。（做完所有project之后再看这个记录，发觉是ThrowerAnt没有完成）

然后再看几个概念的定义才能接受和理解，然后对于六个类也能看得进去具体的代码。花了一个小时才逐步理解一些概念，并且克服workload的恐惧。说实话，我真的只能跟着hint video完成题目。自己完全没有能力独立构思出这个project的思路，初看全局的project构造，直呼看不懂。只能一个problem接着一个problem去写，甚至写完把所有problem的空子填补完全，仍然缺乏总体架构的了解。因为很多时候，完全想不到对方把这个功能抽象成这几个参数返回另一个参数的函数，只能按照对方的函数实现思路来完成函数。



按题目要求要通读Ant.py，之后解锁problem0，接着才是往下做。但是GameState、Place、Hive什么的，估计读了也不知道那些变量具体什么意思、有什么用处。等我到了具体problem再去看problem对应的几个class吧。

### problem1

Problem 1仅需要观察Ant这个类，然后设置food_cost和gamestate.food的自增功能。

读完描述，在code里修改一些部分就可以了。

### problem2

#### 初步审题

这个problem需要重读一下Place的概念，然后应该可以感觉出place组成的tunnel或者colony其实是由link instance组成的linked list。place的entrance和exit，类似双向链表里的pre和next。

Code里说`    # Phase 1: Add an entrance to the exit  `  ，应该是创建一个新的place，然后新place的entrance连接原先的exit，具体怎么做，真的参悟不透，只能看hint video了。Project1和Project2我还能直接跳过hint video的，到了project3真的是只能指望别人hint了，看来class的使用还有大project的接收能力都要在未来强化一下。

Hint video解释了这句话

>   `Place.__init__` should use this logic:
>
>   - A newly created `Place` always starts with its `entrance` as `None`.
>   - If the `Place` has an `exit`, then the `exit`'s `entrance` is set to that `Place`.

显然第一句就是init里面的name赋值和exit赋值，第二句的exit's entrance就基本上是说`self.exit`其实也是一个place。这个place.entrance就是self的这个place

#### 审题与理解

理解了这玩意，再用`python3 ok -q 02 -u`去unlock一下，确保自己理解无误再思考如何用代码实现这个逻辑。

```markdown
Problem 2 > Suite 1 > Case 2
(cases remaining: 4)

Q: p is a Place whose entrance is q and exit is r (q and r are not None). When is p.entrance first set to a non-None value?
Choose the number of the correct choice:
0) Never, it is always set to None
1) When q is constructed
2) When p is constructed
? 1
-- OK! --

---------------------------------------------------------------------  
Problem 2 > Suite 1 > Case 3
(cases remaining: 3)

Q: p is a Place whose entrance is q and exit is r (q and r are not None). When is p.exit first set to a non-None value?
Choose the number of the correct choice:
0) When q is constructed
1) Never, it is always set to None
2) When p is constructed
? 2
-- OK! --
```

遇到上面的问题得出下面的结论：

```python
        # r<-p<-q
        # 当q创建的时候，q.entrance=None, q.exit=p
        # 所以创建p的时候，p.entrance=q，而q.exit=r
```



然后又遇到新的问题，需要读一下Hive和GameState这两个类了

```markdown
Problem 2 > Suite 2 > Case 1
(cases remaining: 2)

>>> from ants import *
>>> from ants_plans import *
>>> #
>>> # Create a test layout where the gamestate is a single row with 3 tiles
>>> beehive, layout = Hive(make_test_assault_plan()), dry_layout       
>>> dimensions = (1, 3)
>>> gamestate = GameState(None, beehive, ant_types(), layout, dimensions)
>>> #
>>> # Simple test for Place
>>> place0 = Place('place_0')
>>> print(place0.exit)
? None
>>> place1 = Place('place_1', place0)
>>> place1.exit is place0
?
```

`place1 = Place('place_1', place0)`解题重点来了！Place里的constructor是这样的`__init__(self, name, exit=None)`，如果新的instance place1的exit就是place0，那么place0就是新创建的place1的出口。而且方式就是place1.exit=place0，在init里面把当前的place1换成self即可。

接下来的这两个描述应该就是解题关键，place1在前，称为previous_place；place0在后，称为next_place。那么`previous_place.exit=next_palce`，且`next_place.entrance=previous_place`。

```markdown
>>> place1.exit is place0
? True
-- OK! --

>>> place0.entrance is place1
? True
```

#### 解题思路

所以解题思路如下：

每次出现`new_place = Place('new', place0)`，则说明这个new_place就是place0的前方的place，所以还要做的事情就是把`place0`的`entrance`跟`new_place`联系到一起。这就对应了那句：*If the `Place` has an `exit`, then the `exit`'s `entrance` is set to that `Place`.*

> 句子里的the `Place`就是`new_place`或者就是`self`，它传入的`exit`不是None，那么就是有一个`exit`。
>
> 然后句中的`exit`也是一个`place`，对应`new_place`这个例子里的`place0`。
>
> 之后有`exit`'s `entrance` is set to that `Place`，就是说把`place0`的`entrance`跟`new_place`划等号

然后结果就是

```python
self.exit.entrance=self
```

这么简单的一句话，结果饶了这么多圈子，我从reading problems, reading codes到watching hint video和doing unlock problems共花了1.5h，最后想明白之后，花了1分钟写下这段代码，然后直接`5 test cases passed! No cases failed.`

当然了，这样会有bug，就是创建第一个place的时候，exit是None，没有下一个place，无法这样赋值。所以应该加一个条件：`self.exit!=None`。

#### 反思

真的是伤脑经，整个problem2其实就是在创建新place的时候，是从左往右创建的，现有一个exit和entrance都是None的place0。然后以place0为出口创建一个place1，这个place1.exit就是place0，而且这一步在新建place1的参数传递过程就就完成了。

这时place1.entrance是None，因为place1的右边是空的。但是呢place0.entrance也是空的，因为创建place0的时候，entrance设置为None，之后一直没改。所以新建了place1，要把place0.entrance也修改为place1才行。但是没法直接`place0.entrance = place1`，新建place1的时候，self是place1，所以就有了赋值的逻辑是`self.exit.entrance=self`。



发现Problem的考点都在于init里面，bound method几乎没用到，估计是因为init涉及几个class的基本概念理解。如果这些instance variables是什么意思都不知道，没法完成基本功能构建，更没法做一个复杂的method了。



### problem 3

ThrowerAnt是有一个place的attribute的，这个继承Insect的属性，所以一个ThrowerAnt的instance可以self.place。

如果这个place有bee，那么就攻击这个place上面的某一个bee，用`choose_bee(self.place.bees)`来返回该地址的某一个bee

如果当前place和front的place都没有bee，那么return None，没有可攻击的对象。

还要注意hive==True的话，该处也是return None（a `ThrowerAnt` will `throw_at` the nearest bee **that is not still in the `Hive`**

而且Hint里说，一个place里是否有bee，用到了Place里的一个属性，叫做self.bees，这是一个有bee instance组成的list。既可以用来检查是否有bee，也可以用于`choose_bee(self.place.bees)`

看了reading material和code，顺便看一下hint video强化理解，之后就有了基本代码的逻辑了，还是比较容易理解和写代码的，直接进入unlock。



#### 解题思路



因为hive总是在last_place的entrance，就是tunnel结束后还有一个hive，target_place从self.place一直移动到hive（target_place.is_hive==True)。

problem 4则是从min_place移动到max_place

```python
        #recursive solution
        def helper(place):
        # self is the instance of the thrower ant
        # but the function is recusive over the place the ant is at
        # so a helper function is implemented to use the self.place as argument and recursive over self.place.entrance.entrance....
            if place.is_hive: #hive总是在last_place的entrance
                return None	
            else:
                if place.bees:
                    return choose_bee(place.bees)
                else:
                    return helper(place.entrance)
            
        return helper(self.place)
        # END Problem 3
```





按照上面的逻辑写就能解决问题，Phase1的难点在于理解题目的逻辑，这个理解了很快就有能想出题目的思路，而且用代码实现起来也很容易。

> PS：而之前的Tree recursion和Trees的题目意思容易理解，但是很难想出解题的思路，更不要提用代码实现了。说来Trees一定要把几个Lab、HW和Discussion里的optional的相关题目做一遍，乃至tutorial的题目也做一遍，不然太生疏了。（Higher Order Function则是要在有代码的情况下理清楚多个function之间的关系，那个也是个难点。



> 写作业的难点在于没思路或者卡bug，学新课的难点在于新的知识难以理解。



## Phase 2



### problem4

没有什么难点，在原先`nearest_bee(self)`的基础之上修改成为`min_range`和`max_range`之间有bee的话，才会返回那个choose函数。

有两种思路，一个是iteration，一种是recursion





```python
        #recursive solution
        def helper(place,curr_range):#把place.entrance传入place就实现了右移的操作
        # self is the instance of the thrower ant
        # but the function is recusive over the place the ant is at
        # so a helper function is implemented to use the self.place as argument and recursive over self.place.entrance.entrance....
            if place.is_hive:
                return None
            elif curr_range < self.min_range:
                return helper(place.entrance,curr_range + 1)
            elif curr_range > self.max_range:
                return None
            elif place.bees:
                return choose_bee(place.bees)
            else:
                return helper(place.entrance,curr_range + 1)
        return helper(self.place,0)
        # END Problem 3 and 4
```



### problem 5

`FireAnt`下的`reduce_health(self, amount)`这个method功能就是FireAnt减少amount生命值，同时FireAnt会让`self.place`上所有bee都减少amount生命值。

题目提示要用Insect的`reduce_health`函数，所以就用`Insect.reduce_health(ant or bee, amount)`。

#### 解题思路

method实现的思路如下：

> 先`Insect.reduce_health(self, amount)`，把当前受到攻击的FireAnt的血量计算一下。
>
> 如果self.health<=0（当前FireAnt死了），amount就要加上FireAnt的damage，然后反击给当前place上的所有bee；如果当前FireAnt没死，那就反击的amount保持不变。
>
> 反击给bees的话，遍历bees的list，对每个bee，都有`Insect.reduce_health(bee, amount)`，这样就完成了FireAnt被攻击和反击的操作，本method也完成了所有功能。

#### bug提醒

但是一些细节要修改一下，调用`Insect.reduce_health(ant or bee, amount)`之后，ant或者bee有可能会被消灭，从而`self.place`和 `place.bees[index]`都会变化。

所以在FIreAnt被攻击之前，用`current_place`来存储`self.place`，不然self被消灭之后`self.place`就是`None`了。

另外就是把bees的这个list另外存给一个`bee_list`，不然如果bees只有两个bee，bees[0]被反击消灭之后，bees[1]就越界了。因此`bee_list=list(current_place.bees)`或`bee_list=current_place.bees[:]`，这样的话`bee_list is not current_place.bees`就是`True`。

```python
    
        Insect.reduce_health(bee_list[index],amount) 
        # 所有的Insect.reduce_health(self,amount)换成 super().reduce_health(amount)
        # Ant.reduce_health(self,amount)也对，Ant.reduce_health(self,amount)
        # Ant.reduce_health = lambda self, amount : print("reduced")
        # 在Ant里面没有reduce_health，所以Ant创建一个reduce_health，super()就是返回到上一层的Ant，而Insect里面没有lambda
        # super().reduce_health(amount)可以被lambda覆盖
        # Insect.reduce_health(self,amount)不能被lambda覆盖
        # 前者才是正确的调用，后者跳了class，不合法
        
        # 所以Ant.reduce_health(bee_list[index],amount) 或者super().reduce_health()

        
        
    	print("DEBUG:",bee_list)
        # reduce会让place里的bee[0]消灭，但是bee_list放的是bees的指针
        # 如果bees[0]被消灭，bee_list还是两个，但是bee_list[0]变成Bee(-1,None)了
```

最后就是有个bug，题目给一个没有bees的情况，但是让FireAnt受到伤害

```markdown
>>> Ant.__init__ = original>>> fire = FireAnt()>>> original = Ant.reduce_health>>> Ant.reduce_health = lambda self, amount: print("reduced") #If this errors, you are not calling the inherited method correctly>>> place = gamestate.places['tunnel_0_4']>>> place.add_insect(fire)>>> fire.reduce_health(1)
```

遇到这个情况，用`print("DEBUG:",current_place.bees)`语句会发现没有bees，这样的话不会进入for循环，而题目要求print一个reduced，所以就单独判断`bees==[]`的时候，print("reduced")并且return None即可。

`>>> Ant.reduce_health = lambda self, amount: print("reduced") `是在Ant类里面创建一个class atrribute, 这个attribute叫做reduce_health，他是一个lambda function 的name



## Phase 3

problem 6 WallAnt，很简单

problem 7 HungryAnt 跟着description写代码就可以，连hint video都不需要看

problem 8 ContainerAnt 要修改的地方有很多处，不过都是小改动，有了前5个problem的基础，思路写起来比较轻松，也不需要看hint video。按照problem description一块一块写代码，实现各个method的功能，有问题的时候根据报错信息来修改即可。

Add container的时候要

remove container的时候，要先container的ant_contained给放到place上，再remove该container

## Phase 4



problem 10就是添加一个Water，Place的subclass，只需要implement `add_insect` method即可，如果防水就pass，不防水就reduce_health(self.ant.health)即可，没有难度。

problem 11的内容是添加一个ScubaThrower，没给框架，要从白板开始写。要注意的是不是`class ScubaThrower(Ant)`，而是`class ScubaThrower(ThrowerAnt)`，按题目要求把class attribute给写好，再写一个init method即可，没难度。

### problem EC QueenAnt

EC会得到Extra Credit，需要做一下。

审题后大致理解如下，首先QueenAnt有init、action和reduce_health三个method，分别是构造函数，加buff函数和自身受攻击的函数。

按照题目要求的三个要点，理解如下：

- 如果queen的health变为0，bees win。调用的bees_win()函数的情景应该是在reduce_health的method。
- action里给后面的ant加buff之前，要判断Queen是true_queen还是imposter。如果是imposter，要给imposter的health降为零，并且从place移除imposter
- remove_from不能移动true_queen，Ant里面的`remove_from(self, place)`已经做过一次跟container相关的修改，如今要再做一次如果self是true_queen，那么直接pass，不是true_queen才做之前的remove操作

#### 解题思路

这个问题比较杂乱，因为代码中有很多个`Problem EC`的分块，要在很多个地方进行相关修改，除了QueenAnt里的init, action和reduce_health，还要再Ant里的remove_from和Ant里的buff(self)进行修改，大方向上修改的内容有三块。

- init method里要有一个true_queen和imposter的标记，因为创建一个QueenAnt的instance的时候就要标记了，至于imposter如何处理，那是在action函数里进行的。

- action是QueenAnt的操作，QueenAnt有三个角色，imposter must die，thrower at bee和 double the damage

  - 先判断如果不是true_queen，要给imposter的health降为零，并且从place移除imposter。

  - 之后是正常的Super().action(gamestate)继承射手的老本行，先随意攻击一个nearest_bee

  - 之后再给它身后的每一个ant加buff。需要对place进行迭代，迭代的index_place则访问其中的ant，使用Ant.buff(index_place.ant)来加buff。 

    - Ant里的buff(self)也需要填充内容。self是index_place.ant，要么是一个ant要么是一个None。而且还要判断该ant是否被加过buff，所以需要Ant里有一个默认为False的class attribute，称其为`buffed`，而且经历过`self.damage*=2`加倍的ant要把`buffed`置为True，这样以后遇到`buffed==True`的判断就不再`self.damage*=2`了。

    - 这里有多个判断，除了判断是否是Queen，还要判断是否加过buff，最后还有一个Container肚子里的ant也要加倍，判断的

    - ```python
              # 首先判断self是否是Ant #这一层判断是因为我们传入的self是Queen里的action，self是place上的ant，它要么是ant要么是None        # 是 判断self是否被加过buff        #    是 pass        #    否 加buff，用self.damage*=2        # 否 pass        # #self有可能是一个container，要另外考虑self内部的东西加buff        # 首先判断self是否是ContainerAnt        # 是 需要判断inner_ant是否要被加buff，如果inner_ant是否被加过buff？        #    是 pass        #    否 inner_ant.damage*=2        # 否 pass
      ```

- reduce_health 不是直接引用super()的reduce_health，而是health-=amount，如果health<=0直接调用Bees_win()结束游戏。

