from random import choices
from abc import ABC
colors = ['\033[33m', '\033[31m', '\033[32m', '\033[34m']
suits = ['♦','♥','♣','♠']
ranks = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']
class Ranks(ABC):
    pass
for i,x in enumerate(ranks):
    setattr(Ranks, f"_{x}", i)
class BaseCard(ABC):
    def can_play(self,other):
        pass
    @property
    def name(self):
        pass
    def place(self):
        pass

class Card(BaseCard):
    class Joker(BaseCard):
        def can_play(self,other):
            return True
        @property
        def name(self):
            return '★'
        def place(self):
            pass
        def __repr__(self):
            return self.name
        def __eq__(self,other):
            return type(self)==type(other)
        def __hash__(self):
            return -1
            
    Joker = Joker()
    @staticmethod
    def draw(k=1):
        return choices(cards,k=k)
    def __new__(cls, id):
        if id >= 52:
            return cls.Joker
        return object.__new__(cls)

    def __init__(self, id):
        self.id = id
    
    def can_play(self,other):
        return (self.rank_value == other.rank_value or 
               self.suit_value == other.suit_value)
    def place(self):
        return self
    @property
    def name(self):
        return self.rank + self.suit
    @property
    def rank_value(self):
        return self.id >> 2
    @property
    def suit_value(self):
        return self.id & 3
    @property
    def rank(self):
        return ranks[self.rank_value]
    @property
    def suit(self):
        return suits[self.suit_value]
    @classmethod
    def color(cls,on):
        if on:
            cls.__repr__ = cls.__repr_color__
        else:
            cls.__repr__ = cls.__repr_no_color__
    def __repr_color__(self):
        return colors[self.suit_value]+self.name+'\033[0m'
    def __repr_no_color__(self):
        return self.name
    __repr__ = __repr_color__
    def __eq__(self,other):
        return type(self)==type(other) and self.id == other.id
    def __hash__(self):
        return self.id
cards = [Card(i) for i in range(55)]
