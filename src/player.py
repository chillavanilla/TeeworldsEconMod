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
    init_player = InitPlayer(name, ID, team, ShowStats, spree)
    if not init_player:
        say("[ERROR] CreatePlayer init_player=None name='" + str(name) + "' ID=" + str(ID))
        sys.exit(1)
    aPlayers.append(init_player)
    #say("added player '" + name + "'")

def InitPlayer(name, ID, team, ShowStats, spree):
    init_player = None
    load_player = LoadStats(name)
    if load_player:
        if ShowStats:
            load_player.ShowStats()
        init_player = Player(name, ID, load_player.flag_time, load_player.best_spree, team)
        init_player.a_haxx0r = load_player.a_haxx0r
        init_player.a_blazeit = load_player.a_blazeit
        init_player.a_satan = load_player.a_satan
        init_player.a_virgin = load_player.a_virgin
        init_player.killingspree = spree
        init_player.WEAPON_KILLS[0] = load_player.WEAPON_KILLS[0]
        init_player.WEAPON_KILLS[1] = load_player.WEAPON_KILLS[1]
        init_player.WEAPON_KILLS[2] = load_player.WEAPON_KILLS[2]
        init_player.WEAPON_KILLS[3] = load_player.WEAPON_KILLS[3]
        init_player.WEAPON_KILLS[4] = load_player.WEAPON_KILLS[4]
        init_player.WEAPON_KILLS[5] = load_player.WEAPON_KILLS[5]
    else:
        init_player = Player(name, ID=ID, team=team)
    return init_player

def GetPlayersArray():
    global aPlayers
    return aPlayers

def DeletePlayer(id):
    global aPlayers
    #aPlayers.remove(GetPlayerByName(name))
    del aPlayers[GetPlayerIndexByID(id)]
    #say("deleted player '" + name + "'")

def CountPlayers():
    global aPlayers
    return len(aPlayers)

def SaveAndDeletePlayerByName(name):
    player = GetPlayerByName(name)
    if not player:
        return False
    SaveAndDeletePlayer(player)

def SaveAndDeletePlayer(player):
    if not player:
        return False
    # dirty killingspree update
    # TODO: do an sql query here to support same player online multiple names
    # for 0.7 same name servers and multiple servers running at once
    player.best_spree = max(player.killingspree, player.best_spree)
    DeletePlayer(player.ID) #delete old player without spree update
    aPlayers.append(player) #add new player with spree update
    SaveStats(player)
    DeletePlayer(player.ID)

def RefreshAllPlayers():
    global aPlayers
    for player in aPlayers:
        p = player
        SaveAndDeletePlayer(player)
        CreatePlayer(p.name, p.ID, p.team, ShowStats=False, spree=p.killingspree)

def GetPlayerIndexByName(name):
    global aPlayers
    index = 0
    for player in aPlayers:
        if (player.name == name):
            return index
        index += 1
    return -1

def GetPlayerIndexByID(ID):
    global aPlayers
    index = 0
    for player in aPlayers:
        if (player.ID == ID):
            return index
        index += 1
    return -1

def GetPlayerByName(name):
    global aPlayers
    for player in aPlayers:
        if (player.name == name):
            return player
    return None

def GetPlayerByID(ID):
    global aPlayers
    for p in aPlayers:
        if (p.ID == ID):
            return p
    return None

def DebugPlayerList():
    global aPlayers
    for p in aPlayers:
        say("  id=" + str(p.ID) + " name='" + str(p.name) + "'")

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

# [server]: player is ready. ClientID=0 addr=172.20.10.9:52244
def HandlePlayerReady(data):
    id_start = data.find("=") + 1
    id_end = data.find(" ", id_start)
    id_str = data[id_start:id_end]
    if g_settings.get("tw_version") == 6:
        id_str = str(int(id_str, 16)) # 0.6 uses hex for ids in ready messages
    # name is actually "(connecting)" but better use None
    CreatePlayer(name=None, ID=id_str, ShowStats=True)

# [server]: player has entered the game. ClientID=0 addr=172.20.10.9:54272
# def HandlePlayerEnter(data):
#     id_start = data.find("=") + 1
#     id_end = data.find(" ", id_start)
#     id_str = data[id_start:id_end]
#     if g_settings.get("tw_version") == 6:
#         id_str = str(int(id_str, 16)) # 0.6 uses hex for ids in enter messages
#     CreatePlayer(name=None, ID=id_str, ShowStats=True)

