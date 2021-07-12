#!/usr/bin/env python3
import os.path
import urllib.parse
from chiller_essential import *
from kills import *
import g_settings

def StatsFile(name):
    return g_settings.get("file_database") + urllib.parse.quote_plus(name) + ".acc"

def HasStats(name):
    if name == None:
        return False
    if os.path.isfile(StatsFile(name)):
        return True
    return False

def save_stats_file(player):
    if not player:
        say("[stats] failed to save player.")
        return False
    name = player.name
    if HasStats(name):
        #say("[stats] found stats --> loading and appending")
        load_player = load_stats_file(name)
        if not load_player:
            say("[stats] (save) error loading stats for player='" + name + "' filename='" + StatsFile(name) + "'")
            sys.exit(1)
            return False
        player = player + load_player
    try:
        sf = open(StatsFile(name), "w")
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
        say("[stats] (save) error saving stats for player='" + name + "' filename='" + StatsFile(name) + "'")
        sys.exit(1)
    return False

def load_stats_file(name):
    from base_player import Player
    if not HasStats(name):
        return None
    try:
        sf = open(StatsFile(name), "r")
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
        say("[ERROR] (load) failed to loaded stats for name='" + name + "' filename='" + StatsFile(name) + "'")
        sys.exit(1)
        return None

def save_stats_partially_file(player):
    if not player:
        say("[stats] (partially) failed to load player.")
        return False
    name = player.name
    if HasStats(name):
        #say("[stats] found stats --> loading and appending")
        load_player = load_stats_file(name)
        if not load_player:
            say("[stats] (partially) error loading stats for player='" + name + "' filename='" + StatsFile(name) + "'")
            sys.exit(1)
            return False
        player = player + load_player
    try:
        sf = open(StatsFile(name), "w")
        sf.write("0" + "\n")
        sf.write("0" + "\n")
        sf.write("0" + "\n")
        sf.write("0" + "\n")
        sf.write("0" + "\n")
        sf.write("0.0" + "\n")
        sf.write("0" + "\n")
        sf.write(str(player.best_spree) + "\n")
        sf.write("0" + "\n")
        sf.write("0" + "\n")
        sf.write("" + "\n")
        sf.write("" + "\n")
        sf.write("" + "\n")
        sf.write("" + "\n")
        sf.close()
        return True
    except:
        say("[stats] (partially) error saving stats for player='" + name + "' filename='" + StatsFile(name) + "'")
        sys.exit(1)
    return False