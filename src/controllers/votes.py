#!/usr/bin/env python3
"""vote module"""

import re
from base.rcon import say, rcon_exec, send_discord
import base.settings

class VotesController:
    """vote logic"""
    def __init__(self):
        self.settings = base.settings.Settings()
        self.chat_controller = None

    def init(self, chat_controller):
        """Init controllers"""
        self.chat_controller = chat_controller

    def is_blocked_reason(self, reason):
        """Check if given vote reason is in the blacklist"""
        reason.lower()
        words = self.settings.get("votes_blocked_reasons")
        if not words:
            return False
        for word in words:
            if reason.find(word.lower()) != -1:
                return True
        return False

    # [server]: '1:zilly dummy' voted kick
    # '0:ChillerDragon' reason='No reason given' cmd='ban 10.52.176.91 5 Banned by vote' force=0
    def handle_call_vote(self, data):
        """Recive vote log line and parse it"""
        # TODO: use regex here to avoid false positives
        if data.find("' voted option '") != -1:
            if self.settings.get("debug"):
                say("[VOTES] skip force on option vote")
            return
        if self.settings.get("votes_force") != 0:
            if self.settings.get("votes_blocked_reasons") is None:
                rcon_exec("vote no")
            else:
                match = re.match(
                    r'.*server\]: \'.+\' voted (spectate|kick) \'.+\' '
                    r'reason=\'(.+)\' cmd=\'.*', data)
                if match:
                    reason = match.group(2)
                    if self.is_blocked_reason(reason):
                        rcon_exec("vote no")
                        say("[ANTI-FUNVOTE] please provide a better reason.")
                else:
                    say("[WARNING] Vote parsing error. Please contact a admin.")
        if self.settings.get("votes_discord") != 0:
            self.chat_controller.admin_contact_msg()
        if self.settings.get("votes_discord") == 2:
            send_discord("vote called " + str(self.settings.get("mod_discord"))
                + "!\n" + str(data[:data.find(" cmd='ban")]))
