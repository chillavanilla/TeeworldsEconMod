#!/usr/bin/env python3
"""The discord thread module"""

import requests
from threading import Thread
import base.settings

class SendDiscord(Thread):
    """Thread for sending discord messages non blocking"""
    def __init__(self, message):
        self.message = message
        Thread.__init__(self)
    def run(self):
        if base.settings.Settings().get("discord_token") is None:
            return
        self.message = self.message.replace("'", "'\\''") # yes shell quote escape is madness
        requests.post("https://discordapp.com/api/webhooks/" + base.settings.Settings().get("discord_token"), data={"content": self.message})
        # requests.post("https://discordapp.com/api/webhooks/" + \
        # base.settings.Settings().get("discord_token"), data={"content": self.message})
