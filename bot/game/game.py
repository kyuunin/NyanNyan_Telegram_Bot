import logging
logger = logging.getLogger(__name__)

from .player import Player
from ..utils.rotdict import RotDict
from ..utils.exceptions import AlreadyJoinedException, PlayerNotFoundException

class Game:
    def __init__(self):
        self.players = RotDict()
        self.order = True
        
    def player(self,player):
        try:
            if isinstance(player, Player):
                player = player.id
            return self.players[player]
        except:
            pass
        raise PlayerNotFoundException
     
    @property
    def active_player(self):
        return self.players.val
        
    def actions(player):
        pass #TODO
    
    def playable_cards(player):
        pass #TODO
        
    def reverse(self):
        self.order = not self.order
                
    def next(self):
        self.players.rot(self.order)
                
    def join(self,player):
        if player.id in self.players:
            raise AlreadyJoinedException
        self.players[player.id] = player
        
    def leave(self,player):
        player = self.player(player)
        del self.players[player.id]
