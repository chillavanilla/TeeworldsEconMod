#!/usr/bin/env python3
import sys
import time
from chat import *
from kills import *
from player import *
from game import *
from flag import *
from sql_stats import InitDataBase

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

def main():
    InitDataBase()
    MainLoop()

if __name__ == "__main__":
    main()

