#!/usr/bin/env python3
"""
Create a huughe player array holding all stats collected so far
Then analyze the array and pick some top players
"""

# from base.rcon import say
# from save_stats import load_stats


# aGlobalPlayers = []


# def load_global_stats():
#     """load players and sort them by kills"""
#     global aGlobalPlayers
#     TotalPlayers = 0
#     BestKills = 0
#     for StatsFile in os.listdir("stats/"):
#         if StatsFile.endswith(".acc"):
#             name = StatsFile[:StatsFile.rfind(".acc")]
#             #say("global stats loading '" + name + "'")
#             tmp_player = load_stats(name)
#             if (tmp_player.kills > BestKills):
#                 say("'" + tmp_player.name + "' new kills score (" +
#                     str(BestKills) + " -> " + str(tmp_player.kills) + ")")
#                 BestKills = tmp_player.kills
#             if not tmp_player:
#                 say("failed to load player")
#             else:
#                 aGlobalPlayers.append(tmp_player)
#                 TotalPlayers += 1
#             continue
#         else:
#             continue
#     say("loaded " + str(TotalPlayers) + " players in total")
#     sort_players_by_kills()


# def sort_players_by_kills():
#     """bubble sort"""
#     global aGlobalPlayers

#     i1 = 0
#     i2 = 0
#     for p1 in aGlobalPlayers:
#         i1 += 1
#         i2 = 0
#         for p2 in aGlobalPlayers:
#             i2 += 1
#             if p1.kills < p2.kills:
#                 say("'" + p1.name + "' (" + str(p1.kills) + ") < '" +
#                     p2.name + "' (" + str(p2.kills) + ")")
#                 tmp = p1
#                 aGlobalPlayers[i1] = p2
#                 #p1 = p2
#                 aGlobalPlayers[i2] = tmp
#                 #p2 = tmp
#     say(" best killer '" +
#         aGlobalPlayers[0].name +
#         "' with " +
#         str(aGlobalPlayers[0].kills) +
#         " kills")
