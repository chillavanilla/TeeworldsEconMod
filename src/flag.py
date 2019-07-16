#!/usr/bin/env python3
import sys
import time
from chat import *
from kills import *
from player import *
import game
import achievements

def HandleFlagCap(data):
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

    time = 60 #cap slower than 60 seconds --> doesnt show time
    if (data.endswith(" seconds)\n")):
        time_start = data.rfind("(") + 1
        time_end = data.rfind(" sec")
        time = data[time_start:time_end]
    achievements.CheckFlag(name, time)
    UpdatePlayerFlagTime(name, time)
    SetFlagger(name, False)
    UpdatePlayerFlagCaps(name, flag_color, 1)
    #say("flag cap '" + name + "' in " + time + " secs color: " + flag_color)

