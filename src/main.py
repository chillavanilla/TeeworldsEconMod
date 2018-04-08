#!/usr/bin/env python3
import global_settings
import sys
import getopt
import time
from chat import *
from kills import *
from player import *
from game import *
from flag import *
#from sql_stats import InitDataBase
from sql_stats import *

#global_settings.init()

def HandleData(data):
    if (data.startswith("[register]")):
        #say("register found: " + data) #working but was only useless chat spam for testing        
        pass
    elif (data.startswith("[Console]")):
        if (data.find("No such command")):
            return
    elif (data.find("' entered and joined the ") != -1):
        if (data.startswith("[chat]: ***")):
            HandlePlayerJoin(data)
    elif (data.find("' has left the game") != -1):
        if (data.startswith("[chat]: ***")):
            HandlePlayerLeave(data)
    elif (data.startswith("[chat]")):
        if (data.startswith("[chat]: ***")):
            if (data.startswith("[chat]: *** The blue flag was captured by '") or data.startswith("[chat]: *** The red flag was captured by '")):
                HandleFlagCap(data)
            elif (data.find("' changed name to '") != -1):
                HandleNameChange(data)
            return
        #say("chat message: " + data)
        HandleChatMessage(data)
    elif (data.startswith("[game]")):
        HandleGame(data)

def MainLoop():
    try:
        while True:
            #time.sleep(1)
            line = sys.stdin.readline()
            if not line:
                break
            HandleData(line[10:]) #cut off the timestamp
    except EOFError:
        pass    # the telnet/netcat process finished; there's no more input

def main(argv):
    try:
        opts, args = getopt.getopt(argv,"hd:s:",["debug=","stats="])
    except getopt.GetoptError:
        print("main.py -d <debug:true/false> -s <stats:SQL/file>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
             print("test.py -i <inputfile> -o <outputfile>")
             sys.exit()
        elif opt in ("-d", "--debug"):
             IsDebug = arg
        elif opt in ("-s", "--stats"):
             StatsMode = arg
    IsDebug = IsDebug.lower()
    StatsMode = StatsMode.lower()
    if IsDebug == "0":
        IsDebug = "false"
    elif IsDebug == "1":
        IsDebug = "true"
    if not IsDebug == "false" and not IsDebug == "true":
        print("invalid debug argument")
        exit()
    if not StatsMode == "sql" and not StatsMode == "file":
        print("invalid stats mode argument")
        exit()
    if IsDebug == "true":
        global_settings.IsDebug = True
    elif IsDebug == "false":
        global_settings.IsDebug = False
    else:
        print("eror with debug mode")
        exit()
    global_settings.StatsMode = StatsMode
    print("[TEM] debug=" + str(IsDebug) + " stats=" + str(StatsMode))
    InitDataBase()
    MainLoop()

if __name__ == "__main__":
    main(sys.argv[1:])

