#!/usr/bin/env python3
"""Chat message related module"""

import sys
import datetime
import re
from base.rcon import say, send_discord
import base.settings
import base.generic
import sql_stats
import version

class ChatController:
    """Handles chat messages"""
    def __init__(self):
        self.settings = base.settings.Settings()
        self.players_controller = None
        self.achievements_controller = None
        self.CHAT_NONE=0
        self.CHAT_ALL=1
        self.CHAT_TEAM=2
        self.CHAT_WHISPER=3

    def init(self, players_controller, achievements_controller):
        """Init controllers"""
        self.players_controller = players_controller
        self.achievements_controller = achievements_controller

    def is_ban_reason_in_str(self, string):
        """Search banned keywords in given string"""
        words = self.settings.get("chat_filter")
        if not words:
            return False
        for word in words:
            if string.find(word) != -1:
                return True
        return False

    # get by id if no argument given
    # get by name if name is argument
    # return player object and identifier (id/name)
    def get_rank_player(self, msg, rank_cmd):
        """Parse command and return player object"""
        if self.settings.get("stats_mode") != "sql":
            say("not supported in file stats mode")
            return None, None
        msg_normal = msg
        msg = msg.lower()
        id_str = self.get_chat_id(msg_normal)
        rankname_start = -1
        if msg.find(rank_cmd + " ") != -1:
            cmd_end = msg.rfind(rank_cmd)
            rankname_start = msg.find(rank_cmd + " ", cmd_end) + len(rank_cmd + " ")
        rankname_end = len(msg) - 1 # cut off newline
        rankname = msg_normal[rankname_start:rankname_end]
        if not rankname or rankname == "" or rankname_start == -1:
            return self.players_controller.get_player_by_id(id_str), id_str
        argplayer = self.players_controller.get_player_by_name(rankname)
        if not argplayer:
            # try to find id prefix in argument name
            pattern = r'(\d{1,2}):(.*)'
            if self.settings.get("tw_version") == "ddnet":
                # F-DDrace 128 slots
                pattern = r'(\d{1,3}):(.*)'
            match = re.match(pattern, rankname)
            if match:
                r_id = match.group(1)
                r_name = match.group(2)
                r_player = self.players_controller.get_player_by_id(r_id)
                if r_player and r_player.name == r_name:
                    argplayer = r_player
        return argplayer, rankname

    def get_rank_name(self, msg, rank_cmd):
        """Parse message and return playername"""
        if self.settings.get("stats_mode") != "sql":
            say("not supported in file stats mode")
            return None
        msg_normal = msg
        msg = msg.lower()
        name_start = base.generic.cfind(msg, ":", 3) + 1
        name_end = msg.find(rank_cmd, name_start)
        name_end = msg.rfind(": ", name_end)
        name = msg_normal[name_start:name_end]
        rankname_start = -1
        if msg.find(rank_cmd + " ") != -1:
            rankname_start = msg.find(rank_cmd + " ", name_end) + len(rank_cmd + " ")
        rankname_end = len(msg) - 1 # cut off newline
        rankname = msg_normal[rankname_start:rankname_end]
        if not rankname or rankname == "" or rankname_start == -1:
            return name
        return rankname

    def get_chat_id(self, msg):
        """Get clientID of the sender"""
        # TODO: move constants to better place
        # TODO: refactor this code
        # TODO: support versions higher than 0.7.5 (care "0.7.10" < "0.7.5" is true in python)
        # in 0.7.5 id position was swapped
        # https://github.com/teeworlds/teeworlds/commit/5090c39d94bad0b6dda8caaef271133c46c00ee0#diff-a2df712cfb938eda9a173f36c865c2cc
        id_str = None # python scoping ?!
        if self.settings.get("tw_version") == "0.7.5":
            mode_start = msg.find(" ") + 1
            mode_end = base.generic.cfind(msg, ":", 2)
            mode_str = msg[mode_start:mode_end]
            msg = msg[mode_end:-1]
            if int(mode_str) == self.CHAT_TEAM:
                id_start = base.generic.cfind(msg, ":", 2) + 1
                id_end = base.generic.cfind(msg, ":", 3)
                id_str = msg[id_start:id_end]
            else:
                id_start = msg.find(":") + 1
                id_end = base.generic.cfind(msg, ":", 2)
                id_str = msg[id_start:id_end]
        else:
            id_start = msg.find(" ") + 1
            id_end = base.generic.cfind(msg, ":", 2)
            id_str = msg[id_start:id_end]
        return id_str

    def get_spam_player(self, msg):
        """Recive the player name of a message"""
        id_str = self.get_chat_id(msg)
        return self.players_controller.get_player_by_id(id_str)

    def spam_protection(self, msg):
        """Takes a message and mutes the author if it is spam"""
        player = self.get_spam_player(msg)
        if not player:
            if self.settings.get("hotplug") == 1:
                return False
            say("[ERROR] spam_protection() failed! please contact an admin")
            sys.exit(1)
        now = datetime.datetime.now()
        diff = now - player.last_chat
        player.last_chat = now
        #say("chat diff seconds: " + str(diff.seconds) + " last_chat: " + str(player.last_chat))
        seconds = diff.seconds
        if seconds < 15:
            player.mute_score += 1
        if player.mute_score > 5:
            if not player.is_muted:
                player.is_muted = True
                say("'" + str(player.name) + "' is banned from the command system (spam)")
        if seconds > 120:
            player.is_muted = False
            player.mute_score = 0
        if player.is_muted:
            return True
        return False

    def is_muted(self, msg):
        """Take a message and return of the message author is muted or not"""
        player = self.get_spam_player(msg)
        if not player:
            if self.settings.get("hotplug") == 1:
                return False
            say("[WARNING] is_muted() failed! please contact an admin")
            return False
        if player.is_muted:
            return True
        return False

    def handle_chat_message(self, msg):
        """
            Main method of this module
            takes a message and parses it for chat commands
        """
        if self.is_muted(msg):
            return
        prefix = self.settings.get("chat_command_prefix")
        is_cmd = True
        msg_normal = msg
        msg = msg.lower()
        # the first possible occurence of a chat command (to filter chat command names)
        chat_cmd_start = base.generic.cfind(msg, ":", 4)
        cmd = msg[chat_cmd_start:-1] # cut newline at end
        if cmd.endswith(": " + prefix + "help") or \
            cmd.endswith(": " + prefix + "info") or \
            cmd.endswith(": " + prefix + "cmdlist"):
            say("==== Teeworlds Econ Mod (TEM) ====")
            say("developed by ChillerDragon version: " + str(version.VERSION))
            say("https://github.com/ChillaVanilla/TeeworldsEconMod")
            say("'" + prefix + "help' to show this help")
            say("'" + prefix + "stats' to show round stats")
            say("'" + prefix + "achievements' to show achievements")
            if self.settings.get("stats_mode") == "sql":
                say("'" + prefix + "top5' for all time stats commands")
                say("'" + prefix + "rank' for all rank commands")
        elif cmd.endswith(": " + prefix + "top5"):
            if self.settings.get("stats_mode") == "sql":
                say("'" + prefix + "top_kills' to see top5 killers of all time")
            if self.settings.get("stats_mode") == "sql":
                say("'" + prefix + "top_flags' to see top5 flag cap times of all time")
            if self.settings.get("stats_mode") == "sql":
                say("'" + prefix + "top_caps' to see top5 flag amount of all time")
            if self.settings.get("stats_mode") == "sql":
                say("'" + prefix + "top_sprees' to see top5 killing sprees of all time")
            else:
                say("not supported in file stats mode")
        #elif cmd.endswith(": " + prefix + "stats_all"):
            #player.print_stats_all(True)
        elif cmd.find(": " + prefix + "stats") != -1:
            if self.settings.get("stats_mode") != "sql":
                say("not supported in file stats mode")
                return
            player, name = self.get_rank_player(msg_normal, ": " + prefix + "stats")
            if not player:
                say("[stats] player '" + str(name) + "' is not online.")
                return
            player.show_stats_round()
            #player.print_stats_all()
        elif cmd.endswith(": " + prefix + "top_caps"):
            if self.settings.get("stats_mode") == "sql":
                sql_stats.best_flag_caps()
            else:
                say("not supported in file stats mode")
        elif cmd.endswith(": " + prefix + "top_flags"):
            if self.settings.get("stats_mode") == "sql":
                sql_stats.best_times()
            else:
                say("not supported in file stats mode")
        elif cmd.endswith(": " + prefix + "top_kills"):
            if self.settings.get("stats_mode") == "sql":
                sql_stats.best_killers()
            else:
                say("not supported in file stats mode")
        elif cmd.endswith(": " + prefix + "top_sprees"):
            if self.settings.get("stats_mode") == "sql":
                sql_stats.best_spree()
            else:
                say("not supported in file stats mode")
        elif cmd.find("" + prefix + "rank_kills") != - 1:
            sql_stats.rank_kills(self.get_rank_name(msg_normal, ": " + prefix + "rank_kills"))
        elif msg.find("" + prefix + "rank_flags") != - 1:
            sql_stats.rank_flag_time(self.get_rank_name(msg_normal, ": " + prefix + "rank_flags"))
        elif msg.find("" + prefix + "rank_caps") != - 1:
            sql_stats.rank_flag_caps(self.get_rank_name(msg_normal, ": " + prefix + "rank_caps"))
        elif cmd.find("" + prefix + "rank_sprees") != - 1:
            sql_stats.rank_spree(self.get_rank_name(msg_normal, ": " + prefix + "rank_sprees"))
        elif cmd.find("" + prefix + "rank_all") != - 1:
            name = self.get_rank_name(msg_normal, ": " + prefix + "rank_all")
            if not name:
                return
            say("=== '" + str(name) + "'s stats ===")
            sql_stats.rank_kills(str(name))
            sql_stats.rank_flag_time(str(name))
            sql_stats.rank_flag_caps(str(name))
            sql_stats.rank_spree(str(name))
        elif cmd.find("" + prefix + "rank") != - 1:
            if self.settings.get("stats_mode") != "sql":
                say("not supported in file stats mode")
                return
            say("'" + prefix + "rank_kills' to show global kills rank")
            say("'" + prefix + "rank_sprees' to show global spree rank")
            say("'" + prefix + "rank_flags' to show global flag time rank")
            say("'" + prefix + "rank_caps' to show global flag capture rank")
        elif cmd.find("" + prefix + "achievements") != - 1:
            name = self.get_rank_name(msg_normal, ": " + prefix + "achievements")
            self.achievements_controller.show_achievements(name)
        elif cmd.endswith(": " + prefix + "test"):
            player, name = self.get_rank_player(msg_normal, ": " + prefix + "test")
            if not player:
                if self.settings.get("hotplug") == 1:
                    return
                say("error")
                sys.exit(1)
            say("got player: " + str(name))
            # say("current spree: " + str(p.killingspree))
        # handle this like a chat command (so it has spam prot)
        elif self.is_ban_reason_in_str(cmd):
            self.admin_contact_msg()
            # players containing : will be cutted in discord message but this is fine for now
            name = self.get_rank_name(msg_normal, ": ")
            if self.settings.get("filter_discord") == 1:
                send_discord(
                    "chat trigger " + \
                    str(self.settings.get("mod_discord")) + \
                    "!\n" + str(msg)
                )
        else:
            is_cmd = False
        if is_cmd:
            self.spam_protection(msg_normal)

    def admin_contact_msg(self):
        """Display the admin contact message in chat"""
        if str(self.settings.get("admin_contact")) == "":
            return
        say(
            "[INFO] Contact the admin " + \
            str(self.settings.get("admin_contact")) + \
            " to report players."
        )
