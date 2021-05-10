def new_exception(name, important):
    globals()[name]=type(name,(RuntimeError,),{"important":important})
new_exception("AlreadyJoined",False)
new_exception("PlayerNotFound",False)
new_exception("GameAlreadyStarted",False)
new_exception("NotEnoughRights",True)
new_exception("UnknownLang",True)
