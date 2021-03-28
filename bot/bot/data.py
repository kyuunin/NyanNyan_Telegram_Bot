import logging
logger = logging.getLogger(__name__)
from traceback import format_exception
from ..utils.messages import messages

def mention(user):
    return user.mention_markdown_v2(user.name)

class Data:
    def __init__(self,update, context):
        self.update=update
        self.context=context
        if "open" not in context.chat_data:
            self.open = True
            
    def reply(self, message, **kwargs):
        self.update.effective_message.reply_markdown_v2(message,**kwargs)
        
    def reply_text(self, message, **kwargs):
        self.update.effective_message.reply_text(message,**kwargs)
        
    @property
    def lang(self):
        return "en"
        
    def message_text(self, val):
        return messages[self.lang][val] % self.info
        
    def message_md(self, val):
        return messages[self.lang][val] % self.info_md
        
    @property
    def info(self):
        return {
            "user": self.user.name,
        }
        
    @property
    def info_md(self):
        return {
            "user": mention(self.user),
        }
        
    @property
    def user(self):
        return self.update.effective_user
        
    @property
    def chat(self):
        return self.update.effective_chat
        
    @property
    def message(self):
        return self.update.effective_message
        
    @property
    def admins(self):
        return {admin.user.id for admin in self.context.bot.get_chat_administrators(self.chat.id)}
        
    @property
    def game(self):
        return self.context.chat_data["game"]
        
    @game.setter
    def game(self,val):
        self.context.chat_data["game"]=val
        
    @property
    def open(self):
        return self.context.chat_data["open"]
        
    @open.setter
    def open(self,val):
        self.context.chat_data["open"]=val
        
    @property
    def error(self):
        return type(self.context.error)
        
    @property
    def full_error(self):
        return self.context.error
        
    @property
    def pretty_error(self):
        return "".join(format_exception(self.error,self.full_error, self.full_error.__traceback__))

        
