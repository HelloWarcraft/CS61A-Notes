# Lecture16 Inheritance的一些要点



## Attribute Assignment Statements

```python
class Account:
    """An account has a balance and a holder.

    >>> a = Account('John')
    >>> a.holder
    'John'
    >>> a.deposit(100)
    100
    >>> a.withdraw(90)
    10
    >>> a.withdraw(90)
    'Insufficient funds'
    >>> a.balance
    10
    >>> a.interest
    0.02
    """

    interest = 0.02  # A class attribute

    def __init__(self, account_holder):
        self.holder = account_holder
        self.balance = 0

    def deposit(self, amount):
        """Add amount to balance."""
        self.balance = self.balance + amount
        return self.balance

    def withdraw(self, amount):
        """Subtract amount from balance if funds are available."""
        if amount > self.balance:
            return 'Insufficient funds'
        self.balance = self.balance - amount
        return self.balance


class CheckingAccount(Account):
    """A bank account that charges for withdrawals.

    >>> ch = CheckingAccount('Jack')
    >>> ch.balance = 20
    >>> ch.withdraw(5)
    14
    >>> ch.interest
    0.01
    """

    withdraw_fee = 1
    interest = 0.01

    def withdraw(self, amount):
        return Account.withdraw(self, amount + self.withdraw_fee)
    # 	amount=amount+1
    # 	if amount > self.balance:
    #         return 'Insufficient funds'
    #     self.balance = self.balance - amount
    #     return self.balance
    #	缺点在于如果Account里的withdraw()变化了，subClass里的withdraw()没法自动跟着Account改变
```

`class CheckingAccount(Account):`的CheckingAccount里面是一个class，为什么后来会有`CheckingAccout('John')`里面装一个string？

Tom.ac=Account('Tom')，这是用Account的构造方法来创建新对象，CheckingAccount是Account的子类，因此子类创建新对象的方式也可以类似，比如John.ac=CheckingAccout('John')

同样可以在CheckingAccount的括号里放一个类，比如放入Tom.ac：`Jack.ac=CheckingAccount(Tom.ac)`，那么Jack.ac就是Tom.ac的子类，他俩在Account类里面的数据是一样的（因为Jack.ac继承了Tom.ac的数据）。而John.ac就跟Tom.ac的数据没关系，数据都是初始数据。



## Inheritance and Attribute Lookup

![image-20210722205414550](https://pica.zhimg.com/80/v2-0c170747bff5386834fbeec40d826cfd_720w.png)

这个例子卡了很久，对`B(1)`，`C(2)`这样的创建出来的新instance没办法很快接受，然后又遇到`b.n=5`，迎应接不暇了。

看到题目后来给出Class&Instance的Frame，感觉挺有帮助的。不然真的很容易搞混class与instance，还有搞混两者内部的变量。



> 以前没学过OOP，类、对象、继承之类的概念，一个lecture听了2h，有些要多多练习听力和多预习了。

