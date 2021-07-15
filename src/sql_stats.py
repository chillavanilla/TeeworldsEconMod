#!/usr/bin/env python3
"""SQL code for stats"""

import os.path
import sqlite3 as lite
import sys
from base.rcon import say, log, echo
import base.settings
from models.player import Player

STATS_TABLE_SCHEMA = """
CREATE TABLE Players (
    ID              INTEGER PRIMARY KEY AUTOINCREMENT,
    Name            TEXT,
    Kills           INTEGER DEFAULT 0,
    KillsHammer     INTEGER DEFAULT 0,
    KillsGun        INTEGER DEFAULT 0,
    KillsShotgun    INTEGER DEFAULT 0,
    KillsGrenade    INTEGER DEFAULT 0,
    KillsRifle      INTEGER DEFAULT 0,
    KillsNinja      INTEGER DEFAULT 0,
    Deaths          INTEGER DEFAULT 0,
    FlagGrabs       INTEGER DEFAULT 0,
    FlagCapsRed     INTEGER DEFAULT 0,
    FlagCapsBlue    INTEGER DEFAULT 0,
    FlagTime        REAL    DEFAULT 0.0,
    FlaggerKills    INTEGER DEFAULT 0,
    BestSpree       INTEGER DEFAULT 0,
    Wins            INTEGER DEFAULT 0,
    Looses          INTEGER DEFAULT 0,
    A_haxx0r        TEXT    DEFAULT '',
    A_blazeit       TEXT    DEFAULT '',
    A_satan         TEXT    DEFAULT '',
    A_virgin        TEXT    DEFAULT ''
);
"""

def init_database():
    """Create database schema"""
    global STATS_TABLE_SCHEMA
    settings = base.settings.Settings()
    if os.path.isfile(settings.get("sql_database")):
        log("database found.")
        return
    con = lite.connect(settings.get("sql_database"), timeout=20)
    with con:
        cur = con.cursor()
        cur.execute(STATS_TABLE_SCHEMA)
        log("created '" + str(settings.get("sql_database")) + "' Players table")

def has_stats(name):
    """Check if playername has stats"""
    con = lite.connect(base.settings.Settings().get("sql_database"), timeout=20)
    with con:
        cur = con.cursor()
        cur.execute("SELECT Name FROM Players WHERE Name = ? AND ID > ?;", (name, 0))
        row = cur.fetchall()
        if row:
            return True
    return False

def load_stats_sql(name):
    """Load sql stats by playername"""
    con = lite.connect(base.settings.Settings().get("sql_database"), timeout=20)
    with con:
        cur = con.cursor()
        cur.execute("""
            SELECT ID,
            Name,
            Kills,
            KillsHammer,
            KillsGun,
            KillsShotgun,
            KillsGrenade,
            KillsRifle,
            KillsNinja,
            Deaths,
            FlagGrabs,
            FlagCapsRed,
            FlagCapsBlue,
            FlagTime,
            FlaggerKills,
            BestSpree,
            Wins,
            Looses,
            A_haxx0r,
            A_blazeit,
            A_satan,
            A_virgin
            FROM Players WHERE Name = ? AND ID > ?;""",
        (name, 0))
        row = cur.fetchall()
        if base.settings.Settings().get("debug"):
            echo("[stats-load] row:" + str(row))
        if not row:
            # say("[stats-load] player='" + str(name) + "' is not in database.")
            return None
        if base.settings.Settings().get("debug"):
            say("[stats-load] " + str(row[0]))
        tmp_player = Player(row[0][1]) #row 0 0 is ID
        tmp_player.kills = row[0][2]
        tmp_player.weapon_kills[0] = row[0][3]
        tmp_player.weapon_kills[1] = row[0][4]
        tmp_player.weapon_kills[2] = row[0][5]
        tmp_player.weapon_kills[3] = row[0][6]
        tmp_player.weapon_kills[4] = row[0][7]
        tmp_player.weapon_kills[5] = row[0][8]
        tmp_player.deaths = row[0][9]
        tmp_player.flag_grabs = row[0][10]
        tmp_player.flag_caps_red = row[0][11]
        tmp_player.flag_caps_blue = row[0][12]
        tmp_player.flag_time = row[0][13]
        tmp_player.flagger_kills = row[0][14]
        tmp_player.best_spree = row[0][15]
        tmp_player.wins = row[0][16]
        tmp_player.looses = row[0][17]
        tmp_player.a_haxx0r = row[0][18]
        tmp_player.a_blazeit = row[0][19]
        tmp_player.a_satan = row[0][20]
        tmp_player.a_virgin = row[0][21]
    return tmp_player

