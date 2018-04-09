#!/usr/bin/env python3
import sys
import time
from chiller_essential import *
from player import *
import global_settings
import sql_stats
import version

def HandleChatMessage(msg):
    msg_normal = msg
    msg = msg.lower()
    if (msg.find("/help") != -1 or msg.find("/info") != -1 or msg.find("/cmdlist") != -1):
        say("==== Teeworlds Econ Mod (TEM) ====")
        say("developed by ChillerDragon version: " + str(version.VERSION))
        say("https://github.com/ChillerDragon/TeeworldsEconMod")
        say("'/help' to show this help")
        say("'/stats' to show stats for all players")
        say("'/stats_all' to show all stats (a bit messy)")
        if global_settings.StatsMode == "sql":
            say("'/top5' for all time stats commands")
    elif (msg.find("/top5") != -1):
        if global_settings.StatsMode == "sql":
            say("'/top_kills' to see top5 killers of all time")
        if global_settings.StatsMode == "sql":
            say("'/top_flags' to see top5 flag caps of all time")
        if global_settings.StatsMode == "sql":
            say("'/top_sprees' to see top5 killing sprees of all time")
        else:
            say("not supported in file stats mode")
    elif (msg.find("/stats_all") != -1):
        PrintStatsAll(True)
    elif (msg.find("/stats") != -1):
        #say("sample rank message...")
        PrintStatsAll()
    elif (msg.find("/dev") != -1):
        say("debug=" + str(global_settings.IsDebug) + " stats=" + global_settings.StatsMode)
    elif (msg.find("/top_flags") != -1):
        if global_settings.StatsMode == "sql":
            sql_stats.BestTimes()
        else:
            say("not supported in file stats mode")
    elif (msg.find("/top_kills") != -1):
        if global_settings.StatsMode == "sql":
            sql_stats.BestKillers()
        else:
            say("not supported in file stats mode")
    elif (msg.find("/top_sprees") != -1):
        if global_settings.StatsMode == "sql":
            sql_stats.BestSprees()
        else:
            say("not supported in file stats mode")

