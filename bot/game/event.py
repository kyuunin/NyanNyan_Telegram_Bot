from abc import ABC
class Event(ABC):
    def __init__(self,player):
        self.player = player
    def __repr__(self):
        return type(self).__name__
class Nyan(Event): pass
class NyanNyan(Event): pass
