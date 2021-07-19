# C语言里的array和Python里的list、tuple和dictionary对比

## array与list

python里有三种常见的容器(container)：list, tuple和dictionary

以前我以为C里面的array和python里的list最接近，因为list有list[index]， 这个跟array[index]很接近。虽然tuple[index]也有用，但是tuple里的元素是固定的没法修改。dictionary[index]的话，则index必须是key-value pair的key才行，有时候key会是string，比较奇葩。



后来发觉list相比array有个缺点，虽然list[index]与array[index]功能接近，但是没法对list[index]赋值。

> 先考虑一个问题，把一个【1 ，2 ，3】序列的第0个数值换成0，如何实现？

下面这个把{1,2,3}这个array第一个元素改为0的代码，用C语言实现的话，直接给array[0]赋值为0就可以修改：

```c
#include"stdio.h"
int main()
{
	int array[]={1,2,3};
	printf("array[0] is %d",array[0]);
    array[0]=0;
	printf("the changed array[0] is %d",array[0]);
 } 
//array[0] is 1
//the changed array[0] is 0 

//把一个值a赋值给array的第0个位置，我下意识地会array[0]=a
//访问array的第0个位置的值的时候，我下意识地用array[0]
```

但是用python的list的话，只能先list.pop(0)，再用一个单独的[0]+原先的list来实现（如果是把第1个数值换成0，list.pop(1)之后就比较麻烦

(list.pop()里面的argument是index，还有个list.remove()，那个括号里argument是list里的element)

```python
list=[1,2,3]
print("list[0] is %d"%list[0])
#list[0]=0 #这个会Error
list.pop(0)
new_list=[0]+list
print("the changed list[0] is %d"%new_list[0])

'''
list[0] is 0
the changed list[0] is 1
'''
```

这个对list[index]无法赋值的操作，让我有些难受，因为有时候就是需要把list[index]的值换成num，如果index是中间的某个下标，再操作就很难了。而array[index]=num就能直接完成。这让我想到了dictionary，dictionary[index]=num就可以完成！

所以array与list有一些共同点，与dictionary也有一些共同点，值得深入探讨一下他们的异同与联系

## array与list和dict区别

tuple其实就是一个不可更改的two-element list，所以忽略了它，仅讨论array、list和dictionary三者的关系。

### 三者区别

#### 三者都是sequence

三者一定程度上可以互换，只要是序列都可以改写成三种格式，比如一个【1，2，3】的sequence可以改写为

```c
array={1,2,3}
```

```python
list=[1,2,3]
```

```python
dictionary={0:1,1:2,2:3}
```

而且`array, list , dictionary`之后都可以在后面加[index]来访问具体的内容（tuple也可以）

#### sequence[index]的区别

如同上面替换sequence数值的例子，某个数值不能直接赋值给list[index]，list[1]='one' 会出现Error，而array和dict可以这样赋值，所以这样看来array和dict比list更优越一些。



但是array有一个缺点，就是array[index]的属性都必须一样，要么都是integer，要么都是string。而list[index]与dict[index]则没有这种要求，可以是不同的属性，比如`list=[1,'two',3]`中`list[0]`是`1`，而`list[1]`是`‘two'`。

### list和dictionary有自己专属的内置函数

array没有内置函数

list的内置函数如下

```python
list=[1,2,3]
list.pop(index)#take index and return list[index], meanwhile list has poped list[index]
#
list.remove(element)#take the element of a list, no returns. list will remove the element
list.append(element)#list will add a new element in the end of the list
list.extend(new_list)#list+new_list (dict1+dict2 is forbidden)
len(list)#return length of the list
```

dictionary的内置函数如下

```python
dictionary={1:'one',2:'two'}
dictionary.keys() # return a list of all the keys
dictionary.values() # return a list of all the values
dictionary.get(key) # return dictionary[key]
dictionary.items() #return dict_items([(1, 'one'), (2, 'two')])，外面再套一个list()或者tuple()就能把dict转化为list或tuple
len(dictionary) #return the length of dictionary

dict(nested_list or list_tuple or nested_tuple) #change list or tuple to dictionary
	>>> dict([(1,2),(3,4)])
    {1: 2, 3: 4}
    >>> dict([[1,2],[3,4]])
    {1: 2, 3: 4}
```

### list与dict的关系

首先，dict的index可以不是数字，而list的index默认是从0开始递增的整数
然后list其实可以用含有tuple的list或者嵌套list来实现dict。比如`nested_list=[[1,'one],[0,'zero]]`，`list_tuple=[(1,"one"),(0,"zero")] `与  `dict={1:"one",0:"zero"}` 在逻辑意义上相等。

> 如果我想把`0对应的字母`替换为`ZERO`的话，直接`dict[0]='ZERO'`即可
>
> 而用`nested_list`的话，则要遍历一下list，找到`nested_list [i] [j]==0`时，把`nested_list [i] [j+1]`的值修改为`‘ZERO'`，而修改嵌套list的值，则更加麻烦。
>
> 用`list_tuple`的话，则tuple内的元素无法修改。

所以dict比list的优越之处在于修改内部某些index对应的element会很方便，dict[index]可以很方便地修改，而list里的element不能修改 



但是list也有优越之处，比如dict很难用内置函数sorted，而把dict转化为list_tuple或者nested_list就可以用了。

> 如果我想把dict里面的元素重新排序，按照key递增的顺序排列，用list_tuple和sorted组合使用就很方便
>
> ```python
> dictionary={1:'one',0:'zero'}
> list_tuple=list(dictionary.items()) # 得到list_tuple=[(1,"one"),(0,"zero")]
> list_tuple_sorted=sorted(list_tuple, key=lambda tuple: tuple[0])
> dictionary=dict(list_tuple_sorted) #这样dictionary就变成了{0:'zero',1:'one'}
> #这里先用list(dict)把dict转成了list，然后又用dict(list)把list转成了dict，可以看出list和dict在特殊情况下可以互相转化
> ```
>
> 而dict和sorted没办法一起使用，原因在于key之后的那个lambda函数，list_tuple里的话，lambda函数输入的是list_tuple的element，也就是tuple，而输出的是tuple[0]，就是1和0这样的数字。
>
> 如果用`sorted(dict, key=lambda tuple: tuple[0]) `，那么lambda函数的输入元素是 `1:'one'`这样的一个key-value pair，这个pair如何没法用pair[0]的方式访问key或者value。所以目前没有办法再sorted里用dict，除非使用`dict.items()`函数
