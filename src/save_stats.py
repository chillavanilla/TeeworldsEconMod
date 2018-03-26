#!/usr/bin/env python3
from chiller_essential import *
from player import *
from kills import *


def SaveStats(name):
    sf = open("stats/" + name + ".acc", "w")
    sf.write("hello wurld\n")


def LoadStats(name):
    pass
