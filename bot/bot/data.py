import logging
logger = logging.getLogger(__name__)
from traceback import format_exception
from telegram import InlineKeyboardButton,InlineKeyboardMarkup,Message 
from ..game import rules, event
from ..utils import messages, exceptions as ex
from .bot_event import base_event

def mention(user):
    return f"[{user.name}](tg://user?id={user.id})"

def chat_attr(fun):
    @property
    def f(self):
        if fun.__name__ in self.chat_data:
            return self.chat_data[fun.__name__]
    @f.setter
    def f(self,val):
        fun(self,val)
        self.chat_data[fun.__name__] = fun(self,val)
    return f

def call(parse_mode=None):
    def helper(fun):
        def inner(self, message, *, buttons=None, **kwargs):
            if buttons:
                kwargs["reply_markup"]=self.buttons[buttons]
            tmp = fun(self)
            if tmp:
                return tmp(self.message_md(message),parse_mode=parse_mode,**kwargs)
            else:
                None
        return inner 
    return helper
    
def edit(msg):
    return msg.edit_text if msg else None

class Data:
    def __init__(self,update, context):
        if isinstance(context, event.EventHandler):
            self.handler = context
            self.event = update
            logger.critical(self.handler)
        else:
            self.update=update
            self.context=context
            if not len(self.chat_data):
                self.open = True
                self.lang = "en"
                self.rule = rules["NyanNyan"]
                self.event_handler = event.EventHandler()
                self.event_handler.events=base_event.events
                self.event_handler.chat_id = self.chat_id
                self.event_handler.bot = self.bot
                self.event_handler.chat_data = self.chat_data
            else:
                self.open = self.open
                
    @property
    def arg(self):
        return self.update, self.context 
            
    #############
    # messaging #
    #############
    def reply_text(self,*args,**kwargs):
        self.message.reply_text(*args,**kwargs)
    def answer(self,message,*args,**kwargs):
        if self.query:
            self.query.answer(self.message_text(message),*args,**kwargs)
            return True
        else:
            return False
    def answer_inline_query(self, *args, **kwargs):
        return self.context.bot.answer_inline_query(self.update.inline_query.id, *args, **kwargs)
    @call("MarkdownV2")
    def reply(self):
        return self.message.reply_text
    @call("MarkdownV2")
    def edit_welcome(self):
        return edit(self.welcome_msg)
    @call("MarkdownV2")
    def send(self):
        def inner(*args, **kwargs):
            return self.bot.send_message(self.chat_id, *args, **kwargs)
        return inner
    def send_sticker(self,*args,**kwargs):
        self.bot.send_sticker(self.chat_id, *args, **kwargs)
    def message_text(self, val):
        return messages[self.lang][val] % self.info
    def message_md(self, val):
        return messages[self.lang][val] % self.info_md
    @property
    def info(self):
        return {
            "user": self.user.name if self.user else None,
            "players": [player.name for player in self.game.players.values()] if self.game else None,
            "state": type(self.game.state).__name__ if self.game else None
        }
    @property
    def info_md(self):
        return {
            "user": mention(self.user) if self.user else None,
            "players": "\n".join(mention(player) for player in self.game.players.values()) if self.game else None,
            "state": type(self.game.state).__name__ if self.game else None
        }
    def sticker(self, s_id):
        return self.bot.get_sticker_set("nyan_nyan_playing_cards_v1").stickers[s_id]
        
        
    #############
    # chat_data #
    #############
    @property
    def via_message(self):
        return self.context.user_data["via_message"]
    @via_message.setter
    def via_message(self,val):
        self.context.user_data["via_message"] = val
    @property
    def via(self):
        return self.via_message.chat.id
    @chat_attr
    def rule(self,val): return val
    @chat_attr
    def welcome_msg(self,val):
        if self.bot_rights.can_pin_messages:
            if self.welcome_msg:
                self.welcome_msg.unpin()
            if val:
                val.pin()
        return val
    @chat_attr
    def event_handler(self,val): return val
    @chat_attr
    def game(self,val): return val
    @chat_attr
    def buttons(self,val): return val
    @chat_attr
    def open(self,val):
        self.buttons = self._buttons[val] 
        return val    
    @chat_attr
    def lang(self, val):
        if val not in messages:
            raise ex.UnknownLang
        return val   
    @property
    def _buttons(self):
        btn_join = InlineKeyboardButton("Join",callback_data="Join")
        btn_start = InlineKeyboardButton("Start",callback_data="Start")
        btn_play = InlineKeyboardButton("Play",switch_inline_query_current_chat=str(self.chat_id))
        mkp_waiting = InlineKeyboardMarkup([[btn_join],[btn_start]])
        mkp_running_closed = InlineKeyboardMarkup([[btn_play]])
        mkp_running_open = InlineKeyboardMarkup([[btn_play],[btn_join]])
        return {
            True:{"waiting":mkp_waiting,"running":mkp_running_open},
            False:{"waiting":mkp_waiting,"running":mkp_running_closed}
        }

        
    #################
    # update fields #
    #################
    @property
    def user(self):
        if hasattr(self, "handler"):
            return None
        return self.update.effective_user
    @property
    def bot(self):
        if hasattr(self, "handler"):
            return self.handler.bot
        return self.context.bot
    @property
    def chat(self):
        return self.update.effective_chat
    @property
    def chat_id(self):
        if hasattr(self, "handler"):
            return self.handler.chat_id
        if self.update.inline_query:
            return int(self.update.inline_query.query)
        if self.update.chosen_inline_result:
            return int(self.update.chosen_inline_result.query)
        return self.update.effective_chat.id
    @property
    def chat_data(self):
        if hasattr(self, "handler"):
            return self.handler.chat_data
        if self.chat_id not in self.context.bot_data:
            self.context.bot_data[self.chat_id] = {}
        return self.context.bot_data[self.chat_id]
    @property
    def message(self):
        if self.update.effective_message:
            return self.update.effective_message
        return self.via_message
    @property
    def query(self):
        return self.update.callback_query
    @property
    def result_id(self):
        return self.update.chosen_inline_result.result_id
    @property
    def admins(self):
        return {admin.user.id for admin in self.context.bot.get_chat_administrators(self.chat.id)}
    @property
    def bot_rights(self):
        return self.bot.get_chat_member(self.chat_id,self.bot.id)
        
    #########
    # error #
    #########
    @property
    def error(self):
        return type(self.context.error)
    @property
    def full_error(self):
        return self.context.error        
    @property
    def pretty_error(self):
        return "".join(format_exception(self.error,self.full_error, self.full_error.__traceback__))

        
