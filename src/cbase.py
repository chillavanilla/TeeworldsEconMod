#!/usr/bin/env python3

import time

def cfind(haystack, needle, offset):
    """Return character index of needle found in haystack at offset"""
    start = haystack.find(needle)
    while start >= 0 and offset > 1:
        start = haystack.find(needle, start+len(needle))
        offset -= 1
    return start

def get_timestamp():
    """Return current timestamp"""
    try:
        return time.perf_counter_ns()
    except AttributeError:
        return (int)(time.time()*(1000000000))
