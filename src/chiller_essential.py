#!/usr/bin/env python3
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

WEAPONS = {
    0: "hammer",
    1: "gun",
    2: "shotgun",
    3: "grenade",
    4: "rifle",
    5: "ninja"
}

