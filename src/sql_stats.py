#!/usr/bin/env python3
from chiller_essential import *
from kills import *
import os.path
import sqlite3 as lite
import sys

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
);
"""

create_stats_table = "CREATE TABLE Players (ID INTEGER PRIMARY KEY AUTOINCREMENT, Name TEXT, Kills INTEGER, Deaths INTEGER, FlagGrabs INTEGER, FlagCapsRed INTEGER, FlagCapsBlue INTEGER, FlagTime REAL, FlaggerKills INTEGER)"

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

def SaveStatsSQL(player):
    con = lite.connect("stats.db")
    '''
    with con:
        cur = con.cursor()
        #cur.execute("INSERT INTO Players VALUES(" + player.name + ", 0,0,0,0,0,0,0);")
        show = "SELECT * FROM Players WHERE Name = '" + player.name + "';"
        cur.execute(show)
        row = cur.fetchall()
    '''
    chiller = "ChillerDragon.*"
    sql_str = "SELECT * FROM Players WHERE Name = '" + chiller + "';"
    with con:
        c = con.cursor()
        c.execute(sql_str)
        row = c.fetchall()
        print(str(row))
        say("sql: " + sql_str)
        say("row: " + str(row))
    pass


def LoadStatsSQL(player):
    pass

