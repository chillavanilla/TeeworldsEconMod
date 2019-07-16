#!/usr/bin/env python3
from chiller_essential import *
from save_stats import *


# Create a huughe player array holding all stats collected so far
# Then analyze the array and pick some top players

aGlobalPlayers=[]

def LoadGlobalStats():
    global aGlobalPlayers
    TotalPlayers = 0
    BestKills = 0
    for StatsFile in os.listdir("stats/"):
        if StatsFile.endswith(".acc"):
            name = StatsFile[:StatsFile.rfind(".acc")]
            #say("global stats loading '" + name + "'")
            tmp_player = LoadStats(name)
            if (tmp_player.kills > BestKills):
                say("'" + tmp_player.name + "' new kills score (" + str(BestKills) + " -> " + str(tmp_player.kills) + ")")
                BestKills = tmp_player.kills
            if not tmp_player:
                say("failed to load player")
            else:
                aGlobalPlayers.append(tmp_player)
                TotalPlayers += 1
            continue
        else:
            continue
    say("loaded " + str(TotalPlayers) + " players in total") 
    SortPlayersByKills()

def SortPlayersByKills():
    global aGlobalPlayers
    
    '''

    t = 0
    for test in aGlobalPlayers:
        t += 1
    say("test: " + str(t))

    index = 0
    while index < 20:
        index += 1
        player = aGlobalPlayers[index]
        say(" test player [" + str(index) + "]  name: " + player.name + " kills: " + str(player.kills))

    return
    '''

    i1 = 0
    i2 = 0
    for p1 in aGlobalPlayers:
        i1 += 1
        i2 = 0
        for p2 in aGlobalPlayers:
            i2 += 1
            if p1.kills < p2.kills:
                say("'" + p1.name + "' (" + str(p1.kills) + ") < '" + p2.name + "' (" + str(p2.kills) + ")")                


                tmp = p1
                

                aGlobalPlayers[i1] = p2                

                #p1 = p2
        

                aGlobalPlayers[i2] = tmp

                #p2 = tmp
    say(" best killer '" + aGlobalPlayers[0].name + "' with " + str(aGlobalPlayers[0].kills) + " kills")
