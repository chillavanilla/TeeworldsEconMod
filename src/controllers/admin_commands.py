#!/usr/bin/env python3
"""Admin commands"""

from base.rcon import echo
import g_settings
import parse_settings
import locked_names

class AdminCommandsController:
    """Admin commands controller"""
    def __init__(self):
        self.players_controller = None

    def init(self, players_controller):
        """Init controllers"""
        self.players_controller = players_controller

    def debug_list_players(self):
        """Print list of players in admin console"""
        for _player in self.players_controller.get_players_array():
            echo("id=" + str(_player.cid) +
                    " addr=" + str(_player.ip_addr) +
                    " name='" + str(_player.name) +
                    "' team=" + str(_player.team))


    def exec_command(self, command, settings_file):
        """Execute admin command"""
        if command in ("cmdlist", "help", "info"):
            echo("Commands: !help, !list, !dev, !reload_settings !locked_names")
        elif command == "reload_settings":
            try:
                parse_settings.read_settings_file(settings_file)
                echo("[==== SETTINGS ====]")
                for key, value in g_settings.SETTINGS.items():
                    sett_val = value[1]
                    if str(key) == "discord_token":
                        if sett_val and len(sett_val) > 6:
                            sett_val = sett_val[:5] + "..."
                    echo("[tem:setting] " + str(key) + " : " + str(sett_val))
            except parse_settings.TemParseError as err:
                echo(str(err))
            locked_names.get_instance(force=True)
        elif command == "list":
            debug_list_players()
            echo(str(self.players_controller.count_players()) + " players online")
        elif command == "dev":
            echo("debug=" + str(g_settings.get("debug")) +
                    " stats=" + g_settings.get("stats_mode"))
        elif command == "locked_names":
            locked_names.get_instance().list_names()
