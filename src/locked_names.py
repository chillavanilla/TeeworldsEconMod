#!/usr/bin/env python3

import json
import ipinfo
import os.path

import chat
import g_settings
import player
import parse_settings

locked_names_instance = None

class LockedNames:
    def __init__(self):
        if not g_settings.get("ipinfo_token") or g_settings.get("ipinfo_token") == "":
            return
        self.ip_handler = ipinfo.getHandler(g_settings.get("ipinfo_token"))

    def write(self, names):
        file = open("locked_names.json", "w")
        file.write(json.dumps(names, sort_keys=True, indent=4) + "\n")
        file.close()

    def read(self):
        if not os.path.isfile('locked_names.json'):
            return None
        file = open("locked_names.json", "r")
        names = file.read()
        file.close()
        return json.loads(names)

    def list_names(self):
        entrys = self.read()
        if not entrys:
            chat.echo("There are no locked names.")
            return
        for entry in entrys:
            chat.echo("name='" + str(entry["name"]) + "' region='" + str(entry["region"]) + "'")

    def check(self, name, ip):
        if not g_settings.get("ipinfo_token") or g_settings.get("ipinfo_token") == "":
            return True
        for entry in self.read():
            if entry["name"] != name:
                continue
            data = self.ip_handler.getDetails(ip)
            if not hasattr(data, "region"):
                return True
            region = data.region
            if region != entry["region"]:
                chat.echo("[locked-names] region missmatch '" + str(region) + "' != '" + str(entry["region"]) + "'")
                return False
            return True
        return True

def GetInstance():
    global locked_names_instance
    if not locked_names_instance:
        locked_names_instance = LockedNames()
    return locked_names_instance
