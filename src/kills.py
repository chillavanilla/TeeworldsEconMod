#!/usr/bin/env python3
"""Module that parses kill messages"""

import sys
import re
from base.rcon import say
import g_settings
import controllers.players

class Player:
    """Store player data for kills"""
    def __init__(self, obj, name, cid):
        self.obj = obj
        self.name = name
        self.cid = cid
class Kill:
    """Data storage class"""
    def __init__(self, killer, victim, weapon):
        self.killer = killer
        self.victim = victim
        self.weapon = weapon

def handle_kills_06(data):
    """Parse vanilla 0.6 kill messages"""
    # sample kill messages:
    # [game]: kill killer='0:ChillerDragon' victim='1:ChillerDragon.*' weapon=3 special=0
    # [game]: kill killer='0:A' victim='1:ChillerDragon.*' weapon=3 special=0

    killer_start = data.find(":", 10) + 1
    killer_end = data.find("' victim='", killer_start + 1)
    killer_name = data[killer_start:killer_end]
    killer = controllers.players.get_player_by_name(killer_name)

    victim_start = data.find(":", killer_end) + 1
    victim_end = data.find("' weapon=", victim_start + 1)
    victim_name = data[victim_start:victim_end]
    victim = controllers.players.get_player_by_name(victim_name)

    weapon_start = data.rfind("weapon=") + 7
    weapon_end = data.rfind(" special=")
    weapon = data[weapon_start:weapon_end]
    return Kill(Player(killer, killer_name, -1), Player(victim, victim_name, -1), weapon)

def handle_kills_07_and_ddnet(data):
    """Handle kill messages in ddnet or 0.7 format"""
    if g_settings.get("tw_version") == "ddnet":
        # [game]: kill killer='5:chiller' victim='5:chiller'
        # weapon=-3 special=0 killer_team:0 victim_team:0

        # [game]: kill killer='6:chiller.*' victim='5:chiller'
        # weapon=-2 special=0 killer_team:0 victim_team:0
        match = re.match(
            r"^\[game\]: kill killer='(?P<k_id>-?\d{1,2}):(?P<k_name>.*)' "
            r"victim='(?P<v_id>-?\d{1,2}):(?P<v_name>.+?)' "
            r"weapon=(?P<weapon>-?\d) "
            r"special=(\d) killer_team:(?P<k_team>-?\d{1,2}) "
            r"victim_team:(?P<v_team>-?\d{1,2})$", data)
    else:
        # teeworlds 0.7
        #                     id:team                   id:team
        # [game]: kill killer='0:0:nameless tee' victim='0:0:nameless tee' weapon=-1 special=0
        # [game]: kill killer='-2:1:' victim='0:0:ChillerDragon' weapon=3 special=0
        # use .* for killer but .+? for victim
        # because killer can be empty if it left the server before the projectile hit
        match = re.match(
            r"^\[game\]: kill killer='(?P<k_id>-?\d{1,2}):(?P<k_team>-?\d{1,2}):(?P<k_name>.*)' "
            r"victim='(?P<v_id>-?\d{1,2}):(?P<v_team>-?\d{1,2}):(?P<v_name>.+?)' "
            r"weapon=(?P<weapon>-?\d) special=(\d)$", data)

    if match:
        if g_settings.get("debug"):
            say(
                "KILLER ID=<%s> TEAM=<%s> NAME=<%s> "
                "VICTIM ID=<%s> TEAM=<%s> NAME=<%s> weapon=<%s>" % (
                    match.group("k_id"), match.group("k_team"), match.group("k_name"),
                    match.group("v_id"), match.group("v_team"), match.group("v_name"),
                    match.group("weapon")
                )
            )
        if match.group("k_name") == "" or int(match.group("k_id")) < 0:
            killer_name = "a left player"
            killer_id = match.group("k_id")
            killer = None
        else:
            killer_name = match.group("k_name")
            killer_id = match.group("k_id")
            killer = controllers.players.get_player_by_id(killer_id)

        victim_name = match.group("v_name")
        victim_id = match.group("v_id")
        victim = controllers.players.get_player_by_id(victim_id)

        weapon = match.group("weapon")
    else:
        say("[ERROR] failed parsing kill msg: " + str(data))
        sys.exit(1)
    return Kill(
        Player(killer, killer_name, killer_id),
        Player(victim, victim_name, victim_id),
        weapon)

def handle_kills(timestamp, data):
    """Parse kill message. Track kills, deaths and flags"""
    kill = None

    if g_settings.get("tw_version")[0:3] == "0.6" or \
        g_settings.get("tw_version") is None: # default 6
        kill = handle_kills_06(data)
    else: # teeworlds 0.7 or ddnet
        kill = handle_kills_07_and_ddnet(data[:-1])

    # don't count suicide as kill or when killer left already
    if not kill.killer.obj == kill.victim.obj and kill.killer.obj:
        if not controllers.players.update_player_kills(kill.killer.obj, 1, int(kill.weapon)):
            if g_settings.get("hotplug") == 1:
                return
            say("[ERROR] failed adding kill:")
            say("   ID=" + str(kill.killer.cid))
            say("   NAME=" + str(kill.killer.name))
            say("   OBJ=" + str(kill.killer.obj))
            say("   DATA=" + data)
            sys.exit(1)
    if str(kill.weapon) != "-3": # don't count disconnect or teamswitch as death
        if not controllers.players.update_player_deaths(kill.victim.obj, kill.killer.name, 1):
            if g_settings.get("hotplug") == 1:
                return
            say("[ERROR] failed adding death:")
            say("   ID=" + str(kill.victim.cid))
            say("   NAME=" + str(kill.victim.name))
            say("   OBJ=" + str(kill.victim.obj))
            say("   DATA=" + data)
            sys.exit(1)

    # say("[KILL] killer=" + killer_name + " victim=" + victim_name + " weapon=" + str(weapon))
    controllers.players.check_flagger_kill(kill.victim.name, kill.killer.name)
    controllers.players.set_flagger(kill.victim.obj, False, timestamp)
