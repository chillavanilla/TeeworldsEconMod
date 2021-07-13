#!/usr/bin/env python3
import sys
import g_settings
import game
import base.generic
import locked_names
from base.rcon import *
from save_stats import *
from models.player import *
import datetime

def create_player(name, cid=-1, ip_addr="", team="", ShowStats=True, spree=0):
    """Get player object from init_player and append it to the player list"""
    global aPlayers
    player = init_player(name, cid, ip_addr, team, ShowStats, spree)
    if not player:
        say("[ERROR] CreatePlayer init_player=None name='" + str(name) + "' id=" + str(cid))
        sys.exit(1)
    aPlayers.append(player)
    #say("added player '" + name + "'")

def init_player(name, cid, ip_addr, team, show_stats, spree):
    """Create player object"""
    player = None
    load_player = load_stats(name)
    if load_player:
        if show_stats and g_settings.get("show_stats_on_join") == 1:
            load_player.show_stats()
        player = Player(name, cid, ip_addr, load_player.flag_time, load_player.best_spree, team)
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
        player = Player(name, cid=cid, ip_addr=ip_addr, team=team)
    return player

def get_players_array():
    """Return player list"""
    global aPlayers
    return aPlayers

def delete_player(cid):
    """Delete player object from list given a client id"""
    global aPlayers
    #aPlayers.remove(get_player_by_name(name))
    del aPlayers[get_player_index_by_id(cid)]
    #say("deleted player '" + name + "'")

def count_players():
    """Count player list"""
    global aPlayers
    return len(aPlayers)

def save_and_delete_player_by_name(name):
    """Get player object by name and save to db then delete it"""
    player = get_player_by_name(name)
    if not player:
        return False
    save_and_delete_player(player)

def save_and_delete_player(player):
    """Save player object to db and then delete it"""
    if not player:
        return False
    # dirty killingspree update
    # TODO: do an sql query here to support same player online multiple names
    # for 0.7 same name servers and multiple servers running at once
    player.best_spree = max(player.killingspree, player.best_spree)
    delete_player(player.cid) #delete old player without spree update
    aPlayers.append(player) #add new player with spree update
    save_stats(player)
    delete_player(player.cid)
    return True

def refresh_all_players():
    """Save and recreate all player objects"""
    global aPlayers
    for player in aPlayers:
        p = player
        save_and_delete_player(player)
        create_player(p.name, p.cid, ip_addr=p.ip_addr, team=p.team, ShowStats=False, spree=p.killingspree)

def get_player_index_by_name(name):
    """Get player index in list by name"""
    global aPlayers
    index = 0
    for player in aPlayers:
        if player.name == name:
            return index
        index += 1
    return -1

def get_player_index_by_id(cid):
    """Get player index in list by client id"""
    global aPlayers
    index = 0
    for player in aPlayers:
        if player.cid == cid:
            return index
        index += 1
    return -1

def get_player_by_name(name):
    """Get player object by name"""
    global aPlayers
    for player in aPlayers:
        if player.name == name:
            return player
    return None

def get_player_by_id(cid):
    """Get player object by client id"""
    global aPlayers
    for p in aPlayers:
        if p.cid == cid:
            return p
    return None

def debug_player_list():
    """Print player list in chat"""
    global aPlayers
    for p in aPlayers:
        say("  id=" + str(p.cid) + " name='" + str(p.name) + "'")

def print_stats_all(debug=False):
    """Print stats of all players in chat"""
    global aPlayers
    if debug:
        say("Kills/Deaths/Spree Grabs/RedCaps/BlueCaps/CapTime/FlaggerKills")
        for player in aPlayers:
            say(
                "'" + player.name +
                "' k/d/s: " + str(player.kills) +
                "/" + str(player.deaths) +
                "/" + str(player.best_spree) +
                " flag g" + str(player.flag_grabs) +
                "/r" + str(player.flag_caps_red) +
                "/b" + str(player.flag_caps_blue) +
                "/t" + str(player.flag_time) +
                "/k" + str(player.flagger_kills))
            #say("debug is_flagger: " + str(player.is_flagger))
    else:
        say("=== stats for all players ===")
        for player in aPlayers:
            say(
                "'" + player.name +
                "' k/d: " + str(player.kills) +
                "/" + str(player.deaths) +
                " spree: " + str(player.best_spree) +
                " flags: " + str(player.flag_caps_red + player.flag_caps_blue) +
                " fastest cap: " + str(player.flag_time))

