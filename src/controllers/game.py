#!/usr/bin/env python3
"""Game related methods like scoring"""

from base.rcon import say, echo
import g_settings

# they are seen as score
CAPS_RED = 0
# it doesnt track how often the blue flag was captured
# but how often the blue team capped the red flag
CAPS_BLUE = 0
GRABS_RED = 0
GRABS_BLUE = 0

class GameController:
    """Game related logic"""
    def __init__(self):
        self.players_controller = None
        self.flags_controller = None
        self.kills_conrtoller = None

    def init(self, players_controller, flags_controller, kills_controller):
        """Init controllers"""
        self.players_controller = players_controller
        self.flags_controller = flags_controller
        self.kills_controller = kills_controller

    def get_best_score(self):
        """Get best score from team red and blue"""
        return max(self.get_score_red(), self.get_score_blue())

    def get_score_red(self):
        """get score from team red"""
        return CAPS_RED * 100 + GRABS_RED

    def get_score_blue():
        """get score from team blue"""
        return CAPS_BLUE * 100 + GRABS_BLUE

    def update_flag_grabs(self, is_red):
        """Increase global flag grab counters"""
        global GRABS_RED
        global GRABS_BLUE
        if is_red:
            GRABS_RED += 1
        else:
            GRABS_BLUE += 1

    def update_flag_caps(self, is_red):
        """Increase global flag capture counters"""
        global CAPS_RED
        global CAPS_BLUE
        if is_red:
            CAPS_RED += 1
        else:
            CAPS_BLUE += 1
        if CAPS_RED > 9:
            self.update_wins(True)
        elif CAPS_BLUE > 9:
            self.update_wins(False)

    def update_wins(self, is_red):
        """Save win"""
        global CAPS_RED
        global CAPS_BLUE
        CAPS_RED = 0
        CAPS_BLUE = 0
        if is_red:
            echo("red won")
            if self.players_controller.count_players() > g_settings.get("win_players"):
                self.players_controller.team_won("red")
        else:
            echo("blue won")
            if self.players_controller.count_players() > g_settings.get("win_players"):
                self.players_controller.team_won("blue")

    def handle_game(self, timestamp, data):
        """Parse game messages"""
        if data.find("kill killer") != -1:
            self.kills_controller.handle_kills(timestamp, data)
        elif data.startswith("[game]: start round type='"):
            global CAPS_RED
            global CAPS_BLUE
            # [game]: start round type='CTF' teamplay='1'
            say("[SERVER] ChillerDragon wishes you all hf & gl c:")
            self.players_controller.refresh_all_players()
            if data.startswith("[game]: start round type='CTF'"):
                if CAPS_RED == 0 and CAPS_BLUE == 0: # already catched by 10 flags auto detection
                    return
                if CAPS_RED > CAPS_BLUE:
                    self.update_wins(True)
                elif CAPS_RED < CAPS_BLUE:
                    self.update_wins(False)
                else:
                    say("draw lul")
        elif data.startswith("[game]: flag_grab player='"):
            self.flags_controller.handle_flag_grab(timestamp, data)
        # [2019-10-15 11:41:04][game]: flag_capture player='0:ChillerDragon' team=0
        elif data.startswith("[game]: flag_capture player='"):
            self.flags_controller.handle_flag_cap(data)
            # # UNUSED CODE FOR NOW
            # # NOT PRECISE ENOUGH
            # # DOES NOTHING CURRENTLY
            # # WOULD SUPPORT 0.7 VERSIONS PRIOR TO THIS COMMIT
            # # https://github.com/teeworlds/teeworlds/commit/5c1d32f65ecaf893d589875df9eaedc1c1a76858
            # # IT IS HIGHLY RECOMMENDED TO USE A LATER TW VERSION TO NOT MESS UP RECORDS
            # id_start = data.find("'", 10) + 1
            # id_end   = base.generic.cfind(data, ":", 2)
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

    WEAPONS = {
        0: "hammer",
        1: "gun",
        2: "shotgun",
        3: "grenade",
        4: "rifle",
        5: "ninja"
    }

    # since vanilla has 16 slots max
    # supporting Duotriguple kills would mean that
    # while one multikill probably the whole server respawned once min
    # which means that if this is possible there is probably no multi maximum
    # but it would require:
    # - close enough spawns
    # - enough weapon pickups
    # - crazy teamplay to get all players low hp all the time
    #
    # so i decided duotriguple is cool enough for now...
    MULTIS = {
        0:  "NULL",
        1:  "single",
        2:  "double",
        3:  "triple",
        4:  "quadruple",
        5:  "quintuple",
        6:  "sextuple",
        7:  "septuple",
        8:  "octuple",
        9:  "nonuple",
        10: "decuple",
        11: "undecuple",
        12: "duodecuple",
        13: "tredecuple",
        14: "quattuordecuple",
        15: "quindecuple",
        16: "sexdecuple",
        17: "septendecuple",
        18: "octodecuple",
        19: "novemdecuple",
        20: "viguple",
        21: "unviguple",
        22: "duoviguple",
        23: "treviguple",
        24: "quattuorviguple",
        25: "quinviguple",
        26: "sexviguple",
        27: "septenviguple",
        28: "octoviguple",
        29: "novemviguple",
        30: "triguple",
        31: "untriguple",
        32: "duotriguple"
    }
