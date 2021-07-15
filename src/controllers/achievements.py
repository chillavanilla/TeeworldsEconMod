#!/usr/bin/env python3
"""This module defines the achievement methods"""

import sys
from base.rcon import say
from models.player import CONNECTED_PLAYERS
import save_stats
import base.settings

class AchievementsController:
    """Controls achievements"""
    def __init__(self):
        self.settings = base.settings.Settings()
        self.players_controller = None

    def init(self, players_controller):
        """Init controllers"""
        self.players_controller = players_controller

    def show_achievements(self, name):
        """Print achievements of player in chat"""
        global CONNECTED_PLAYERS
        _player = None
        for player in CONNECTED_PLAYERS:
            if player.name == name:
                _player = player
                break
        # player not online -> load from database
        if not _player:
            _player = save_stats.load_stats(name)
        if not _player:
            say("'" + str(name) + "' is unranked on this server")
            return False

        if str(_player.a_haxx0r) == "" and str(_player.a_blazeit) == "" and str(
                _player.a_satan) == "" and str(_player.a_virgin) == "":
            say("'" + str(name) + "' didn't unlock any achievements yet")
            return True
        say("=== '" + str(name) + "'s achievements ===")
        if str(_player.a_haxx0r) != "":
            say("[" + str(_player.a_haxx0r) + "] haxx0r")
        if str(_player.a_blazeit) != "":
            say("[" + str(_player.a_blazeit) + "] blaze it")
        if str(_player.a_satan) != "":
            say("[" + str(_player.a_satan) + "] satan")
        if str(_player.a_virgin) != "":
            say("[" + str(_player.a_virgin) + "] virgin")
        return True


    def check_flag(self, player_obj, time):
        """Check if the flag time is an achievement"""
        if not player_obj:
            if self.settings.get("hotplug") == 1:
                return
            say("[ERROR] check flag failed: invalid player.")
            sys.exit(1)
        name = player_obj.name
        if str(time) == "13.37":
            if self.players_controller.update_achievement(player_obj, "haxx0r"):
                say("[achievement] '" + str(name) + "' unlocked: haxx0r")
        elif str(time) == "4.20":
            if self.players_controller.update_achievement(player_obj, "blazeit"):
                say("[achievement] '" + str(name) + "' unlocked: blaze it")
        elif str(time) == "6.66":
            if self.players_controller.update_achievement(player_obj, "satan"):
                say("[achievement] '" + str(name) + "' unlocked: satan")
        elif str(time) == "6.90":
            if self.players_controller.update_achievement(player_obj, "virgin"):
                say("[achievement] '" + str(name) + "' unlocked: virgin")
        # else:
            #say("'" + str(time) + "' is no achievement time")
