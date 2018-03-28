#!/usr/bin/env python3

#This Test script shoukd do the same as the sql_stats.py
#but this test runs fine and it displays the row found in the database
#no idea why this code isnt working in sql_stats.py


import sqlite3 as lite
import sys

def say(str):
    sys.stdout.write(str)
    sys.stdout.flush()


'''

con = lite.connect("stats.db")

chiller = "ChillerDragon.*"

sql_str = "SELECT * FROM Players WHERE Name = '" + chiller + "';"


with con:
    c = con.cursor()
    c.execute(sql_str)
    row = c.fetchall()
    print(str(row))

'''

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



SaveStatsSQL("STETETZADUHIWAD")
