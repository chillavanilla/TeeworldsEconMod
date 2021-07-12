#!/usr/bin/env python3
import sys
import g_settings
import discord_thread

def escape_string_killers(s):
    return s.replace('"', '\\"')

def rcon_exec(s):
    if g_settings.get("debug"):
        say("rcon_exec('" + str(s) + "')")
    sys.stdout.write(s + '\n')
    sys.stdout.flush()

def say(s):
    sys.stdout.write('say "' + escape_string_killers(s) + '"\n')
    sys.stdout.flush()

def broadcast(s):
    sys.stdout.write('broadcast "' + escape_string_killers(s) + '"\n')
    sys.stdout.flush()

def echo(s):
    sys.stdout.write('echo "' + escape_string_killers(s) + '"\n')
    sys.stdout.flush()

def log(s):
    sys.stdout.write("###[log]: " + str(s) + "\n")
    sys.stdout.flush()

def send_discord(message):
    dt = discord_thread.send_discord(message)
    dt.start()

WEAPONS = {
    0: "hammer",
    1: "gun",
    2: "shotgun",
    3: "grenade",
    4: "rifle",
    5: "ninja"
}

# since vanilla has 16 slots max
# supporting Duotriguple kills would mean that
# while one multikill probably the whole server respawned once min
# which means that if this is possible there is probably no multi maximum
# but it would require:
# - close enough spawns
# - enough weapon pickups
# - crazy teamplay to get all players low hp all the time
#
# so i decided duotriguple is cool enough for now...
MULTIS = {
    0:  "NULL",
    1:  "single",
    2:  "double",
    3:  "triple",
    4:  "quadruple",
    5:  "quintuple",
    6:  "sextuple",
    7:  "septuple",
    8:  "octuple",
    9:  "nonuple",
    10: "decuple",
    11: "undecuple",
    12: "duodecuple",
    13: "tredecuple",
    14: "quattuordecuple",
    15: "quindecuple",
    16: "sexdecuple",
    17: "septendecuple",
    18: "octodecuple",
    19: "novemdecuple",
    20: "viguple",
    21: "unviguple",
    22: "duoviguple",
    23: "treviguple",
    24: "quattuorviguple",
    25: "quinviguple",
    26: "sexviguple",
    27: "septenviguple",
    28: "octoviguple",
    29: "novemviguple",
    30: "triguple",
    31: "untriguple",
    32: "duotriguple"
}
