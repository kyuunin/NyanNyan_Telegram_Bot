from ..game.event import *
import logging
logger = logging.getLogger("event")

base_event = EventHandler()
@base_event.register(StartTurn)
def start_turn(handler,game,event):
    from .data import Data
    data = Data(event,handler)
    logger.critical(handler.chat_data)
    old_msg=data.welcome_msg
    new_msg=data.send("running",buttons="running")
    logger.critical(new_msg)
    data.welcome_msg=new_msg
    old_msg.delete()
