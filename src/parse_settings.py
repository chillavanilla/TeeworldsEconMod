#!/usr/bin/env python3
"""Module for parsing tem setting files"""

from base.rcon import echo
import base.settings

class TemParseError(Exception):
    """Tem Parser Exception"""
    def __init__(self, value):
        Exception.__init__(self)
        self.value = value
    def __str__(self):
        return repr(self.value)

def parse_error(err_type, err_msg):
    """Throw parser error"""
    echo("[ERROR:settings] " + str(err_type) + ": " + str(err_msg))
    raise TemParseError(err_type + ": " + err_msg)

def parse_bool(val, line_num):
    """Parse boolean"""
    val = val.lower()
    if val in ("0", "false"):
        return False
    if val in ("1", "true"):
        return True
    parse_error("BoolError", "cannot parse bool " + str(line_num) + ":'" + str(val) + "'")
    return False

def parse_list_dyn(val):
    """Parse dynamic list type"""
    if val is None or val == "" or val == ",":
        return None
    return val.split(',')

def parse_list(sett, val, line_num):
    """Parse list type"""
    raw_list = base.settings.Settings().settings_dict[sett][0]
    raw_list = raw_list[1:-1]
    list_vals = raw_list.split(',')
    if val in list_vals:
        return str(val)
    parse_error("ListError", str(line_num) + ":'" + str(val) + "' not in list " + str(list_vals))
    return ""

def read_settings_line(line, line_num):
    """Parse single line of tem settings file"""
    split = line.find("=")
    sett = line[3:split]
    val = line[split+1:].strip()
    settings = base.settings.Settings()
    if sett not in settings.settings_dict:
        parse_error(
            "UnkownSetting",
            "line[" + str(line_num) + "] setting[" + str(sett) + "] value[" + str(val) + "]")

    # make sure file_database is a folder
    if sett == "file_database":
        if val[-1] != "/":
            val += "/"

    if settings.settings_dict[sett][0] == "str":
        settings.settings_dict[sett][1] = str(val)
    elif settings.settings_dict[sett][0] == "int":
        settings.settings_dict[sett][1] = int(val)
    elif settings.settings_dict[sett][0] == "bool":
        settings.settings_dict[sett][1] = parse_bool(val, line_num)
    elif settings.settings_dict[sett][0][0] == "[":
        if settings.settings_dict[sett][0][1] == "]": # empty list ( no limit )
            settings.settings_dict[sett][1] = parse_list_dyn(val)
        else: # pre defined allowed values in list
            settings.settings_dict[sett][1] = parse_list(sett, val, line_num)
    else:
        parse_error(
            "TypeError",
            "invalid type " + str(line_num) + ":'" + str(settings.settings_dict[sett][0]) + "'")

def read_settings_file(file):
    """Parse settings file given a filepath"""
    line_num = 0
    with open(file) as file_io:
        for line in file_io:
            line_num += 1
            if line[0] == "#":
                continue # ignore comments
            if line[:3] == "sh_":
                continue # ignore shell settings
            if not line.strip():
                continue # ignore empty lines
            read_settings_line(line, line_num)
