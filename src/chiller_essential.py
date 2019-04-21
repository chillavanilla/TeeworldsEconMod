#!/usr/bin/env python3.7
import sys

def EscapeStringKillers(str):
    return str.replace('"', '\\"')

def say(str):
    sys.stdout.write('say "' + EscapeStringKillers(str) + '"\n')
    sys.stdout.flush()

def broadcast(str):
    sys.stdout.write('broadcast "' + EscapeStringKillers(str) + '"\n')
    sys.stdout.flush()

def echo(str):
    sys.stdout.write('echo "' + EscapeStringKillers(str) + '"\n')
    sys.stdout.flush()

def log(s):
    sys.stdout.write("###[log]: " + str(s) + "\n")
    sys.stdout.flush()

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
    1:  "Single",
    2:  "Double",
    3:  "Triple",
    4:  "Quadruple",
    5:  "Quintuple",
    6:  "Sextuple",
    7:  "Septuple",
    8:  "Octuple",
    9:  "Nonuple",
    10: "Decuple",
    11: "Undecuple",
    12: "Duodecuple",
    13: "Tredecuple",
    14: "Quattuordecuple",
    15: "Quindecuple",
    16: "Sexdecuple",
    17: "Septendecuple",
    18: "Octodecuple",
    19: "Novemdecuple",
    20: "Viguple",
    21: "Unviguple",
    22: "Duoviguple",
    23: "Treviguple",
    24: "Quattuorviguple",
    25: "Quinviguple",
    26: "Sexviguple",
    27: "Septenviguple",
    28: "Octoviguple",
    29: "Novemviguple",
    30: "Triguple",
    31: "Untriguple",
    32: "Duotriguple"
}
