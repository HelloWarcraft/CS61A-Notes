# Lab07中的Magic: The Lambda-ing

Magic游戏的规则如下，这个游戏附带有几个子问题，一开始没理解游戏的规则和游戏操作对象是什么东西，卡了挺久。

> ## Magic: The Lambda-ing
>
> In the next part of this lab, we will be implementing a card game! This game is inspired by the similarly named [Magic: The Gathering](https://en.wikipedia.org/wiki/Magic:_The_Gathering).
>
> You can start the game by typing:
>
> ```
> python3 cardgame.py
> ```
>
> **This game doesn't work yet**. If we run this right now, the code will error, since we haven't implemented anything yet. When it's working, you can exit the game and return to the command line with `Ctrl-C` or `Ctrl-D`.
>
> This game uses several different files.
>
> - Code for all the questions in this lab can be found in `classes.py`.
> - Some utility for the game can be found in `cardgame.py`, but you won't need to open or read this file. This file doesn't actually mutate any instances directly - instead, it calls methods of the different classes, maintaining a strict abstraction barrier.
> - If you want to modify your game later to add your own custom cards and decks, you can look in `cards.py` to see all the standard cards and the default deck; here, you can add more cards and change what decks you and your opponent use. If you're familiar with the original game, you may notice the cards were not created with balance in mind, so feel free to modify the stats and add/remove cards as desired.
>
> **Rules of the Game** This game is a little involved, though not nearly as much as its namesake. Here's how it goes:
>
> There are two players. Each player has a hand of cards and a deck, and at the start of each round, each player draws a random card from their deck. If a player's deck is empty when they try to draw, they will automatically lose the game. Cards have a name, an attack statistic, and a defense statistic. Each round, each player chooses one card to play from their own hands. The card with the higher *power* wins the round. Each played card's power value is calculated as follows:
>
> ```
> (player card's attack) - (opponent card's defense) / 2
> ```
>
> For example, let's say Player 1 plays a card with 2000 attack/1000 defense and Player 2 plays a card with 1500 attack/3000 defense. Their cards' powers are calculated as:
>
> ```
> P1: 2000 - 3000/2 = 2000 - 1500 = 500
> P2: 1500 - 1000/2 = 1500 - 500 = 1000
> ```
>
> So Player 2 would win this round.
>
> The first player to win 8 rounds wins the match!
>
> However, there are a few effects we can add (in the optional questions section) to make this game a bit more interesting. Cards are split into Tutor, TA, and Professor types, and each type has a different *effect* when they're played. All effects are applied before power is calculated during that round:
>
> - A Tutor card will cause the opponent to discard and re-draw the first 3 cards in their hand.
> - A TA card will swap the opponent card's attack and defense.
> - A Professor card will add the opponent card's attack and defense to all cards in their deck and then remove all cards in the opponent's deck that share its attack *or* defense!
>
> These are a lot of rules to remember, so refer back here if you need to review them, and let's start making the game!

## 解题过程

对于Cards可以按照class里constructor method和general method理解一下属性和power()之类的东西，到了player和deck就卡住了。对player问题下的第一个doctest无法理解，而且不懂什么是deck。

### Q4: Making Cards

下面是题目描述

> To play a card game, we're going to need to have cards, so let's make some! We're gonna implement the basics of the `Card` class first.
>
> First, implement the `Card` class constructor in `classes.py`. This constructor takes three arguments:
>
> - the `name` of the card, a string
> - the `attack` stat of the card, an integer
> - the `defense` stat of the card, an integer
>
> Each `Card` instance should keep track of these values using instance attributes called `name`, `attack`, and `defense`.
>
> You should also implement the `power` method in `Card`, which takes in another card as an input and calculates the current card's power. Check the Rules section if you want a refresher on how power is calculated.
>
> ```python
> class Card:
>     cardtype = 'Staff'
> 
>     def __init__(self, name, attack, defense):
>         """
>         Create a Card object with a name, attack,
>         and defense.
>         >>> staff_member = Card('staff', 400, 300)
>         >>> staff_member.name
>         'staff'
>         >>> staff_member.attack
>         400
>         >>> staff_member.defense
>         300
>         >>> other_staff = Card('other', 300, 500)
>         >>> other_staff.attack
>         300
>         >>> other_staff.defense
>         500
>         """
>         "*** YOUR CODE HERE ***"
> 
>     def power(self, opponent_card):
>         """
>         Calculate power as:
>         (player card's attack) - (opponent card's defense)/2
>         >>> staff_member = Card('staff', 400, 300)
>         >>> other_staff = Card('other', 300, 500)
>         >>> staff_member.power(other_staff)
>         150.0
>         >>> other_staff.power(staff_member)
>         150.0
>         >>> third_card = Card('third', 200, 400)
>         >>> staff_member.power(third_card)
>         200.0
>         >>> third_card.power(staff_member)
>         50.0
>         """
>         "*** YOUR CODE HERE ***"
> ```
>
> Use Ok to test your code:
>
> ```
> python3 ok -q Card.__init__
> python3 ok -q Card.power
> ```

这两个程序填空还是比较简单的，Cards里有name，attack和defense这三个instance variables，然后一个power()的method，至于其中的self则是代指current instance。

> （还是 [mini lecture](https://youtu.be/5uNdgu4mxxQ) 手把手写一个class，我才懂self的来历，其他教程都没解释这个self，尤其是国内北理和浙大的python讲到类与对象这一块的时候，都没有白板编程的过程，就漏了self的解释，让人一直有这个一个疑惑漏洞）

构造函数里的name,attack和defense是传入的参数，self.name之类的才是具体对象(或者叫具体实例)的属性，所以有self.name=name之类的。

至于power函数，则是一个公式` (player card's attack) - (opponent card's defense)/2` 放入power函数之中即可。

### Q5: Making a Player

下面是Q5的题目描述

> Now that we have cards, we can make a deck, but we still need players to actually use them. We'll now fill in the implementation of the `Player` class.
>
> A `Player` instance has three instance attributes:
>
> - `name` is the player's name. When you play the game, you can enter your name, which will be converted into a string to be passed to the constructor.
> - `deck` is an instance of the `Deck` class. You can draw from it using its `.draw()` method.
> - `hand` is a list of `Card` instances. Each player should start with 5 cards in their hand, drawn from their `deck`. Each card in the hand can be selected by its index in the list during the game. When a player draws a new card from the deck, it is added to the end of this list.
>
> Complete the implementation of the constructor for `Player` so that `self.hand` is set to a list of 5 cards drawn from the player's `deck`.
>
> Next, implement the `draw` and `play` methods in the `Player` class. The `draw` method draws a card from the deck and adds it to the player's hand. The `play` method removes and returns a card from the player's hand at the given index.
>
> > Call `deck.draw()` when implementing `Player.__init__` and `Player.draw`. Don't worry about how this function works - leave it all to the abstraction!
>
> ```
> class Player:
>     def __init__(self, deck, name):
>         """Initialize a Player object.
>         A Player starts the game by drawing 5 cards from their deck. Each turn,
>         a Player draws another card from the deck and chooses one to play.
>         >>> test_card = Card('test', 100, 100)
>         >>> test_deck = Deck([test_card.copy() for _ in range(6)])
>         >>> test_player = Player(test_deck, 'tester')
>         >>> len(test_deck.cards)
>         1
>         >>> len(test_player.hand)
>         5
>         """
>         self.deck = deck
>         self.name = name
>         "*** YOUR CODE HERE ***"
> 
>     def draw(self):
>         """Draw a card from the player's deck and add it to their hand.
>         >>> test_card = Card('test', 100, 100)
>         >>> test_deck = Deck([test_card.copy() for _ in range(6)])
>         >>> test_player = Player(test_deck, 'tester')
>         >>> test_player.draw()
>         >>> len(test_deck.cards)
>         0
>         >>> len(test_player.hand)
>         6
>         """
>         assert not self.deck.is_empty(), 'Deck is empty!'
>         "*** YOUR CODE HERE ***"
> 
>     def play(self, card_index):
>         """Remove and return a card from the player's hand at the given index.
>         >>> from cards import *
>         >>> test_player = Player(standard_deck, 'tester')
>         >>> ta1, ta2 = TACard("ta_1", 300, 400), TACard("ta_2", 500, 600)
>         >>> tutor1, tutor2 = TutorCard("t1", 200, 500), TutorCard("t2", 600, 400)
>         >>> test_player.hand = [ta1, ta2, tutor1, tutor2]
>         >>> test_player.play(0) is ta1
>         True
>         >>> test_player.play(2) is tutor2
>         True
>         >>> len(test_player.hand)
>         2
>         """
>         "*** YOUR CODE HERE ***"
> ```
>
> 
>
> Use Ok to test your code:
>
> ```
> python3 ok -q Player.__init__
> python3 ok -q Player.draw
> python3 ok -q Player.play
> ```



这题从Player的构造函数就开始卡住了，name和deck两个属性，我找deck的意思找了版半天，无法理解什么是deck，代入例子只有`test_deck = Deck([test_card.copy() for _ in range(6)])`，然后发现又要去Deck这个类去理解什么是Deck有那些attribute和method，整的有些乱。想直接写self.hand然后又写不下去，看到hint说可以call deck.draw() without knowing how this function works，但是不理解deck.draw()怎么工作的，自己又无法完成self.hand的赋值。

于是一层一层地先分析Deck类，然后看deck.draw()的原理，最后再代入构造函数的doctest的这个例子。

#### text editor里的Deck类

下面是template里写好的Deck类，题目并不需要自己写一个Deck类，而是需要理解Deck类的组成与作用。

```python
########################################
# Do not edit anything below this line #
########################################

class Deck:
    def __init__(self, cards): 
        """
        With a list of cards as input, create a deck.
        This deck should keep track of the cards it contains, and
        we should be able to draw from the deck, taking a random
        card out of it.
        """
        self.cards = cards

    def draw(self):
        """
        Draw a random card and remove it from the deck.
        """
        assert self.cards, 'The deck is empty!'
        rand_index = random.randrange(len(self.cards))
        return self.cards.pop(rand_index)

    def is_empty(self):
        return len(self.cards) == 0

    def copy(self):
        """
        Create a copy of this deck.
        """
        return Deck([card.copy() for card in self.cards])

```

一直往下滑之后发现有一个不要修改的区域，里面是Deck的一个构造方法和三个实例方法，构造方法里只有一个cards，而`cards`是什么？由doctest的`Deck([test_card.copy() for _ in range(6)])`这个例子可以推断出`[test_card.copy() for _ in range(6)]`就是一个`cards`。

而`test_card.copy()`是啥，找到Card类里的instance method，发现`test_card.copy()`返回的是`Card(self.name, self.attack, self.defense)`，也就是Card类的一个对象或者一个实例，因此推断出cards is a list of Card instances，就是一个由牌组成的列表，这个牌是Card类的实例。这张牌的构造方法里有名字、攻击和防御三个属性，同时这个牌有power effect repr和copy四个方法。

而重新理解Deck，在翻译出来的词里面可以找到一个概念：牌组。Deck类的构造方法里只有一个属性就是cards，一组牌，显然Deck就是牌组的意思，Deck的实例会由一个牌组的属性，此外由三个实例方法：draw, is_empty和copy。

#### deck.draw()的原理

既然Deck是一个牌组类，deck就是牌组类的一个实例，`deck.draw()`就是Deck类里的draw()，（因为Player里也有一个draw），Deck里的draw()如下：

```python
    def draw(self):
        """
        Draw a random card and remove it from the deck.
        """
        assert self.cards, 'The deck is empty!'
        rand_index = random.randrange(len(self.cards))
        return self.cards.pop(rand_index)
```

显然`deck.draw()`的值就应该是`deck.cards.pop(rand_index)`，`deck.cards`之前已经讨论过，是一些Card实例的列表，这个列表里pop出来一个random index的元素，这个排出来的元素就是`deck.draw()`了。

怎么看，都像是deck里原来有n个Card实例，显然随机打出一张牌，打出的这张牌就是`deck.draw()`，而`deck.cards`这个列表自然就少了一张牌。

#### Player构造函数里的doctest

```python
        A Player starts the game by drawing 5 cards from their deck. Each turn,
        a Player draws another card from the deck and chooses one to play.
        >>> test_card = Card('test', 100, 100)
        >>> test_deck = Deck([test_card.copy() for _ in range(6)])
        >>> test_player = Player(test_deck, 'tester')
        >>> len(test_deck.cards)
        1
        >>> len(test_player.hand)
        5
```

首先由一个Card类的实例`test_card`，它的构造函数里的属性为姓名'test'，攻击和防御都是100。`test_deck`则是一个含有6张相同`test_card`牌的Deck实例。

而`test_player = Player(test_deck, 'tester')`之后，就发现`test_deck`这个实例里面的cards属性只有1张牌了，而test_player.hand则变成了一个手里有5张牌的list。显self.hand是类似`test_deck.cards`的list，而且` Player(test_deck, 'tester')`这个构造函数是有6张牌的牌组`test_deck`在给`'tester'`这个人发5张牌。而`deck.draw()`正好就是发牌，因此做5次`self.hand+=[deck.draw()]`即可。

#### Player类里的draw()和play()

已经搞定Deck之后，余下的看doctet理解完题意就可以完成该方法了。



```python
    def draw(self):
        """Draw a card from the player's deck and add it to their hand.
        >>> test_card = Card('test', 100, 100)
        >>> test_deck = Deck([test_card.copy() for _ in range(6)])
        >>> test_player = Player(test_deck, 'tester')
        >>> test_player.draw()
        >>> len(test_deck.cards)
        0
        >>> len(test_player.hand)
        6
        """
        assert not self.deck.is_empty(), 'Deck is empty!'
        "*** YOUR CODE HERE ***"
```

doctest前三句跟之前的一样，都是先创建一个`test_card`的牌实例，然后有创建一个含有6张牌的`test_deck`牌组实例，然后通过`test_player = Player(test_deck, 'tester')`给tester这个人分配5张牌。

之后`player.draw()`，然后就发现`len(test_deck.cards)`减少了1，`len(test_player.hand)`多了1，显然这个`player.draw()`是让player从deck里的cards又要了一张牌到手里。就是利用`self.deck.draw()`再给`self.hand`再发一张牌。



```python
    def play(self, card_index):
        """Remove and return a card from the player's hand at the given index.
        >>> from cards import *
        >>> test_player = Player(standard_deck, 'tester')
        >>> ta1, ta2 = TACard("ta_1", 300, 400), TACard("ta_2", 500, 600)
        >>> tutor1, tutor2 = TutorCard("t1", 200, 500), TutorCard("t2", 600, 400)
        >>> test_player.hand = [ta1, ta2, tutor1, tutor2]
        >>> test_player.play(0) is ta1
        True
        >>> test_player.play(2) is tutor2
        True
        >>> len(test_player.hand)
        2
        """
        "*** YOUR CODE HERE ***"
        # 从>>> test_player.play(0) is ta1可以看出返回的是一个card object
        # test_player.hand = [ta1, ta2, tutor1, tutor2]，依次pop(card_index)，且返回pop的card
        # self.hand是一个card组成的list，从里面pop下标为card_index的card就可以了，而且返回值就是pop值
```

