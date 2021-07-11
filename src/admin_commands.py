#!/usr/bin/env python3

import chat
import g_settings
import player
import parse_settings
import locked_names

def debug_list_players():
    for p in player.GetPlayersArray():
        chat.echo("id=" + str(p.ID) + " addr=" + str(p.IP) + " name='" + str(p.name) + "' team=" + str(p.team))

def exec_command(command, settings_file):
    if ((command == "cmdlist") or (command == "help") or (command == "info")):
        chat.echo("Commands: !help, !list, !dev, !reload_settings !locked_names")
    elif (command == "reload_settings"):
        try:
            parse_settings.read_settings_file(settings_file)
            chat.echo("[==== SETTINGS ====]")
            for key, value in g_settings.SETTINGS.items():
                sett_val = value[1]
                if str(key) == "discord_token":
                    if sett_val and len(sett_val) > 6:
                        sett_val = sett_val[:5] + "..."
                chat.echo("[tem:setting] " + str(key) + " : " + str(sett_val))
        except parse_settings.TemParseError as x:
            chat.echo(str(x))
        locked_names.get_instance(Force = True)
    elif (command == "list"):
        debug_list_players()
        chat.echo(str(player.count_players()) + " players online")
    elif (command == "dev"):
        chat.echo("debug=" + str(g_settings.get("debug")) + " stats=" + g_settings.get("stats_mode"))
    elif (command == "locked_names"):
        locked_names.get_instance().list_names()
