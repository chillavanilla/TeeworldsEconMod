#!/usr/bin/env python3
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
        player.TeamWon("red")
    else:
        echo("blue won")
        player.TeamWon("blue")

def HandleGame(data):
    if (data.find("kill killer") != -1):
        kills.HandleKills(data)
    elif (data.startswith("[game]: start round type='")):
        say("[SERVER] ChillerDragon wishes you all hf & gl c:")
        #TODO: reset IsFlagger value here and maybe reset all values here
        pass
    elif (data.startswith("[game]: flag_grab player='")):
        name_start = data.find(":", 10) + 1  # first '
        name_end   = data.rfind("'")     # last '
        name = data[name_start:name_end]
        player.UpdatePlayerFlagGrabs(name, 1)
        player.SetFlagger(name, True)
        #say("'" + name + "' grabbed the flag")
