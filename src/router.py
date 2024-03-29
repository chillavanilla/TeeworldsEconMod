#!/usr/bin/env python3
"""Yes I do ruby"""

import re
import base.settings

class Router:
    """Such RoR much WowW"""
    def __init__(self, settings_file: str):
        self.settings = base.settings.Settings(settings_file)
        self.players_controller = None
        self.game_controller = None
        self.flags_controller = None
        self.chat_controller = None
        self.votes_controller = None
        self.admin_commands_controller = None

    def init(self, controllers: dict):
        """Init controllers"""
        self.players_controller = controllers['players']
        self.game_controller = controllers['game']
        self.flags_controller = controllers['flags']
        self.chat_controller = controllers['chat']
        self.votes_controller = controllers['votes']
        self.admin_commands_controller = controllers['admin_commands']

    def handle_data(self, timestamp: str, data: str):
        """Pass log line on to the resposible parsers"""
        if self.settings.get("tw_version") is None:
            # [server]: version 0.6 626fce9a778df4d4
            # [server]: version 0.7 802f1be60a05665f
            # [server]: netversion 0.7 802f1be60a05665f
            if data.find("[server]: version 0.6 ") != -1:
                self.settings.set("tw_version", "0.6")
            if data.find("[server]: version 0.7 ") != - \
                    1 or data.find("[server]: netversion 0.7 ") != -1:
                self.settings.set("tw_version", "0.7")
        match = re.match(r'\[server\]: game version (.*)', data)
        if match:
            version = match.group(1)
            if version.find("0.7/0.6") != -1:
                version = "ddnet"
            self.settings.set("tw_version", version)
        if data.startswith("[register]"):
            # working but was only useless chat spam for testing
            # chat.say("register found: " + data)
            pass
        elif data.lower().startswith("[console]"):
            if data.find("No such command") != -1:
                return
            if data.lower().startswith("[console]: !"):
                self.admin_commands_controller.exec_command(
                    data.lower()[12:-1],
                    self.settings.filepath)
        # [server]: '1:zilly dummy' voted kick '0:ChillerDragon'
        # reason='No reason given' cmd='ban 10.52.176.91 5 Banned by vote' force=0
        # also matches name changes "'foo' -> 'bar'"
        elif data.startswith("[server]: '"):
            data_chomp = data[:-1]
            if data_chomp.endswith("force=1") or data_chomp.endswith("force=0"):
                self.votes_controller.handle_call_vote(data_chomp)
        elif data.startswith("[server]: client dropped. cid="):
            self.players_controller.handle_player_leave(data[:-1])  # chop of newline
        elif data.startswith("[server]: player is ready. ClientID="):
            self.players_controller.handle_player_ready(data[:-1])  # chop of newline
        elif data.startswith("[dummy]: Dummy connected: "):
            self.players_controller.handle_dummy_ready(data[:-1])  # chop of newline
        # elif data.startswith("[server]: player has entered the game. ClientID="):
        #     player.handle_player_enter(data[:-1]) # chop of newline
        elif data.startswith("[game]: team_join player='"):
            self.players_controller.handle_player_team(data[:-1])  # chop of newline
        elif data.startswith("[chat]") or data.startswith("[teamchat]"):
            if data.startswith("[chat]: ***"):
                if (data.startswith("[chat]: *** The blue flag was captured by '")
                        or data.startswith("[chat]: *** The red flag was captured by '")):
                    self.flags_controller.handle_flag_cap_06(data)
                elif data.find("' changed name to '") != -1:
                    self.players_controller.handle_name_change(data)
                return
            self.chat_controller.handle_chat_message(data)
        elif data.startswith("[game]"):
            self.game_controller.handle_game(timestamp, data)
