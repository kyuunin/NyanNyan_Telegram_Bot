from .card import Card
class Rule:
    def can_play(self,card,game):
        if card == Card.Joker:
            return True
        return (card.can_play(game.top_card) and
         game.state.can_play(card))
        
