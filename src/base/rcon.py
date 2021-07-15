#!/usr/bin/env python3
"""Essential wrappers around the teeworlds api"""

import sys
import base.settings
import discord.thread

def escape_string_killers(msg):
    """Helper method to fix string escape in teeworlds commands"""
    return msg.replace('"', '\\"')

def rcon_exec(cmd):
    """Execute given rcon command"""
    if base.settings.Settings().get("debug"):
        say("rcon_exec('" + str(cmd) + "')")
    sys.stdout.write(cmd + '\n')
    sys.stdout.flush()

def say(msg):
    """Print given message"""
    sys.stdout.write('say "' + escape_string_killers(msg) + '"\n')
    sys.stdout.flush()

def broadcast(msg):
    """Broadcast given message"""
    sys.stdout.write('broadcast "' + escape_string_killers(msg) + '"\n')
    sys.stdout.flush()

def echo(msg):
    """Echo given message"""
    sys.stdout.write('echo "' + escape_string_killers(msg) + '"\n')
    sys.stdout.flush()

def log(msg):
    """Print given message to logfiles only"""
    sys.stdout.write("###[log]: " + str(msg) + "\n")
    sys.stdout.flush()

def send_discord(message):
    """Send a discord message in newly spawned thread"""
    thread = discord.thread.SendDiscord(message)
    thread.start()
