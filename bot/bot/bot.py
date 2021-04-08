import logging
logger = logging.getLogger("bot")

from telegram.ext.filters import Filters
from .server import Server
from .data import Data, mention
from ..game import Game, Player
from ..utils import messages, exceptions as ex
    
with open("TOKEN", "r") as f:
    bot = Server(token=f.readline()[:-1], use_context=True)
conv = bot.conversation( per_user=False)

_filter = Filters.chat_type.groups & Filters.update.message

@bot.error
def error(update, context):
    data = Data(update, context)
    if data.error in messages[data.lang]:
        logger.info(data.message_text(data.error))
        data.reply(data.message_md(data.error))
    else:
        logger.error(data.pretty_error)
        data.reply(data.message_md("error"))
        
@bot.command("error", filters=Filters.update.message)
def error(update, context):
    raise RuntimeError


@conv.entry_point.command("new", description="Create new Game", filters=_filter)
def new(update, context):
    data = Data(update, context)
    data.game = Game(data.rule,data.event_handler)
    logger.info(data.message_text("new"))
    data.reply(data.message_md("new"))
    return "waiting"

@conv.waiting.command("join", description="Join game", filters=_filter)
def join(update, context):
    data = Data(update, context)
    data.game.join(Player(data.user.id, data.user.name,7))
    logger.info(data.message_text("join"))
    data.reply(data.message_md("join"))
@conv.running.command("join", filters=_filter)
def _(update, context):
    data = Data(update, context)
    if data.open:
        return join(update, context)
    raise ex.GameAlreadyStarted
    
@conv.waiting.command("leave", description="Leave game", filters=_filter)
@conv.running.command("leave", filters=_filter)
def leave(update, context):
    data = Data(update, context)
    data.game.leave(data.user.id)
    logger.info(data.message_text("leave"))
    data.reply(data.message_md("leave"))
    
@conv.waiting.command("start", description="Start the Game", filters=_filter)    
def start(update, context):
    data = Data(update, context)
    logger.info(data.message_text("start"))
    data.reply(data.message_md("start"))
    return "running"
      
@conv.fallbacks.command("end", description="End the Game")    
def end(update, context):
    data = Data(update, context)
    data.game = None
    logger.info(data.message_text("end"))
    data.reply(data.message_md("end"))
    return -1
    
   
def assert_admin(data):
    if data.user.id not in data.admins:
        raise NotEnoughRights
def lang_command(lang, **kwargs):
    def fun(update, context):
        data = Data(update, context)
        assert_admin(data)
        data.lang = lang
        logger.info(data.message_text("lang"))
        data.reply(data.message_md("lang"))
    return bot.command(lang, fun, **kwargs)
    
for lang in messages:
    lang_command(lang, description=messages[lang]["lang_help"], filters=_filter)
    
@bot.command("open", description="Allow player to Join running Games", filters=_filter)    
def open(update, context):
    data = Data(update, context)
    assert_admin(data)
    data.open = True
    logger.info(data.message_text("open"))
    data.reply(data.message_md("open"))
        
@bot.command("close", description="Disallow player to Join running Games", filters=_filter)    
def close(update, context):
    data = Data(update, context)
    assert_admin(data)
    data.open = False
    logger.info(data.message_text("close"))
    data.reply(data.message_md("close"))
