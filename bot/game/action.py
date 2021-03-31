from ..utils import singleton
no_options = [None]

@singleton
class Draw_Card:
    @property
    def options(self):
        return no_options
    def do(self, player, game, option):
        from .state import Phase2
        player.draw(1)
        game.state = Phase2

@singleton
class Pass:
    @property
    def options(self):
        return no_options
    def do(self, player, game, option):
        from .state import Phase1
        game.state = Phase1
        game.end_turn()
