#!/usr/bin/env python3
import datetime
import re
from chiller_essential import *
import cbase
import player
import kills
import flag

caps_red = 0 # they are seen as score
caps_blue = 0 # it doesnt track how often the blue flag was captured but how often the blue team capped the red flag
grabs_red = 0
grabs_blue = 0

def get_best_score():
    return max(get_score_red(), get_score_blue())

def get_score_red():
    return caps_red * 100 + grabs_red

def get_score_blue():
    return caps_blue * 100 + grabs_blue

def update_flag_grabs(is_red):
    global grabs_red
    global grabs_blue
    if is_red:
        grabs_red += 1
    else:
        grabs_blue += 1

def update_flag_caps(is_red):
    global caps_red
    global caps_blue
    if is_red:
        caps_red += 1
    else:
        caps_blue += 1
    if caps_red > 9:
        update_wins(True)
    elif caps_blue > 9:
        update_wins(False)

def update_wins(is_red):
    global caps_red
    global caps_blue
    caps_red = 0
    caps_blue = 0
    if is_red:
        echo("red won")
        if player.count_players() > g_settings.get("win_players"):
            player.team_won("red")
    else:
        echo("blue won")
        if player.count_players() > g_settings.get("win_players"):
            player.team_won("blue")

def handle_game(timestamp, data):
    if (data.find("kill killer") != -1):
        kills.handle_kills(timestamp, data)
    elif (data.startswith("[game]: start round type='")):
        global caps_red
        global caps_blue
        # [game]: start round type='CTF' teamplay='1'
        say("[SERVER] ChillerDragon wishes you all hf & gl c:")
        player.refresh_all_players()
        if (data.startswith("[game]: start round type='CTF'")):
            if caps_red == 0 and caps_blue == 0: # already catched by 10 flags auto detection
                return
            if caps_red > caps_blue:
                update_wins(True)
            elif caps_red < caps_blue:
                update_wins(False)
            else:
                say("draw lul")
    elif (data.startswith("[game]: flag_grab player='")):
        id_start = data.find("'", 10) + 1
        id_end   = cbase.cfind(data, ":", 2)
        id_str   = data[id_start:id_end]
        p = player.get_player_by_id(id_str)
        if not p:
            say("[ERROR] flag_grab player not found ID=" + str(id_str))
            player.debug_player_list()
            sys.exit(1)
        name_start = data.find(":", 10) + 1  # first '
        name_end   = data.rfind("'")     # last '
        name       = data[name_start:name_end]
        if p.name != name:
            say("[ERROR] name missmatch p.name='" + str(p.name) + "' name='" + str(name) + "'")
            sys.exit(1)
        player.update_player_flag_grabs(p, 1)
        player.set_flagger(p, True, timestamp)
        if g_settings.get("debug"):
            say("[DEBUG] '" + str(name) + "' grabbed the flag ts=" + str(timestamp))
    # [2019-10-15 11:41:04][game]: flag_capture player='0:ChillerDragon' team=0
    elif (data.startswith("[game]: flag_capture player='")):
        flag.HandleFlapCap07(data)
        """
        # UNUSED CODE FOR NOW
        # NOT PRECISE ENOUGH
        # DOES NOTHING CURRENTLY
        # WOULD SUPPORT 0.7 VERSIONS PRIOR TO THIS COMMIT
        # https://github.com/teeworlds/teeworlds/commit/5c1d32f65ecaf893d589875df9eaedc1c1a76858
        # IT IS HIGHLY RECOMMENDED TO USE A LATER TW VERSION TO NOT MESS UP RECORDS
        id_start = data.find("'", 10) + 1
        id_end   = cbase.cfind(data, ":", 2)
        id_str = data[id_start:id_end]
        p = player.get_player_by_id(id_str)
        if not p:
            say("[ERROR] flag_cap player not found ID=" + str(id_str))
            player.debug_player_list()
            sys.exit(1)
        # logs are only seconds precise but usual tw mesurement is two digits more precise
        t1 = datetime.datetime.strptime(p.grab_timestamp, "%Y-%m-%d %H:%M:%S")
        t2 = datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        diff = (t2 - t1).total_seconds()
        if g_settings.get("debug"):
            say("'" + str(p.name) + "' capped the flag ts=" + str(timestamp) + " secs=" + str(diff))
        """