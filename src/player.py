#!/usr/bin/env python3
import sys
import g_settings
import game
import cbase
import locked_names
from chiller_essential import *
from save_stats import *
from base_player import *
import datetime

def create_player(name, cid=-1, ip="", team="", ShowStats=True, spree=0):
    global aPlayers
    player = init_player(name, cid, ip, team, ShowStats, spree)
    if not init_player:
        say("[ERROR] CreatePlayer init_player=None name='" + str(name) + "' id=" + str(cid))
        sys.exit(1)
    aPlayers.append(player)
    #say("added player '" + name + "'")

def init_player(name, cid, ip, team, ShowStats, spree):
    player = None
    load_player = load_stats(name)
    if load_player:
        if ShowStats:
            load_player.show_stats()
        player = Player(name, cid, ip, load_player.flag_time, load_player.best_spree, team)
        player.a_haxx0r = load_player.a_haxx0r
        player.a_blazeit = load_player.a_blazeit
        player.a_satan = load_player.a_satan
        player.a_virgin = load_player.a_virgin
        player.killingspree = spree
        player.weapon_kills[0] = load_player.weapon_kills[0]
        player.weapon_kills[1] = load_player.weapon_kills[1]
        player.weapon_kills[2] = load_player.weapon_kills[2]
        player.weapon_kills[3] = load_player.weapon_kills[3]
        player.weapon_kills[4] = load_player.weapon_kills[4]
        player.weapon_kills[5] = load_player.weapon_kills[5]
    else:
        player = Player(name, cid=cid, ip=ip, team=team)
    return player

def GetPlayersArray():
    global aPlayers
    return aPlayers

def delete_player(cid):
    global aPlayers
    #aPlayers.remove(get_player_by_name(name))
    del aPlayers[get_player_index_by_id(cid)]
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
    delete_player(player.cid) #delete old player without spree update
    aPlayers.append(player) #add new player with spree update
    SaveStats(player)
    delete_player(player.cid)

def refresh_all_players():
    global aPlayers
    for player in aPlayers:
        p = player
        save_and_delete_player(player)
        create_player(p.name, p.cid, ip=p.ip, team=p.team, ShowStats=False, spree=p.killingspree)

def get_player_index_by_name(name):
    global aPlayers
    index = 0
    for player in aPlayers:
        if (player.name == name):
            return index
        index += 1
    return -1

def get_player_index_by_id(cid):
    global aPlayers
    index = 0
    for player in aPlayers:
        if (player.cid == cid):
            return index
        index += 1
    return -1

def get_player_by_name(name):
    global aPlayers
    for player in aPlayers:
        if (player.name == name):
            return player
    return None

def get_player_by_id(cid):
    global aPlayers
    for p in aPlayers:
        if (p.cid == cid):
            return p
    return None

def debug_player_list():
    global aPlayers
    for p in aPlayers:
        say("  id=" + str(p.cid) + " name='" + str(p.name) + "'")

def print_stats_all(debug=False):
    global aPlayers
    if (debug):
        say("Kills/Deaths/Spree Grabs/RedCaps/BlueCaps/CapTime/FlaggerKills")
        for player in aPlayers:
            say("'" + player.name + "' k/d/s: " + str(player.kills) + "/" + str(player.deaths) + "/" + str(player.best_spree) + " flag g" + str(player.flag_grabs) + "/r" + str(player.flag_caps_red) + "/b" + str(player.flag_caps_blue) + "/t" + str(player.flag_time) + "/k" + str(player.flagger_kills))
            #say("debug is_flagger: " + str(player.is_flagger))
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
    create_player(name=None, cid=id_str, ip=ip_str, ShowStats=True)

# [server]: player has entered the game. ClientID=0 addr=172.20.10.9:54272
# def handle_player_enter(data):
#     id_start = data.find("=") + 1
#     id_end = data.find(" ", id_start)
#     id_str = data[id_start:id_end]
#     if g_settings.get("tw_version")[0:3] == "0.6":
#         id_str = str(int(id_str, 16)) # 0.6 uses hex for ids in enter messages
#     create_player(name=None, id=id_str, ShowStats=True)

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
        delete_player(player.cid) # delete invalid tmp player
        create_player(name, player.cid, player.ip, player.team)
        locked = locked_names.get_instance()
        if not locked.check(name, player.ip):
            rcon_exec("kick " + str(player.cid) + " please change name")
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
    create_player(new, player.cid, player.ip, team=team)

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
    player.is_flagger = IsFlag
    player.grab_timestamp = timestamp
    return True

def check_flagger_kill(victim, killer):
    global aPlayers
    for v in aPlayers:
        if (v.name == victim):
            for k in aPlayers:
                if (k.name == killer):
                    if (v.is_flagger == True):
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
    diff = now - p.last_kill
    if diff > 300000000:
        return now
    if p.last_kill == p.last_multi_kill:
        p.current_multi += 1
        if p.current_multi > 32:
            p.current_multi = 2 # after Duotriguple start from double agian
    else:
        p.current_multi = 2
        p.is_combo_multi = False
    if p.last_kill_weapon != weapon:
        p.is_combo_multi = True
    weapon_str = WEAPONS[weapon]
    if p.is_combo_multi:
        weapon_str = "combo"
    say("'" + p.name + "' did a " + weapon_str + " " + MULTIS[p.current_multi] + " kill!")
    p.double_kills[weapon] += 1
    p.last_multi_kill = now
    return now

def update_player_kills(player, kills, weapon):
    # say("kill weapon=" + WEAPONS[weapon])
    if not player:
        return False
    if weapon < 0: # ddrace has negative weapons disconnect
        return True
    player.last_kill = process_multi_kills(player, weapon)
    player.last_kill_weapon = weapon
    player.kills += kills
    player.weapon_kills[weapon] += kills
    # only activate killingsprees on 8+ players
    if count_players() > g_settings.get("spree_players"):
        player.killingspree += kills
        if (player.killingspree % 10 == 0):
            broadcast("'" + player.name + "' is on a killing spree with " + str(player.killingspree) + " kills ")
    return True
    
def update_player_deaths(player, killer, deaths):
    if not player:
        return False
    player.deaths += deaths
    # only activate killingsprees on 8+ players
    if count_players() > g_settings.get("spree_players"):
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
    if color == "blue":
        player.flag_caps_blue += caps
    elif color == "red":
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
        if time < float(player.flag_time):
            diff = player.flag_time - time
            diff = float("{0:.2f}".format(diff))
            say("[FastCap] '" + player.name + "' " + str(diff) + " seconds faster")
            player.flag_time = time
        elif int(player.flag_time) == 0:
            player.flag_time = time
        return True
    except:
        say("[ERROR] error calculating flag time (" + str(time) + ") and (" + str(player.flag_time) + ")")
        sys.exit(1)
    return False
