#!/usr/bin/env python3
"""TeeworldsEconMod entry point file"""

import os.path
import sys
import re
import getopt
import g_settings
import parse_settings
import chat
from chiller_essential import log, echo
import game
import votes
import controllers.players
import flag
import sql_stats
import admin_commands

SETTINGS_FILE = ""


def handle_data(timestamp, data):
    global SETTINGS_FILE
    if g_settings.get("tw_version") is None:
        # [server]: version 0.6 626fce9a778df4d4
        # [server]: version 0.7 802f1be60a05665f
        # [server]: netversion 0.7 802f1be60a05665f
        if data.find("[server]: version 0.6 ") != -1:
            g_settings.set("tw_version", "0.6")
        if data.find("[server]: version 0.7 ") != - \
                1 or data.find("[server]: netversion 0.7 ") != -1:
            g_settings.set("tw_version", "0.7")
    m = re.match(r'\[server\]: game version (.*)', data)
    if m:
        version = m.group(1)
        if version.find("0.7/0.6") != -1:
            version = "0.7.5"
        g_settings.set("tw_version", version)
    if data.startswith("[register]"):
        # working but was only useless chat spam for testing
        # chat.say("register found: " + data)
        pass
    elif data.lower().startswith("[console]"):
        if data.find("No such command") != -1:
            return
        if data.lower().startswith("[console]: !"):
            admin_commands.exec_command(data.lower()[12:-1], SETTINGS_FILE)
    # [server]: '1:zilly dummy' voted kick '0:ChillerDragon' reason='No reason given' cmd='ban 10.52.176.91 5 Banned by vote' force=0
    # also matches name changes "'foo' -> 'bar'"
    elif data.startswith("[server]: '"):
        data_chomp = data[:-1]
        if data_chomp.endswith("force=1") or data_chomp.endswith("force=0"):
            votes.handle_call_vote(data_chomp)
    elif data.startswith("[server]: client dropped. cid="):
        controllers.players.handle_player_leave(data[:-1])  # chop of newline
    elif data.startswith("[server]: player is ready. ClientID="):
        controllers.players.handle_player_ready(data[:-1])  # chop of newline
    # elif data.startswith("[server]: player has entered the game. ClientID="):
    #     player.handle_player_enter(data[:-1]) # chop of newline
    elif data.startswith("[game]: team_join player='"):
        controllers.players.handle_player_team(data[:-1])  # chop of newline
    elif data.startswith("[chat]") or data.startswith("[teamchat]"):
        if data.startswith("[chat]: ***"):
            if (data.startswith("[chat]: *** The blue flag was captured by '")
                    or data.startswith("[chat]: *** The red flag was captured by '")):
                flag.HandleFlagCap06(timestamp, data)
            elif data.find("' changed name to '") != -1:
                controllers.players.handle_name_change(data)
            return
        chat.handle_chat_message(data)
    elif data.startswith("[game]"):
        game.handle_game(timestamp, data)


def main_loop():
    """The main game loop"""
    while True:
        try:
            line = sys.stdin.readline()
            if not line:
                break
            if g_settings.get("tw_version") is None or g_settings.get(
                    "tw_version")[0:3] == "0.6":
                handle_data(line[1:9], line[10:])  # cut off the timestamp
            else:  # 0.7 has longer timestamps
                handle_data(line[1:20], line[21:])  # cut off the timestamp
        except EOFError:
            # the telnet/netcat process finished; there's no more input
            echo("[WARNING] End of file error.")
            sys.exit(2)
        except UnicodeDecodeError:
            echo("[WARNING] UnicodeDecodeError! Please contact an admin.")


def main(argv):
    """Entry point method"""
    global SETTINGS_FILE
    try:
        opts, args = getopt.getopt(argv, "hs:", ["settings="])
    except getopt.GetoptError:
        print("main.py -s <settings file>")
        sys.exit(2)
    for arg in args:
        if arg == "help":
            print("main.py settings=/path/to/tem.settings")
            sys.exit()
    for opt, arg in opts:
        if opt == "-h":
            print("main.py settings=/path/to/tem.settings")
            sys.exit()
        elif opt in ("-s", "--settings"):
            SETTINGS_FILE = arg

    if SETTINGS_FILE == "":
        print("Missing argument settings file.")
        sys.exit(2)

    if not os.path.isfile(SETTINGS_FILE):
        print(
            "[ERROR] settings file path invalid '" +
            str(SETTINGS_FILE) +
            "'")
        sys.exit(2)
    parse_settings.read_settings_file(SETTINGS_FILE)

    log("[TEM] loaded settings: ")
    log(g_settings.SETTINGS)
    sql_stats.init_database()
    main_loop()


if __name__ == "__main__":
    main(sys.argv[1:])
