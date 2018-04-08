#!/usr/bin/env python3
from chiller_essential import *
from kills import *
import os.path
import sqlite3 as lite
import sys
from player import Player

create_stats_table = """
CREATE TABLE Players (
    ID              INTEGER PRIMARY KEY AUTOINCREMENT,
    Name            TEXT,
    Kills           INTEGER,
    Deaths          INTEGER,
    FlagGrabs       INTEGER,
    FlagCapsRed     INTEGER,
    FlagCapsBlue    INTEGER,
    FlagTime        REAL,
    FlaggerKills    INTEGER,
    BestSpree       INTEGER
);
"""

create_stats_table = "CREATE TABLE Players (ID INTEGER PRIMARY KEY AUTOINCREMENT, Name TEXT, Kills INTEGER, Deaths INTEGER, FlagGrabs INTEGER, FlagCapsRed INTEGER, FlagCapsBlue INTEGER, FlagTime REAL, FlaggerKills INTEGER, BestSpree INTEGER)"

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
        c.execute("SELECT * FROM Players WHERE Name = ? AND ID > ?;", (name, 0))
        row = c.fetchall()
        print(str(row))
        say("row: " + str(row))
        if not row:
            return None
        #say("row[0][1]: " + str(row[0][1]))
        tmp_player = Player(row[0][1])
        tmp_player.kills = row[0][2]
        tmp_player.deaths = row[0][3]
        tmp_player.flag_grabs = row[0][4]
        tmp_player.flag_caps_red = row[0][5]
        tmp_player.flag_caps_blue = row[0][6]
        tmp_player.flag_time = row[0][7]
        tmp_player.flagger_kills = row[0][8]
        tmp_player.best_spree = row[0][9]
    return tmp_player

def SaveStatsSQL(name):
    from player import GetPlayerByName
    player = GetPlayerByName(name)
    if not player:
        say("[stats-sql] failed to load player '" + name + "'")
        return False
    if HasStats(name):
        say("[stats-sql] found stats --> loading and appending")
        load_player = LoadStatsSQL(name)
        if not load_player:
            say("[stats-sql] error loading stats for player '" + name + "'")
            return False
        player = player + load_player

    con = lite.connect("stats.db")
    with con:
        cur = con.cursor()
        cur.execute("INSERT INTO Players (Name, Kills, Deaths) VALUES (?, ?, ?)", (player, player.kills, player.deaths))
        row = cur.fetchall()
        print(str(row))
    return True

def LoadAllPlayersSQL():
    con = lite.connect("stats.db")
    with con:
        c = con.cursor()
        c.execute("SELECT * FROM Players;")
        row = c.fetchall()
        print(str(row))
