from ..utils import singleton
from .action import *
from .card import Ranks, Card
no_actions = ()
@singleton
class Phase1:
    _actions = (Draw_Cards(1),)
    def can_play(self, card, game, player):
        return game.active_player == player
    def actions(self, player, game):
        if player==game.active_player:
            return self._actions
        else:
            return no_actions

@singleton
class Phase2:
    _actions = (Pass,)
    def can_play(self, card, game, player):
        return game.active_player == player
    def actions(self, player, game):
        if player==game.active_player:
            return self._actions
        else:
            return no_actions
@singleton
class Answer:
    _actions = (Pass,)
    def can_play(self, card, game, player):
        return player in game.answers and card == Card.Joker
    def actions(self, player, game):
        if player in game.answers:
            return self._actions
        else:
            return no_actions

class Choose:
    def __init__(self, n, effect):
        self.effect = effect
        self.n = n
    def can_play(self, card, game, player):
        return game.active_player == player
    def actions(self, player, game):
        if player==game.active_player:
            return (Choose_Player(self.effect),)
        else:
            return no_actions
        
@singleton    
class Suit:
    def can_play(self, card, game, player):
        return False
    def actions(self, player, game):
        if player==game.active_player:
            return (Choose_Suit,)
        else:
            return no_actions

class Draw:
    def __init__(self, n, playable=set()):
        self.n = n
        self.playable = playable
    def can_play(self, card, game, player):
        return game.active_player == player and (card == Card.Joker or card.rank_value in self.playable) 
    def actions(self, player, game):
        if player==game.active_player:
            return (Draw_Cards(self.n),)
        else:
            return no_actions
