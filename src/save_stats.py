#!/usr/bin/env python3
from chiller_essential import *
from kills import *
import os.path
from file_stats import *
from sql_stats import *

def SaveStats(name):
    return SaveStatsFile(name)
    '''
    from player import GetPlayerByName
    player = GetPlayerByName(name)
    if not player:
        say("[stats] failed to load player '" + name + "'")
        return False
    SaveStatsSQL(player)
    '''

def LoadStats(name):
    return LoadStatsFile(name)

