#!/usr/bin/env python3
import os.path
import urllib.parse
from chiller_essential import *
from kills import *
import g_settings

def StatsFile(name):
    return g_settings.get("file_database") + urllib.parse.quote_plus(name) + ".acc"

def HasStats(name):
    if name is None:
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
        stats_file = open(StatsFile(name), "w")
        stats_file.write(str(player.kills) + "\n")
        stats_file.write(str(player.deaths) + "\n")
        stats_file.write(str(player.flag_grabs) + "\n")
        stats_file.write(str(player.flag_caps_red) + "\n")
        stats_file.write(str(player.flag_caps_blue) + "\n")
        stats_file.write(str(player.flag_time) + "\n")
        stats_file.write(str(player.flagger_kills) + "\n")
        stats_file.write(str(player.best_spree) + "\n")
        stats_file.write(str(player.wins) + "\n")
        stats_file.write(str(player.looses) + "\n")
        stats_file.write(str(player.a_haxx0r) + "\n")
        stats_file.write(str(player.a_blazeit) + "\n")
        stats_file.write(str(player.a_satan) + "\n")
        stats_file.write(str(player.a_virgin) + "\n")
        stats_file.close()
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
        stats_file = open(StatsFile(name), "r")
        player = Player(name)
        player.kills = int(stats_file.readline())
        player.deaths = int(stats_file.readline())
        player.flag_grabs = int(stats_file.readline())
        player.flag_caps_red = int(stats_file.readline())
        player.flag_caps_blue = int(stats_file.readline())
        player.flag_time = float(stats_file.readline())
        player.flagger_kills = int(stats_file.readline())
        player.best_spree = int(stats_file.readline())
        player.wins = int(stats_file.readline())
        player.looses = int(stats_file.readline())
        player.a_haxx0r = str(stats_file.readline())
        player.a_blazeit = str(stats_file.readline())
        player.a_satan = str(stats_file.readline())
        player.a_virgin = str(stats_file.readline())
        stats_file.close()
        return player
    except:
        say("[ERROR] (load) failed to loaded stats for name='" + name +
            "' filename='" + StatsFile(name) + "'")
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