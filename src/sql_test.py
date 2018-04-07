#!/usr/bin/env python3

import sqlite3 as lite
import sys



def TestSQL():
    con = lite.connect("stats.db")

    name = "test test"


    with con:
        c = con.cursor()
        #c.execute("SELECT * FROM Players WHERE Name = ? AND Kills > ?", (name, 0))
        c.execute("SELECT * FROM Players WHERE Name = ? AND ID > ?", (name, 0))
        row = c.fetchall()
        print(str(row))