def save_stats_sql(player):
    """Save sql stats of player object"""
    name = player.name
    con = lite.connect(base.settings.Settings().get("sql_database"), timeout=20)
    if not player:
        say("[stats-sql] failed to load player '" + name + "'")
        return False
    if has_stats(name):
        #say("[stats-sql] found stats --> loading and appending")
        load_player = load_stats_sql(name)
        if not load_player:
            say("[stats-sql] error loading stats for player '" + name + "'")
            sys.exit(1)
        player = player + load_player
        with con:
            cur = con.cursor()
            update_str = """
            UPDATE Players
            SET Kills = ?, Deaths = ?,
            KillsHammer = ?, KillsGun = ?,
            KillsShotgun = ?, KillsGrenade = ?,
            KillsRifle = ?, KillsNinja = ?,
            FlagGrabs = ?,
            FlagCapsRed = ?, FlagCapsBlue = ?,
            FlagTime = ?, FlaggerKills = ?,
            BestSpree = ?,
            Wins = ?, Looses = ?,
            A_haxx0r = ?, A_blazeit = ?, A_satan = ?, A_virgin = ?
            WHERE Name = ?;
            """
            cur.execute(
                update_str,
                (
                    player.kills, player.deaths,
                    player.weapon_kills[0], player.weapon_kills[1],
                    player.weapon_kills[2], player.weapon_kills[3],
                    player.weapon_kills[4], player.weapon_kills[5],
                    player.flag_grabs,
                    player.flag_caps_red, player.flag_caps_blue,
                    player.flag_time, player.flagger_kills,
                    player.best_spree,
                    player.wins, player.looses,
                    player.a_haxx0r, player.a_blazeit, player.a_satan, player.a_virgin,
                    player.name
                )
            )
        if base.settings.Settings().get("debug"):
            say("[stats-SQL] updated player '" + name + "'")
    else: #no stats yet --> add entry
        with con:
            cur = con.cursor()
            insert_str = """
            INSERT INTO Players
            (
                Name,
                Kills, Deaths,
                KillsHammer, KillsGun, KillsShotgun, KillsGrenade, KillsRifle, KillsNinja,
                FlagGrabs, FlagCapsRed, FlagCapsBlue, FlagTime, FlaggerKills,
                BestSpree,
                Wins, Looses,
                A_haxx0r, A_blazeit, A_satan, A_virgin
            )
            VALUES (
                ?,
                ?, ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?, ?,
                ?, ?,
                ?,
                ?, ?,
                ?, ?, ?, ?
            );
            """
            cur.execute(
                insert_str,
                (
                    player.name,
                    player.kills, player.deaths,
                    player.weapon_kills[0],
                    player.weapon_kills[1],
                    player.weapon_kills[2],
                    player.weapon_kills[3],
                    player.weapon_kills[4],
                    player.weapon_kills[5],
                    player.flag_grabs,
                    player.flag_caps_red, player.flag_caps_blue,
                    player.flag_time, player.flagger_kills,
                    player.best_spree,
                    player.wins, player.looses,
                    player.a_haxx0r, player.a_blazeit, player.a_satan, player.a_virgin
                )
            )
            row = cur.fetchall()
        if base.settings.Settings().get("debug"):
            echo(str(row))
            say("[stats-SQL] added new player to database '" + name + "'")
    return True

