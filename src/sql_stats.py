#!/usr/bin/env python3
from chiller_essential import *
from kills import *
import os.path
import sqlite3 as lite
import sys
from base_player import *
import global_settings

create_stats_table = """
CREATE TABLE Players (
    ID              INTEGER PRIMARY KEY AUTOINCREMENT,
    Name            TEXT,
    Kills           INTEGER DEFAULT 0,
    Deaths          INTEGER DEFAULT 0,
    FlagGrabs       INTEGER DEFAULT 0,
    FlagCapsRed     INTEGER DEFAULT 0,
    FlagCapsBlue    INTEGER DEFAULT 0,
    FlagTime        REAL    DEFAULT 0.0,
    FlaggerKills    INTEGER DEFAULT 0,
    BestSpree       INTEGER DEFAULT 0,
    Wins            INTEGER DEFAULT 0,
    Looses          INTEGER DEFAULT 0
);
"""

def InitDataBase():
    global create_stats_table
    IsTable = False
    if os.path.isfile("stats.db"):
        print("stats.db found")
        return True
    con = lite.connect("stats.db")
    with con:
        cur = con.cursor()
        cur.execute(create_stats_table)
        print("created stats.db Players table")

def HasStats(name):
    con = lite.connect("stats.db")
    with con:
        c = con.cursor()
        c.execute("SELECT Name FROM Players WHERE Name = ? AND ID > ?;", (name, 0))
        row = c.fetchall()
        if row:
            return True
    return False

def LoadStatsSQL(name):
    con = lite.connect("stats.db")
    with con:
        c = con.cursor()
        c.execute("SELECT ID, Name, Kills, Deaths, FlagGrabs, FlagCapsRed, FlagCapsBlue, FlagTime, FlaggerKills, BestSpree, Wins, Looses FROM Players WHERE Name = ? AND ID > ?;", (name, 0))
        row = c.fetchall()
        #print(str(row))
        if global_settings.IsDebug:
            say("[stats-load] " + str(row[0]))
        if not row:
            return None
        tmp_player = Player(row[0][1]) #row 0 0 is ID
        tmp_player.kills = row[0][2]
        tmp_player.deaths = row[0][3]
        tmp_player.flag_grabs = row[0][4]
        tmp_player.flag_caps_red = row[0][5]
        tmp_player.flag_caps_blue = row[0][6]
        tmp_player.flag_time = row[0][7]
        tmp_player.flagger_kills = row[0][8]
        tmp_player.best_spree = row[0][9]
        tmp_player.wins = row[0][10]
        tmp_player.looses = row[0][11]
    return tmp_player

def SaveStatsSQL(name):
    from player import GetPlayerByName
    player = GetPlayerByName(name)
    con = lite.connect("stats.db")
    if not player:
        say("[stats-sql] failed to load player '" + name + "'")
        return False
    if HasStats(name):
        #say("[stats-sql] found stats --> loading and appending")
        load_player = LoadStatsSQL(name)
        if not load_player:
            say("[stats-sql] error loading stats for player '" + name + "'")
            return False
        player = player + load_player
        with con:
            cur = con.cursor()
            update_str = """
            UPDATE Players
            SET Kills = ?, Deaths = ?,
            FlagGrabs = ?, FlagCapsRed = ?, FlagCapsBlue = ?, FlagTime = ?, FlaggerKills = ?,
            BestSpree = ?,
            Wins = ?, Looses = ?
            WHERE Name = ?;
            """
            cur.execute(update_str, (player.kills, player.deaths, player.flag_grabs, player.flag_caps_red, player.flag_caps_blue, player.flag_time, player.flagger_kills, player.best_spree, player.wins, player.looses, player.name))
        if global_settings.IsDebug:
            say("[stats-SQL] updated player '" + name + "'")
    else: #no stats yet --> add entry
        with con:
            cur = con.cursor()
            insert_str = """
            INSERT INTO Players
            (Name, Kills, Deaths, FlagGrabs, FlagCapsRed, FlagCapsBlue, FlagTime, FlaggerKills, BestSpree, Wins, Looses)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
            """
            cur.execute(insert_str, (player.name, player.kills, player.deaths, player.flag_grabs, player.flag_caps_red, player.flag_caps_blue, player.flag_time, player.flagger_kills, player.best_spree, player.wins, player.looses))
            row = cur.fetchall()
            print(str(row))
        if global_settings.IsDebug:
            say("[stats-SQL] added new player to database '" + name + "'")
    return True

