#!/bin/bash

function print_log_lines() {
    while IFS= read -r line
    do
        echo "$line"
        sleep 0.1
    done < $1
}

failed=0
passed=0
total=0

for log in $(ls logs/*)
do
    echo   "+---------------------------------------+"
    printf "| log: %-32s |\n" $log
    echo   "+---------------------------------------+"
    echo " === settings === "
    cat ../tem.settings
    echo " ================ "
    print_log_lines $log | ../src/main.py --settings=../tem.settings
    if [ $? -eq 0 ]
    then
        printf "[\033[0;32mSUCCESS\033[0m]\n"
        passed=$((passed+1))
    else
        printf "[\033[0;31mFAILED\033[0m]\n"
        failed=$((failed+1))
    fi
    total=$((total+1))
done

echo " --------------------------------------- "
echo ""
printf "failed: \033[0;31m$failed/$total\033[0m\n"
printf "passed: \033[0;32m$passed/$total\033[0m\n"

if [ $failed -gt 0 ]
then
    exit 1
fi
