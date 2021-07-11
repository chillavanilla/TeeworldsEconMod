#!/usr/bin/env python3
import sys
import time
import g_settings
import game
import cbase
import locked_names
from chiller_essential import *
from save_stats import *
from base_player import *
import datetime

def create_player(name, ID=-1, IP="", team="", ShowStats=True, spree=0):
    global aPlayers
    player = init_player(name, ID, IP, team, ShowStats, spree)
    if not init_player:
        say("[ERROR] CreatePlayer init_player=None name='" + str(name) + "' ID=" + str(ID))
        sys.exit(1)
    aPlayers.append(player)
    #say("added player '" + name + "'")

def init_player(name, ID, IP, team, ShowStats, spree):
    player = None
    load_player = load_stats(name)
    if load_player:
        if ShowStats:
            load_player.show_stats()
        player = Player(name, ID, IP, load_player.flag_time, load_player.best_spree, team)
        player.a_haxx0r = load_player.a_haxx0r
        player.a_blazeit = load_player.a_blazeit
        player.a_satan = load_player.a_satan
        player.a_virgin = load_player.a_virgin
        player.killingspree = spree
        player.WEAPON_KILLS[0] = load_player.WEAPON_KILLS[0]
        player.WEAPON_KILLS[1] = load_player.WEAPON_KILLS[1]
        player.WEAPON_KILLS[2] = load_player.WEAPON_KILLS[2]
        player.WEAPON_KILLS[3] = load_player.WEAPON_KILLS[3]
        player.WEAPON_KILLS[4] = load_player.WEAPON_KILLS[4]
        player.WEAPON_KILLS[5] = load_player.WEAPON_KILLS[5]
    else:
        player = Player(name, ID=ID, IP=IP, team=team)
    return player

def GetPlayersArray():
    global aPlayers
    return aPlayers

def delete_player(id):
    global aPlayers
    #aPlayers.remove(get_player_by_name(name))
    del aPlayers[get_player_index_by_id(id)]
    #say("deleted player '" + name + "'")

def count_players():
    global aPlayers
    return len(aPlayers)

def save_and_delete_player_by_name(name):
    player = get_player_by_name(name)
    if not player:
        return False
    save_and_delete_player(player)

def save_and_delete_player(player):
    if not player:
        return False
    # dirty killingspree update
    # TODO: do an sql query here to support same player online multiple names
    # for 0.7 same name servers and multiple servers running at once
    player.best_spree = max(player.killingspree, player.best_spree)
    delete_player(player.ID) #delete old player without spree update
    aPlayers.append(player) #add new player with spree update
    SaveStats(player)
    delete_player(player.ID)

def refresh_all_players():
    global aPlayers
    for player in aPlayers:
        p = player
        save_and_delete_player(player)
        create_player(p.name, p.ID, IP=p.IP, team=p.team, ShowStats=False, spree=p.killingspree)

def get_player_index_by_name(name):
    global aPlayers
    index = 0
    for player in aPlayers:
        if (player.name == name):
            return index
        index += 1
    return -1

def get_player_index_by_id(ID):
    global aPlayers
    index = 0
    for player in aPlayers:
        if (player.ID == ID):
            return index
        index += 1
    return -1

def get_player_by_name(name):
    global aPlayers
    for player in aPlayers:
        if (player.name == name):
            return player
    return None

def get_player_by_id(ID):
    global aPlayers
    for p in aPlayers:
        if (p.ID == ID):
            return p
    return None

def debug_player_list():
    global aPlayers
    for p in aPlayers:
        say("  id=" + str(p.ID) + " name='" + str(p.name) + "'")

def print_stats_all(debug=False):
    global aPlayers
    if (debug):
        say("Kills/Deaths/Spree Grabs/RedCaps/BlueCaps/CapTime/FlaggerKills")
        for player in aPlayers:
            say("'" + player.name + "' k/d/s: " + str(player.kills) + "/" + str(player.deaths) + "/" + str(player.best_spree) + " flag g" + str(player.flag_grabs) + "/r" + str(player.flag_caps_red) + "/b" + str(player.flag_caps_blue) + "/t" + str(player.flag_time) + "/k" + str(player.flagger_kills))
            #say("debug IsFlagger: " + str(player.IsFlagger))
    else:
        say("=== stats for all players ===")
        for player in aPlayers:
            say("'" + player.name + "' k/d: " + str(player.kills) + "/" + str(player.deaths) + " spree: " + str(player.best_spree) + " flags: " + str(player.flag_caps_red + player.flag_caps_blue) + " fastest cap: " + str(player.flag_time))

