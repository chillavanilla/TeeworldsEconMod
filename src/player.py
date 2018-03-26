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

def PrintStatsAll():
    global aPlayers
    for player in aPlayers:
        say("player '" + player.name + "' k/d: " + str(player.kills) + "/" + str(player.deaths))

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
