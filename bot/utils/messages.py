from .exceptions import *
messages = {
    "en": {
        AlreadyJoinedException: "%(user)s already joined",
        PlayerNotFoundException: "%(user)s didn't join",
        NotEnoughRights: "you don't have enough rights",
        GameAlreadyStarted: "Game already started",
        "error": "Internal Error",
        "new": "New game was created",
        "join": "%(user)s joined",
        "leave": "%(user)s left",
        "start": "start Game",
        "end": "end Game",
        "open": "Game is now open",
        "close": "Game is now closed",
    },
    "en_md": {
        "new": "New game was created\nPlayers can enter with /join\nWhen everyone is ready to play use /start",
    }
    "de": {
        AlreadyJoinedException: "%(user)s ist schon beigetreten",
        PlayerNotFoundException: "%(user)s ist nicht beigetreten",
        NotEnoughRights: "nicht die notwendinge rechte",
        GameAlreadyStarted: "",
        "error": "Interner Fehler",
        "new": "",
        "join": "",
        "leave": "",
        "start": "",
        "end": "",
        "open": "",
        "close": "",
    }
    "de_md":{}
}
