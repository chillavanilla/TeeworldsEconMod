#!/usr/bin/env python3

import time

def cfind(str, substr, n):
    start = str.find(substr)
    while start >= 0 and n > 1:
        start = str.find(substr, start+len(substr))
        n -= 1
    return start

def get_timestamp():
    try:
        return time.perf_counter_ns()
    except AttributeError:
        return (int)(time.time()*(1000000000))
