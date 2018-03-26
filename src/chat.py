#!/usr/bin/env python3
import sys
import time
from chiller_essential import *
from player import *
from save_stats import *

def HandleChatMessage(msg):
    msg_normal = msg
    msg = msg.lower()
    if (msg.find("/help") != -1 or msg.find("/info") != -1 or msg.find("/cmdlist") != -1):
        say("==== help ====")
        say("command list comming soon...")
    elif (msg.find("/stats") != -1):
        #say("sample rank message...")
        PrintStatsAll()
    elif (msg.find("/test") != -1):
        SaveStats("where_am_i")
