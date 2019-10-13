#!/usr/bin/env python3

# this bot takes a discord webhook token as argument
# and then posts stdin to the webhook
# can be used to pipe the tail -f of the teeworlds log into discord
# example:
# tail -fn1 logs/tee.log | PYTHONIOENCODING="UTF-8" ./bot.py 583224417517094692/8YBS_8Ft3naXarmLnMTxtAq5LfNvyZrYG7aZjLnGyy9ZNwhIlM0niR2n_rfRLUn5a8CA

import sys
import requests
import time

token=""

def HandleData(line):
    global token
    line = str(line)
    chat_str = "][chat]: "
    if (line.find(chat_str) == -1):
        return
    line_start = line.find(chat_str) + len(chat_str)
    line = line[line_start:]
    print("line: " + line)
    requests.post("https://discordapp.com/api/webhooks/" + token, data={"content": line})

def main():
    global token
    if (len(sys.argv) != 2):
        print("usage: ./bot.py <discordtoken>")
        sys.exit(1)
    token=sys.argv[1]
    try:
        while True:
            line = sys.stdin.readline()
            if not line:
                break
            line = line[:-1] # cut timestamp and newline at the end
            HandleData(line)
    except EOFError:
        pass    # the telnet/netcat process finished; there's no more input
    except UnicodeEncodeError:
        print("[WARNING] UnicodeEncodeError! Please contact an admin.")
        pass

if __name__ == "__main__":
    main()
