#!/usr/bin/env python3
from chiller_essential import *

# [2020-01-04 15:31:47][server]: '1:zilly dummy' voted kick '0:ChillerDragon' reason='No reason given' cmd='ban 10.52.176.91 5 Banned by vote' force=0
def HandleCallVote(data):
    # TODO: use regex here to avoid false positives
    if data.find("' voted option '") != -1:
        if g_settings.get("debug"):
            say("[VOTES] skip force on option vote")
        return
    if g_settings.get("votes_force") != 0:
        rcon_exec("vote no")
    if g_settings.get("votes_discord") != 0:
        say("[INFO] Contact the admin on discord (" + str(g_settings.get("admin_discord")) + ") to report players.")
    if g_settings.get("votes_discord") == 2:
        send_discord("vote called " + str(g_settings.get("mod_discord")) + "!\n" + str(data))
