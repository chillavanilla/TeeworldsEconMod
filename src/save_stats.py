#!/usr/bin/env python3
"""Generic stats wrapper deligating to sql and file based stats"""

from file_stats import save_stats_file, load_stats_file, save_stats_partially_file
from sql_stats import save_stats_sql, load_stats_sql, save_stats_partially_sql
import g_settings


def save_stats(player):
    """save by player object to support duplicated names"""
    if g_settings.get("stats_mode") == "sql":
        return save_stats_sql(player)
    return save_stats_file(player)

def load_stats(name):
    """load stats by name"""
    if g_settings.get("stats_mode") == "sql":
        return load_stats_sql(name)
    return load_stats_file(name)

def save_stats_partially(player):
    """
    save specific stats before game end if needed
    for now it is only killingspree record
    see https://github.com/chillavanilla/TeeworldsEconMod/issues/28
    for details
    """
    if g_settings.get("stats_mode") == "sql":
        return save_stats_partially_sql(player)
    return save_stats_partially_file(player)
