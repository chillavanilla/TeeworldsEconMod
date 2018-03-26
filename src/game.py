#!/usr/bin/env python3
from chiller_essential import *
from player import *
from kills import *

def HandleGame(data):
    if (data.find("kill killer") != -1):
        HandleKills(data)    
    elif (data.startswith("[game]: start round type='")):
        #say("new round new luck") #working but dont send this useless msg pls
        pass
    elif (data.startswith("[game]: flag_grab player='")):
        name_start = data.find(":", 10) + 1  # first '
        name_end   = data.rfind("'")     # last '
        name = data[name_start:name_end]
        UpdatePlayerFlagGrabs(name, 1)
