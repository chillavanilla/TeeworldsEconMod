#!/bin/bash

ts="[2019-09-19 12:44:17]"

function log() {
    echo "${ts}$1"
    sleep 0.1
}

log "[engine]: running on unix-linux-amd64"
log "[engine]: arch is little endian"
log "[storage]: couldn't open storage.cfg"
log "[storage]: using standard paths"
log "[storage]: added path '$USERDIR' ('/home/chiller/.teeworlds')"
log "[storage]: added path '$DATADIR' ('/usr/share/games/teeworlds/data')"
log "[storage]: added path '$CURRENTDIR' ('/home/chiller/Desktop/vanilla7')"
log "[storage]: added path '$APPDIR' ('.')"
log "[console]: executing 'autoexec.cfg'"
log "[server]: starting..."
log "[datafile]: loading. filename='maps/ctf5_f.map'"
log "[datafile]: allocsize=2408"
log "[datafile]: readsize=2080"
log "[datafile]: swaplen=2100"
log "[datafile]: item_size=1712"
log "[datafile]: loading done. datafile='maps/ctf5_f.map'"
log "[datafile]: loading data index=11 size=223 uncompressed=712"
log "[datafile]: loading data index=12 size=1219 uncompressed=5156"
log "[datafile]: loading data index=13 size=19 uncompressed=468"
log "[datafile]: loading data index=14 size=560 uncompressed=1524"
log "[datafile]: loading data index=15 size=830 uncompressed=2468"
log "[datafile]: loading data index=16 size=1303 uncompressed=5220"
log "[datafile]: loading data index=17 size=330 uncompressed=1192"
log "[datafile]: loading data index=18 size=1695 uncompressed=7284"
log "[datafile]: loading data index=19 size=1146 uncompressed=4492"
log "[datafile]: loading data index=20 size=156 uncompressed=648"
log "[datafile]: loading data index=21 size=27 uncompressed=512"
log "[server]: maps/ctf5_f.map sha256 is 8692f4f91239b298b6ecadb4700d1a7a7f166742e3864d8026a41c1d43e64a42"
log "[server]: maps/ctf5_f.map crc is 3a1694a7"
log "[econ]: bound to localhost:1337"
log "[server]: server name is 'ChillerDragon's Vanilla test server 7'"
log "[server]: version 0.7 802f1be60a05665f"
log "[engine/mastersrv]: refreshing master server addresses"
log "[register]: refreshing ip addresses"
log "[engine/mastersrv]: saving addresses"
log "[register]: fetching server counts"
log "[register]: chose 'master1.teeworlds.com' as master, sending heartbeats"
log "[server]: player is ready. ClientID=0 addr=172.20.10.9:62522"
log "[game]: Teams are balanced (red=1 blue=0)"
log "[server]: player has entered the game. ClientID=0 addr=172.20.10.9:62522"
log "[game]: team_join player='0:nameless tee' team=0"
log "[chat]: 0:1:nameless tee: /rank"
log "[chat]: 0:1:nameless tee: /stats"
log "[server]: player is ready. ClientID=1 addr=172.20.10.9:53784"
log "[game]: start match type='CTF' teamplay='1'"
log "[game]: Teams are balanced (red=1 blue=1)"
log "[server]: player has entered the game. ClientID=1 addr=172.20.10.9:53784"
log "[game]: team_join player='1:nameless tee' team=1"
log "[game]: pickup player='0:nameless tee' item=2"
log "[game]: kill killer='0:nameless tee' victim='1:nameless tee' weapon=3 special=0"
log "[game]: kill killer='0:nameless tee' victim='1:nameless tee' weapon=3 special=0"
log "[game]: kill killer='0:nameless tee' victim='1:nameless tee' weapon=3 special=0"
log "[game]: kill killer='0:nameless tee' victim='1:nameless tee' weapon=3 special=0"
log "[game]: kill killer='0:nameless tee' victim='1:nameless tee' weapon=3 special=0"
log "[game]: kill killer='0:nameless tee' victim='1:nameless tee' weapon=3 special=0"
log "[game]: kill killer='0:nameless tee' victim='1:nameless tee' weapon=3 special=0"
log "[game]: kill killer='0:nameless tee' victim='1:nameless tee' weapon=3 special=0"
log "[game]: kill killer='0:nameless tee' victim='1:nameless tee' weapon=3 special=0"
log "[game]: pickup player='0:nameless tee' item=2"
log "[game]: pickup player='0:nameless tee' item=1"
log "[game]: pickup player='0:nameless tee' item=1"
log "[game]: pickup player='0:nameless tee' item=1"
log "[game]: pickup player='0:nameless tee' item=3"
log "[game]: kill killer='0:nameless tee' victim='1:nameless tee' weapon=3 special=0"
log "[game]: pickup player='0:nameless tee' item=1"
log "[game]: pickup player='0:nameless tee' item=1"
log "[game]: pickup player='0:nameless tee' item=1"
log "[server]: client dropped. cid=0 addr=172.20.10.9:62522 reason=''"
log "[game]: kill killer='0:nameless tee' victim='0:nameless tee' weapon=-3 special=0"
log "[game]: leave player='0:nameless tee'"
log "[game]: Teams are balanced (red=0 blue=1)"
log "[register]: WARNING: Master server is not responding, switching master"
log "[engine/mastersrv]: refreshing master server addresses"
log "[register]: refreshing ip addresses"
log "[engine/mastersrv]: saving addresses"
log "[register]: fetching server counts"
log "[server]: client dropped. cid=1 addr=172.20.10.9:53784 reason=''"
log "[game]: kill killer='1:nameless tee' victim='1:nameless tee' weapon=-3 special=0"
log "[game]: leave player='1:nameless tee'"
log "[game]: Teams are balanced (red=0 blue=0)"
log "[register]: chose 'master1.teeworlds.com' as master, sending heartbeats"





sleep 1

