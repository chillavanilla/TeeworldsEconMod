#!/usr/bin/env python3
"""TeeworldsEconMod entry point file"""

import os.path
import sys
import getopt
import parse_settings
import base.settings
from base.rcon import log, echo
import controllers.players
import controllers.chat
import controllers.votes
import controllers.achievements
import controllers.kills
import controllers.flags
import controllers.game
import controllers.admin_commands
import sql_stats
import router

SETTINGS_FILE = ""


def main_loop(_router):
    """The main game loop"""
    while True:
        try:
            line = sys.stdin.readline()
            if not line:
                break
            if base.settings.Settings().get("tw_version") is None or base.settings.Settings().get(
                    "tw_version")[0:3] == "0.6":
                _router.handle_data(line[1:9], line[10:])  # cut off the timestamp
            else:  # 0.7 has longer timestamps
                _router.handle_data(line[1:20], line[21:])  # cut off the timestamp
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
    log(base.settings.Settings().settings_dict)
    sql_stats.init_database()
    players_controller = controllers.players.PlayersController()
    flags_controller = controllers.flags.FlagsController()
    game_controller = controllers.game.GameController()
    chat_controller = controllers.chat.ChatController()
    votes_controller = controllers.votes.VotesController()
    achievements_controller = controllers.achievements.AchievementsController()
    kills_controller = controllers.kills.KillsController()
    admin_commands_controller = controllers.admin_commands.AdminCommandsController()
    flags_controller.init(players_controller, game_controller, achievements_controller)
    game_controller.init(players_controller, flags_controller, kills_controller)
    players_controller.init(game_controller, flags_controller)
    chat_controller.init(players_controller, achievements_controller)
    votes_controller.init(chat_controller)
    kills_controller.init(players_controller)
    admin_commands_controller.init(players_controller)
    achievements_controller.init(players_controller)
    _router = router.Router(SETTINGS_FILE)
    _router.init(
        {
        'players': players_controller,
        'game': game_controller,
        'flags': flags_controller,
        'chat': chat_controller,
        'votes': votes_controller,
        'admin_commands': admin_commands_controller
        }
    )
    main_loop(_router)


if __name__ == "__main__":
    main(sys.argv[1:])
