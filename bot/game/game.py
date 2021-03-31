import logging
logger = logging.getLogger(__name__)

from ..utils import RotDict, exceptions as ex
from .player import Player
from .card import Card
from .state import NoState

class Game:
    def __init__(self):
        self.players = RotDict()
        self.order = True
        self.top_card = None
        while not self.top_card:
            self.top_card = Card.draw(1)[0].place()
        self._deck = None
        self.multiplier = 1
        self.turns = 1
        self.state = NoState
        
    def player(self,player):
        try:
            if isinstance(player, Player):
                player = player.id
            return self.players[player]
        except:
            pass
        raise ex.PlayerNotFound
    @property
    def deck(self):
        return self._deck
    @deck.setter
    def deck(self,val):
        self.deck = val
        self.top_card = val.draw(1)
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
            raise ex.AlreadyJoined
        self.players[player.id] = player
        
    def leave(self,player):
        player = self.player(player)
        del self.players[player.id]
