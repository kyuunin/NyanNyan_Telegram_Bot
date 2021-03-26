import logging
logger = logging.getLogger(__name__)

from .server import Server,Conversation
from .data import Data, mention


with open("TOKEN", "r") as f:
    server = Server(token=f.readline()[:-1], use_context=True)
conv = server.conversation( per_user=False)


@conv.entry_point.command("new", description="Create a new Game")
def new(update, context):
    data = Data(update, context)
    data.reply_text("New game was created.\nPlayers can enter with /join.\nWhen everyone is ready to play use /start.")
    return "waiting"
    
@conv.waiting.command("join", description="Join the game")
def join(update, context):
    data = Data(update, context)
    data.players[data.user.id]=data.user
    data.reply(f"{mention(data.user)} joins")
    
@conv.waiting.command("start", description="Start the Game")    
def start(update, context):
    data = Data(update, context)
    data.reply_text("start Game")
    return "running"
    
@conv.running.command("start")    
def start(update, context):
    data = Data(update, context)
    data.reply_text("Game is already Running")
    
@conv.running.command("players", description="Lists all players")
@conv.waiting.command("players")
def players(update, context):
    data = Data(update, context)
    data.reply("Players: " + ", ".join(f"{mention(player)}" for player in data.players.values()))
    
@conv.fallbacks.command("end", description="End the Game")    
def end(update, context):
    data = Data(update, context)
    data.players.clear()
    data.reply_text("end Game")
    return -1
