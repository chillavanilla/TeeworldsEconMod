#!/usr/bin/env python3
import sys
import time
from chiller_essential import *
import cbase
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
    elif (msg.find("/rank") != - 1):
        name_start = cbase.cfind(msg, ":", 3) + 1
        name_end = msg.find(": /rank", name_start)
        name_end = msg.rfind(": ", name_end)
        name = msg_normal[name_start:name_end]
        rankname_start = -1
        if (msg.find(": /rank ") != -1):
            rankname_start = msg.find(": /rank ", name_end) + len(": /rank ")
        rankname_end = len(msg) - 1 #cut off newline
        rankname = msg_normal[rankname_start:rankname_end]
        if not rankname or rankname == "" or rankname_start == -1:
            sql_stats.ShowRank(name)
        else:
            sql_stats.ShowRank(rankname)
            #say(" name start: " + str(name_start) + " end: " + str(name_end))
            #say(" rankname start: " + str(rankname_start) + " end: " + str(rankname_end))
            #say(" showing rank for '" + str(rankname) + "'")
    elif (msg.find("/test") != - 1):
        echo(" hello test wolrd ")
        say("test failed")
