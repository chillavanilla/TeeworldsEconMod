#!/usr/bin/env python3
"""The module defines the Player object and some helper methods"""

import datetime
from base.rcon import say

CONNECTED_PLAYERS = []


def calc_kd(kills, deaths):
    """Return the Kills/Deaths ratio as a string."""
    if kills == 0:
        return str(0)
    if deaths == 0:
        return str(kills)
    return str("%.2f" % (kills / deaths))


def best_time(time1, time2):
    """Return the best of two given times."""
    time = min(time1, time2)
    if time == 0:
        return max(time1, time2)  # if no time yet --> set the highest
    return time  # if captured already use lowest time


def a_best(achievement1, achievement2):
    """Return the best of two given achievements"""
    if achievement1 == "":
        return achievement2
    elif achievement2 == "":
        return achievement1
    if achievement1 < achievement2:
        return achievement1  # use oldest time
    return achievement2


class Player:
    """The Player object keeps track of stats"""

    def __init__(self, name, cid=-1, ip_addr="", time=0.0, spree=0, team=""):
        self.cid = cid
        self.ip_addr = ip_addr
        self.name = name
        self.kills = 0
        self.weapon_kills = {
            0: 0,  # hammer
            1: 0,  # gun
            2: 0,  # shotgun
            3: 0,  # grenade
            4: 0,  # rifle
            5: 0  # ninja
        }
        self.double_kills = {
            0: 0,  # hammer
            1: 0,  # gun
            2: 0,  # shotgun
            3: 0,  # grenade
            4: 0,  # rifle
            5: 0  # ninja
        }
        self.deaths = 0
        self.flag_grabs = 0
        self.flag_caps_red = 0
        self.flag_caps_blue = 0
        self.flag_time = time
        self.flagger_kills = 0
        self.best_spree = spree
        self.wins = 0
        self.looses = 0
        self.a_haxx0r = ""
        self.a_blazeit = ""
        self.a_satan = ""
        self.a_virgin = ""
        # round variables (not saved)
        self.killingspree = 0
        self.last_kill = 0               # time
        self.last_multi_kill = None       # time
        self.last_multi_kill_weapon = None  # weapon id
        self.current_multi = 0           # max 32
        self.is_combo_multi = False       # gets set to true if weapons switch during multi
        self.is_flagger = False
        self.team = team
        self.last_chat = datetime.datetime.now()
        self.mute_score = 0
        self.is_muted = False
        self.grab_timestamp = ""

    def __add__(self, other):
        tmp_player = Player(self.name)
        tmp_player.kills = self.kills + other.kills
        tmp_player.double_kills[0] = self.double_kills[0] + \
            other.double_kills[0]  # hammer
        tmp_player.double_kills[1] = self.double_kills[1] + \
            other.double_kills[1]  # gun
        tmp_player.double_kills[2] = self.double_kills[2] + \
            other.double_kills[2]  # shotgun
        tmp_player.double_kills[3] = self.double_kills[3] + \
            other.double_kills[3]  # grenade
        tmp_player.double_kills[4] = self.double_kills[4] + \
            other.double_kills[4]  # rilfe
        tmp_player.double_kills[5] = self.double_kills[5] + \
            other.double_kills[5]  # ninja
        # tmp_player.weapon_kills[0] = self.weapon_kills[0] + other.weapon_kills[0] # hammer
        # tmp_player.weapon_kills[1] = self.weapon_kills[1] + other.weapon_kills[1] # gun
        # tmp_player.weapon_kills[2] = self.weapon_kills[2] + other.weapon_kills[2] # shotgun
        # tmp_player.weapon_kills[3] = self.weapon_kills[3] + other.weapon_kills[3] # grenade
        # tmp_player.weapon_kills[4] = self.weapon_kills[4] + other.weapon_kills[4] # rilfe
        # tmp_player.weapon_kills[5] = self.weapon_kills[5] + other.weapon_kills[5] # ninja
        tmp_player.weapon_kills[0] = max(
            self.weapon_kills[0],
            other.weapon_kills[0])  # hammer
        tmp_player.weapon_kills[1] = max(
            self.weapon_kills[1], other.weapon_kills[1])  # gun
        tmp_player.weapon_kills[2] = max(
            self.weapon_kills[2],
            other.weapon_kills[2])  # shotgun
        tmp_player.weapon_kills[3] = max(
            self.weapon_kills[3],
            other.weapon_kills[3])  # grenade
        tmp_player.weapon_kills[4] = max(
            self.weapon_kills[4],
            other.weapon_kills[4])  # rilfe
        tmp_player.weapon_kills[5] = max(
            self.weapon_kills[5],
            other.weapon_kills[5])  # ninja
        tmp_player.deaths = self.deaths + other.deaths
        tmp_player.flag_grabs = self.flag_grabs + other.flag_grabs
        tmp_player.flag_caps_red = self.flag_caps_red + other.flag_caps_red
        tmp_player.flag_caps_blue = self.flag_caps_blue + other.flag_caps_blue
        tmp_player.flag_time = best_time(self.flag_time, other.flag_time)
        tmp_player.flagger_kills = self.flagger_kills + other.flagger_kills
        tmp_player.best_spree = max(self.best_spree, other.best_spree)
        tmp_player.wins = self.wins + other.wins
        tmp_player.looses = self.looses + other.looses
        tmp_player.a_haxx0r = a_best(self.a_haxx0r, other.a_haxx0r)
        tmp_player.a_blazeit = a_best(self.a_blazeit, other.a_blazeit)
        tmp_player.a_satan = a_best(self.a_satan, other.a_satan)
        tmp_player.a_virgin = a_best(self.a_virgin, other.a_virgin)
        # say("== merging '" + other.name + "' -> into -> '" + self.name + "' ===")
        # say("src: ")
        # say("k/d: " +
        #     str(other.kills) +
        #     " g/r/b/t: " +
        #     str(other.flag_grabs) +
        #     "/" +
        #     str(other.flag_caps_red) +
        #     "/" +
        #     str(other.flag_caps_blue) +
        #     "/" +
        #     str(other.flag_time))
        # say("dst: ")
        # say("k/d: " +
        #     str(self.kills) +
        #     " g/r/b/t: " +
        #     str(self.flag_grabs) +
        #     "/" +
        #     str(self.flag_caps_red) +
        #     "/" +
        #     str(self.flag_caps_blue) +
        #     "/" +
        #     str(self.flag_time))
        # say("merge: ")
        # say("k/d: " +
        #     str(tmp_player.kills) +
        #     " g/r/b/t: " +
        #     str(tmp_player.flag_grabs) +
        #     "/" +
        #     str(tmp_player.flag_caps_red) +
        #     "/" +
        #     str(tmp_player.flag_caps_blue) +
        #     "/" +
        #     str(tmp_player.flag_time))
        return tmp_player

    def show_stats(self):
        """Send a string with the stats into the chat"""
        say("[stats] '" +
            str(self.name) +
            "' kills: " +
            str(self.kills) +
            " deaths: " +
            str(self.deaths) +
            " killingspree: " +
            str(self.best_spree))
        #say("[stats] '" + self.name + "' flagtime: " + str(self.flag_time))

    def show_stats_round(self):
        """Send a string with the round stats into the chat"""
        say("[round-stats] '" + str(self.name) + "' kd: " + calc_kd(self.kills,
            self.deaths) + " (" + str(self.kills) + "/" + str(self.deaths) + ")")
        # say("hammer: " + str(self.weapon_kills[0]))
        # say("gun: " + str(self.weapon_kills[1]))
        # say("shotgun: " + str(self.weapon_kills[2]))
        # say("grenade: " + str(self.weapon_kills[3]))
        # say("rifle: " + str(self.weapon_kills[4]))
        # say("ninja: " + str(self.weapon_kills[5]))
