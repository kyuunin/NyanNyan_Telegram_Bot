from bot.game import Game, Player
from bot.game.card import Card, cards
from bot.game.rule import Rule
rule = Rule()
game = Game(rule)
game.join(Player(0,"Chris",7))
game.join(Player(1,"Denzel",7))
game.join(Player(2,"Franz",7))
print(f"game.active_player.hand = {game.active_player.hand}")
print(f"game.top_card = {game.top_card}")
