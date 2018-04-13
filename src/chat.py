#!/usr/bin/env python3
import sys
import time
from chiller_essential import *
import cbase
import player
import global_settings
import sql_stats
import version
import game
import achievements

def GetRankName(msg, rank_cmd):
    if not global_settings.StatsMode == "sql":
        say("not supported in file stats mode")
        return None
    msg_normal = msg
    msg = msg.lower()
    name_start = cbase.cfind(msg, ":", 3) + 1
    name_end = msg.find(rank_cmd, name_start)
    name_end = msg.rfind(": ", name_end)
    name = msg_normal[name_start:name_end]
    rankname_start = -1
    if (msg.find(rank_cmd + " ") != -1):
        rankname_start = msg.find(rank_cmd + " ", name_end) + len(rank_cmd + " ")
    rankname_end = len(msg) - 1 #cut off newline
    rankname = msg_normal[rankname_start:rankname_end]
    if not rankname or rankname == "" or rankname_start == -1:
        return name
    return rankname

def HandleChatMessage(msg):
    msg_normal = msg
    msg = msg.lower()
    chat_cmd_start = cbase.cfind(msg, ":", 4) # the first possible occurence of a chat command (to filter chat command names)
    cmd = msg[chat_cmd_start:-1] #cut newline at end
    if (cmd.endswith(": /help") or cmd.endswith(": /info") or cmd.endswith(": /cmdlist")):
        say("==== Teeworlds Econ Mod (TEM) ====")
        say("developed by ChillerDragon version: " + str(version.VERSION))
        say("https://github.com/ChillerDragon/TeeworldsEconMod")
        say("'/help' to show this help")
        say("'/stats' to show stats for all players")
        say("'/stats_all' to show all stats (a bit messy)")
        say("'/achievements' to show achievements")
        if global_settings.StatsMode == "sql":
            say("'/top5' for all time stats commands")
            say("'/rank' for all rank commands")
    elif (cmd.endswith(": /top5")):
        if global_settings.StatsMode == "sql":
            say("'/top_kills' to see top5 killers of all time")
        if global_settings.StatsMode == "sql":
            say("'/top_flags' to see top5 flag caps of all time")
        if global_settings.StatsMode == "sql":
            say("'/top_sprees' to see top5 killing sprees of all time")
        else:
            say("not supported in file stats mode")
    elif (cmd.endswith(": /stats_all")):
        player.PrintStatsAll(True)
    elif (cmd.endswith(": /stats")):
        #say("sample rank message...")
        player.PrintStatsAll()
    elif (cmd.endswith(": /top_flag")):
        if global_settings.StatsMode == "sql":
            sql_stats.BestTimes()
        else:
            say("not supported in file stats mode")
    elif (cmd.endswith(": /top_kill")):
        if global_settings.StatsMode == "sql":
            sql_stats.BestKillers()
        else:
            say("not supported in file stats mode")
    elif (cmd.endswith(": /top_spree")):
        if global_settings.StatsMode == "sql":
            sql_stats.BestSprees()
        else:
            say("not supported in file stats mode")
    elif (cmd.find("/rank_kills") != - 1):
        sql_stats.RankKills(GetRankName(msg_normal, ": /rank_kills"))
    elif (msg.find("/rank_flags") != - 1):
        sql_stats.RankFlagTime(GetRankName(msg_normal, ": /rank_flags"))
    elif (cmd.find("/rank_sprees") != - 1):
        sql_stats.RankSpree(GetRankName(msg_normal, ": /rank_sprees"))
    elif (cmd.find("/rank_all") != - 1):
        name = GetRankName(msg_normal, ": /rank_all")
        if not name:
            return
        say("=== '" + str(name) + "'s stats ===")
        sql_stats.RankKills(str(name))
        sql_stats.RankFlagTime(str(name))
        sql_stats.RankSpree(str(name))
    elif (cmd.find("/rank") != - 1):
        if not global_settings.StatsMode == "sql":
            say("not supported in file stats mode")
            return
        say("'/rank_kills' to show global kills rank")
        say("'/rank_sprees' to show global spree rank")
        say("'/rank_flags' to show global flag time rank")
    elif (cmd.find("/achievements") != - 1):
        name = GetRankName(msg_normal, ": /achievements")
        achievements.ShowAchievements(name)
    elif (cmd.endswith(": /test")):
        say("test failed")
        '''
        str = "\"test'hello#world"
        say(str)
        echo(str)
        broadcast(str)
        name = GetRankName(msg_normal, ": /test")
        pPlayer = player.GetPlayerByName(name)
        if not pPlayer:
            say("error")
            return
        say("'" + str(pPlayer.name) + "' team: " + str(pPlayer.team))
        say("wins: " + str(pPlayer.wins) + " looses: " + str(pPlayer.looses))
        echo(" hello test wolrd ")
        #say("red: " + str(game.caps_red) + " blue: " + str(game.caps_blue))
        '''
