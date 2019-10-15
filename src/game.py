#!/usr/bin/env python3
import datetime
from chiller_essential import *
import cbase
import player
import kills

caps_red = 0 # they are seen as score
caps_blue = 0 # it doesnt track how often the blue flag was captured but how often the blue team capped the red flag
grabs_red = 0
grabs_blue = 0

def GetBestScore():
    return max(GetScoreRed(), GetScoreBlue())

def GetScoreRed():
    return caps_red * 100 + grabs_red

def GetScoreBlue():
    return caps_blue * 100 + grabs_blue

def UpdateFlagGrabs(IsRed):
    global grabs_red
    global grabs_blue
    if IsRed:
        grabs_red += 1
    else:
        grabs_blue += 1

def UpdateFlagCaps(IsRed):
    global caps_red
    global caps_blue
    if IsRed:
        caps_red += 1
    else:
        caps_blue += 1
    if caps_red > 9:
        UpdateWins(True)
    elif caps_blue > 9:
        UpdateWins(False)

def UpdateWins(IsRed):
    global caps_red
    global caps_blue
    caps_red = 0
    caps_blue = 0
    if IsRed:
        echo("red won")
        if player.CountPlayers() > g_settings.get("win_players"):
            player.TeamWon("red")
    else:
        echo("blue won")
        if player.CountPlayers() > g_settings.get("win_players"):
            player.TeamWon("blue")

def HandleGame(timestamp, data):
    if (data.find("kill killer") != -1):
        kills.HandleKills(timestamp, data)
    elif (data.startswith("[game]: start round type='")):
        global caps_red
        global caps_blue
        # [game]: start round type='CTF' teamplay='1'
        say("[SERVER] ChillerDragon wishes you all hf & gl c:")
        player.RefreshAllPlayers()
        if (data.startswith("[game]: start round type='CTF'")):
            if caps_red == 0 and caps_blue == 0: # already catched by 10 flags auto detection
                return
            if caps_red > caps_blue:
                UpdateWins(True)
            elif caps_red < caps_blue:
                UpdateWins(False)
            else:
                say("draw lul")
    elif (data.startswith("[game]: flag_grab player='")):
        name_start = data.find(":", 10) + 1  # first '
        name_end   = data.rfind("'")     # last '
        name = data[name_start:name_end]
        player.UpdatePlayerFlagGrabs(name, 1)
        player.SetFlagger(name, True, timestamp)
        if g_settings.get("debug"):
            say("'" + str(name) + "' grabbed the flag ts=" + str(timestamp))
    # [2019-10-15 11:41:04][game]: flag_capture player='0:ChillerDragon' team=0
    elif (data.startswith("[game]: flag_capture player='")):
        # UNUSED CODE FOR NOW
        # NOT PRECISE ENOUGH
        # DOES NOTHING CURRENTLY
        id_start = data.find("'", 10) + 1
        id_end   = cbase.cfind(data, ":", 2)
        id_str = data[id_start:id_end]
        p = player.GetPlayerByID(id_str)
        if not p:
            say("[ERROR] flag_cap player not found ID=" + str(id_str))
            player.DebugPlayerList()
            sys.exit(1)
        # logs are only seconds precise but usual tw mesurement is two digits more precise
        t1 = datetime.datetime.strptime(p.grab_timestamp, "%Y-%m-%d %H:%M:%S")
        t2 = datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        diff = (t2 - t1).total_seconds()
        if g_settings.get("debug"):
            say("'" + str(p.name) + "' capped the flag ts=" + str(timestamp) + " secs=" + str(diff))