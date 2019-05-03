#!/usr/bin/env python3.7

SETTINGS = {
    "debug": ["bool", False],
    "stats_mode": ["[file,sql]", "file"],
    "flag_players": ["int", 7],      # more than x players needed to count flag caps and grabs
    "win_players": ["int", 1],       # more than x players needed to count team wins
    "spree_players": ["int", 7],     # more than x players needed to count killingsprees
    "admin_discord": ["str", "ChillerDragon#0643"],
    "sql_database": ["str", "stats.db"],
    "file_database": ["str", "stats/"],
    "discord_token": ["str", None]
}

def get(setting):
    return SETTINGS[setting][1]
