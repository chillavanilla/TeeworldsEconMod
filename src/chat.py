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
    words = g_settings.get("chat_filter")
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
        return None, None
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

CHAT_NONE=0
CHAT_ALL=1
CHAT_TEAM=2
CHAT_WHISPER=3

def GetChatID(msg):
    # TODO: move constants to better place
    # TODO: refactor this code
    # TODO: support versions higher than 0.7.5 (care "0.7.10" < "0.7.5" is true in python)
    # in 0.7.5 id position was swapped
    # https://github.com/teeworlds/teeworlds/commit/5090c39d94bad0b6dda8caaef271133c46c00ee0#diff-a2df712cfb938eda9a173f36c865c2cc
    id_str = None # python scoping ?!
    if g_settings.get("tw_version") == "0.7.5":
        mode_start = msg.find(" ") + 1
        mode_end = cbase.cfind(msg, ":", 2)
        mode_str = msg[mode_start:mode_end]
        msg = msg[mode_end:-1]
        if int(mode_str) == CHAT_TEAM:
            id_start = cbase.cfind(msg, ":", 2) + 1
            id_end = cbase.cfind(msg, ":", 3)
            id_str = msg[id_start:id_end]
        else:
            id_start = msg.find(":") + 1
            id_end = cbase.cfind(msg, ":", 2)
            id_str = msg[id_start:id_end]
    else:
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
        if g_settings.get("hotplug") == 1:
            return False
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
        if g_settings.get("hotplug") == 1:
            return False
        say("[WARNING] IsMuted() failed! please contact an admin")
        return False
    if (p.IsMuted):
        return True
    return False

def HandleChatMessage(msg):
    if IsMuted(msg):
        return
    prefix = g_settings.get("chat_command_prefix")
    IsCmd = True
    msg_normal = msg
    msg = msg.lower()
    chat_cmd_start = cbase.cfind(msg, ":", 4) # the first possible occurence of a chat command (to filter chat command names)
    cmd = msg[chat_cmd_start:-1] #cut newline at end
    if (cmd.endswith(": " + prefix + "help") or cmd.endswith(": " + prefix + "info") or cmd.endswith(": " + prefix + "cmdlist")):
        say("==== Teeworlds Econ Mod (TEM) ====")
        say("developed by ChillerDragon version: " + str(version.VERSION))
        say("https://github.com/ChillaVanilla/TeeworldsEconMod")
        say("'" + prefix + "help' to show this help")
        say("'" + prefix + "stats' to show round stats")
        say("'" + prefix + "achievements' to show achievements")
        if g_settings.get("stats_mode") == "sql":
            say("'" + prefix + "top5' for all time stats commands")
            say("'" + prefix + "rank' for all rank commands")
    elif (cmd.endswith(": " + prefix + "top5")):
        if g_settings.get("stats_mode") == "sql":
            say("'" + prefix + "top_kills' to see top5 killers of all time")
        if g_settings.get("stats_mode") == "sql":
            say("'" + prefix + "top_flags' to see top5 flag cap times of all time")
        if g_settings.get("stats_mode") == "sql":
            say("'" + prefix + "top_caps' to see top5 flag amount of all time")
        if g_settings.get("stats_mode") == "sql":
            say("'" + prefix + "top_sprees' to see top5 killing sprees of all time")
        else:
            say("not supported in file stats mode")
    #elif (cmd.endswith(": " + prefix + "stats_all")):
        #player.PrintStatsAll(True)
    elif (cmd.find(": " + prefix + "stats") != -1):
        if not g_settings.get("stats_mode") == "sql":
            say("not supported in file stats mode")
            return
        p, name = GetRankPlayer(msg_normal, ": " + prefix + "stats")
        if not p:
            say("[stats] player '" + str(name) + "' is not online.")
            return
        p.ShowStatsRound()
        #player.PrintStatsAll()
    elif (cmd.endswith(": " + prefix + "top_caps")):
        if g_settings.get("stats_mode") == "sql":
            sql_stats.BestFlagCaps()
        else:
            say("not supported in file stats mode")
    elif (cmd.endswith(": " + prefix + "top_flags")):
        if g_settings.get("stats_mode") == "sql":
            sql_stats.BestTimes()
        else:
            say("not supported in file stats mode")
    elif (cmd.endswith(": " + prefix + "top_kills")):
        if g_settings.get("stats_mode") == "sql":
            sql_stats.BestKillers()
        else:
            say("not supported in file stats mode")
    elif (cmd.endswith(": " + prefix + "top_sprees")):
        if g_settings.get("stats_mode") == "sql":
            sql_stats.BestSprees()
        else:
            say("not supported in file stats mode")
    elif (cmd.find("" + prefix + "rank_kills") != - 1):
        sql_stats.RankKills(GetRankName(msg_normal, ": " + prefix + "rank_kills"))
    elif (msg.find("" + prefix + "rank_flags") != - 1):
        sql_stats.RankFlagTime(GetRankName(msg_normal, ": " + prefix + "rank_flags"))
    elif (msg.find("" + prefix + "rank_caps") != - 1):
        sql_stats.RankFlagCaps(GetRankName(msg_normal, ": " + prefix + "rank_caps"))
    elif (cmd.find("" + prefix + "rank_sprees") != - 1):
        sql_stats.RankSpree(GetRankName(msg_normal, ": " + prefix + "rank_sprees"))
    elif (cmd.find("" + prefix + "rank_all") != - 1):
        name = GetRankName(msg_normal, ": " + prefix + "rank_all")
        if not name:
            return
        say("=== '" + str(name) + "'s stats ===")
        sql_stats.RankKills(str(name))
        sql_stats.RankFlagTime(str(name))
        sql_stats.RankFlagCaps(str(name))
        sql_stats.RankSpree(str(name))
    elif (cmd.find("" + prefix + "rank") != - 1):
        if not g_settings.get("stats_mode") == "sql":
            say("not supported in file stats mode")
            return
        say("'" + prefix + "rank_kills' to show global kills rank")
        say("'" + prefix + "rank_sprees' to show global spree rank")
        say("'" + prefix + "rank_flags' to show global flag time rank")
        say("'" + prefix + "rank_caps' to show global flag capture rank")
    elif (cmd.find("" + prefix + "achievements") != - 1):
        name = GetRankName(msg_normal, ": " + prefix + "achievements")
        achievements.ShowAchievements(name)
    elif (cmd.endswith(": " + prefix + "test")):
        p, name = GetRankPlayer(msg_normal, ": " + prefix + "test")
        if not p:
            if g_settings.get("hotplug") == 1:
                return
            say("error")
            sys.exit(1)
        say("got player: " + str(name))
        # say("current spree: " + str(p.killingspree))
    # handle this like a chat command (so it has spam prot)
    elif (IsBanReasonInStr(cmd)):
        admin_contact_msg()
        name = GetRankName(msg_normal, ": ") # players containing : will be cutted in discord message but this is fine for now
        if g_settings.get("filter_discord") == 1:
            send_discord("chat trigger " + str(g_settings.get("mod_discord")) + "!\n" + str(msg))
    else:
        IsCmd = False
    if IsCmd:
        SpamProtection(msg_normal)

def admin_contact_msg():
    if str(g_settings.get("admin_contact")) == "":
        return
    say("[INFO] Contact the admin " + str(g_settings.get("admin_contact")) + " to report players.")
