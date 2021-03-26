import logging
logger = logging.getLogger(__name__)

from telegram.ext import Updater,CommandHandler,InlineQueryHandler,MessageHandler,PollHandler,PollAnswerHandler, ConversationHandler, CallbackQueryHandler
from telegram import BotCommand
from collections import defaultdict

def app(fun):
    def inner(val):
        if val is None: 
            return fun
        return fun(val)
    return inner

class HandlerList:
    def __init__(self):
        self.data = []
        self.commands = []
        self.convs = []
        
    def __lshift__(self, handler):
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
        
    def inline_query(self, callback=None, *, group=0, **kwargs):
        @app
        def inner(x):
            self << (InlineQueryHandler(x,**kwargs), group)
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
    def __getattr__(self,val):
        return self.states[val]
    def finish(self):
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
        return ConversationHandler(self.entry_point.data, {k:v.data for k,v in self.states.items()}, self.fallbacks.data, **self.kwargs)

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
        group = 0
        if isinstance(handler,tuple):
            if len(handler) == 1:
                handler, = handler
            elif len(handler) == 2:
                handler,group = handler
        self.updater.dispatcher.add_handler(handler,group)
    def error(self,callback=None,**kwargs):
        return app(lambda x: self.updater.dispatcher.add_error_handler(x,**kwargs))(callback)
    def start(self):
        conv_iter(self,self.commands)
        self.updater.dispatcher.bot.set_my_commands(self.commands)
        self.updater.start_polling()    
        

