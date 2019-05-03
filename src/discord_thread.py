#!/usr/bin/env python3.7

import g_settings
import requests
from threading import Thread

class send_discord(Thread):
    def __init__(self, message):
        self.message = message
        Thread.__init__(self)
    def run(self):
        if g_settings.get("discord_token") != None:
            requests.post("https://discordapp.com/api/webhooks/" + g_settings.get("discord_token"), data={"content": self.message})
