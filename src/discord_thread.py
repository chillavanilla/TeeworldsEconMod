#!/usr/bin/env python3

import g_settings
import os
from threading import Thread
# import requests

class send_discord(Thread):
    def __init__(self, message):
        self.message = message
        Thread.__init__(self)
    def run(self):
        if g_settings.get("discord_token") != None:
            self.message = self.message.replace("'", "'\\''") # yes shell quote escape is madness
            os.system("python src/discord/webhook.py '" + g_settings.get("discord_token") + "' '" + self.message + "'")
            # requests.post("https://discordapp.com/api/webhooks/" + g_settings.get("discord_token"), data={"content": self.message})
