#!/usr/bin/env python3
"""Plaintext based database"""

import sys
import os.path
import urllib.parse
from base.rcon import say
import base.settings
from models.player import Player

def stats_path(name: str) -> str:
    """Generate path to statsfile of given name"""
    return base.settings.Settings().get("file_database") + urllib.parse.quote_plus(name) + ".acc"

def hash_stats(name: str) -> str:
    """Check if given name has a stats record"""
    if name is None:
        return False
    if os.path.isfile(stats_path(name)):
        return True
    return False

def save_stats_file(player: Player):
    """Save stats to file given a player object"""
    if not player:
        say("[stats] failed to save player.")
        return False
    name = player.name
    if hash_stats(name):
        #say("[stats] found stats --> loading and appending")
        load_player = load_stats_file(name)
        if not load_player:
            say(
                "[stats] (save) error loading stats for player='" + \
                name + "' filename='" + \
                stats_path(name) + "'"
                )
            sys.exit(1)
        player = player + load_player
    try:
        with open(stats_path(name), "w") as stats_file:
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
    except OSError:
        say(
            "[stats] (save) error saving stats for player='" + \
            name + "' filename='" + stats_path(name) + "'")
        sys.exit(1)

def load_stats_file(name: str):
    """Return player object given a name"""
    if not hash_stats(name):
        return None
    try:
        with open(stats_path(name), "r") as stats_file:
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
    except OSError:
        say("[ERROR] (load) failed to loaded stats for name='" + name +
            "' filename='" + stats_path(name) + "'")
        sys.exit(1)
        return None

def save_stats_partially_file(player: Player) -> bool:
    """Save only killingspree"""
    if not player:
        say("[stats] (partially) failed to load player.")
        return False
    name = player.name
    if hash_stats(name):
        #say("[stats] found stats --> loading and appending")
        load_player = load_stats_file(name)
        if not load_player:
            say(
                "[stats] (partially) error loading stats for player='" + \
                name + \
                "' filename='" + \
                stats_path(name) + "'"
                )
            sys.exit(1)
        player = player + load_player
    try:
        with open(stats_path(name), "w") as stats_file:
            stats_file.write("0" + "\n")
            stats_file.write("0" + "\n")
            stats_file.write("0" + "\n")
            stats_file.write("0" + "\n")
            stats_file.write("0" + "\n")
            stats_file.write("0.0" + "\n")
            stats_file.write("0" + "\n")
            stats_file.write(str(player.best_spree) + "\n")
            stats_file.write("0" + "\n")
            stats_file.write("0" + "\n")
            stats_file.write("" + "\n")
            stats_file.write("" + "\n")
            stats_file.write("" + "\n")
            stats_file.write("" + "\n")
            stats_file.close()
            return True
    except OSError:
        say(
            "[stats] (partially) error saving stats for player='" + \
            name + "' filename='" + stats_path(name) + "'")
        sys.exit(1)
