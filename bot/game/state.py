from ..utils import singleton
from .action import *
from .card import Ranks
no_actions = ()
@singleton
class Phase1:
    _actions = (Draw_Cards(1),)
    def can_play(self, card):
        return True
    def actions(self, player, game):
        if player==game.active_player:
            return self._actions
        else:
            return no_actions

@singleton
class Phase2:
    _actions = (Pass,)
    def can_play(self, card):
        return True
    def actions(self, player, game):
        if player==game.active_player:
            return self._actions
        else:
            return no_actions
@singleton
class Answer:
    _actions = (Answer_Card,)
    def can_play(self, card):
        return True
    def actions(self, player, game):
        if player in game.answers:
            return self._actions
        else:
            return no_actions

class Choose:
    def __init__(self, n, effect):
        self.effect = effect
        self.n = n
    def can_play(self, card):
        return True
    def actions(self, player, game):
        if player==game.active_player:
            return (Choose_Player(self.effect),)
        else:
            return no_actions

class Draw2:
    def __init__(self, n):
        self.n = n
    def can_play(self, card):
        return card.rank_value == Ranks._7
    def actions(self, player, game):
        if player==game.active_player:
            return (Draw_Cards(self.n),)
        else:
            return no_actions
