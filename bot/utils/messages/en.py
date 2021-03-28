from ..exceptions import *
messages = {
    AlreadyJoinedException: "%(user)s already joined",
    PlayerNotFoundException: "%(user)s didn't join",
    NotEnoughRights: "you don't have enough rights",
    GameAlreadyStarted: "Game already started",
    UnknownLang: "Unknown Language",
    "lang": "language set to English",
    "lang_help": "set language to English",
    "error": "Internal Error",
    "new": "New game was created",
    "join": "%(user)s joined",
    "leave": "%(user)s left",
    "start": "start Game",
    "end": "end Game",
    "open": "Game is now open",
    "close": "Game is now closed",
    "md": {
        "new": 
            "New game was created\n"+
            "Players can enter with /join\n"+
            "When everyone is ready to play use /start",
    }
}
