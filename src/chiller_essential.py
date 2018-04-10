#!/usr/bin/env python3
import sys

def say(str):
    sys.stdout.write("say " + str + "\n")
    sys.stdout.flush()

def broadcast(str):
    sys.stdout.write("broadcast " + str + "\n")
    sys.stdout.flush()

def echo(str):
    sys.stdout.write("echo " + str + "\n")
    sys.stdout.flush()

