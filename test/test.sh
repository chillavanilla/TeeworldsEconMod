#!/bin/bash
echo "testing teeworlds 0.6"
./fakeserver6.sh | ../src/main.py --settings=../tem.settings
echo "testing teeworlds 0.7"
./fakeserver7.sh | ../src/main.py --settings=../tem.settings
