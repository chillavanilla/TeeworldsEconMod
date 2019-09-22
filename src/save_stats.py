#!/usr/bin/env python3
from file_stats import *
from sql_stats import *
import g_settings

# save by player object to support duplicated names
def SaveStats(player):
    if g_settings.get("stats_mode") == "sql":
        return SaveStatsSQL(player)
    return SaveStatsFile(player)

# load by name
def LoadStats(name):
    if g_settings.get("stats_mode") == "sql":
        return LoadStatsSQL(name)
    return LoadStatsFile(name)

