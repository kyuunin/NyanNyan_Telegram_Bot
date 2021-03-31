from ..utils import singleton
from .action import *
no_actions = []
@singleton
class Phase1:
    def can_play(self, card):
        return True
    def actions(self, player, active_player):
        if player==active_player:
            return [Draw_Card]
        else:
            return no_actions

@singleton
class Phase2:
    def can_play(self, card):
        return True
    def actions(self, player, active_player):
        if player==active_player:
            return [Pass]
        else:
            return no_actions

