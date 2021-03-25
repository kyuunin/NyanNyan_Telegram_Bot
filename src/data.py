import logging
logger = logging.getLogger(__name__)

def mention(user):
    return user.mention_markdown_v2(user.name)

class Data:
    def __init__(self,update, context):
        self.update=update
        self.context=context
        if len(self.context.chat_data) == 0:
            self.context.chat_data["players"] = {}
            
    def reply(self, message, **kwargs):
        self.update.effective_message.reply_markdown_v2(message,**kwargs)
        
    def reply_text(self, message, **kwargs):
        self.update.effective_message.reply_text(message,**kwargs)
        
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
    def players(self):
        return self.context.chat_data["players"]
        
    @players.setter
    def players(self,val):
        self.context.chat_data["players"] = val
