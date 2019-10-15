#!/usr/bin/env python3
import sys
import time
import datetime
import re
from chiller_essential import *
import g_settings
import cbase
import player
import sql_stats
import version
import game
import achievements

def IsBanReasonInStr(str):
    words = g_settings.get("discord_filter")
    if not words:
        return False
    for word in words:
        if (str.find(word) != -1):
            return True
    return False

# get by id if no argument given
# get by name if name is argument
# return player object and identifier (id/name)
def GetRankPlayer(msg, rank_cmd):
    if not g_settings.get("stats_mode") == "sql":
        say("not supported in file stats mode")
        return None
    msg_normal = msg
    msg = msg.lower()
    id_str = GetChatID(msg_normal)
    rankname_start = -1
    if (msg.find(rank_cmd + " ") != -1):
        cmd_end = msg.rfind(rank_cmd)
        rankname_start = msg.find(rank_cmd + " ", cmd_end) + len(rank_cmd + " ")
    rankname_end = len(msg) - 1 #cut off newline
    rankname = msg_normal[rankname_start:rankname_end]
    if not rankname or rankname == "" or rankname_start == -1:
        return player.GetPlayerByID(id_str), id_str
    argplayer = player.GetPlayerByName(rankname)
    if not argplayer:
        # try to find id prefix in argument name
        m = re.match( r'(\d{1,2}):(.*)', rankname)
        if m:
            r_id = m.group(1)
            r_name = m.group(2)
            r_player = player.GetPlayerByID(r_id)
            if r_player and r_player.name == r_name:
                argplayer = r_player
    return argplayer, rankname

def GetRankName(msg, rank_cmd):
    if not g_settings.get("stats_mode") == "sql":
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

# TODO: unused? remove?
def GetSpamName(msg):
    name_start = cbase.cfind(msg, ":", 3) + 1
    name_end = msg.find(": ", name_start + 1)
    name = msg[name_start:name_end]
    return name

def GetChatID(msg):
    id_start = msg.find(" ") + 1
    id_end = cbase.cfind(msg, ":", 2)
    id_str = msg[id_start:id_end]
    return id_str

def GetSpamPlayer(msg):
    id_str = GetChatID(msg)
    return player.GetPlayerByID(id_str)

def SpamProtection(msg):
    p = GetSpamPlayer(msg)
    if not p:
        say("[ERROR] SpamProtection() failed! please contact an admin")
        sys.exit(1)
    now = datetime.datetime.now()
    diff = now - p.LastChat
    p.LastChat = now
    #say("chat diff seconds: " + str(diff.seconds) + " LastChat: " + str(p.LastChat))
    seconds = diff.seconds
    if (seconds < 15):
        p.MuteScore += 1
    if (p.MuteScore > 5):
        if not p.IsMuted:
            p.IsMuted = True
            say("'" + str(p.name) + "' is banned from the command system (spam)")
    if (seconds > 120):
        p.IsMuted = False
        p.MuteScore = 0
    if (p.IsMuted):
        return True
    return False

def IsMuted(msg):
    p = GetSpamPlayer(msg)
    if not p:
        say("[WARNING] IsMuted() failed! please contact an admin")
        return False
    if (p.IsMuted):
        return True
    return False

