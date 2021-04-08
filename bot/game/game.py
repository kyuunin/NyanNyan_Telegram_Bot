import logging
logger = logging.getLogger("game")

from ..utils import RotDict, exceptions as ex
from .player import Player
from .card import Card
from .state import Phase1
from .event import *
from collections import Iterable

class Game:
    def __init__(self, rule, event):
        self.event = event
        self.rule = rule
        self.players = RotDict()
        self.top_card = None
        while not self.top_card:
            self.top_card = Card.draw(1)[0].place()
        
    @property
    def rule(self):
        return self._rule
    @rule.setter
    def rule(self,val):
        val.init_game(self)
        self._rule = val
        
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
        return self.state.actions(self.player(player), self)
    
    def do(self, player, action, option):
        if action not in self.actions(player):
            raise RuntimeError #custom error
        action.do(player,self,option)
        
    
    def playable_cards(self, player):
        hand = self.hand(player)
        return [(card, self.rule.can_play(card,self,player)) for card in hand]
        
    def play_card(self, player, card_id):
        player = self.player(player)
        hand = self.hand(player)
        if not self.rule.can_play(hand[card_id],self,player):
            raise RuntimeError #custom error
        self.rule.play_card(hand, card_id, self, player)
        if len(hand)==1:
            self.event(self,Nyan(player))
        if len(hand)==0:
            self.leave(player)
            self.event(self,NyanNyan(player))
       
    def end_turn(self):
        if self.turns == 1:
            player = self.next().val
            while player.skips != 0:
                player.skips -= 1
                player = self.next().val
            self.event(self,StartTurn(player))
        else:
            self.turns -= 1
    
    def mod_players(self,fun,start=0,end=None):
        start = None if start is None else start if self.order else -start
        end = None if end is None else end if self.order else -end
        self.players.apply(fun,start,end)
    def reverse(self):
        self.order = not self.order
                
    def next(self):
        return self.players.rot(self.order)
        
    def next_player(self):
        pass
                
    def join(self,player):
        if player.id in self.players:
            logger.info(f"{player} already joined")
            raise ex.AlreadyJoined
        logger.info(f"{player} joined with hand {player.hand}")
        self.players[player.id] = player
        
    def leave(self,player):
        player = self.player(player)
        del self.players[player.id]
