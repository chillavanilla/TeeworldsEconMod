#!/bin/bash
# this script adds a new line to all statsfiles
# only use this script if you know what you are doing
# it is needed to update statsfiles on a new update where a new value gets added

for file in stats/*.acc; do echo "0" >> "$file"; done
