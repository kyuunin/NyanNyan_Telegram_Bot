import logging
logger = logging.getLogger(__name__)

class Player:
    def __init__(self,id,name):
        self.id=id
        self.name=name
    def __repr__(self):
        return self.name