def save_stats_partially_sql(player):
    """Save only killing spree of given player object"""
    name = player.name
    con = lite.connect(base.settings.Settings().get("sql_database"), timeout=20)
    if not player:
        say("[stats-sql] failed to load player '" + name + "'")
        return False
    if has_stats(name):
        #say("[stats-sql] found stats --> loading and appending")
        load_player = load_stats_sql(name)
        if not load_player:
            say("[stats-sql] error loading stats for player '" + name + "'")
            sys.exit(1)
        player = player + load_player
        with con:
            cur = con.cursor()
            update_str = """
            UPDATE Players
            SET BestSpree = ?
            WHERE Name = ?;
            """
            cur.execute(
                update_str,
                (
                    player.best_spree,
                    player.name
                )
            )
        if base.settings.Settings().get("debug"):
            say("[stats-SQL] updated player '" + name + "'")
    else: #no stats yet --> add entry
        with con:
            cur = con.cursor()
            insert_str = """
            INSERT INTO Players
            (
                Name,
                BestSpree
            )
            VALUES (
                ?,
                ?
            );
            """
            cur.execute(
                insert_str,
                (
                    player.name,
                    player.best_spree
                )
            )
            row = cur.fetchall()
        if base.settings.Settings().get("debug"):
            echo(str(row))
            say("[stats-SQL] added new player to database '" + name + "'")
    return True

###################
#  D i s p l a y  #
#    S t a t s    #
###################

def rank_spree(name):
    """Print spree rank of given name"""
    if not name:
        return False
    con = lite.connect(base.settings.Settings().get("sql_database"), timeout=20)
    with con:
        cur = con.cursor()
        cur.execute(
            """
            SELECT PlayerRank, Name, BestSpree
            FROM (SELECT COUNT(*) AS PlayerRank
            FROM Players
            WHERE BestSpree > (SELECT BestSpree FROM Players WHERE Name = ?)),
            (SELECT Name, BestSpree FROM Players WHERE Name = ?);
            """,
            (name, name))
        row = cur.fetchall()
        if not row:
            say("'" + str(name) + "' is unranked.")
            return False
        rank = row[0][0] + 1 #first rank is 1 not 0
        name = row[0][1]
        value = row[0][2]
        say(str(rank) + ". '" + str(name) + "' spree " + str(value))
        return True

def rank_flag_time(name):
    """Print flag time rank of given name"""
    if not name:
        return False
    con = lite.connect(base.settings.Settings().get("sql_database"), timeout=20)
    with con:
        cur = con.cursor()
        cur.execute(
            """
            SELECT PlayerRank, Name, FlagTime
            FROM (SELECT COUNT(*) AS PlayerRank
            FROM Players WHERE FlagTime > 0.0
            AND FlagTime < (SELECT FlagTime FROM Players WHERE Name = ?)),
            (SELECT Name, FlagTime FROM Players WHERE Name = ?);
            """,
            (name, name))
        row = cur.fetchall()
        if not row:
            say("'" + str(name) + "' is unranked.")
            return False
        rank = row[0][0] + 1 #first rank is 1 not 0
        name = row[0][1]
        value = row[0][2]
        if str(value) == "0.0":
            say("[FastCap] '" + str(name) + "' is unranked.")
            return False
        say(str(rank) + ". '" + str(name) + "' time " + str(value))
    return True

