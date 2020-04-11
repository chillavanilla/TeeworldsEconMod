#!/usr/bin/env python3

from chiller_essential import *
import g_settings

class TemParseError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

def parse_error(err_type, err_msg):
    echo("[ERROR:settings] " + str(err_type) + ": " + str(err_msg))
    raise TemParseError(err_type + ": " + err_msg)

def parse_bool(sett, val, line_num):
        val = val.lower()
        if val == "0" or val == "false":
            return False
        elif val == "1" or val == "true":
            return True
        else:
            parse_error("BoolError", "cannot parse bool " + str(line_num) + ":'" + str(val) + "'")

def parse_list_dyn(sett, val, line_num):
    if val == None or val == "" or val == ",":
        return None
    return val.split(',')

def parse_list(sett, val, line_num):
    raw_list = g_settings.SETTINGS[sett][0]
    raw_list = raw_list[1:-1]
    list_vals = raw_list.split(',')
    if val in list_vals:
        return str(val)
    parse_error("ListError", str(line_num) + ":'" + str(val) + "' not in list " + str(list_vals))

def ReadSettingsLine(line, line_num):
    s = line.find("=")
    sett = line[3:s]
    val = line[s+1:].strip()
    if sett not in g_settings.SETTINGS:
        parse_error("UnkownSetting", "line[" + str(line_num) + "] setting[" + str(sett) + "] value[" + str(val) + "]")

    # make sure file_database is a folder
    if sett == "file_database":
        if val[-1] != "/":
            val += "/"

    if g_settings.SETTINGS[sett][0] == "str":
        g_settings.SETTINGS[sett][1] = str(val)
    elif g_settings.SETTINGS[sett][0] == "int":
        g_settings.SETTINGS[sett][1] = int(val)
    elif g_settings.SETTINGS[sett][0] == "bool":
        g_settings.SETTINGS[sett][1] = parse_bool(sett, val, line_num)
    elif g_settings.SETTINGS[sett][0][0] == "[":
        if g_settings.SETTINGS[sett][0][1] == "]": # empty list ( no limit )
            g_settings.SETTINGS[sett][1] = parse_list_dyn(sett, val, line_num)
        else: # pre defined allowed values in list
            g_settings.SETTINGS[sett][1] = parse_list(sett, val, line_num)
    else:
        parse_error("TypeError", "invalid type " + str(line_num) + ":'" + str(g_settings.SETTINGS[sett][0]) + "'")

def ReadSettingsFile(file):
    line_num = 0
    with open(file) as f:
        for line in f:
            line_num += 1
            if line[0] == "#":
                continue # ignore comments
            elif line[:3] == "sh_":
                continue # ignore shell settings
            elif not line.strip():
                continue # ignore empty lines
            ReadSettingsLine(line, line_num)
