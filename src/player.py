#!/usr/bin/env python3
import sys
import time
import g_settings
import game
import cbase
from chiller_essential import *
from save_stats import *
from base_player import *
import datetime

def CreatePlayer(name, ID=-1, team="", ShowStats=True, spree=0):
    global aPlayers
    load_player = LoadStats(name)
    if load_player:
        if ShowStats:
            load_player.ShowStats()
        add_player = Player(name, ID, load_player.flag_time, load_player.best_spree, team)
        add_player.a_haxx0r = load_player.a_haxx0r
        add_player.a_blazeit = load_player.a_blazeit
        add_player.a_satan = load_player.a_satan
        add_player.a_virgin = load_player.a_virgin
        add_player.killingspree = spree
        add_player.WEAPON_KILLS[0] = load_player.WEAPON_KILLS[0]
        add_player.WEAPON_KILLS[1] = load_player.WEAPON_KILLS[1]
        add_player.WEAPON_KILLS[2] = load_player.WEAPON_KILLS[2]
        add_player.WEAPON_KILLS[3] = load_player.WEAPON_KILLS[3]
        add_player.WEAPON_KILLS[4] = load_player.WEAPON_KILLS[4]
        add_player.WEAPON_KILLS[5] = load_player.WEAPON_KILLS[5]
        aPlayers.append(add_player)
    else:
        aPlayers.append(Player(name, ID=ID, team=team))
    #say("added player '" + name + "'")

def GetPlayersArray():
    global aPlayers
    return aPlayers

def DeletePlayer(name):
    global aPlayers
    #aPlayers.remove(GetPlayerByName(name))
    del aPlayers[GetPlayerIndex(name)]
    #say("deleted player '" + name + "'")

def CountPlayers():
    global aPlayers
    return len(aPlayers)

def SaveAndDeletePlayer(name):
    player = GetPlayerByName(name)
    if not player:
        return False
    #dirty killingspree update
    player.best_spree = max(player.killingspree, player.best_spree)
    DeletePlayer(name) #delete old player without spree update
    aPlayers.append(player) #add new player with spree update
    SaveStats(name)
    DeletePlayer(name)

def RefreshAllPlayers():
    global aPlayers
    for player in aPlayers:
        p = player
        SaveAndDeletePlayer(player.name)
        CreatePlayer(p.name, p.ID, p.team, ShowStats=False, spree=p.killingspree)

def GetPlayerIndex(name):
    global aPlayers
    index = 0
    for player in aPlayers:
        if (player.name == name):
            return index
        index += 1
    return -1

def GetPlayerByName(name):
    global aPlayers
    for player in aPlayers:
        if (player.name == name):
            return player
    return None

def GetPlayerByID(id):
    global aPlayers
    for p in aPlayers:
        if (p.ID == id):
            return p
    return None

def PrintStatsAll(debug=False):
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

# [server]: player has entered the game. ClientID=0 addr=172.20.10.9:54272
def HandlePlayerEnter(data):
    id_start = data.find("=") + 1
    id_end = data.find(" ", id_start)
    id = data[id_start:id_end]
    CreatePlayer(name=None, ID=id)

# [server]: client dropped. cid=1 addr=172.20.10.9:53784 reason=''
def HandlePlayerLeave(data):
    id_start = data.find("=") + 1
    id_end = data.find(" ", id_start)
    id = data[id_start:id_end]
    player = GetPlayerByID(id)
    if player == None:
        say("[ERROR] invalid player left id=" + str(id))
        sys.exit(1)
    SaveAndDeletePlayer(player.name)

# [game]: team_join player='0:ChillerDragon' team=0
def HandlePlayerTeam(data):
    id_start = data.find("'") + 1
    id_end = cbase.cfind(data, ":", 2)
    id = data[id_start:id_end]
    player = GetPlayerByID(id)
    if player == None:
        say("[ERROR] teamchange failed id=" + str(id) + " data=" + str(data))
        sys.exit(1)
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
        player.name = name
    elif player.name != name:
        say("[ERROR] untracked namechange from '" + player.name + "' to '" + name + "'")
        sys.exit(1)

def HandleNameChange(data):
    old_start = data.find("'") + 1
    old_end = data.find("' changed name to '")
    old = data[old_start:old_end]
    new_start = old_end + len("' changed name to '")
    new_end = data.rfind("'")
    new = data[new_start:new_end]
    team = ""
    player = GetPlayerByName(old)
    if not player:
        say("[ERROR] name_change player not found name=" + str(old))
        sys.exit(1)
    team = player.team
    SaveAndDeletePlayer(old)
    CreatePlayer(new, player.ID, team=team)

