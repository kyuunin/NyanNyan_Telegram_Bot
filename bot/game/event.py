from abc import ABC
class Event(ABC):
    def __init__(self,player):
        self.player = player
    def __repr__(self):
        return type(self).__name__
class Nyan(Event): pass
class NyanNyan(Event): pass
class StartTurn(Event): pass

class EventHandler:
    def __init__(self):
        self.events = {}
    def register(self,event,fun = None):
        def inner(fun):
            self.events[event] = fun
            return fun
        return inner if fun is None else inner(fun)
    def __call__(self, game, event):
        self.events[type(event)](game,event)
        

