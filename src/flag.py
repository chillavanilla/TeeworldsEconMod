#!/usr/bin/env python3
import sys
import time
from chat import *
from kills import *
import player
import game
import achievements
import g_settings

def __HandleFlagCap(player_obj, time, flag_color):
    if not player_obj:
        say("[ERROR] flag capture error: player is invalid.")
        sys.exit(1)
    if flag_color == player_obj.team:
        say("[ERROR] flag capture error: flag color matches team color.")
        say("   team=" + player_obj.team)
        say("   flag=" + flag_color)
        sys.exit(1)
    name = player_obj.name
    achievements.CheckFlag(player_obj, time)
    player.UpdatePlayerFlagTime(player_obj, time)
    player.SetFlagger(player_obj, False)
    player.UpdatePlayerFlagCaps(player_obj, flag_color, 1)
    if g_settings.get("debug"):
        say("[DEBUG] flag cap '" + name + "' in '" + str(time) + "' secs color: '" + flag_color + "'")

# 0.6 exclusive
def HandleFlagCap06(timestamp, data):
    if g_settings.get("tw_version")[0:3] != "0.6":
        return
    flag_color = "pink"
    if (data.find("blue", 5, 20) != -1):
        flag_color = "blue"
        game.UpdateFlagCaps(True)
    elif (data.find("red", 5, 20) != -1):
        flag_color = "red"
        game.UpdateFlagCaps(False)

    name_start = data.find("'") + 1
    name_end = data.rfind("'")
    name = data[name_start:name_end] 

    time = "60.00" # cap slower than 60 seconds --> doesnt show time
    if (data.endswith(" seconds)\n")):
        time_start = data.rfind("(") + 1
        time_end = data.rfind(" sec")
        time = data[time_start:time_end]
    p = player.GetPlayerByName(name)
    __HandleFlagCap(p, time, flag_color)

# 0.7 exclusive
def HandleFlapCap07(data):
    if g_settings.get("tw_version")[0:3] != "0.7":
        return
    # old 0.7
    # flag_capture player='0:ChillerDragon' team=0
    # new 0.7
    # flag_capture player='0:ChillerDragon' team=0 time=6.32
    # flag_capture player='0:ChillerDragon' team=0 time=0.72
    # flag_capture player='0:ChillerDragon' team=0 time=1.30
    # flag_capture player='0:ChillerDragon' team=0 time=113.94
    data = data[:-1]
    m = re.match(r"^\[game\]: flag_capture player='(?P<id>-?\d{1,2}):(?P<name>.*)' team=(?P<team>-?\d{1,2}) time=(?P<time>\d+\.\d{2})$", data)
    if not m:
        if g_settings.get("debug"):
            say("[WARNING] flag time not found. Please update to newer version of teeworlds.")
        return
    if g_settings.get("debug"):
        say("[DEBUG] flag cap in '" + m.group("time") + "' seconds.")
    p = player.GetPlayerByID(m.group("id"))
    flag_color = "red"
    if p.team == "red":
        flag_color = "blue"
    __HandleFlagCap(p, m.group("time"), flag_color)
