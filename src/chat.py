#!/usr/bin/env python3
import sys
import time
from chiller_essential import *

def HandleChatMessage(msg):
    if (msg.find("/help") != -1):
        say("=== help ===")

