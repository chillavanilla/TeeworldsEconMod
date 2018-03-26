#!/usr/bin/env python3
import sys
import time
from chiller_essential import *
from player import *
from save_stats import *

def HandleChatMessage(msg):
    msg_normal = msg
    msg = msg.lower()
    if (msg.find("/help") != -1 or msg.find("/info") != -1 or msg.find("/cmdlist") != -1):
        say("==== Teeworlds Econ Mod (TEM) ====")
        say("developed by ChillerDragon")
        say("https://github.com/ChillerDragon/TeeworldsEconMod")
        say("command list comming soon...")
    elif (msg.find("/stats") != -1):
        #say("sample rank message...")
        PrintStatsAll()
    elif (msg.find("/test") != -1):
        global aPlayers
        say("saving stats for '" + aPlayers[0].name + "'")
        SaveStats(aPlayers[0].name)
