#!/usr/bin/env python3
from chiller_essential import *
import cbase
import g_settings
import player

def HandleKills(data):
    killer_name = ""
    victim_name = ""
    killer_id = -1
    victim_id = -1
    killer = None
    victim = None
    weapon = ""

    if g_settings.get("tw_version") == 6 or g_settings.get("tw_version") == None: # default 6
        #sample kill messages:
        #[game]: kill killer='0:ChillerDragon' victim='1:ChillerDragon.*' weapon=3 special=0
        #[game]: kill killer='0:A' victim='1:ChillerDragon.*' weapon=3 special=0
        #0123456789111111111122222222223333333333
        #          012345678901234567890123456789

        # Could do: use regex by chuck norris
        # https://github.com/chuck-norris-network/teeworlds-econ-js/blob/79e6d668ee64aaaf3a714297a3c726a1867c974f/src/handlers/handle-kill-message.coffee
        """
        regex = re.compile("^\[game\]: kill killer='(?P<killer_id>[0-9]+):(.+?)' victim='([0-9]+)+:(.+?)' weapon=([0-9-]+) special=[0-9]+$")
        m = regex.match("[game]: kill killer='0:ChillerDragon' victim='1:ChillerDragon.*' weapon=3 special=0")
        if m:
            echo(m.group("killer_id"))
        """

        killer_start = data.find(":", 10) + 1
        killer_end = data.find("' victim='", killer_start + 1)
        killer_name = data[killer_start:killer_end]
        killer = player.GetPlayerByName(killer_name)

        victim_start = data.find(":", killer_end) + 1
        victim_end = data.find("' weapon=", victim_start + 1)
        victim_name = data[victim_start:victim_end]
        victim = player.GetPlayerByName(victim_name)

        weapon_start = data.rfind("weapon=") + 7
        weapon_end = data.rfind(" special=")
        weapon = data[weapon_start:weapon_end]
    else: # teeworlds 0.7
        # teeworlds 0.7
        #                     id:team                   id:team
        # [game]: kill killer='0:0:nameless tee' victim='0:0:nameless tee' weapon=-1 special=0
        killer_start = cbase.cfind(data, ":", 3) + 1
        killer_end = data.find("' victim='", killer_start + 1)
        killer_name = data[killer_start:killer_end]

        victim_start = data.find(":", killer_end) + 1
        victim_start = data.find(":", victim_start) + 1
        victim_end = data.find("' weapon=", victim_start + 1)
        victim_name = data[victim_start:victim_end]

        killer_start = data.find("'") + 1
        killer_end = cbase.cfind(data, ":", 2)
        killer_id = data[killer_start:killer_end]
        killer = player.GetPlayerByID(killer_id)

        victim_start = data.find("' victim='") + len("' victim='")
        victim_end = data.find(":", victim_start)
        victim_id = data[victim_start:victim_end]
        victim = player.GetPlayerByID(victim_id)

        weapon_start = data.rfind("weapon=") + 7
        weapon_end = data.rfind(" special=")
        weapon = data[weapon_start:weapon_end]

        # TODO: use regex or wildcard.. anything
        if (data.startswith("[game]: kill killer='-2:1:' victim='") or
            data.startswith("[game]: kill killer='-2:0:' victim='")):
            killer_id = -1
            killer = None

    if not killer == victim and killer: # don't count suicide as kill or when killer left already
        if not player.UpdatePlayerKills(killer, 1, int(weapon)):
            say("error adding kill for '" + str(killer_id) + ":" + killer_name + "'")
            sys.exit(1)
    if not str(weapon) == "-3": #don't count disconnect or teamswitch as death
        if not player.UpdatePlayerDeaths(victim, killer_name, 1):
            say("error adding death for '" + str(victim_id) + ":" + victim_name + "'")
            sys.exit(1)

    # say("[KILL] killer=" + killer_name + " victim=" + victim_name + " weapon=" + str(weapon))
    player.CheckFlaggerKill(victim_name, killer_name)
    player.SetFlagger(victim_name, False)
