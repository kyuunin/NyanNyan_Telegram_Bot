import logging
logger = logging.getLogger(__name__)

from ..utils import RotDict, exceptions as ex
from .player import Player
from .card import Card
from .state import Phase1
from collections import Iterable

class Game:
    def __init__(self, rule):
        self.rule = rule
        self.players = RotDict()
        self.order = True
        self.top_card = None
        while not self.top_card:
            self.top_card = Card.draw(1)[0].place()
        self.multiplier = 1
        self.turns = 1
        self.state = Phase1
        
    def player(self,player):
        try:
            if isinstance(player, Player):
                player = player.id
            return self.players[player]
        except:
            pass
        raise ex.PlayerNotFound
        
    def hand(self,player):
        if isinstance(player, str):
            hand = self.player(player).hand
        elif isinstance(player, Iterable):
            hand = player
        else:
            hand = self.player(player).hand
        return hand

    @property
    def active_player(self):
        return self.players.val
        
    def actions(self, player):
        return self.state.actions(self.player(player), self.active_player)
    
    def do(self, player, action, option):
        action.do(player,self,option)
    
    def playable_cards(self, player):
        hand = self.hand(player)
        return [(card, self.rule.can_play(card,self)) for card in hand]
        
    def play_card(self, player, card):
        hand = self.hand(player)
        if not self.rule.can_play(hand[card],self):
            raise RuntimeError #custom error
        place = hand[card].place()
        if place:
            self.top_card = place
        del hand[card]
        self.end_turn()
        
    def end_turn(self):
        player = self.active_player
        if player.skips == 0:
            self.next()
        else:
            player.skips -= 1
        
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