def SetFlagger(name, IsFlag):
    global aPlayers
    for player in aPlayers:
        if (player.name == name):
            player.IsFlagger = IsFlag
            return True
    return False

def CheckFlaggerKill(victim, killer):
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

def UpdateAchievement(name, ach):
    ts = str(datetime.datetime.now().year) + "-" +  str(datetime.datetime.now().month) + "-" + str(datetime.datetime.now().day)
    global aPlayers
    for player in aPlayers:
        if (player.name == name):
            if ach == "haxx0r":
                if not player.a_haxx0r == "":
                    return False
                player.a_haxx0r = A_Best(ts, player.a_haxx0r)
            elif ach == "blazeit":
                if not player.a_blazeit == "":
                    return False
                player.a_blazeit = A_Best(ts, player.a_blazeit)
            elif ach == "satan":
                if not player.a_satan == "":
                    return False
                player.a_satan = A_Best(ts, player.a_satan)
            elif ach == "virgin":
                if not player.a_virgin == "":
                    return False
                player.a_virgin = A_Best(ts, player.a_virgin)
            else:
                say("[WARNING] unknown achievement '" + str(ach) + "'")
                return
            return True
    return False

def ProcessMultiKills(p, weapon):
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

def UpdatePlayerKills(name, kills, weapon):
    # say("kill weapon=" + WEAPONS[weapon])
    global aPlayers
    for player in aPlayers:
        if (player.name == name):
            player.LastKill = ProcessMultiKills(player, weapon)
            player.LastKillWeapon = weapon
            player.kills += kills
            player.WEAPON_KILLS[weapon] += kills
            if CountPlayers() > g_settings.get("spree_players"): # only activate killingsprees on 8+ players
                player.killingspree += kills
                if (player.killingspree % 10 == 0):
                    broadcast("'" + player.name + "' is on a killing spree with " + str(player.killingspree) + " kills ")
            return True
    return False
    
def UpdatePlayerDeaths(name, killer, deaths):
    global aPlayers
    for player in aPlayers:
        if (player.name == name):
            player.deaths += deaths
            if CountPlayers() > g_settings.get("spree_players"): # only activate killingsprees on 8+ players
                if player.killingspree > 9:
                    broadcast("'" + player.name + "'s killing spree with " + str(player.killingspree) + " kills was ended by '" + killer + "'")
                if player.killingspree > player.best_spree:
                    if (player.killingspree > 9):
                        say("'" + player.name + "' new killingspree record! Old: " + str(player.best_spree) + " New: " + str(player.killingspree))
                    player.best_spree = player.killingspree
                player.killingspree = 0
            return True
    return False

def TeamWon(team):
    global aPlayers
    if not team == "red" and not team == "blue":
        say("[WARNING] invalid team won " + str(team))
    for player in aPlayers:
        if player.team == team:
            player.wins += 1
        elif not player.team == "" and not player.team == "spectator":
            player.looses += 1

def UpdatePlayerFlagGrabs(name, grabs):
    if not CountPlayers() > g_settings.get("flag_players"):
        return
    global aPlayers
    for player in aPlayers:
        if (player.name == name):
            player.flag_grabs += grabs
            game.UpdateFlagGrabs(player.team == "red")
            return True
    return False

def UpdatePlayerFlagCaps(name, color, caps):
    if not CountPlayers() > g_settings.get("flag_players"):
        return
    global aPlayers
    for player in aPlayers:
        if (player.name == name):
            if (color == "blue"):
                player.flag_caps_blue += caps
            elif (color == "red"):
                player.flag_caps_red += caps
            else:
                say("savage '" + name + "' captured the pink flag")
            return True
    return False

def UpdatePlayerFlagTime(name, time):
    global aPlayers
    time = float(time)
    for player in aPlayers:
        if (player.name == name):
            try: # TypeError: unorderable types: float() < str()
                if (time < float(player.flag_time)):
                    diff = player.flag_time - time
                    diff = float("{0:.2f}".format(diff))
                    say("[FastCap] '" + name + "' " + str(diff) + " seconds faster")
                    player.flag_time = time
                elif (int(player.flag_time) == 0):
                    player.flag_time = time
                return True
            except:
                say("[WARNING] error calculating flag time (" + str(time) + ") and (" + str(player.flag_time) + ")")
                sys.exit(1)
    return False