# [server]: client dropped. cid=1 addr=172.20.10.9:53784 reason=''
def HandlePlayerLeave(data):
    id_start = data.find("=") + 1
    id_end = data.find(" ", id_start)
    id_str = data[id_start:id_end]
    player = GetPlayerByID(id_str)
    if player == None:
        echo("[ERROR] invalid player left id=" + str(id_str))
        say("   DATA=" + str(data))
        sys.exit(1)
    SaveAndDeletePlayer(player)

# [game]: team_join player='0:ChillerDragon' team=0
# [game]: team_join player='0:ChillerDragon' team=0->-1
def HandlePlayerTeam(data):
    global aPlayers
    id_start = data.find("'") + 1
    id_end = cbase.cfind(data, ":", 2)
    id_str = data[id_start:id_end]
    player = GetPlayerByID(id_str)
    if player == None:
        say("[ERROR] teamchange failed id=" + str(id_str) + " data=" + str(data))
        DebugPlayerList()
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
        DeletePlayer(player.ID) # delete invalid tmp player
        CreatePlayer(name, player.ID, player.team)
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
    SaveAndDeletePlayerByName(old)
    CreatePlayer(new, player.ID, team=team)

def SetFlagger(player, IsFlag, timestamp = ""):
    if not player:
        if IsFlag:
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

def UpdateAchievement(player, ach):
    if not player:
        say("[ERROR] failed achievement: invalid player.")
        sys.exit(1)
        return False
    ts = str(datetime.datetime.now().year) + "-" +  str(datetime.datetime.now().month) + "-" + str(datetime.datetime.now().day)
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
        return False
    return True

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

def UpdatePlayerKills(player, kills, weapon):
    # say("kill weapon=" + WEAPONS[weapon])
    if not player:
        return False
    player.LastKill = ProcessMultiKills(player, weapon)
    player.LastKillWeapon = weapon
    player.kills += kills
    player.WEAPON_KILLS[weapon] += kills
    if CountPlayers() > g_settings.get("spree_players"): # only activate killingsprees on 8+ players
        player.killingspree += kills
        if (player.killingspree % 10 == 0):
            broadcast("'" + player.name + "' is on a killing spree with " + str(player.killingspree) + " kills ")
    return True
    
def UpdatePlayerDeaths(player, killer, deaths):
    if not player:
        return False
    player.deaths += deaths
    if CountPlayers() > g_settings.get("spree_players"): # only activate killingsprees on 8+ players
        if player.killingspree > 9:
            broadcast("'" + player.name + "'s killing spree with " + str(player.killingspree) + " kills was ended by '" + killer + "'")
        if player.killingspree > player.best_spree:
            if (player.killingspree > 9):
                say("'" + player.name + "' new killingspree record! Old: " + str(player.best_spree) + " New: " + str(player.killingspree))
            player.best_spree = player.killingspree
            SaveStatsPartially(player)
        player.killingspree = 0
    return True

def TeamWon(team):
    global aPlayers
    if not team == "red" and not team == "blue":
        say("[WARNING] invalid team won " + str(team))
    for player in aPlayers:
        if player.team == team:
            player.wins += 1
        elif not player.team == "" and not player.team == "spectator":
            player.looses += 1

def UpdatePlayerFlagGrabs(player, grabs):
    if not CountPlayers() > g_settings.get("flag_players"):
        return False
    if not player:
        return False
    player.flag_grabs += grabs
    game.UpdateFlagGrabs(player.team == "red")
    return True

def UpdatePlayerFlagCaps(player, color, caps):
    if not player:
        say("[ERROR] failed player.UpdatePlayerFlagCaps: invalid player.")
        sys.exit(1)
        return False
    if not CountPlayers() > g_settings.get("flag_players"):
        return False
    if (color == "blue"):
        player.flag_caps_blue += caps
    elif (color == "red"):
        player.flag_caps_red += caps
    else:
        say("savage '" + player.name + "' captured the pink flag")
        return False
    return True

def UpdatePlayerFlagTime(player, time):
    if not player:
        say("[ERROR] failed player.UpdatePlayerFlagTime: invalid player.")
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
