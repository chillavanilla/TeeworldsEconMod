#!/usr/bin/env python3
from chiller_essential import *

def HandleKills(data):
    from player import UpdatePlayerKills, UpdatePlayerDeaths
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
        print(m.group("killer_id"))
    """

    killer_start = data.find(":", 10) + 1
    killer_end = data.find("' victim='", killer_start + 1)
    killer_name = data[killer_start:killer_end]

    victim_start = data.find(":", killer_end) + 1
    victim_end = data.find("' weapon=", victim_start + 1)
    victim_name = data[victim_start:victim_end]

    if killer_name == victim_name: #ignore selfkills also because it would be annoying on disconnect
        return
    if not UpdatePlayerKills(killer_name, 1):
        say("error adding kill for '" + killer_name + "'")
    if not UpdatePlayerDeaths(victim_name, 1):
        say("error adding death for '" + victim_name + "'")
    #say("[KILL] killer=" + killer_name + " victim=" + victim_name)

