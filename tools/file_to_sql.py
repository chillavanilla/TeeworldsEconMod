#!/usr/bin/env python3
#
# WARNING! this script is outdated and untested
# it most likley corrupts your data!
#
# Update file stats to sql stats with this script
# put this script in the same directory as your stats/ folder
# then it will read all stats files and save them to stats.db
#
import os.path
import sqlite3 as lite
import sys

AddedPlayers = 0
UpdatedPlayers = 0

def say(str):
    print(str)

def best_time(t1, t2):
    t = min(t1,t2)
    if t == 0:
        return max(t1, t2) #if no time yet --> set the highest
    return t #if captured already use lowest time

class Player:
    def __init__(self, name, time=0.0, spree=0):
        self.name = name
        self.kills = 0
        self.deaths = 0
        self.flag_grabs = 0
        self.flag_caps_red = 0
        self.flag_caps_blue = 0
        self.flag_time = time
        self.flagger_kills = 0
        self.best_spree = spree
        #round variables (not saved)
        self.killingspree = 0
        self.is_flagger = False
    def __add__(self, other):
        tmp_player = Player(self.name)
        tmp_player.kills = self.kills + other.kills
        tmp_player.deaths = self.deaths + other.deaths
        tmp_player.flag_grabs = self.flag_grabs + other.flag_grabs
        tmp_player.flag_caps_red = self.flag_caps_red + other.flag_caps_red
        tmp_player.flag_caps_blue = self.flag_caps_blue + other.flag_caps_blue
        tmp_player.flag_time = best_time(self.flag_time, other.flag_time)
        tmp_player.flagger_kills = self.flagger_kills + other.flagger_kills
        tmp_player.best_spree = max(self.best_spree, other.best_spree)
        """
        say("== merging '" + other.name + "' -> into -> '" + self.name + "' ===")
        say("src: ")
        say("k/d: " + str(other.kills) + " g/r/b/t: " + str(other.flag_grabs) + "/" + str(other.flag_caps_red) + "/" + str(other.flag_caps_blue) + "/" + str(other.flag_time))
        say("dst: ")
        say("k/d: " + str(self.kills) + " g/r/b/t: " + str(self.flag_grabs) + "/" + str(self.flag_caps_red) + "/" + str(self.flag_caps_blue) + "/" + str(self.flag_time))
        say("merge: ")
        say("k/d: " + str(tmp_player.kills) + " g/r/b/t: " + str(tmp_player.flag_grabs) + "/" + str(tmp_player.flag_caps_red) + "/" + str(tmp_player.flag_caps_blue) + "/" + str(tmp_player.flag_time))
        """
        return tmp_player
    def show_stats(self):
        say("[stats] '" + self.name + "' kills: " + str(self.kills) + " deaths: " + str(self.deaths) + " killingspree: " + str(self.best_spree))

STATS_TABLE_SCHEMA = """
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
    BestSpree       INTEGER DEFAULT 0
);
"""

def init_database():
    global STATS_TABLE_SCHEMA
    IsTable = False
    if os.path.isfile("stats.db"):
        print("stats.db found")
        return True
    con = lite.connect("stats.db")
    with con:
        cur = con.cursor()
        cur.execute(STATS_TABLE_SCHEMA)
        print("created stats.db Players table")

def HasStatsFile(name):
    if os.path.isfile("stats/" + name + ".acc"):
        return True
    return False

def load_stats_file(name):
    if not HasStatsFile(name):
        return None
    try:
        sf = open("stats/" + name + ".acc", "r")
        player = Player(name)
        player.kills = int(sf.readline())
        player.deaths = int(sf.readline())
        player.flag_grabs = int(sf.readline())
        player.flag_caps_red = int(sf.readline())
        player.flag_caps_blue = int(sf.readline())
        player.flag_time = float(sf.readline())
        player.flagger_kills = int(sf.readline())
        player.best_spree = int(sf.readline())
        sf.close()
        return player
    except:
        say("[ERROR] failed to loaded stats for '" + name + "'")
        sys.exit(1)
        return None

def HasStatsSQL(name):
    con = lite.connect("stats.db")
    with con:
        c = con.cursor()
        c.execute("SELECT Name FROM Players WHERE Name = ? AND ID > ?;", (name, 0))
        row = c.fetchall()
        if row:
            return True
    return False

def load_stats_sql(name):
    con = lite.connect("stats.db")
    with con:
        c = con.cursor()
        c.execute("SELECT * FROM Players WHERE Name = ? AND ID > ?;", (name, 0))
        row = c.fetchall()
        #say("[stats-load] " + str(row[0]))
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
    return tmp_player

def save_stats_sql(player):
    global AddedPlayers
    global UpdatedPlayers
    con = lite.connect("stats.db")
    if not player:
        say("[stats-sql] failed to load player '" + name + "'")
        return False
    name = player.name
    if HasStatsSQL(name):
        #say("[stats-sql] found stats --> loading and appending")
        load_player = load_stats_sql(name)
        if not load_player:
            say("[stats-sql] error loading stats for player '" + name + "'")
            sys.exit(1)
            return False
        player = player + load_player
        UpdatedPlayers += 1
        with con:
            cur = con.cursor()
            update_str = """
            UPDATE Players
            SET Kills = ?, Deaths = ?,
            FlagGrabs = ?, FlagCapsRed = ?, FlagCapsBlue = ?, FlagTime = ?, FlaggerKills = ?,
            BestSpree = ?
            WHERE Name = ?;
            """
            cur.execute(update_str, (player.kills, player.deaths, player.flag_grabs, player.flag_caps_red, player.flag_caps_blue, player.flag_time, player.flagger_kills, player.best_spree, player.name))
        if global_settings.IsDebug:
            say("[stats-SQL] updated player '" + name + "'")
    else: #no stats yet --> add entry
        AddedPlayers += 1
        with con:
            cur = con.cursor()
            insert_str = """
            INSERT INTO Players
            (Name, Kills, Deaths, FlagGrabs, FlagCapsRed, FlagCapsBlue, FlagTime, FlaggerKills, BestSpree)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
            """
            cur.execute(insert_str, (player.name, player.kills, player.deaths, player.flag_grabs, player.flag_caps_red, player.flag_caps_blue, player.flag_time, player.flagger_kills, player.best_spree))
            row = cur.fetchall()
            print(str(row))
        #say("[stats-SQL] added new player to database '" + name + "'")
    return True


#
#  DEPENDENCIES END
#


def FileToSQL():
    global AddedPlayers
    global UpdatedPlayers
    TotalPlayers = 0

    say("creating stats.db")
    init_database()
    say("searching stats files in stats/ ...")

    for StatsFile in os.listdir("stats/"):
        if StatsFile.endswith(".acc"):
            name = StatsFile[:StatsFile.rfind(".acc")]
            #say("global stats loading '" + name + "'")
            #tmp_player = load_stats(name)
            if name:
                player = load_stats_file(name)
                if player:
                    save_stats_sql(player)
                    TotalPlayers += 1
                else:
                    say("failed to load player from file")
            else:
                say("weird error")
                sys.exit(1)
    say("Finished with " + str(TotalPlayers) + " players in total")
    say("Updated: " + str(UpdatedPlayers) + " Added: " + str(AddedPlayers))

FileToSQL()

