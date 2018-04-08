#!/usr/bin/env python3
from chiller_essential import *
from kills import *
import os.path
from file_stats import *
from sql_stats import *

def SaveStats(name):
    return SaveStatsSQL(name)
    return SaveStatsFile(name)

def LoadStats(name):
    return LoadStatsSQL(name)
    return LoadStatsFile(name)

