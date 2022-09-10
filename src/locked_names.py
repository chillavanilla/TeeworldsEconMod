#!/usr/bin/env python3
"""Locked names module ban based on ip region"""

import json
import os.path
import ipinfo
from confusables import is_confusable

import base.settings
from base.rcon import echo

LOCKED_NAMES_INSTANCE = None

class LockedNames:
    """Locked names class"""
    def __init__(self):
        self.settings = base.settings.Settings()
        if not self.settings.get("ipinfo_token") or self.settings.get("ipinfo_token") == "":
            return
        self.ip_handler = ipinfo.getHandler(self.settings.get("ipinfo_token"))

    @staticmethod
    def write(names):
        """Write names to json"""
        with open("locked_names.json", "w", encoding='UTF-8') as file:
            file.write(json.dumps(names, sort_keys=True, indent=4) + "\n")
            file.close()

    @staticmethod
    def read():
        """Read locked names from json"""
        if not os.path.isfile('locked_names.json'):
            return None
        with open("locked_names.json", "r", encoding='UTF-8') as file:
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
            str_names = 'missing field "names"'
            str_regions = ''
            str_ips = ''
            if hasattr(entry, 'names'):
                str_names = "names='" + str(entry["names"]) + "'"
            if hasattr(entry, 'regions'):
                str_regions = " regions='" + str(entry["regions"]) + "'"
            if hasattr(entry, 'ips'):
                str_ips = " ips='" + str(entry["ips"]) + "'"
            echo(str_names + str_regions + str_ips)

    @staticmethod
    def strip_null_chars(string: str):
        """Given a string returns a version with all the invisble unicodes removed"""
        for confusable in (
            '\u200b',
            '\u200c',
            '\u200d',
            '\u200e',
            '\u200f',
            '\u2060',
            '\u2061',
            '\u2062',
            '\u2063',
            '\u2064',
            '\u2065',
            '\u2066',
            '\u2067',
            '\u2068',
            '\u2069',
            '\u206a',
            '\u206b',
            '\u206c',
            '\u206d',
            '\u206e',
            '\u206f'):
            string = string.replace(confusable, "")
        return string

    def check(self, name: str, ip_addr: str) -> bool:
        """
        Check if a given name is using a forbidden ip address

        Returns True if check passed (name is allowed with this ip)
        """
        if not self.settings.get("ipinfo_token") or self.settings.get("ipinfo_token") == "":
            return True
        entrys = self.read()
        if not entrys:
            return True
        for entry in entrys:
            for entry_name in entry['names']:
                if not is_confusable(self.strip_null_chars(name), entry_name):
                    continue
                if hasattr(entry, "ips"):
                    for entry_ip in entry['ips']:
                        if entry_ip == ip_addr:
                            return True
                    # if ips is specified but regions not
                    # one of the ips has to match
                    if not hasattr(entry, "regions"):
                        return False
                data = self.ip_handler.getDetails(ip_addr)
                if not hasattr(data, "region"):
                    return True
                region = data.region
                if not region in entry['regions']:
                    echo(
                        "[locked-names] region missmatch '" + \
                        str(region) + "' not included in '" + str(entry['regions']) + "'"
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
