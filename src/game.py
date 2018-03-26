#!/usr/bin/env python3
from chiller_essential import *
from player import *
from kills import *

def HandleGame(data):
    if (data.find("kill killer") != -1):
        HandleKills(data)    
    if (data.startswith("[game]: start round type='")):
        #say("new round new luck") #working but dont send this useless msg pls
        pass
