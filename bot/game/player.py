class Player:
    def __init__(self,id,name):
        self.id=id
        self.name=name
        self.skips=0
    def __repr__(self):
        return self.name
