#!/usr/bin/env python3
import sys
import time
from chiller_essential import *
from save_stats import *
from base_player import *

aPlayers=[]

def CreatePlayer(name, team=""):
    global aPlayers
    load_player = LoadStats(name)
    if load_player:
        load_player.ShowStats()
        aPlayers.append(Player(name, load_player.flag_time, load_player.best_spree, team))
    else:
        aPlayers.append(Player(name, team=team))
    #say("added player '" + name + "'")

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

def HandlePlayerTeamSwap(data, IsSpec=False):
    name_start = data.find("'") + 1
    name_end = data.rfind("' joined the ", name_start)
    name = data[name_start:name_end]
    player = GetPlayerByName(name)
    if not player: #something went wrong
        say("[WARNING] something went wrong with '" + str(name) + "' s team switch")
        return False
    DeletePlayer(name)
    team = ""
    if IsSpec:
        team = "spectator"
    elif data.find("' joined the red", name_start) != -1:
        team = "red"
    elif data.find("' joined the blue", name_start) != -1:
        team = "blue"
    player.team = team
    aPlayers.append(player)

def HandlePlayerJoin(data):
    name_start = data.find("'") + 1
    name_end = data.find("' entered and joined the ", name_start)
    name = data[name_start:name_end]    
    if GetPlayerByName(name): #filter double names (could happen due rejoining or team switch)
        return False
    team = ""
    if data.find("' entered and joined the red", name_start) != -1:
        team = "red"
    elif data.find("' entered and joined the blue", name_start) != -1:
        team = "blue"
    CreatePlayer(name, team)
            
def HandlePlayerLeave(data):
    name_start = data.find("'") + 1
    name_end = data.find("' has left the game", name_start)
    name = data[name_start:name_end]
    SaveAndDeletePlayer(name)

def HandleNameChange(data):
    old_start = data.find("'") + 1
    old_end = data.find("' changed name to '")
    old = data[old_start:old_end]
    new_start = old_end + len("' changed name to '")
    new_end = data.rfind("'")
    new = data[new_start:new_end]
    SaveAndDeletePlayer(old)
    CreatePlayer(new)

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

def UpdatePlayerKills(name, kills):
    global aPlayers
    for player in aPlayers:
        if (player.name == name):
            player.kills += kills
            if CountPlayers() > 7: # only activate killingsprees on 8+ players
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
            if CountPlayers() > 7: # only activate killingsprees on 8+ players
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
    global aPlayers
    for player in aPlayers:
        if (player.name == name):
            player.flag_grabs += grabs
            return True
    return False

def UpdatePlayerFlagCaps(name, color, caps):
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
                    say("'" + name + "' captured the flag " + str(diff) + " seconds faster")
                    player.flag_time = time
                elif (int(player.flag_time) == 0):
                    player.flag_time = time
                return True
            except:
                say("[WARNING] error calculating flag time (" + str(time) + ") and (" + str(player.flag_time) + ")")
    return False


