#!/bin/bash
# Only supports latest 0.7 servers
# because it looks in ~/.teeworlds/dumps
# for the logs
#
# WARNING:
# do not run twice!
# only works once because then the server is running inside this script
# and has to be restarted manually
shopt -s extglob # used for trailing slashes globbing

is_debug=0
if [[ "$2" == "-v" ]] || [[ "$2" == "--verbose" ]]
then
    is_debug=1
fi

if [ "$#" -lt "1" ]
then
    echo "Usage: $0 <tem settings>"
    exit 1
fi

function dbg() {
    if [ "$is_debug" -ne "1" ]
    then
        return 1
    fi
    echo "[debug] $1"
}

procs=$(pgrep -fc restart_empty.sh)
procs=$((procs))
echo "procs: $procs"
if [ $procs -gt 1 ]
then
    ps aux | grep restart_empty.sh | grep -v grep
    echo "Error: $procs restart_empty.sh instances running already."
    exit 1
fi

twdumps=~/.teeworlds/dumps
temsettings=$1

if [ ! -f start_tem.sh ]
then
    echo "Error: start_tem.sh not found!"
    echo "       make sure to execute this script from tem root"
    echo "       ./tools/restart_empty.sh"
    exit 1
fi
if [ ! -d $twdumps ]
then
    echo "Error: teeworlds dumps path not found."
    echo "       Make sure to use latest teeworlds 0.7 server."
    exit 1
fi
if [ ! -f "$temsettings" ]
then
    echo "Error: settings file not found."
    exit 1
fi

# TODO: exit with error when log path starts with /
logpath=$(grep -o '^[^#]*' "$temsettings" | grep '^sh_logs_path=' | cut -d '=' -f2)
logpath="$twdumps/$logpath"
logpath="${logpath%%+(/)}" # strip trailing slash
logpath=$(echo "$logpath" | xargs) # strip trailing spaces
logfile=$(ls $logpath | sort | tail -n1)
echo "Found logpath: $logpath"
echo "Latest log: $logfile"
logfile="$logpath/$logfile"

if [ ! -f "$logfile" ]
then
    echo "Full log path: $logfile"
    echo "Error: logfile does not exist."
    exit 1
fi

function try_restart() {
    ready=$(grep -cP '^\[.{19}]\[server\]: player is ready. ClientID=' "$logfile")
    drop=$(grep -cP '^\[.{19}]\[server\]: client dropped. cid=' "$logfile")
    total=$((ready - drop))

    dbg "ready=$ready dropped=$drop"
    dbg "totoal=$total"

    if [ "$total" -eq "0" ]
    then
        echo "Server is empty -> RESTARTING ..."
        echo "stopping..."
        pkill -f "./start_tem.sh $temsettings"
        pkill -f "settings=$temsettings"
        echo "starting..."
        ./start_tem.sh "$temsettings"
        exit 0 # do not keep restarting when server crashed
    else
        printf "Restart failed players=%s " "$total"
    fi
}

function sleep_s() {
    t=$1
    for ((i=0;i<t;i++))
    do
        printf '.'
        sleep 1
    done
    echo ""
}

while true;
do
    try_restart
    sleep_s 5
done

