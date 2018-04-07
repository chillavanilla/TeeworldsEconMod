#!/usr/bin/env python3
import sys
import time
from chiller_essential import *
from player import *
from sql_stats import *
from sql_test import *
from save_stats import *

def HandleChatMessage(msg):
    msg_normal = msg
    msg = msg.lower()
    if (msg.find("/help") != -1 or msg.find("/info") != -1 or msg.find("/cmdlist") != -1):
        say("==== Teeworlds Econ Mod (TEM) ====")
        say("developed by ChillerDragon")
        say("https://github.com/ChillerDragon/TeeworldsEconMod")
        say("'/help' to show this help")
        say("'/stats' to show stats for all players")
        say("'/stats_all' to show all stats (a bit messy)")
    elif (msg.find("/stats_all") != -1):
        PrintStatsAll(True)
    elif (msg.find("/stats") != -1):
        #say("sample rank message...")
        PrintStatsAll()
    elif (msg.find("/test") != -1):
        from global_stats import LoadGlobalStats
        #LoadGlobalStats() #does shit and crashes server
        #from sql_stats import SaveStatsSQL
        SaveStatsSQL("chiller")
        pass
    elif (msg.endswith("test2\n")):
        say("test failed")
        TestSQL()
