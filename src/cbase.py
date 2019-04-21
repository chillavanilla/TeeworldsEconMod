#!/usr/bin/env python3.7

def cfind(str, substr, n):
    start = str.find(substr)
    while start >= 0 and n > 1:
        start = str.find(substr, start+len(substr))
        n -= 1
    return start
