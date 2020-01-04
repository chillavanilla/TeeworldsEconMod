#!/usr/bin/env python3

SETTINGS = {
    "debug": ["bool", False],
    "stats_mode": ["[file,sql]", "file"],
    "flag_players": ["int", 7],      # more than x players needed to count flag caps and grabs
    "win_players": ["int", 1],       # more than x players needed to count team wins
    "spree_players": ["int", 7],     # more than x players needed to count killingsprees
    "admin_discord": ["str", "ChillerDragon#0643"],
    "sql_database": ["str", "stats.db"],
    "file_database": ["str", "stats/"],
    "discord_token": ["str", None],
    "discord_filter": ["[]", None],
    "tw_version": ["int", None],
    "mod_discord": ["str", "<@&573940781082083339>"],
    "votes_discord": ["int", 0],    # 1=chat info 2=ping on discord when vote is called
    "votes_force": ["int", 0]       # force no when a vote is called
}

def get(setting):
    return SETTINGS[setting][1]

def set(setting, value):
    SETTINGS[setting][1] = value
