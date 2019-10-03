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

# save specific stats before game end if needed
# for now it is only killingspree record
# see https://github.com/chillavanilla/TeeworldsEconMod/issues/28
# for details
def SaveStatsPartially(player):
    if g_settings.get("stats_mode") == "sql":
        return SaveStatsPartiallySQL(player)
    return SaveStatsPartiallyFile(player)