def rank_flag_caps(name):
    """Print flag caps rank of given name"""
    if not name:
        return False
    con = lite.connect(base.settings.Settings().get("sql_database"), timeout=20)
    with con:
        cur = con.cursor()
        cur.execute(
                """
                SELECT PlayerRank, Name, FlagCaps FROM
                (SELECT COUNT(*) AS PlayerRank
                FROM Players
                WHERE FlagCapsRed + FlagCapsBlue > (SELECT (FlagCapsRed + FlagCapsBlue)
                AS FlagCaps FROM Players WHERE Name = ?)),
                (SELECT Name, (FlagCapsRed + FlagCapsBlue) AS FlagCaps
                FROM Players WHERE Name = ?);
                """,
                (name, name))
        row = cur.fetchall()
        if not row:
            say("'" + str(name) + "' is unranked.")
            return False
        rank = row[0][0] + 1 #first rank is 1 not 0
        name = row[0][1]
        value = row[0][2]
        say(str(rank) + ". '" + str(name) + "' flagcaps " + str(value))
        return True

def rank_kills(name):
    """Print kills rank of given name"""
    if not name:
        return False
    con = lite.connect(base.settings.Settings().get("sql_database"), timeout=20)
    with con:
        cur = con.cursor()
        cur.execute(
            """
            SELECT PlayerRank, Name, Kills
            FROM (SELECT COUNT(*) AS PlayerRank
            FROM Players
            WHERE Kills > (SELECT Kills FROM Players WHERE Name = ?)),
            (SELECT Name, Kills FROM Players WHERE Name = ?);
            """
            , (name, name))
        row = cur.fetchall()
        if not row:
            say("'" + str(name) + "' is unranked.")
            return False
        rank = row[0][0] + 1 #first rank is 1 not 0
        name = row[0][1]
        kills = row[0][2]
        say(str(rank) + ". '" + str(name) + "' kills " + str(kills))
        return True

def best_flag_caps():
    """Print best flag caps"""
    con = lite.connect(base.settings.Settings().get("sql_database"), timeout=20)
    with con:
        cur = con.cursor()
        cur.execute(
            """
            SELECT Name, (FlagCapsRed + FlagCapsBlue) AS FlagCaps
            FROM Players
            WHERE  FlagCaps > 0
            ORDER BY FlagCaps DESC LIMIT 5;
            """
            )
        row = cur.fetchall()
        if not row:
            say("something went wrong")
            return
        for index, val in enumerate(row):
            name = val[0]
            value = val[1]
            say(str(index + 1) + ". '" + str(name) + "' flagcaps: " + str(value))

def best_spree():
    """Print best spree"""
    con = lite.connect(base.settings.Settings().get("sql_database"), timeout=20)
    with con:
        cur = con.cursor()
        cur.execute(
            """
            SELECT Name, BestSpree
            FROM Players
            WHERE BestSpree > 0
            ORDER BY BestSpree DESC LIMIT 5;
            """
            )
        row = cur.fetchall()
        if not row:
            say("something went wrong")
            return
        for index, val in enumerate(row):
            name = val[0]
            value = val[1]
            say(str(index + 1) + ". '" + str(name) + "' spree: " + str(value))

def best_times():
    """Print best times"""
    con = lite.connect(base.settings.Settings().get("sql_database"), timeout=20)
    with con:
        cur = con.cursor()
        cur.execute(
            """
            SELECT Name, FlagTime
            FROM Players
            WHERE FlagTime > 0.0
            ORDER BY FlagTime ASC LIMIT 5;
            """
            )
        row = cur.fetchall()
        if not row:
            say("something went wrong")
            return
        for index, val in enumerate(row):
            name = val[0]
            value = val[1]
            say(str(index + 1) + ". '" + str(name) + "' time: " + str(value))

def best_killers():
    """Print best killers"""
    con = lite.connect(base.settings.Settings().get("sql_database"), timeout=20)
    with con:
        cur = con.cursor()
        cur.execute("SELECT Name, Kills FROM Players ORDER BY Kills DESC LIMIT 5;")
        row = cur.fetchall()
        if not row:
            say("something went wrong")
            return
        for index, val in enumerate(row):
            name = val[0]
            kills = val[1]
            say(str(index + 1) + ". '" + str(name) + "' kills: " + str(kills))
