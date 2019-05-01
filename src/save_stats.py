#!/usr/bin/env python3
from file_stats import *
from sql_stats import *
import g_settings

def SaveStats(name):
    if g_settings.get("stats_mode") == "sql":
        return SaveStatsSQL(name)
    return SaveStatsFile(name)

def LoadStats(name):
    if g_settings.get("stats_mode") == "sql":
        return LoadStatsSQL(name)
    return LoadStatsFile(name)

