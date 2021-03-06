from ..utils import singleton
from .card import cards
from abc import ABC
no_options = ()
class Action(ABC):
    def options(self, player, game):
        return no_options
    def do(self, player, game, option):
        pass
    def __repr__(self):
        return type(self).__name__

class Draw_Cards(Action):
    def __init__(self, n):
        self.n = n
    def do(self, player, game, option):
        from .state import Phase1,Phase2
        player.draw(self.n)
        if game.state == Phase1:
            game.state = Phase2
        else:
            game.state = Phase1
    def __eq__(self, other):
        return type(self)==type(other) and self.n == other.n
    def __repr__(self):
        return f"Draw {self.n}"
        
class Choose_Player(Action):
    def __init__(self, effect):
        self.effect = effect
    def options(self, player, game):
        return list(game.players)
    def do(self, player, game, option):
        from .state import Phase1, Choose, Answer
        player = game.players[option]
        if player in game.answers:
            game.answers[player] = (self.effect, game.answers[player][1]+1)
        else:
            game.answers[player] = (self.effect,1)
        if game.state.n > 1:
            game.state = Choose(game.state.n-1,self.effect)
        else:
            game.state = Answer
    def __eq__(self, other):
        return type(self)==type(other) and self.effect == other.effect
    def __repr__(self):
        return f"Choose_Player"
    
@singleton    
class Choose_Suit(Action):
    _options = tuple(range(4))
    def options(self, player, game):
        return self._options
    def do(self, player, game, option):
        game.top_card = cards[option]
        game.end_turn()
    
@singleton
class Pass(Action):
    def do(self, player, game, option):
        from .state import Phase1, Answer
        if player in game.answers:
            for _ in range(game.answers[player][1]):
                game.answers[player][0](player)
            del game.answers[player]
        if len(game.answers):
            game.state = Answer
        else:
            game.state = Phase1
            game.end_turn()
