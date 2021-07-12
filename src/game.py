#!/usr/bin/env python3
"""Game related methods like scoring"""

from chiller_essential import say, echo
import controllers.players
import kills
import flag
import g_settings

# they are seen as score
CAPS_RED = 0
# it doesnt track how often the blue flag was captured
# but how often the blue team capped the red flag
CAPS_BLUE = 0
GRABS_RED = 0
GRABS_BLUE = 0

def get_best_score():
    """Get best score from team red and blue"""
    return max(get_score_red(), get_score_blue())

def get_score_red():
    """get score from team red"""
    return CAPS_RED * 100 + GRABS_RED

def get_score_blue():
    """get score from team blue"""
    return CAPS_BLUE * 100 + GRABS_BLUE

def update_flag_grabs(is_red):
    """Increase global flag grab counters"""
    global GRABS_RED
    global GRABS_BLUE
    if is_red:
        GRABS_RED += 1
    else:
        GRABS_BLUE += 1

def update_flag_caps(is_red):
    """Increase global flag capture counters"""
    global CAPS_RED
    global CAPS_BLUE
    if is_red:
        CAPS_RED += 1
    else:
        CAPS_BLUE += 1
    if CAPS_RED > 9:
        update_wins(True)
    elif CAPS_BLUE > 9:
        update_wins(False)

def update_wins(is_red):
    """Save win"""
    global CAPS_RED
    global CAPS_BLUE
    CAPS_RED = 0
    CAPS_BLUE = 0
    if is_red:
        echo("red won")
        if controllers.players.count_players() > g_settings.get("win_players"):
            controllers.players.team_won("red")
    else:
        echo("blue won")
        if controllers.players.count_players() > g_settings.get("win_players"):
            controllers.players.team_won("blue")

def handle_game(timestamp, data):
    """Parse game messages"""
    if data.find("kill killer") != -1:
        kills.handle_kills(timestamp, data)
    elif data.startswith("[game]: start round type='"):
        global CAPS_RED
        global CAPS_BLUE
        # [game]: start round type='CTF' teamplay='1'
        say("[SERVER] ChillerDragon wishes you all hf & gl c:")
        controllers.players.refresh_all_players()
        if data.startswith("[game]: start round type='CTF'"):
            if CAPS_RED == 0 and CAPS_BLUE == 0: # already catched by 10 flags auto detection
                return
            if CAPS_RED > CAPS_BLUE:
                update_wins(True)
            elif CAPS_RED < CAPS_BLUE:
                update_wins(False)
            else:
                say("draw lul")
    elif data.startswith("[game]: flag_grab player='"):
        flag.handle_flag_grab(timestamp, data)
    # [2019-10-15 11:41:04][game]: flag_capture player='0:ChillerDragon' team=0
    elif data.startswith("[game]: flag_capture player='"):
        flag.handle_flag_cap(data)
        # # UNUSED CODE FOR NOW
        # # NOT PRECISE ENOUGH
        # # DOES NOTHING CURRENTLY
        # # WOULD SUPPORT 0.7 VERSIONS PRIOR TO THIS COMMIT
        # # https://github.com/teeworlds/teeworlds/commit/5c1d32f65ecaf893d589875df9eaedc1c1a76858
        # # IT IS HIGHLY RECOMMENDED TO USE A LATER TW VERSION TO NOT MESS UP RECORDS
        # id_start = data.find("'", 10) + 1
        # id_end   = cbase.cfind(data, ":", 2)
        # id_str = data[id_start:id_end]
        # p = player.get_player_by_id(id_str)
        # if not p:
        #     say("[ERROR] flag_cap player not found ID=" + str(id_str))
        #     player.debug_player_list()
        #     sys.exit(1)
        # # logs are only seconds precise but usual tw mesurement is two digits more precise
        # t1 = datetime.datetime.strptime(p.grab_timestamp, "%Y-%m-%d %H:%M:%S")
        # t2 = datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        # diff = (t2 - t1).total_seconds()
        # if g_settings.get("debug"):
        #     say("'" + str(p.name) +
        #         "' capped the flag ts=" +
        #         str(timestamp) +
        #         " secs=" + str(diff))
