#!/usr/bin/env python3
from chiller_essential import *
from base_player import *
import player

def ShowAchivements(name):
    global aPlayers
    for player in aPlayers:
        if player.name == name:
            if str(player.a_haxx0r) == "" and str(player.a_blazeit) == "" and str(player.a_satan) == "" and str(player.a_virgin) == "":
                say("'" + str(name) + "' didn't unlock any achivements yet")
                return True
            say("=== '" + str(name) + "'s achivements ===")
            if not str(player.a_haxx0r) == "":
                say("[" + str(player.a_haxx0r) +"] haxx0r")
            if not str(player.a_blazeit) == "":
                say("[" + str(player.a_blazeit) +"] blaze it")
            if not str(player.a_satan) == "":
                say("[" + str(player.a_satan) +"] satan")
            if not str(player.a_virgin) == "":
                say("[" + str(player.a_virgin) +"] virgin")
            return True
    return False

def CheckFlag(name, time):
    if str(time) == str(13.37):
        if player.UpdateAchivement(name, "haxx0r"):
            say("[achivement] '" + str(name) + "' unlocked: haxx0r")
    elif str(time) == str(4.2):
        if player.UpdateAchivement(name, "blazeit"):
            say("[achivement] '" + str(name) + "' unlocked: blaze it")
    elif str(time) == str(6.66):
        if player.UpdateAchivement(name, "satan"):
            say("[achivement] '" + str(name) + "' unlocked: satam")
    elif str(time) == str(6.9):
        if player.UpdateAchivement(name, "virgin"):
            say("[achivement] '" + str(name) + "' unlocked: virgin")
    #else:
        #say("'" + str(time) + "' is no achivement time")
