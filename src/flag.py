#!/usr/bin/env python3
import sys
import time
from chat import *
from kills import *
from player import *
from game import *

def HandleFlagCap(data):
    flag_color = "pink"
    if (data.find("blue", 5, 20) != -1):
        flag_color = "blue"
    elif (data.find("red", 5, 20) != -1):
        flag_color = "red"

    name_start = data.find("'") + 1
    name_end = data.rfind("'")
    name = data[name_start:name_end] 

    time_start = data.rfind("(") + 1
    time_end = data.rfind(" sec")
    time = data[time_start:time_end]

    say("flag cap '" + name + "' in " + time + " secs color: " + flag_color)

    UpdatePlayerFlagCaps(name, flag_color, 1)
