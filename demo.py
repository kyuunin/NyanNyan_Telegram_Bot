from bot.game import *
from bot.game.state import Answer
from bot.game.card import Card, cards
from traceback import print_exc
from sys import argv
import os
cls = lambda: None#os.system('clear')
def info(*args,**kwargs):
    cls()
    print(*args,**kwargs)
    
event_handler = event.EventHandler()
@event_handler.register(event.Nyan)
def nyan(game,event):
    states[event.player] = event
    
@event_handler.register(event.NyanNyan)
def nyan_nyan(game,event):
    states[event.player] = event
    
@event_handler.register(event.StartTurn)
def start_turn(game,event):
    player = event.player
    cls()
    input(f"{player}, it's your turn")
    

def dialog():
    while True:
        try:
            if game.state == Answer:
                for player in game.answers:
                    cls()
                    input(f"{player}, you have to Answer?")
            else:
                player = game.active_player
            states[player] = None
            playable_cards = game.playable_cards(player)
            actions = game.actions(player)
            select = int(input(turn_info%{
                "turns": game.turns,
                "states": states,
                "top_card": game.top_card,
                "hand": playable_cards,
                "actions": actions
            }))
            if select == 0:
                card_dict = {i:c[0] for i,c in enumerate(playable_cards) if c[1]}
                print("select card")
                print("\n".join(f"{i:2}: {c}" for i,c in card_dict.items()))
                select = int(input())
                if select in card_dict:
                    game.play_card(player,select)
                    info()
                else:
                    info("Card not Playable")
            elif select == 1:
                print("select action")
                print("\n".join(f"{i:2}: {a}" for i,a in enumerate(actions)))
                action = actions[int(input())]
                print(f"{action} selected")
                options = action.options(player, game)
                if len(options):
                    print("select option")
                    print("\n".join(f"{i:2}: {o}" for i,o in enumerate(options)))
                    option = options[int(input())]
                    print(f"{option} selected")
                else:
                    option = None
                game.do(player,action,option)
                info()   
            else:
                info("Unknown Option")
        except Exception as e:
            print_exc()

turn_start="""
%(player)s,
it's your Turn.
you have %(turns)s turns left"""
turn_info="""Player states: %(states)s
The top card is %(top_card)s.
These is your hand: %(hand)s
and your actions: %(actions)s
Do you want to play a card(0) or make an action(1)
"""
_, rule = argv
game = Game(rules[rule], event_handler)
game.join(Player(0,"Chris",7))
game.join(Player(1,"Denzel",7))
game.join(Player(2,"Franz",7))
game.join(Player(3,"Paul",7))
game.join(Player(4,"Gustav",7))
states = {p:None for p in game.players.values()}
print(states)
game.event(game,event.StartTurn(game.active_player))
dialog()
