#!/usr/bin/env python3.7

import g_settings
import sys

def parse_bool(sett, val):
        val = val.lower()
        if val == "0" or val == "false":
            return False
        elif val == "1" or val == "true":
            return True
        else:
            print("[ERROR] settings type error cannot parse bool '" + str(g_settings.SETTINGS[sett][1]) + "'")
            sys.exit(2)

def parse_list(sett, val):
    raw_list = g_settings.SETTINGS[sett][0]
    raw_list = raw_list[1:-1]
    list_vals = raw_list.split(',')
    if val in list_vals:
        return str(val)
    print("[ERROR] settings type '" + str(val) + "' not in list " + str(list_vals))
    sys.exit(2)

def ReadSettingsLine(line):
    s = line.find("=")
    sett = line[3:s]
    val = line[s+1:].strip()
    if sett not in g_settings.SETTINGS:
        print("[ERROR] unknown setting setting[" + str(sett) + "] value[" + str(val) + "]")
        sys.exit(2)

    if g_settings.SETTINGS[sett][0] == "str":
        g_settings.SETTINGS[sett][1] = str(val)
    elif g_settings.SETTINGS[sett][0] == "int":
        g_settings.SETTINGS[sett][1] = int(val)
    elif g_settings.SETTINGS[sett][0] == "bool":
        g_settings.SETTINGS[sett][1] = parse_bool(sett, val)
    elif g_settings.SETTINGS[sett][0][0] == "[":
        g_settings.SETTINGS[sett][1] = parse_list(sett, val)
    else:
        print("[ERROR] settings type error invalid type '" + str(g_settings.SETTINGS[sett][0]) + "'")
        sys.exit(2)

def ReadSettingsFile(file):
    with open(file) as f:
        for line in f:
            if line[0] == "#":
                continue # ignore comments
            elif line[:3] == "sh_":
                continue # ignore shell settings
            ReadSettingsLine(line)
