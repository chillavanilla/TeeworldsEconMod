#!/bin/bash

start_ts=`date +%s.%N`

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
        if [[ ! $line =~ '[datafile]'|'[register]'|'[engine/mastersrv]'|'[storage]'|'[econ]'|'[engine]' ]]
        then
            sleep 0.1
        fi
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

# timestamp credits go to jwchew
# https://unix.stackexchange.com/a/88802
end_ts=`date +%s.%N`

dt=$(echo "$end_ts - $start_ts" | bc)
dd=$(echo "$dt/86400" | bc)
dt2=$(echo "$dt-86400*$dd" | bc)
dh=$(echo "$dt2/3600" | bc)
dt3=$(echo "$dt2-3600*$dh" | bc)
dm=$(echo "$dt3/60" | bc)
ds=$(echo "$dt3-60*$dm" | bc)


echo " --------------------------------------- "
echo ""
printf "Total runtime: %d:%02d:%02d:%02.4f\n" $dd $dh $dm $ds
printf "failed: \033[0;31m$failed/$total\033[0m\n"
printf "passed: \033[0;32m$passed/$total\033[0m\n"

if [ $failed -gt 0 ]
then
    exit 1
fi
