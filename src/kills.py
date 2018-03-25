#!/usr/bin/env python3
from chiller_essential import *

def HandleKills(data):
    if (data.find("kill killer=")):
        say("KILL!")