#
# Display
# Stats
#

def RankSpree(name):
    if not name:
        return False
    con = lite.connect("stats.db")
    with con:
        c = con.cursor()
        c.execute("SELECT PlayerRank, Name, BestSpree FROM (SELECT COUNT(*) AS PlayerRank FROM Players WHERE BestSpree > (SELECT BestSpree FROM Players WHERE Name = ?)), (SELECT Name, BestSpree FROM Players WHERE Name = ?);", (name, name))
        row = c.fetchall()
        if not row:
            say("'" + str(name) + "' is unranked.")
            return None
        rank = row[0][0] + 1 #first rank is 1 not 0
        name = row[0][1]
        value = row[0][2]
        say(str(rank) + ". '" + str(name) + "' spree " + str(value))

def RankFlagTime(name):
    if not name:
        return False
    con = lite.connect("stats.db")
    with con:
        c = con.cursor()
        c.execute("SELECT PlayerRank, Name, FlagTime FROM (SELECT COUNT(*) AS PlayerRank FROM Players WHERE FlagTime < (SELECT FlagTime FROM Players WHERE Name = ?)), (SELECT Name, FlagTime FROM Players WHERE Name = ?);", (name, name))
        row = c.fetchall()
        if not row:
            say("'" + str(name) + "' is unranked.")
            return None
        rank = row[0][0] + 1 #first rank is 1 not 0
        name = row[0][1]
        value = row[0][2]
        say(str(rank) + ". '" + str(name) + "' time " + str(value))

def RankKills(name):
    if not name:
        return False
    con = lite.connect("stats.db")
    with con:
        c = con.cursor()
        c.execute("SELECT PlayerRank, Name, Kills FROM (SELECT COUNT(*) AS PlayerRank FROM Players WHERE Kills > (SELECT Kills FROM Players WHERE Name = ?)), (SELECT Name, Kills FROM Players WHERE Name = ?);", (name, name))
        row = c.fetchall()
        if not row:
            say("'" + str(name) + "' is unranked.")
            return None
        rank = row[0][0] + 1 #first rank is 1 not 0
        name = row[0][1]
        kills = row[0][2]
        say(str(rank) + ". '" + str(name) + "' kills " + str(kills))

def BestSprees():
    con = lite.connect("stats.db")
    with con:
        c = con.cursor()
        c.execute("SELECT Name, BestSpree FROM Players WHERE BestSpree > 0 ORDER BY BestSpree DESC LIMIT 5;")
        row = c.fetchall()
        if not row:
            say("something went wrong")
            return None
        for x in range(0, len(row)):
            name = row[x][0]
            value = row[x][1]
            say(str(x + 1) + ". '" + str(name) + "' spree: " + str(value))

def BestTimes():
    con = lite.connect("stats.db")
    with con:
        c = con.cursor()
        c.execute("SELECT Name, FlagTime FROM Players WHERE FlagTime > 0.0 ORDER BY FlagTime ASC LIMIT 5;")
        row = c.fetchall()
        if not row:
            say("something went wrong")
            return None
        for x in range(0, len(row)):
            name = row[x][0]
            value = row[x][1]
            say(str(x + 1) + ". '" + str(name) + "' time: " + str(value))

def BestKillers():
    con = lite.connect("stats.db")
    with con:
        c = con.cursor()
        c.execute("SELECT Name, Kills FROM Players ORDER BY Kills DESC LIMIT 5;")
        row = c.fetchall()
        if not row:
            say("something went wrong")
            return None
        for x in range(0, len(row)):
            name = row[x][0]
            kills = row[x][1]
            say(str(x + 1) + ". '" + str(name) + "' kills: " + str(kills))

