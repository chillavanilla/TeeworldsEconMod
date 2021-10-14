#!/usr/bin/env python3
"""Global user configuration module"""

class Settings:
    """Global user settings"""
    settings_dict = {
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
        "tw_version": ["[0.6,0.7,0.7.5,ddnet]", None],
        "mod_discord": ["str", "<@&573940781082083339>"],
        "votes_discord": ["int", 0],    # 1=chat info 2=ping on discord when vote is called
        "votes_force": ["int", 0],      # force no when a vote is called
        "votes_blocked_reasons": ["[]", None],
        "ipinfo_token": ["str", ""],
        # set to one when start_tem.sh attaches to logfile
        # rather than start a server this ignores some ERRORS
        "hotplug": ["int", 0],
        "chat_command_prefix": ["str", "/"],
        "show_stats_on_join": ["int", 1],
        "show_sprees": ["int", 1]
    }
    def __init__(self, filepath = ""):
        self.filepath = filepath

    def get(self, setting):
        """Get tem setting value by key"""
        return self.settings_dict[setting][1]

    def set(self, setting, value):
        """Set tem setting value and key"""
        self.settings_dict[setting][1] = value
