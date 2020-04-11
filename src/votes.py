#!/usr/bin/env python3
import re
from chiller_essential import *

def IsBlockedReason(reason):
    words = g_settings.get("votes_blocked_reasons")
    if not words:
        return False
    for word in words:
        if (reason.find(word) != -1):
            return True
    return False

# [2020-01-04 15:31:47][server]: '1:zilly dummy' voted kick '0:ChillerDragon' reason='No reason given' cmd='ban 10.52.176.91 5 Banned by vote' force=0
def HandleCallVote(data):
    # TODO: use regex here to avoid false positives
    if data.find("' voted option '") != -1:
        if g_settings.get("debug"):
            say("[VOTES] skip force on option vote")
        return
    if g_settings.get("votes_force") != 0:
        if g_settings.get("votes_blocked_reasons") == None:
            rcon_exec("vote no")
        else:
            m = re.match(r'.*server\]: \'.+\' voted (spectate|kick) \'.+\' reason=\'(.+)\' cmd=\'.*', data)
            if m:
                reason = m.group(2)
                if IsBlockedReason(reason):
                    rcon_exec("vote no")
                    say("[ANTI-FUNVOTE] please provide a better reason.")
            else:
                say("[WARNING] Vote parsing error. Please contact a admin.")
    if g_settings.get("votes_discord") != 0:
        say("[INFO] Contact the admin on discord (" + str(g_settings.get("admin_discord")) + ") to report players.")
    if g_settings.get("votes_discord") == 2:
        send_discord("vote called " + str(g_settings.get("mod_discord")) + "!\n" + str(data[:data.find(" cmd='ban")]))
