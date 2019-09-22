#!/bin/bash

if [ "$1" == "--help" ] || [ "$1" == "-h" ]
then
    echo "usage: $0 [ log directory ] [ settings directory ]"
    echo "  options:"
    echo "    log dir      - path to directory containing tw .log files"
    echo "                   default: logs"
    echo "    settings dir - path to directory containing tem .test files"
    echo "                   default: settings"
    echo "  description:"
    echo "    pipes all logs-settings combinations into tem python script."
    exit
fi

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

mkdir -p stats

function test_log() {
    log=$1
    setting=$2
    echo   "+---------------------------------------+"
    printf "| log: %-32s |\n" $log
    echo   "+---------------------------------------+"
    echo " === setting: $setting === "
    cat $setting
    echo " ================ "
    print_log_lines $log | ../src/main.py --settings=$setting
    if [ $? -eq 0 ]
    then
        printf "[\033[0;32mSUCCESS\033[0m]\n"
        passed=$((passed+1))
    else
        printf "[\033[0;31mFAILED\033[0m]\n"
        failed=$((failed+1))
    fi
    total=$((total+1))
}

logs_path=logs
settings_path=settings
if [ $# -gt 0 ]
then
    if [ ! -d "$1" ]
    then
        echo "Errro logs path not found '$1'"
        exit 1
    fi
    logs_path="$1"
fi
if [ $# -gt 1 ]
then
    if [ ! -d "$2" ]
    then
        echo "Errro settings path not found '$2'"
        exit 1
    fi
    settings_path="$2"
fi

for log in $(ls $logs_path/*.log)
do
    for setting in $(ls $settings_path/*.test)
    do
        test_log $log $setting
    done
done

echo " --------------------------------------- "
echo ""
printf "failed: \033[0;31m$failed/$total\033[0m\n"
printf "passed: \033[0;32m$passed/$total\033[0m\n"

if [ $failed -gt 0 ]
then
    exit 1
fi
