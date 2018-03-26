#!/usr/bin/env python3
import sys
import time
from chiller_essential import *

aPlayers=[]


class Player:
    def __init__(self, name):
        self.name = name
        self.kills = 0
        self.deaths = 0
        self.flag_grabs = 0
        self.flag_caps_red = 0
        self.flag_caps_blue = 0
        self.flag_time = 0.0

def CreatePlayer(name):
    global aPlayers
    aPlayers.append(Player(name))
    #say("added player '" + name + "'")

def DeletePlayer(name):
    global aPlayers
    #aPlayers.remove(GetPlayerByName(name))
    del aPlayers[GetPlayerIndex(name)]
    #say("deleted player '" + name + "'")

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

def PrintStatsAll():
    global aPlayers
    for player in aPlayers:
        say("player '" + player.name + "' k/d: " + str(player.kills) + "/" + str(player.deaths) + " flag g" + str(player.flag_grabs) + "/r" + str(player.flag_caps_red) + "/b" + str(player.flag_caps_blue) + "/t" + str(player.flag_time))

def HandlePlayerJoin(data):
    name_start = data.find("'") + 1
    name_end = data.find("' entered and joined the ", name_start)
    name = data[name_start:name_end]    

    if GetPlayerByName(name): #filter double names (could happen due rejoining or team switch)
        return False

    CreatePlayer(name)

def HandlePlayerLeave(data):
    name_start = data.find("'") + 1
    name_end = data.find("' has left the game", name_start)
    name = data[name_start:name_end]

    if not GetPlayerByName(name):
        return False

    DeletePlayer(name)

# Update Player Values

def UpdatePlayerKills(name, kills):
    global aPlayers
    for player in aPlayers:
        if (player.name == name):
            player.kills += kills
            return True
    return False
    
def UpdatePlayerDeaths(name, deaths):
    global aPlayers
    for player in aPlayers:
        if (player.name == name):
            player.deaths += deaths
            return True
    return False

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
            if (time < player.flag_time):
                diff = player.flag_time - time
                say("'" + name + "' captured the flag " + str(diff) + " seconds faster")
                player.flag_time = time
            elif (int(player.flag_time) == 0):  
                player.flag_time = time
            return True
    return False


