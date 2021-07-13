#!/usr/bin/env python3
"""Essential wrappers around the teeworlds api"""

import sys
import g_settings
import discord.thread

def escape_string_killers(msg):
    """Helper method to fix string escape in teeworlds commands"""
    return msg.replace('"', '\\"')

def rcon_exec(cmd):
    """Execute given rcon command"""
    if g_settings.get("debug"):
        say("rcon_exec('" + str(cmd) + "')")
    sys.stdout.write(cmd + '\n')
    sys.stdout.flush()

def say(msg):
    """Print given message"""
    sys.stdout.write('say "' + escape_string_killers(msg) + '"\n')
    sys.stdout.flush()

def broadcast(msg):
    """Broadcast given message"""
    sys.stdout.write('broadcast "' + escape_string_killers(msg) + '"\n')
    sys.stdout.flush()

def echo(msg):
    """Echo given message"""
    sys.stdout.write('echo "' + escape_string_killers(msg) + '"\n')
    sys.stdout.flush()

def log(msg):
    """Print given message to logfiles only"""
    sys.stdout.write("###[log]: " + str(msg) + "\n")
    sys.stdout.flush()

def send_discord(message):
    """Send a discord message in newly spawned thread"""
    thread = discord.thread.SendDiscord(message)
    thread.start()

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
