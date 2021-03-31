from ..utils import singleton

@singleton
class NoState:
    def can_play(card):
        return True

