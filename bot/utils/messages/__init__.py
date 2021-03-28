from os import listdir
messages = {
    lang[:-3]: __import__("bot.utils.messages."+lang[:-3], globals(), locals(), ["messages"], 0).messages 
    for lang in listdir("bot/utils/messages") if lang[0] != "_"
}
