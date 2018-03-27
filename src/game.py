#!/usr/bin/env python3
from chiller_essential import *
from player import *
from kills import *

def HandleGame(data):
    if (data.find("kill killer") != -1):
        HandleKills(data)    
    elif (data.startswith("[game]: start round type='")):
        say("[SERVER] ChillerDragon wishes you all hf & gl c:")
        #TODO: reset IsFlagger value here and maybe reset all values here
        pass
    elif (data.startswith("[game]: flag_grab player='")):
        name_start = data.find(":", 10) + 1  # first '
        name_end   = data.rfind("'")     # last '
        name = data[name_start:name_end]
        UpdatePlayerFlagGrabs(name, 1)
        SetFlagger(name, True)
        #say("'" + name + "' grabbed the flag")
