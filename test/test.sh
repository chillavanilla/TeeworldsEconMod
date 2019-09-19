#!/bin/bash

function print_log_lines() {
    while IFS= read -r line
    do
        echo "$line"
        sleep 0.1
    done < $1
}

for log in $(ls logs/*)
do
    echo   "+---------------------------------------+"
    printf "| log: %-32s |\n" $log
    echo   "+---------------------------------------+"
    print_log_lines $log | ../src/main.py --settings=../tem.settings
done

