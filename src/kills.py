#!/usr/bin/env python3
import re
from chiller_essential import *
import cbase
import g_settings
import controllers.players

def handle_kills(timestamp, data):
    killer_name = ""
    victim_name = ""
    killer_id = -1
    victim_id = -1
    killer = None
    victim = None
    weapon = ""

    if g_settings.get("tw_version")[0:3] == "0.6" or g_settings.get("tw_version") == None: # default 6
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
    else: # teeworlds 0.7 or ddnet

        data = data[:-1]
        if g_settings.get("tw_version") == "ddnet":
            # [game]: kill killer='5:ChillerDragon' victim='5:ChillerDragon' weapon=-3 special=0 killer_team:0 victim_team:0
            # [game]: kill killer='6:ChillerDragon.*' victim='5:ChillerDragon' weapon=-2 special=0 killer_team:0 victim_team:0
            m = re.match(r"^\[game\]: kill killer='(?P<k_id>-?\d{1,2}):(?P<k_name>.*)' victim='(?P<v_id>-?\d{1,2}):(?P<v_name>.+?)' weapon=(?P<weapon>-?\d) special=(\d) killer_team:(?P<k_team>-?\d{1,2}) victim_team:(?P<v_team>-?\d{1,2})$", data)
        else:
            # teeworlds 0.7
            #                     id:team                   id:team
            # [game]: kill killer='0:0:nameless tee' victim='0:0:nameless tee' weapon=-1 special=0
            # [game]: kill killer='-2:1:' victim='0:0:ChillerDragon' weapon=3 special=0
            #                                                                                       use .* for killer but .+? for victim because killer can be empty if it left the server before the projectile hit
            m = re.match(r"^\[game\]: kill killer='(?P<k_id>-?\d{1,2}):(?P<k_team>-?\d{1,2}):(?P<k_name>.*)' victim='(?P<v_id>-?\d{1,2}):(?P<v_team>-?\d{1,2}):(?P<v_name>.+?)' weapon=(?P<weapon>-?\d) special=(\d)$", data)

        if m:
            if g_settings.get("debug"):
                say("KILLER ID=<%s> TEAM=<%s> NAME=<%s> VICTIM ID=<%s> TEAM=<%s> NAME=<%s> weapon=<%s>" % (
                        m.group("k_id"), m.group("k_team"), m.group("k_name"),
                        m.group("v_id"), m.group("v_team"), m.group("v_name"),
                        m.group("weapon")
                    )
                )
            if m.group("k_name") == "" or int(m.group("k_id")) < 0:
                killer_name = "a left player"
                killer_id = m.group("k_id")
                killer = None
            else:
                killer_name = m.group("k_name")
                killer_id = m.group("k_id")
                killer = controllers.players.get_player_by_id(killer_id)

            victim_name = m.group("v_name")
            victim_id = m.group("v_id")
            victim = controllers.players.get_player_by_id(victim_id)

            weapon = m.group("weapon")
        else:
            say("[ERROR] failed parsing kill msg: " + str(data))
            sys.exit(1)

    if not killer == victim and killer: # don't count suicide as kill or when killer left already
        if not controllers.players.update_player_kills(killer, 1, int(weapon)):
            if g_settings.get("hotplug") == 1:
                return
            say("[ERROR] failed adding kill:")
            say("   ID=" + str(killer_id))
            say("   NAME=" + str(killer_name))
            say("   OBJ=" + str(killer))
            say("   DATA=" + data)
            sys.exit(1)
    if not str(weapon) == "-3": # don't count disconnect or teamswitch as death
        if not controllers.players.update_player_deaths(victim, killer_name, 1):
            if g_settings.get("hotplug") == 1:
                return
            say("[ERROR] failed adding death:")
            say("   ID=" + str(victim_id))
            say("   NAME=" + str(victim_name))
            say("   OBJ=" + str(victim))
            say("   DATA=" + data)
            sys.exit(1)

    # say("[KILL] killer=" + killer_name + " victim=" + victim_name + " weapon=" + str(weapon))
    controllers.players.check_flagger_kill(victim_name, killer_name)
    controllers.players.set_flagger(victim, False, timestamp)
