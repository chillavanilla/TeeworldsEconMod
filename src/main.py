#!/usr/bin/env python3.7

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

def HandleData(data):
    if (data.startswith("[register]")):
        # chat.say("register found: " + data) #working but was only useless chat spam for testing
        pass
    elif (data.startswith("[Console]")):
        if (data.find("No such command") != -1):
            return
        elif (data.startswith("[Console]: !list")):
            chat.echo(str(CountPlayers()) + " players online")
        elif (data.startswith("[Console]: !dev")):
            chat.echo("debug=" + str(g_settings.get("debug")) + " stats=" + g_settings.get("stats_mode"))
    elif (data.endswith("' joined the spectators\n")):
        player.HandlePlayerTeamSwap(data, True)
    elif (data.find("' entered and joined the ") != -1):
        if (data.startswith("[chat]: ***")):
            player.HandlePlayerJoin(data)
    elif (data.find("' joined the ") != -1 and data.endswith(" team\n")):
        if (data.startswith("[chat]: ***")):
            player.HandlePlayerTeamSwap(data)
    elif (data.find("' has left the game") != -1):
        if (data.startswith("[chat]: ***")):
            player.HandlePlayerLeave(data)
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
    try:
        while True:
            line = sys.stdin.readline()
            if not line:
                break
            HandleData(line[10:]) #cut off the timestamp
    except EOFError:
        pass    # the telnet/netcat process finished; there's no more input
    except UnicodeDecodeError:
        chat.say("[WARNING] UnicodeDecodeError! Please contact an admin.")
        pass

def main(argv):
    settings_file = ""
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

