import logging
logger = logging.getLogger("bot")

from telegram.ext.filters import Filters
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, InlineQueryResultArticle, InputTextMessageContent, InlineQueryResultCachedSticker
from telegram.error import BadRequest
from .server import Server
from .data import Data, mention
from ..game import Game, Player
from ..utils import messages, exceptions as ex
    
with open("TOKEN", "r") as f:
    bot = Server(token=f.readline()[:-1], use_context=True)
conv = bot.conversation(per_user=False)
with open("DEVS", "r") as f:
    devs = {int(x) for x in f}
_filter = Filters.chat_type.groups & Filters.update.message

@bot.error
def error(data):
    if data.error in messages[data.lang]:
        logger.info(data.message_text(data.error))
        if (not data.answer(data.error, data.error.important) and data.error.important):
            data.reply(data.error)
    else:
        logger.error(data.pretty_error)
        if data.error != BadRequest:
            data.reply("error")
        
@bot.command("error", filters=Filters.update.message)
def error(data):
    if data.user.id in devs:
        raise RuntimeError

@bot.command("log", filters=Filters.update.message)
def log(update, context):
    data = Data(update, context)
    if data.user.id in devs:
        with open("url","r") as f:
            data.reply_text(f.read())

@bot.command("via", filters=Filters.update.message)
def via(update, context):
    data = Data(update, context)
    if data.user.id in devs:
        data.reply_text(data.via)
        
@conv.entry_point.command("new", description="Create new Game", filters=_filter)
def new(data):
    data.game = Game(data.rule, data.event_handler)
    logger.info(data.message_text("new"))
    data.welcome_msg=data.reply("new", buttons="waiting")
    return "waiting"

@conv.waiting.callback_query(pattern="Join")
@conv.waiting.command("join", description="Join game", filters=_filter)
def join(data):
    data.game.join(Player(data.user.id, data.user.name,7))
    logger.info(data.message_md("join"))
    data.answer("join")
    data.edit_welcome(conv.state(data), buttons=conv.state(data))
    
@conv.running.callback_query(pattern="Join")
@conv.running.command("join", filters=_filter)
def join2(data):
    if data.open:
        return join(*data.arg)
    raise ex.GameAlreadyStarted
    
@conv.waiting.command("leave", description="Leave game", filters=_filter)
@conv.running.command("leave", filters=_filter)
def leave(data):
    data.game.leave(data.user.id)
    logger.info(data.message_text("leave"))
    data.answer("leave")
    data.edit_welcome(conv.state(data), buttons=conv.state(data))
    
@conv.waiting.callback_query(pattern="Start")
@conv.waiting.command("start", description="Start the Game", filters=_filter)    
def start(data):
    logger.info(data.message_text("start"))
    data.answer("start")
    data.edit_welcome("running", buttons="running")
    data.send_sticker(data.sticker(data.game.top_card.id))
    return "running"
      
@bot.inline_query
def play(data):
    x = "\n".join(s.file_unique_id for s in data.bot.get_sticker_set("nyan_nyan_playing_cards_v1").stickers)
    if conv.check((data.chat_id,),"running") and data.user.id in data.game.players:
        playable_cards=data.game.playable_cards(data.user.id)
        cards = ((card.id if playable else card.id+55) for card, playable in playable_cards)
        data.answer_inline_query(
            [
                InlineQueryResultCachedSticker(
                    id=i, 
                    sticker_file_id=data.sticker(card_id).file_id,
                ) for i,card_id in enumerate(cards)
            ], #TODO add actions
            cache_time=0
        )
    else:
        data.answer_inline_query([],cache_time=0)
      
@bot.message(Filters.via_bot(bot.id))
def check_message(data):
    data.via_message = data.update.message

@bot.chosen_inline_result
def choose_action(data):
    if data.chat_id == data.via and conv.check((data.chat_id,),"running") and data.user.id in data.game.players:
        logger.info(data.update)
        #TODO handle actions
        data.game.play_card(data.user.id, int(data.result_id))
        data.reply_text("success")
    else:
        data.reply_text("failure")
      
@conv.fallbacks.command("end", description="End the Game")    
def end(data):
    data.game = None
    logger.info(data.message_text("end"))
    data.edit_welcome("end")
    data.welcome_msg=None
    return -1
    
def assert_admin(data):
    if data.user.id not in data.admins:
        raise ex.NotEnoughRights
def lang_command(lang, **kwargs):
    def fun(data):
        assert_admin(data)
        data.lang = lang
        logger.info(data.message_text("lang"))
        data.reply("lang")
    return bot.command(lang, fun, **kwargs)
    
for lang in messages:
    lang_command(lang, description=messages[lang]["lang_help"], filters=_filter)
    
@bot.command("open", description="Allow player to Join running Games", filters=_filter)    
def opens(data):
    assert_admin(data)
    data.open = True
    logger.info(data.message_text("open"))
    data.edit_welcome(conv.state(data), buttons=conv.state(data))
        
@bot.command("close", description="Disallow player to Join running Games", filters=_filter)    
def close(data):
    assert_admin(data)
    data.open = False
    logger.info(data.message_text("close"))
    data.edit_welcome(conv.state(data), buttons=conv.state(data))
