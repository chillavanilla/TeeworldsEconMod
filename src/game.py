#!/usr/bin/env python3.7
from chiller_essential import *
import player
import kills

caps_red = 0 # they are seen as score
caps_blue = 0 # it doesnt track how often the blue flag was captured but how often the blue team capped teh red flag

def UpdateFlags(IsRed):
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

def HandleGame(data):
    if (data.find("kill killer") != -1):
        kills.HandleKills(data)
    elif (data.startswith("[game]: start round type='")):
        global caps_red
        global caps_blue
        # [game]: start round type='CTF' teamplay='1'
        say("[SERVER] ChillerDragon wishes you all hf & gl c:")
        player.RefreshAllPlayers()
        if (data.startswith("[game]: start round type='CTF'")):
            if caps_red == 0 and caps_blue == 0: #already catched by 10 flags auto detection
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
        player.SetFlagger(name, True)
        #say("'" + name + "' grabbed the flag")
