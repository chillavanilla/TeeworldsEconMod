#!/usr/bin/env python3
import sys
import time
from chat import *
from kills import *

def HandleData(data):
    if (data.startswith("[register]")):
        #say("register found: " + data) #working but was only useless chat spam for testing        
        pass
    elif (data.startswith("[Console]")):
        if (data.find("No such command")):
            return
    elif (data.startswith("[chat]")):
        if (data.find("[chat]: ***") != -1):
            return
        #say("chat message: " + data)
        HandleChatMessage(data)
    elif (data.startswith("[game]")):
        if (data.find("kill killer") != -1):
            HandleKills(data)    

try:
    while True:
        #time.sleep(1)
        line = sys.stdin.readline()
        if not line:
            break
        HandleData(line[10:]) #cut off the timestamp
except EOFError:
    pass    # the telnet/netcat process finished; there's no more input

