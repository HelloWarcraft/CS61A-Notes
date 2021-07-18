# 写一个函数来返回一个整数a的最大digit和最小digit

这个是[Project 1: The Game of Hog ](https://cs61a.org/proj/hog/)里面problem 4的函数more_boar( )里的关键部分。

我最开始实现的途径是 `if digit>max: max=digit`的逐个存储的方式，但是感觉还要设置max和min的初始值，解法并不完美。用list列表的话，又每次要`list+=[a%10]`然后每次`a=a//10`，今天跟partner会议讨论[Project 2:  cats-Autocorrected Typing Software ](https://cs61a.org/proj/cats/)之前想起来这个部分还缺少一个perfect solution，就在讨论完毕cats之后又回到了hog的problem 4。



我最初的解法是这样的：

```python
def max_min(a)
    max_a=0 # initial value of max digit
    min_a=9 # initial value of min digit

    temp=a 
    # temp is the substitute of a, b or any input integer
    while temp!=0: # find the max and min digit of a
        digit=temp%10 # 得到digit之后，判断digit与max_a和min_b的关系
        if digit>max_a:
            max_a=digit
        if digit<min_a:
            min_a=digit
        temp=temp//10
    return max_a,min_a
```

显然这个解法不仅每次要通过`temp=temp//10`来迭代，而且还有`min_a`和`max_a`的初始值这种冗余且容易忘记的部分。当时就感觉这个解法并非完美解法，只是满足correctness的拼凑型代码而已，当时就留了一个注释说需要找一个perfect solution，今天在cats之后讨论了一下，发掘两个优化后的版本。

## 优化版本1

`min_a`和`max_a`的初始值可以想到用min(List)的操作来替换，即把temp的每个digit放到List里，然后返回`max(List)`和`min(List)`，这就需要用一个列表List来储存所有的digits

修改如下：

```python
def max_min(a)
	temp=a
    # temp is the substitute of a
    List=[]
    while temp!=0: # find the max and min digit of a
        digit=temp%10 # 得到digit之后，判断digit与max_a和min_b的关系
        List+=[digit]
        temp=temp//10
    return max(List),min(List)
```

## 优化版本2

之后partner又提出一个想法，用str函数，如果a是3456，str(a)可以得到`‘3456’`，这样每一个digit就可以用`str(a)[index]`来访问，进一步地可以用List Comprehesion来实现一个由digits组成的List:
`[(str(a))[index] for index in range(len(s))]`
但是这样的话，如果`a=3456`，得到的List就是`['3','4','5','6']`，虽然可以对该List进行max(List)和min(List)操作，但是得到的是一个字符，其实也问题不大，用`int(character)`函数就可以把character转成数字，例如`int('1')=1`

这个需要对python的已有功能函数有些了解，比如`str(number), int(character)`，这方面我了解的较少，确实有所收获。

用了`str(a)`之后就无需`temp=temp//10`来迭代了，省事儿不少，修改之后的代码如下：

```python
def max_min(a):
    "如何找到一个number的all digits，并且找到其中的max和min呢(不用数组的情况下)，我上面的那个算法不是perfect solution呀"
    #perfect solution
    s=str(a)
    max_a=int(max([s[index] for index in range(len(s))]))
    min_a=int(min([int(s[index]) for index in range(len(s))])
    return max_a,min_a
```
上面这个代码应该是非常简洁和优美的代码了，也算是一次成功的讨论和代码简化，值得记录。