# [server]: player is ready. ClientID=0 addr=172.20.10.9:52244
def handle_player_ready(data):
    id_start = data.find("=") + 1
    id_end = data.find(" ", id_start)
    id_str = data[id_start:id_end]
    ip_start = data.find("addr=") + 5
    ip_end = data.find(":", ip_start)
    ip_str = data[ip_start:ip_end]
    if g_settings.get("tw_version")[0:3] == "0.6":
        id_str = str(int(id_str, 16)) # 0.6 uses hex for ids in ready messages
    # name is actually "(connecting)" but better use None
    create_player(name=None, ID=id_str, IP=ip_str, ShowStats=True)

# [server]: player has entered the game. ClientID=0 addr=172.20.10.9:54272
# def handle_player_enter(data):
#     id_start = data.find("=") + 1
#     id_end = data.find(" ", id_start)
#     id_str = data[id_start:id_end]
#     if g_settings.get("tw_version")[0:3] == "0.6":
#         id_str = str(int(id_str, 16)) # 0.6 uses hex for ids in enter messages
#     create_player(name=None, ID=id_str, ShowStats=True)

# [server]: client dropped. cid=1 addr=172.20.10.9:53784 reason=''
def handle_player_leave(data):
    id_start = data.find("=") + 1
    id_end = data.find(" ", id_start)
    id_str = data[id_start:id_end]
    player = get_player_by_id(id_str)
    if player == None:
        echo("[WARNING] invalid player left id=" + str(id_str))
        echo("   DATA=" + str(data))
    save_and_delete_player(player)

# [game]: team_join player='0:ChillerDragon' team=0
# [game]: team_join player='0:ChillerDragon' team=0->-1
def handle_player_team(data):
    global aPlayers
    id_start = data.find("'") + 1
    id_end = cbase.cfind(data, ":", 2)
    id_str = data[id_start:id_end]
    player = get_player_by_id(id_str)
    if player == None:
        if g_settings.get("hotplug") == 1:
            return
        say("[ERROR] teamchange failed id=" + str(id_str) + " data=" + str(data))
        debug_player_list()
        sys.exit(1)
    team="invalid"
    data_end = data[-5:]
    change = data_end.rfind(">")
    if change != -1:
        team = data_end[change+1:]
    else:
        team = str(data[data.rfind("=") + 1:])
    if team == "0":
        player.team = "red"
    elif team == "1":
        player.team = "blue"
    elif team == "-1":
        player.team = "spectator"
    else:
        say("[ERROR] invalid team=" + str(team))
        sys.exit(1)
    name_start = cbase.cfind(data, ":", 2) + 1
    name_end = data.rfind("'")
    name = data[name_start:name_end]
    if player.name == None:
        # player just joined and still has to be loaded
        delete_player(player.ID) # delete invalid tmp player
        create_player(name, player.ID, player.IP, player.team)
        locked = locked_names.get_instance()
        if not locked.check(name, player.IP):
            rcon_exec("kick " + str(player.ID) + " please change name")
    elif player.name != name:
        # https://github.com/chillavanilla/TeeworldsEconMod/issues/49
        # it is very rare but possible that one joins without name
        # the during join the placeholder (connecting) is shown in the logs
        # but later the actual name is used
        if player.name == "(connecting)":
            say("[WARNING] untracked namechange from '" + player.name + "' to '" + name + "'")
            player.name = name
        else:
            say("[ERROR] untracked namechange from '" + player.name + "' to '" + name + "'")
            sys.exit(1)

def handle_name_change(data):
    old_start = data.find("'") + 1
    old_end = data.find("' changed name to '")
    old = data[old_start:old_end]
    new_start = old_end + len("' changed name to '")
    new_end = data.rfind("'")
    new = data[new_start:new_end]
    team = ""
    player = get_player_by_name(old)
    if not player:
        if g_settings.get("hotplug") == 1:
            return
        say("[ERROR] name_change player not found name=" + str(old))
        sys.exit(1)
    team = player.team
    save_and_delete_player_by_name(old)
    create_player(new, player.ID, player.IP, team=team)

def set_flagger(player, IsFlag, timestamp = ""):
    if not player:
        if IsFlag:
            if g_settings.get("hotplug") == 1:
                return
            say("[ERROR] set flagger failed: invalid player.")
            sys.exit(1)
        return False
    if IsFlag and timestamp == "":
        say("[ERROR] set flagger failed: empty timestamp.")
        sys.exit(1)
        return False
    player.IsFlagger = IsFlag
    player.grab_timestamp = timestamp
    return True

def check_flagger_kill(victim, killer):
    global aPlayers
    for v in aPlayers:
        if (v.name == victim):
            for k in aPlayers:
                if (k.name == killer):
                    if (v.IsFlagger == True):
                        #say("'" + killer + "' killed the flagger '" + victim + "'")
                        k.flagger_kills += 1
    return False

# Update Player Values

