#!/usr/bin/env python3
"""flag grabs and captures"""

import sys
import re
from base.rcon import say
import controllers.players
import game
import achievements
import base.generic
import g_settings

def __handle_flag_cap(player_obj, time, flag_color):
    """called by 0.6 and 0.7 parser"""
    if not player_obj:
        if g_settings.get("hotplug") == 1:
            return
        say("[ERROR] flag capture error: player is invalid.")
        sys.exit(1)
    if flag_color == player_obj.team:
        say("[ERROR] flag capture error: flag color matches team color.")
        say("   team=" + player_obj.team)
        say("   flag=" + flag_color)
        sys.exit(1)
    name = player_obj.name
    achievements.check_flag(player_obj, time)
    controllers.players.update_player_flag_time(player_obj, time)
    controllers.players.set_flagger(player_obj, False)
    controllers.players.update_player_flag_caps(player_obj, flag_color, 1)
    if g_settings.get("debug"):
        say("[DEBUG] flag cap '" + name +
            "' in '" + str(time) + "' secs color: '" + flag_color + "'")

def handle_flag_cap_06(data):
    """0.6 flag cap"""
    if g_settings.get("tw_version")[0:3] != "0.6":
        return
    flag_color = "pink"
    if data.find("blue", 5, 20) != -1:
        flag_color = "blue"
        game.update_flag_caps(True)
    elif data.find("red", 5, 20) != -1:
        flag_color = "red"
        game.update_flag_caps(False)

    name_start = data.find("'") + 1
    name_end = data.rfind("'")
    name = data[name_start:name_end]

    time = "60.00" # cap slower than 60 seconds --> doesnt show time
    if data.endswith(" seconds)\n"):
        time_start = data.rfind("(") + 1
        time_end = data.rfind(" sec")
        time = data[time_start:time_end]
    player = controllers.players.get_player_by_name(name)
    __handle_flag_cap(player, time, flag_color)

def handle_flag_cap(data):
    """0.7 flag cap"""
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
    match = re.match(
        r"^\[game\]: flag_capture player='(?P<id>-?\d{1,2}):(?P<name>.*)' "
        r"team=(?P<team>-?\d{1,2}) time=(?P<time>\d+\.\d{2})$", data)
    if not match:
        if g_settings.get("debug"):
            say("[WARNING] flag time not found. Please update to newer version of teeworlds.")
        return
    if g_settings.get("debug"):
        say("[DEBUG] flag cap in '" + match.group("time") + "' seconds.")
    player = controllers.players.get_player_by_id(match.group("id"))
    flag_color = "red"
    if player.team == "red":
        flag_color = "blue"
    __handle_flag_cap(player, match.group("time"), flag_color)

def handle_flag_grab(timestamp, data):
    """parse flag grab message"""
    id_start = data.find("'", 10) + 1
    id_end   = base.generic.cfind(data, ":", 2)
    id_str   = data[id_start:id_end]
    player = controllers.players.get_player_by_id(id_str)
    if not player:
        if g_settings.get("hotplug") == 1:
            return
        say("[ERROR] flag_grab player not found ID=" + str(id_str))
        controllers.players.debug_player_list()
        sys.exit(1)
    name_start = data.find(":", 10) + 1  # first '
    name_end   = data.rfind("'")     # last '
    name       = data[name_start:name_end]
    if player.name != name:
        say("[ERROR] name missmatch p.name='" + str(player.name) + "' name='" + str(name) + "'")
        sys.exit(1)
    controllers.players.update_player_flag_grabs(player, 1)
    controllers.players.set_flagger(player, True, timestamp)
    if g_settings.get("debug"):
        say("[DEBUG] '" + str(name) + "' grabbed the flag ts=" + str(timestamp))
