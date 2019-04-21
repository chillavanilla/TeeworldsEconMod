#!/usr/bin/env python3.7
from chiller_essential import *
from base_player import *
import player
import save_stats

def ShowAchievements(name):
    global aPlayers
    player = None
    for p in aPlayers:
        if p.name == name:
            player = p
            break
    # player not online -> load from database
    if not player:
        player = save_stats.LoadStats(name)
    if not player:
        say("'" + str(name) + "' is unranked on this server")
        return False

    if str(player.a_haxx0r) == "" and str(player.a_blazeit) == "" and str(player.a_satan) == "" and str(player.a_virgin) == "":
        say("'" + str(name) + "' didn't unlock any achievements yet")
        return True
    say("=== '" + str(name) + "'s achievements ===")
    if not str(player.a_haxx0r) == "":
        say("[" + str(player.a_haxx0r) +"] haxx0r")
    if not str(player.a_blazeit) == "":
        say("[" + str(player.a_blazeit) +"] blaze it")
    if not str(player.a_satan) == "":
        say("[" + str(player.a_satan) +"] satan")
    if not str(player.a_virgin) == "":
        say("[" + str(player.a_virgin) +"] virgin")
    return True


def CheckFlag(name, time):
    if str(time) == "13.37":
        if player.UpdateAchievement(name, "haxx0r"):
            say("[achievement] '" + str(name) + "' unlocked: haxx0r")
    elif str(time) == "4.20":
        if player.UpdateAchievement(name, "blazeit"):
            say("[achievement] '" + str(name) + "' unlocked: blaze it")
    elif str(time) == "6.66":
        if player.UpdateAchievement(name, "satan"):
            say("[achievement] '" + str(name) + "' unlocked: satan")
    elif str(time) == "6.90":
        if player.UpdateAchievement(name, "virgin"):
            say("[achievement] '" + str(name) + "' unlocked: virgin")
    #else:
        #say("'" + str(time) + "' is no achievement time")