def update_achievement(player, ach):
    if not player:
        say("[ERROR] failed achievement: invalid player.")
        sys.exit(1)
        return False
    ts = str(datetime.datetime.now().year) + "-" +  str(datetime.datetime.now().month) + "-" + str(datetime.datetime.now().day)
    if ach == "haxx0r":
        if not player.a_haxx0r == "":
            return False
        player.a_haxx0r = a_best(ts, player.a_haxx0r)
    elif ach == "blazeit":
        if not player.a_blazeit == "":
            return False
        player.a_blazeit = a_best(ts, player.a_blazeit)
    elif ach == "satan":
        if not player.a_satan == "":
            return False
        player.a_satan = a_best(ts, player.a_satan)
    elif ach == "virgin":
        if not player.a_virgin == "":
            return False
        player.a_virgin = a_best(ts, player.a_virgin)
    else:
        say("[WARNING] unknown achievement '" + str(ach) + "'")
        return False
    return True

def process_multi_kills(p, weapon):
    now = cbase.get_timestamp()
    diff = now - p.LastKill
    if (diff > 300000000):
        return now
    if (p.LastKill == p.LastMultiKill):
        p.CurrentMulti += 1
        if (p.CurrentMulti > 32):
            p.CurrentMulti = 2 # after Duotriguple start from double agian
    else:
        p.CurrentMulti = 2
        p.IsComboMulti = False
    if (p.LastKillWeapon != weapon):
        p.IsComboMulti = True
    weapon_str = WEAPONS[weapon]
    if (p.IsComboMulti):
        weapon_str = "combo"
    say("'" + p.name + "' did a " + weapon_str + " " + MULTIS[p.CurrentMulti] + " kill!")
    p.DOUBLE_KILLS[weapon] += 1
    p.LastMultiKill = now
    return now

def update_player_kills(player, kills, weapon):
    # say("kill weapon=" + WEAPONS[weapon])
    if not player:
        return False
    if weapon < 0: # ddrace has negative weapons disconnect
        return True
    player.LastKill = process_multi_kills(player, weapon)
    player.LastKillWeapon = weapon
    player.kills += kills
    player.WEAPON_KILLS[weapon] += kills
    if count_players() > g_settings.get("spree_players"): # only activate killingsprees on 8+ players
        player.killingspree += kills
        if (player.killingspree % 10 == 0):
            broadcast("'" + player.name + "' is on a killing spree with " + str(player.killingspree) + " kills ")
    return True
    
def update_player_deaths(player, killer, deaths):
    if not player:
        return False
    player.deaths += deaths
    if count_players() > g_settings.get("spree_players"): # only activate killingsprees on 8+ players
        if player.killingspree > 9:
            broadcast("'" + player.name + "'s killing spree with " + str(player.killingspree) + " kills was ended by '" + killer + "'")
        if player.killingspree > player.best_spree:
            if (player.killingspree > 9):
                say("'" + player.name + "' new killingspree record! Old: " + str(player.best_spree) + " New: " + str(player.killingspree))
            player.best_spree = player.killingspree
            save_stats_partially(player)
        player.killingspree = 0
    return True

def team_won(team):
    global aPlayers
    if not team == "red" and not team == "blue":
        say("[WARNING] invalid team won " + str(team))
    for player in aPlayers:
        if player.team == team:
            player.wins += 1
        elif not player.team == "" and not player.team == "spectator":
            player.looses += 1

def update_player_flag_grabs(player, grabs):
    if not count_players() > g_settings.get("flag_players"):
        return False
    if not player:
        return False
    player.flag_grabs += grabs
    game.update_flag_grabs(player.team == "red")
    return True

def update_player_flag_caps(player, color, caps):
    if not player:
        say("[ERROR] failed player.update_player_flag_caps: invalid player.")
        sys.exit(1)
        return False
    if not count_players() > g_settings.get("flag_players"):
        return False
    if (color == "blue"):
        player.flag_caps_blue += caps
    elif (color == "red"):
        player.flag_caps_red += caps
    else:
        say("savage '" + player.name + "' captured the pink flag")
        return False
    return True

def update_player_flag_time(player, time):
    if not player:
        say("[ERROR] failed player.update_player_flag_time: invalid player.")
        sys.exit(1)
        return False
    time = float(time)
    try: # TypeError: unorderable types: float() < str()
        if (time < float(player.flag_time)):
            diff = player.flag_time - time
            diff = float("{0:.2f}".format(diff))
            say("[FastCap] '" + player.name + "' " + str(diff) + " seconds faster")
            player.flag_time = time
        elif (int(player.flag_time) == 0):
            player.flag_time = time
        return True
    except:
        say("[ERROR] error calculating flag time (" + str(time) + ") and (" + str(player.flag_time) + ")")
        sys.exit(1)
    return False
