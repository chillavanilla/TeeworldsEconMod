#!/usr/bin/env python3
"""Admin commands"""

from chiller_essential import echo
import g_settings
import controllers.players
import parse_settings
import locked_names


def debug_list_players():
    """Print list of players in admin console"""
    for _player in controllers.players.get_players_array():
        echo("id=" + str(_player.cid) +
                  " addr=" + str(_player.ip_addr) +
                  " name='" + str(_player.name) +
                  "' team=" + str(_player.team))


def exec_command(command, settings_file):
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
        locked_names.get_instance(Force=True)
    elif command == "list":
        debug_list_players()
        echo(str(controllers.players.count_players()) + " players online")
    elif command == "dev":
        echo("debug=" + str(g_settings.get("debug")) +
                  " stats=" + g_settings.get("stats_mode"))
    elif command == "locked_names":
        locked_names.get_instance().list_names()
