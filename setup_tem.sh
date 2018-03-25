#!/bin/bash
echo "====================="
echo " Teeworlds Econ Mod  "
echo " by ChillerDragon    "
echo "====================="

if [ ! -f passwords.passwd ]; then
    echo "error passwords.passwd file not found"
    exit
fi

echo "found passwords file."

echo "connecting to server via econ"

./nc.exp `cat passwords.passwd`
