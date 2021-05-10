import logging
logger = logging.getLogger("rule")

from .card import Card,Ranks
from .state import *

def skip(player):
    player.skips += 1

effects = {}
def add_effect(fun):
    effects[getattr(Ranks,fun.__name__)] = fun
@add_effect
def _2(game):
    game.mod_players(skip,1,2*game.multiplier)
    game.multiplier = 1
    game.end_turn()
@add_effect
def _3(game):
    if game.block:
        game.block = 0
    else:
        game.block = game.multiplier
        game.first = game.active_player
        game.multiplier = 1
    game.end_turn()
@add_effect
def _4(game):
    game.state=Draw(4*game.multiplier)
    game.multiplier = 1
    game.end_turn()
@add_effect
def _5(game):
    game.end_turn()
@add_effect
def _6(game):
    game.end_turn()
    
play_on_7 = {Ranks._7}
@add_effect
def _7(game):
    if type(game.state) == Draw:
        game.state=Draw(game.state.n+2*game.multiplier,play_on_7)
    else:
        game.state=Draw(2*game.multiplier,play_on_7)
    game.multiplier = 1
    game.end_turn()
@add_effect
def _8(game):
    game.mod_players(skip,1,game.multiplier)
    game.multiplier = 1
    game.end_turn()
@add_effect
def _9(game):
    game.order = not game.order
    game.end_turn()
@add_effect
def _10(game):
    game.turns += game.multiplier
    game.multiplier = 1
    game.end_turn()
@add_effect
def _J(game):
    game.state=Suit
@add_effect
def _Q(game):
    #TODO case 5
    cards = Card.draw()
    if cards[0] == Card.Joker:
        game.active_player.hand += cards
        game.end_turn()
    else:
        game.rule.play_card(cards,0,game)
@add_effect
def _K(game):
    game.state=Choose(game.multiplier, skip)
    game.multiplier = 1
@add_effect
def _A(game):
    game.multiplier *= 2
    game.end_turn()
    
rules = {}
def add_rule(name, rule):
    rules[name] = rule

class Rule:
    def init_game(self,game):
        game.order = True
        game.multiplier = 1
        game.turns = 1
        game.state = Phase1
        game.block = 0
        game.first = None
        game.answers = {}
    def __init__(self, effects):
        self.effects = effects
    def can_play(self, card, game, player):
        if game.block:
            return card == Card.Joker or card.rank_value == Ranks._3
        return (card.can_play(game.top_card) or card.rank_value == Ranks._J) and game.state.can_play(card,game,player)
    def play_card(self, hand, card_id, game, player = None):
        card = hand[card_id]
        if game.state == Answer:
            effect, n = game.answers[player]
            if n == 1:
                del game.answers[player]
            else:
                game.answers[player] = effect, n-1
            if not len(game.answers):
                game.state = Phase1
                game.end_turn()
        else:
            if card != Card.Joker:
                game.top_card = card
                if card.rank_value in self.effects:
                    self.effects[card.rank_value](game)
                else:
                    game.end_turn()
            else:
                game.end_turn()
        del hand[card_id]
        if game.state == Phase2:
            game.state = Phase1
            
add_rule("MauMau", Rule({k:v for k,v in effects.items() if k in {Ranks._7,Ranks._8,Ranks._J}}))
add_rule("NyanNyan", Rule(effects))
add_rule("Null", Rule({}))
    
       
