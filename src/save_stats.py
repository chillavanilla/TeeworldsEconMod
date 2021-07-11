#!/usr/bin/env python3
from file_stats import *
from sql_stats import *
import g_settings

# save by player object to support duplicated names
def SaveStats(player):
    if g_settings.get("stats_mode") == "sql":
        return save_stats_sql(player)
    return SaveStatsFile(player)

# load by name
def load_stats(name):
    if g_settings.get("stats_mode") == "sql":
        return load_stats_sql(name)
    return load_stats_file(name)

# save specific stats before game end if needed
# for now it is only killingspree record
# see https://github.com/chillavanilla/TeeworldsEconMod/issues/28
# for details
def save_stats_partially(player):
    if g_settings.get("stats_mode") == "sql":
        return save_stats_partially_sql(player)
    return save_stats_partially_file(player)