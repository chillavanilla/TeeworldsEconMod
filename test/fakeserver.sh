#!/bin/bash

function log()
{
    echo "XXXXXXXXXX$1"
}
log "starting fake server..."
sleep 0.5
log "[chat]: *** 'ChillerDragon' entered and joined the red team"
sleep 0.5
log "[chat]: *** 'ChillerDragon.*' entered and joined the blue team"
sleep 0.5
log "[chat]: *** '(2)ChillerDrago' entered and joined the blue team"
sleep 0.5
log "[game]: kill killer='0:ChillerDragon' victim='3:(2)ChillerDrago' weapon=2 special=2"
log "[game]: kill killer='0:ChillerDragon' victim='3:(2)ChillerDrago' weapon=2 special=2"
log "[game]: kill killer='0:ChillerDragon' victim='3:(2)ChillerDrago' weapon=3 special=2"
sleep 0.5
log "[game]: kill killer='0:ChillerDragon' victim='3:(2)ChillerDrago' weapon=3 special=2"
log "[game]: kill killer='0:ChillerDragon' victim='3:(2)ChillerDrago' weapon=3 special=2"
log "[game]: kill killer='0:ChillerDragon' victim='3:(2)ChillerDrago' weapon=4 special=2"
sleep 2