def HandleChatMessage(msg):
    if IsMuted(msg):
        return
    IsCmd = True
    msg_normal = msg
    msg = msg.lower()
    chat_cmd_start = cbase.cfind(msg, ":", 4) # the first possible occurence of a chat command (to filter chat command names)
    cmd = msg[chat_cmd_start:-1] #cut newline at end
    if (cmd.endswith(": /help") or cmd.endswith(": /info") or cmd.endswith(": /cmdlist")):
        say("==== Teeworlds Econ Mod (TEM) ====")
        say("developed by ChillerDragon version: " + str(version.VERSION))
        say("https://github.com/ChillaVanilla/TeeworldsEconMod")
        say("'/help' to show this help")
        say("'/stats' to show round stats")
        say("'/achievements' to show achievements")
        if g_settings.get("stats_mode") == "sql":
            say("'/top5' for all time stats commands")
            say("'/rank' for all rank commands")
    elif (cmd.endswith(": /top5")):
        if g_settings.get("stats_mode") == "sql":
            say("'/top_kills' to see top5 killers of all time")
        if g_settings.get("stats_mode") == "sql":
            say("'/top_flags' to see top5 flag cap times of all time")
        if g_settings.get("stats_mode") == "sql":
            say("'/top_caps' to see top5 flag amount of all time")
        if g_settings.get("stats_mode") == "sql":
            say("'/top_sprees' to see top5 killing sprees of all time")
        else:
            say("not supported in file stats mode")
    #elif (cmd.endswith(": /stats_all")):
        #player.PrintStatsAll(True)
    elif (cmd.find(": /stats") != -1):
        p, name = GetRankPlayer(msg_normal, ": /stats")
        if not p:
            say("[stats] player '" + str(name) + "' is not online.")
            return
        p.ShowStatsRound()
        #player.PrintStatsAll()
    elif (cmd.endswith(": /top_caps")):
        if g_settings.get("stats_mode") == "sql":
            sql_stats.BestFlagCaps()
        else:
            say("not supported in file stats mode")
    elif (cmd.endswith(": /top_flags")):
        if g_settings.get("stats_mode") == "sql":
            sql_stats.BestTimes()
        else:
            say("not supported in file stats mode")
    elif (cmd.endswith(": /top_kills")):
        if g_settings.get("stats_mode") == "sql":
            sql_stats.BestKillers()
        else:
            say("not supported in file stats mode")
    elif (cmd.endswith(": /top_sprees")):
        if g_settings.get("stats_mode") == "sql":
            sql_stats.BestSprees()
        else:
            say("not supported in file stats mode")
    elif (cmd.find("/rank_kills") != - 1):
        sql_stats.RankKills(GetRankName(msg_normal, ": /rank_kills"))
    elif (msg.find("/rank_flags") != - 1):
        sql_stats.RankFlagTime(GetRankName(msg_normal, ": /rank_flags"))
    elif (msg.find("/rank_caps") != - 1):
        sql_stats.RankFlagCaps(GetRankName(msg_normal, ": /rank_caps"))
    elif (cmd.find("/rank_sprees") != - 1):
        sql_stats.RankSpree(GetRankName(msg_normal, ": /rank_sprees"))
    elif (cmd.find("/rank_all") != - 1):
        name = GetRankName(msg_normal, ": /rank_all")
        if not name:
            return
        say("=== '" + str(name) + "'s stats ===")
        sql_stats.RankKills(str(name))
        sql_stats.RankFlagTime(str(name))
        sql_stats.RankFlagCaps(str(name))
        sql_stats.RankSpree(str(name))
    elif (cmd.find("/rank") != - 1):
        if not g_settings.get("stats_mode") == "sql":
            say("not supported in file stats mode")
            return
        say("'/rank_kills' to show global kills rank")
        say("'/rank_sprees' to show global spree rank")
        say("'/rank_flags' to show global flag time rank")
        say("'/rank_caps' to show global flag capture rank")
    elif (cmd.find("/achievements") != - 1):
        name = GetRankName(msg_normal, ": /achievements")
        achievements.ShowAchievements(name)
    elif (cmd.endswith(": /test")):
        p, name = GetRankPlayer(msg_normal, ": /test")
        if not p:
            say("error")
            sys.exit(1)
        say("got player: " + str(name))
        # say("current spree: " + str(p.killingspree))
    # handle this like a chat command (so it has spam prot)
    elif (IsBanReasonInStr(cmd)): 
        say("[INFO] Contact the admin on discord (" + str(g_settings.get("admin_discord")) + ") to report players.")
        name = GetRankName(msg_normal, ": ") # players containing : will be cutted in discord message but this is fine for now
        send_discord("send help <@&573940781082083339>!")
    else:
        IsCmd = False
    if IsCmd:
        SpamProtection(msg_normal)
