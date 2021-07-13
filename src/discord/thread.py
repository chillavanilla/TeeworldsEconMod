#!/usr/bin/env python3
"""The discord thread module"""

import os
from threading import Thread
import g_settings
# import requests

class SendDiscord(Thread):
    """Thread for sending discord messages non blocking"""
    def __init__(self, message):
        self.message = message
        Thread.__init__(self)
    def run(self):
        if g_settings.get("discord_token") is None:
            return
        self.message = self.message.replace("'", "'\\''") # yes shell quote escape is madness
        os.system(
            "python src/discord/webhook.py '" + \
            g_settings.get("discord_token") + \
            "' '" + self.message + "'"
            )
        # requests.post("https://discordapp.com/api/webhooks/" + \
        # g_settings.get("discord_token"), data={"content": self.message})