# [server]: player is ready. ClientID=0 addr=172.20.10.9:52244
def handle_player_ready(data):
    """Parse the 'player is ready' message"""
    id_start = data.find("=") + 1
    id_end = data.find(" ", id_start)
    id_str = data[id_start:id_end]
    ip_start = data.find("addr=") + 5
    ip_end = data.find(":", ip_start)
    # ddnet ips are encasulated in <{ }>
    if g_settings.get("tw_version") == "ddnet":
        ip_start += 2
    ip_str = data[ip_start:ip_end]
    if g_settings.get("tw_version")[0:3] == "0.6":
        id_str = str(int(id_str, 16)) # 0.6 uses hex for ids in ready messages
    # name is actually "(connecting)" but better use None
    create_player(name=None, cid=id_str, ip_addr=ip_str, ShowStats=True)

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
    """Parse the 'client dropped' message"""
    id_start = data.find("=") + 1
    id_end = data.find(" ", id_start)
    id_str = data[id_start:id_end]
    player = get_player_by_id(id_str)
    if player is None:
        echo("[WARNING] invalid player left id=" + str(id_str))
        echo("   DATA=" + str(data))
    save_and_delete_player(player)

# [game]: team_join player='0:ChillerDragon' team=0
# [game]: team_join player='0:ChillerDragon' team=0->-1
def handle_player_team(data):
    """Parse 'team_join' message"""
    global aPlayers
    id_start = data.find("'") + 1
    id_end = base.generic.cfind(data, ":", 2)
    id_str = data[id_start:id_end]
    player = get_player_by_id(id_str)
    if player is None:
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
    name_start = base.generic.cfind(data, ":", 2) + 1
    name_end = data.rfind("'")
    name = data[name_start:name_end]
    if player.name is None:
        # player just joined and still has to be loaded
        delete_player(player.cid) # delete invalid tmp player
        create_player(name, player.cid, player.ip_addr, player.team)
        locked = locked_names.get_instance()
        if not locked.check(name, player.ip_addr):
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
    """Parse 'changed name to' chat message"""
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
    create_player(new, player.cid, player.ip_addr, team=team)
    locked = locked_names.get_instance()
    if not locked.check(new, player.ip_addr):
        rcon_exec("kick " + str(player.cid) + " please change name")

def set_flagger(player, is_flag, timestamp = ""):
    """Update flagger attribute of player object"""
    if not player:
        if is_flag:
            if g_settings.get("hotplug") == 1:
                return
            say("[ERROR] set flagger failed: invalid player.")
            sys.exit(1)
        return False
    if is_flag and timestamp == "":
        say("[ERROR] set flagger failed: empty timestamp.")
        sys.exit(1)
        return False
    player.is_flagger = is_flag
    player.grab_timestamp = timestamp
    return True

def check_flagger_kill(victim_name, killer_name):
    """Check if a kill is affecting flaggers"""
    global aPlayers
    for victim in aPlayers:
        if victim.name != victim_name:
            continue
        for killer in aPlayers:
            if killer.name != killer_name:
                continue
            if victim.is_flagger is True:
                #say("'" + killer_name + "' killed the flagger '" + victim + "'")
                killer.flagger_kills += 1
    return False

# Update Player Values

