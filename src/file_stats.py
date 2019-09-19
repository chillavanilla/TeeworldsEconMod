#!/usr/bin/env python3
from chiller_essential import *
from kills import *
import g_settings
import os.path

def HasStats(name):
    if name == None:
        return False
    if os.path.isfile(g_settings.get("file_database") + name + ".acc"):
        return True
    return False

def SaveStatsFile(name):
    from player import GetPlayerByName
    player = GetPlayerByName(name)
    if not player:
        say("[stats] failed to load player '" + name + "'")
        return False
    if HasStats(name):
        #say("[stats] found stats --> loading and appending")
        load_player = LoadStatsFile(name)
        if not load_player:
            say("[stats] error loading stats for player '" + name + "'")
            return False
        player = player + load_player
    try:
        sf = open(g_settings.get("file_database") + name + ".acc", "w")
        sf.write(str(player.kills) + "\n")
        sf.write(str(player.deaths) + "\n")
        sf.write(str(player.flag_grabs) + "\n")
        sf.write(str(player.flag_caps_red) + "\n")
        sf.write(str(player.flag_caps_blue) + "\n")
        sf.write(str(player.flag_time) + "\n")
        sf.write(str(player.flagger_kills) + "\n")
        sf.write(str(player.best_spree) + "\n")
        sf.write(str(player.wins) + "\n")
        sf.write(str(player.looses) + "\n")
        sf.write(str(player.a_haxx0r) + "\n")
        sf.write(str(player.a_blazeit) + "\n")
        sf.write(str(player.a_satan) + "\n")
        sf.write(str(player.a_virgin) + "\n")
        sf.close()
        return True
    except:
        say("[stats] error saving stats for '" + name + "'")
    return False

def LoadStatsFile(name):
    from player import Player
    if not HasStats(name):
        return None
    try:
        sf = open(g_settings.get("file_database") + name + ".acc", "r")
        player = Player(name)
        player.kills = int(sf.readline())
        player.deaths = int(sf.readline())
        player.flag_grabs = int(sf.readline())
        player.flag_caps_red = int(sf.readline())
        player.flag_caps_blue = int(sf.readline())
        player.flag_time = float(sf.readline())
        player.flagger_kills = int(sf.readline())
        player.best_spree = int(sf.readline())
        player.wins = int(sf.readline())
        player.looses = int(sf.readline())
        player.a_haxx0r = str(sf.readline())
        player.a_blazeit = str(sf.readline())
        player.a_satan = str(sf.readline())
        player.a_virgin = str(sf.readline())
        sf.close()
        return player
    except:
        say("[ERROR] failed to loaded stats for '" + name + "'")
        return None
