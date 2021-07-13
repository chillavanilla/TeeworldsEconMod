#!/usr/bin/env python3
"""Locked names module ban based on ip region"""

import json
import os.path
import ipinfo

import g_settings
from base.rcon import echo

LOCKED_NAMES_INSTANCE = None

class LockedNames:
    """Locked names class"""
    def __init__(self):
        if not g_settings.get("ipinfo_token") or g_settings.get("ipinfo_token") == "":
            return
        self.ip_handler = ipinfo.getHandler(g_settings.get("ipinfo_token"))

    @staticmethod
    def write(names):
        """Write names to json"""
        with open("locked_names.json", "w") as file:
            file.write(json.dumps(names, sort_keys=True, indent=4) + "\n")
            file.close()

    @staticmethod
    def read():
        """Read locked names from json"""
        if not os.path.isfile('locked_names.json'):
            return None
        with open("locked_names.json", "r") as file:
            names = file.read()
            file.close()
            return json.loads(names)

    def list_names(self):
        """List all locked names in rcon console"""
        entrys = self.read()
        if not entrys:
            echo("There are no locked names.")
            return
        for entry in entrys:
            echo("name='" + str(entry["name"]) + "' region='" + str(entry["region"]) + "'")

    def check(self, name, ip_addr):
        """Check if a given name is using a forbidden ip address"""
        if not g_settings.get("ipinfo_token") or g_settings.get("ipinfo_token") == "":
            return True
        for entry in self.read():
            if entry["name"] != name:
                continue
            data = self.ip_handler.getDetails(ip_addr)
            if not hasattr(data, "region"):
                return True
            region = data.region
            if region != entry["region"]:
                echo(
                    "[locked-names] region missmatch '" + \
                    str(region) + "' != '" + str(entry["region"]) + "'"
                    )
                return False
            return True
        return True

def get_instance(force = False):
    """Return global locked names instance if none create one"""
    global LOCKED_NAMES_INSTANCE
    if not LOCKED_NAMES_INSTANCE or force:
        LOCKED_NAMES_INSTANCE = LockedNames()
    return LOCKED_NAMES_INSTANCE
