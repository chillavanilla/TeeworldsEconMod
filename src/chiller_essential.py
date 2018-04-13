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

