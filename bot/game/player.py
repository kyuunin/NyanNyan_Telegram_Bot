from .card import Card
class Player:
    def __init__(self,id,name,n):
        self.id=id
        self.name=name
        self.skips=0
        self.hand = Card.draw(n)
    def draw(self,n):
        self.hand += Card.draw(n)
    def __repr__(self):
        return self.name
    def __eq__(self,other):
        return self.id==other.id
