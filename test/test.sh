#!/bin/bash
./fakeserver.sh | ../src/main.py --debug true --stats sql
