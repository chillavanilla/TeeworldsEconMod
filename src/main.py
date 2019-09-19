#!/usr/bin/env python3

import os.path
import sys
import getopt
import time
import g_settings
import parse_settings
import chat
import game
import player
import flag
import sql_stats

settings_file = ""
tw_version=None

def DebugListPlayers():
    for p in player.GetPlayersArray():
        chat.echo("id=" + str(p.ID) + " name='" + str(p.name) + "' team=" + str(p.team))

def HandleData(data):
    global settings_file
    global tw_version
    if (tw_version == None):
        # [server]: version 0.6 626fce9a778df4d4
        # [server]: version 0.7 802f1be60a05665f
        if (data.find("[server]: version 0.6 ") != -1):
            tw_version = 6
        if (data.find("[server]: version 0.7 ") != -1):
            tw_version = 7
    if (data.startswith("[register]")):
        # chat.say("register found: " + data) #working but was only useless chat spam for testing
        pass
    elif (data.startswith("[Console]")):
        if (data.find("No such command") != -1):
            return
        elif (data.startswith("[Console]: !cmdlist")) or (data.startswith("[Console]: !help")) or (data.startswith("[Console]: !info")):
            chat.echo("Commands: !help, !list, !dev, !reload_settings")
        elif (data.startswith("[Console]: !reload_settings")):
            try:
                parse_settings.ReadSettingsFile(settings_file)
                chat.echo("[==== SETTINGS ====]")
                for key, value in g_settings.SETTINGS.items():
                    chat.echo("[tem:setting] " + str(key) + " : " + str(value[1]))
            except parse_settings.TemParseError as x:
                chat.echo(str(x))
        elif (data.startswith("[Console]: !list")):
            DebugListPlayers()
            chat.echo(str(player.CountPlayers()) + " players online")
        elif (data.startswith("[Console]: !dev")):
            chat.echo("debug=" + str(g_settings.get("debug")) + " stats=" + g_settings.get("stats_mode"))
    elif (data.startswith("[server]: client dropped. cid=")):
        player.HandlePlayerLeave(data[:-1]) # chop of newline
    elif (data.startswith("[server]: player has entered the game. ClientID=")):
        player.HandlePlayerEnter(data[:-1]) # chop of newline
    elif (data.startswith("[game]: team_join player='")):
        player.HandlePlayerTeam(data[:-1]) # chop of newline
    elif (data.startswith("[chat]") or data.startswith("[teamchat]")):
        if (data.startswith("[chat]: ***")):
            if (data.startswith("[chat]: *** The blue flag was captured by '") or data.startswith("[chat]: *** The red flag was captured by '")):
                flag.HandleFlagCap(data)
            elif (data.find("' changed name to '") != -1):
                player.HandleNameChange(data)
            return
        chat.HandleChatMessage(data)
    elif (data.startswith("[game]")):
        game.HandleGame(data)

def MainLoop():
    while True:
        try:
            line = sys.stdin.readline()
            if not line:
                break
            if tw_version == None or tw_version == 6:
                HandleData(line[10:]) # cut off the timestamp
            else: # 0.7 has longer timestamps
                HandleData(line[21:]) # cut off the timestamp
        except EOFError:
            # the telnet/netcat process finished; there's no more input
            chat.echo("[WARNING] End of file error.")
            sys.exit(2)
        except UnicodeDecodeError:
            chat.say("[WARNING] UnicodeDecodeError! Please contact an admin.")
            pass

def main(argv):
    global settings_file
    try:
        opts, args = getopt.getopt(argv,"hs:",["settings="])
    except getopt.GetoptError:
        print("main.py -s <settings file>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
             print("main.py settings=/path/to/tem.settings")
             sys.exit()
        elif opt in ("-s", "--settings"):
            settings_file = arg

    if settings_file == "":
        print("Missing argument settings file.")
        sys.exit(2)

    if not os.path.isfile(settings_file):
        print("[ERROR] settings file path invalid '" + str(settings_file) + "'")
        sys.exit(2)
    parse_settings.ReadSettingsFile(settings_file)

    chat.log("[TEM] loaded settings: ")
    chat.log(g_settings.SETTINGS)
    sql_stats.InitDataBase()
    MainLoop()

if __name__ == "__main__":
    main(sys.argv[1:])

