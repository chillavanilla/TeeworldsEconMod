#!/usr/bin/env python3

SETTINGS = {
    "debug": ["bool", False],
    "stats_mode": ["[file,sql]", "file"],
    "flag_players": ["int", 7],      # more than x players needed to count flag caps and grabs
    "win_players": ["int", 1],       # more than x players needed to count team wins
    "spree_players": ["int", 7],     # more than x players needed to count killingsprees
    "admin_contact": ["str", ""],
    "sql_database": ["str", "stats.db"],
    "file_database": ["str", "stats/"],
    "discord_token": ["str", None],
    "chat_filter": ["[]", None],
    "filter_discord": ["int", 0],    # 0=off 1=send message to discord when chat_filter matches
    "tw_version": ["[0.6,0.7,0.7.5]", None],
    "mod_discord": ["str", "<@&573940781082083339>"],
    "votes_discord": ["int", 0],    # 1=chat info 2=ping on discord when vote is called
    "votes_force": ["int", 0],      # force no when a vote is called
    "votes_blocked_reasons": ["[]", None],
    "ipinfo_token": [ "str", ""]
}

def get(setting):
    return SETTINGS[setting][1]

def set(setting, value):
    SETTINGS[setting][1] = value
