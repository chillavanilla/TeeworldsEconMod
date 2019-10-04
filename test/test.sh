#!/bin/bash

delay=0

verbose=0
logs_path=logs
settings_path=settings

RESET="\033[0m"
BOLD="\033[1m"

function set_paths() {
    if [ $# -gt 0 ]
    then
        if [ ! -d "$1" ]
        then
            echo "Error logs path not found '$1'"
            exit 1
        fi
        logs_path="$1"
        echo "using custom logs path: $1"
    fi
    if [ $# -gt 1 ]
    then
        if [ ! -d "$2" ]
        then
            echo "Error settings path not found '$2'"
            exit 1
        fi
        settings_path="$2"
        echo "using custom settings path: $2"
    fi
}

if [ "$1" == "--help" ] || [ "$1" == "-h" ]
then
    echo    "usage: $0 [OPTION] [LOG_DIR] [SETTINGS_DIR]"
    echo    "  arguments:"
    echo -e "    OPTION       - ${BOLD}-h${RESET} show this help page."
    echo -e "                   ${BOLD}-v${RESET} verbose output."
    echo -e "                   ${BOLD}--help${RESET} equivalent to ${BOLD}-h${RESET}"
    echo -e "                   ${BOLD}--verbose${RESET} equivalent to ${BOLD}-v${RESET}"
    echo    "    LOG DIR      - path to directory containing tw .log files"
    echo    "                   default: logs"
    echo    "    SETTINGS DIR - path to directory containing tem .test files"
    echo    "                   default: settings"
    echo    "  description:"
    echo    "    pipes all logs-settings combinations into tem python script."
    exit
elif [ "$1" == "--verbose" ] || [ "$1" == "-v" ]
then
    verbose=1
    set_paths $2 $3
else
    set_paths $1 $2
fi

function print_log_lines() {
    while IFS= read -r line
    do
        echo "$line"
        if [[ ! $line =~ '[datafile]'|'[register]'|'[engine/mastersrv]'|'[storage]'|'[econ]'|'[engine]' ]]
        then
            if [ "$delay" == "1" ]
            then
                sleep 0.1
            fi
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
    log_lines=$(print_log_lines $log | ../src/main.py --settings=$setting)
    show_lines=$verbose
    if [ $? -eq 0 ]
    then
        printf "[\033[0;32mSUCCESS\033[0m]\n"
        passed=$((passed+1))
    else
        printf "[\033[0;31mFAILED\033[0m]\n"
        failed=$((failed+1))
        show_lines=1
    fi
    if [ "$show_lines" == "1" ]
    then
        echo " === setting: $setting === "
        cat $setting
        echo " ================ "
        echo "$log_lines"
    fi
    total=$((total+1))
}

start_ts=`date +%s.%N`

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

echo ""
printf "Total runtime: %d:%02d:%02d:%02.4f\n" $dd $dh $dm $ds
printf "failed: \033[0;31m$failed/$total\033[0m\n"
printf "passed: \033[0;32m$passed/$total\033[0m\n"

if [ $failed -gt 0 ]
then
    exit 1
fi
