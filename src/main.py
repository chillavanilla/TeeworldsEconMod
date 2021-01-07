#!/usr/bin/env python3

import os.path
import sys
import re
import getopt
import time
import g_settings
import parse_settings
import chat
import game
import votes
import player
import flag
import sql_stats
import admin_commands

settings_file = ""

def HandleData(timestamp, data):
    global settings_file
    if (g_settings.get("tw_version") == None):
        # [server]: version 0.6 626fce9a778df4d4
        # [server]: version 0.7 802f1be60a05665f
        # [server]: netversion 0.7 802f1be60a05665f
        if (data.find("[server]: version 0.6 ") != -1):
            g_settings.set("tw_version", "0.6")
        if (data.find("[server]: version 0.7 ") != -1 or data.find("[server]: netversion 0.7 ") != -1):
            g_settings.set("tw_version", "0.7")
    m = re.match(r'\[server\]: game version (.*)', data)
    if m:
        g_settings.set("tw_version", m.group(1))
    if (data.startswith("[register]")):
        # chat.say("register found: " + data) #working but was only useless chat spam for testing
        pass
    elif (data.lower().startswith("[console]")):
        if (data.find("No such command") != -1):
            return
        elif (data.lower().startswith("[console]: !")):
            admin_commands.ExecCommand(data.lower()[12:-1], settings_file)
    # [2020-01-04 15:31:47][server]: '1:zilly dummy' voted kick '0:ChillerDragon' reason='No reason given' cmd='ban 10.52.176.91 5 Banned by vote' force=0
    elif (data.startswith("[server]: '")): # also matches name changes "'foo' -> 'bar'"
        d = data[:-1]
        if (d.endswith("force=1") or d.endswith("force=0")):
            votes.HandleCallVote(d)
    elif (data.startswith("[server]: client dropped. cid=")):
        player.HandlePlayerLeave(data[:-1]) # chop of newline
    elif (data.startswith("[server]: player is ready. ClientID=")):
        player.HandlePlayerReady(data[:-1]) # chop of newline
    # elif (data.startswith("[server]: player has entered the game. ClientID=")):
    #     player.HandlePlayerEnter(data[:-1]) # chop of newline
    elif (data.startswith("[game]: team_join player='")):
        player.HandlePlayerTeam(data[:-1]) # chop of newline
    elif (data.startswith("[chat]") or data.startswith("[teamchat]")):
        if (data.startswith("[chat]: ***")):
            if (data.startswith("[chat]: *** The blue flag was captured by '") or data.startswith("[chat]: *** The red flag was captured by '")):
                flag.HandleFlagCap06(timestamp, data)
            elif (data.find("' changed name to '") != -1):
                player.HandleNameChange(data)
            return
        chat.HandleChatMessage(data)
    elif (data.startswith("[game]")):
        game.HandleGame(timestamp, data)

def MainLoop():
    while True:
        try:
            line = sys.stdin.readline()
            if not line:
                break
            if g_settings.get("tw_version") == None or g_settings.get("tw_version")[0:3] == "0.6":
                HandleData(line[1:9], line[10:]) # cut off the timestamp
            else: # 0.7 has longer timestamps
                HandleData(line[1:20], line[21:]) # cut off the timestamp
        except EOFError:
            # the telnet/netcat process finished; there's no more input
            chat.echo("[WARNING] End of file error.")
            sys.exit(2)
        except UnicodeDecodeError:
            chat.echo("[WARNING] UnicodeDecodeError! Please contact an admin.")
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