def update_achievement(player, ach):
    """Update achievement given achievement string and player object"""
    if not player:
        say("[ERROR] failed achievement: invalid player.")
        sys.exit(1)
        return False
    timestamp = str(datetime.datetime.now().year) + \
        "-" +  str(datetime.datetime.now().month) + \
        "-" + str(datetime.datetime.now().day)
    if ach == "haxx0r":
        if not player.a_haxx0r == "":
            return False
        player.a_haxx0r = a_best(timestamp, player.a_haxx0r)
    elif ach == "blazeit":
        if not player.a_blazeit == "":
            return False
        player.a_blazeit = a_best(timestamp, player.a_blazeit)
    elif ach == "satan":
        if not player.a_satan == "":
            return False
        player.a_satan = a_best(timestamp, player.a_satan)
    elif ach == "virgin":
        if not player.a_virgin == "":
            return False
        player.a_virgin = a_best(timestamp, player.a_virgin)
    else:
        say("[WARNING] unknown achievement '" + str(ach) + "'")
        return False
    return True

def process_multi_kills(player, weapon):
    """Check if a kill is a multikill"""
    now = base.generic.get_timestamp()
    diff = now - player.last_kill
    if diff > 300000000:
        return now
    if player.last_kill == player.last_multi_kill:
        player.current_multi += 1
        if player.current_multi > 32:
            player.current_multi = 2 # after Duotriguple start from double agian
    else:
        player.current_multi = 2
        player.is_combo_multi = False
    if player.last_kill_weapon != weapon:
        player.is_combo_multi = True
    weapon_str = WEAPONS[weapon]
    if player.is_combo_multi:
        weapon_str = "combo"
    say("'" + player.name + "' did a " + weapon_str + " " + MULTIS[player.current_multi] + " kill!")
    player.double_kills[weapon] += 1
    player.last_multi_kill = now
    return now

def update_player_kills(player, kills, weapon):
    """bundle all the logic that happens on a kill"""
    # say("kill weapon=" + WEAPONS[weapon])
    if not player:
        return False
    if weapon < 0: # ddnet has negative weapons disconnect
        return True
    player.last_kill = process_multi_kills(player, weapon)
    player.last_kill_weapon = weapon
    player.kills += kills
    player.weapon_kills[weapon] += kills
    # only activate killingsprees on 8+ players
    if count_players() > g_settings.get("spree_players"):
        player.killingspree += kills
        if player.killingspree % 10 == 0:
            broadcast(
                "'" + player.name +
                "' is on a killing spree with " +
                str(player.killingspree) + " kills "
                )
    return True

def update_player_deaths(player, killer, deaths):
    """bundle all the logic that happens on a death"""
    if not player:
        return False
    player.deaths += deaths
    # only activate killingsprees on 8+ players
    if count_players() > g_settings.get("spree_players"):
        if player.killingspree > 9:
            broadcast(
                "'" + player.name +
                "'s killing spree with " + str(player.killingspree) +
                " kills was ended by '" + killer + "'"
                )
        if player.killingspree > player.best_spree:
            if player.killingspree > 9:
                say(
                    "'" + player.name +
                    "' new killingspree record! Old: " +
                    str(player.best_spree) +
                    " New: "
                    + str(player.killingspree)
                    )
            player.best_spree = player.killingspree
            save_stats_partially(player)
        player.killingspree = 0
    return True

def team_won(team):
    """Update wins and loses for all players"""
    global aPlayers
    if not team == "red" and not team == "blue":
        say("[WARNING] invalid team won " + str(team))
    for player in aPlayers:
        if player.team == team:
            player.wins += 1
        elif not player.team == "" and not player.team == "spectator":
            player.looses += 1

def update_player_flag_grabs(player, grabs):
    """Update flag grab stats"""
    if count_players() <= g_settings.get("flag_players"):
        return False
    if not player:
        return False
    player.flag_grabs += grabs
    game.update_flag_grabs(player.team == "red")
    return True

def update_player_flag_caps(player, color, caps):
    """Update flag cap stats"""
    if not player:
        say("[ERROR] failed player.update_player_flag_caps: invalid player.")
        sys.exit(1)
        return False
    if count_players() <= g_settings.get("flag_players"):
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
    """Update flag time stats"""
    if not player:
        say("[ERROR] failed player.update_player_flag_time: invalid player.")
        sys.exit(1)
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
    except TypeError as error:
        say(
            "[ERROR] error calculating flag time (" +
            str(time) +
            ") and (" +
            str(player.flag_time) + ")"
            )
        say(error)
        sys.exit(1)
