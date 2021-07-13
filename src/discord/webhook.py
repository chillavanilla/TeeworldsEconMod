#!/usr/bin/env python
"""discord webhook request"""

import sys
import requests

if len(sys.argv) != 3:
    print("usage: " + str(sys.argv[0]) + " <token> <message>")
    sys.exit(2)

token = sys.argv[1]
message = sys.argv[2]
requests.post("https://discordapp.com/api/webhooks/" + token, data={"content": message})
