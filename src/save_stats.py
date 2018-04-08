#!/usr/bin/env python3
from file_stats import *
from sql_stats import *
import global_settings

def SaveStats(name):
    if global_settings.StatsMode == "sql":
        return SaveStatsSQL(name)
    return SaveStatsFile(name)

def LoadStats(name):
    if global_settings.StatsMode == "sql":
        return LoadStatsSQL(name)
    return LoadStatsFile(name)

