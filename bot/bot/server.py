import logging
logger = logging.getLogger(__name__)

from telegram.ext import *
from telegram import BotCommand
from collections import defaultdict
from inspect import signature
from traceback import format_exc
from .data import Data

def cb(callback):
    def inner(update, context):
        data = Data(update, context)
        param = signature(callback).parameters
        return callback(**{k:v for k,v in locals().items() if k in param})
    return inner

def app(fun):
    def inner(val):
        if val is None: 
            return lambda x: fun(cb(x))
        return fun(cb(val))
    return inner
    
class UpdateHandler(Handler):
    def __init__(self,filters,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.filters = filters
    def check_update(self,update):
        logger.critical(self.filters.__dict__)
        self.filters.filter(update)

class HandlerList:
    def __init__(self):
        self.data = []
        self.commands = []
        self.convs = []
        
    def __lshift__(self, handler):
        logger.debug("%s added to %s"%(handler,self))
        if isinstance(handler,tuple):
            if len(handler) == 1:
                handler, = handler
            elif len(handler) == 2:
                handler,_ = handler
        self.data.append(handler)

    def conversation(self, *, group=0, **kwargs):
        res = Conversation(**kwargs)
        self.convs.append((res,group))
        return res

    def command(self, command, callback=None, *, description = None, group=0, **kwargs):
        if description is not None:
            self.commands.append(BotCommand(command,description))
        @app
        def inner(x):
            self << (CommandHandler(command,x,**kwargs), group)
            return x
        return inner(callback)
        
    def update_handler(self, filters, callback=None, *, description = None, group=0, **kwargs):
        if description is not None:
            self.commands.append(BotCommand(command,description))
        @app
        def inner(x):
            self << (UpdateHandler(filters,x,**kwargs), group)
            return x
        return inner(callback)
        
    def inline_query(self, callback=None, *, group=0, **kwargs):
        @app
        def inner(x):
            self << (InlineQueryHandler(x,**kwargs), group)
            return x
        return inner(callback)
        
    def chosen_inline_result(self, callback=None, *, group=0, **kwargs):
        @app
        def inner(x):
            self << (ChosenInlineResultHandler(x,**kwargs), group)
            return x
        return inner(callback)
        
    def poll(self, callback=None, *, group=0, **kwargs):
        @app
        def inner(x):
            self << (PollHandler(x,**kwargs), group)
            return x
        return inner(callback)
        
    def poll_answer(self, callback=None, *, group=0, **kwargs):
        @app
        def inner(x):
            self << (PollAnswerHandler(x,**kwargs), group)
            return x
        return inner(callback)
        
    def callback_query(self, callback=None, *, group=0, **kwargs):
        @app
        def inner(x):
            self << (CallbackQueryHandler(x,**kwargs), group)
            return x
        return inner(callback)
        
    def message(self, filters, callback=None, *, group=0, **kwargs):
        @app
        def inner(x):
            self << (MessageHandler(filters,x,**kwargs), group)
            return x
        return inner(callback)
        
def conv_iter(hl,commands):
    for conv, group in hl.convs:
        hl << (conv.finish(), group)
        commands += conv.commands
    hl.convs = []
    
class Conversation:
    def __init__(self,**kwargs):
        self.kwargs = kwargs
        self.entry_point = HandlerList()
        self.fallbacks = HandlerList()
        self.states = defaultdict(lambda:HandlerList())
        self.commands = []
        self.conversation = None
    def __getattr__(self,val):
        return self.states[val]
    def state(self,data):
        try:
            return self.conversation.conversations[self.conversation._get_key(data.update)]
        except KeyError:
            return None
    def check(self,ids,state):
        try:
            return self.conversation.conversations[ids] == state
        except:
            return False
    def finish(self):
        if self.conversation is None:
            conv_iter(self.entry_point,self.commands)
            self.commands += self.entry_point.commands
            self.entry_point.commands = []
            conv_iter(self.fallbacks,self.commands)
            self.commands += self.fallbacks.commands
            self.entry_point.commands = []
            for hl in self.states.values():
                conv_iter(hl,self.commands)
                self.commands += hl.commands
                hl.commands = []
            self.conversation = ConversationHandler(self.entry_point.data, {k:v.data for k,v in self.states.items()}, self.fallbacks.data, **self.kwargs)
        return self.conversation
class Server(HandlerList): 
    def __init__(self, *args, **kwargs):
        self.updater = Updater(*args, **kwargs) 
        self.commands = [] 
        self.convs = []
        @self.command("help", description="Shows help")
        def help(update, context):
            from .data import Data
            data = Data(update, context)
            data.reply_text("\n".join(f"/{com.command} - {com.description}" for com in self.commands))
    def __lshift__(self,handler):
        logger.debug("%s added to server"%(handler,))
        group = 0
        if isinstance(handler,tuple):
            if len(handler) == 1:
                handler, = handler
            elif len(handler) == 2:
                handler,group = handler
        self.updater.dispatcher.add_handler(handler,group)
    def error(self,callback=None,**kwargs):
        @app
        def inner(x):
            self.updater.dispatcher.add_error_handler(x,**kwargs)
            return x
        return inner(callback)
    def start(self):
        conv_iter(self,self.commands)
        self.updater.dispatcher.bot.set_my_commands(self.commands)
        self.updater.start_polling() 
    @property
    def id(self):
        return self.updater.dispatcher.bot.id
        

