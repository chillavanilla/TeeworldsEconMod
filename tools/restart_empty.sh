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
is_ping=0
mode="Restart"
if [[ "$2" == "-v" ]] || [[ "$2" == "--verbose" ]]
then
    is_debug=1
elif [[ "$2" == "-p" ]] || [[ "$2" == "--ping" ]]
then
    is_ping=1
    mode="Ping"
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

function sleep_m() {
    t=$1
    for ((i=0;i<t;i++))
    do
        printf '.'
        sleep 1m
    done
    echo ""
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
discord_token=$(grep -o '^[^#]*' "$temsettings" | grep '^py_discord_token=' | tail -n1 | cut -d '=' -f2)
logpath=$(grep -o '^[^#]*' "$temsettings" | grep '^sh_logs_path=' | tail -n1 | cut -d '=' -f2)
logpath="$twdumps/$logpath"
logpath="${logpath%%+(/)}" # strip trailing slash
logpath=$(echo "$logpath" | xargs) # strip trailing spaces
logfile=$(ls $logpath | sort | tail -n1)
echo "Found logpath: $logpath"
echo "Latest log: $logfile"
logfile="$logpath/$logfile"

if [ "$is_ping" == "1" ]
then
    if [ "$discord_token" == "" ]
    then
        echo "Error: no py_discord_token found in settings."
        exit 1
    fi
fi
if [ ! -f "$logfile" ]
then
    echo "Full log path: $logfile"
    echo "Error: logfile does not exist."
    exit 1
fi

function ping_discord() {
    url="https://discordapp.com/api/webhooks/$discord_token"
    echo "url: $url"
    curl -H "Content-Type: application/json" \
    -X POST \
    -d '{"username": "SERVER-STATUS", "content": "Server is empty <@173505964433997824>! connected='"$1"' dropped='"$2"'"}' $url
}

function restart_srv() {
    echo "Server is empty -> RESTARTING ..."
    echo "stopping..."
    pkill -f "./start_tem.sh $temsettings"
    pkill -f "settings=$temsettings"
    echo "starting..."
    ./start_tem.sh "$temsettings"
}

function check_empty() {
    ready=$(grep -cP '^\[.{19}]\[server\]: player is ready. ClientID=' "$logfile")
    drop=$(grep -cP '^\[.{19}]\[server\]: client dropped. cid=' "$logfile")
    total=$((ready - drop))

    dbg "ready=$ready dropped=$drop"
    dbg "totoal=$total"

    if [ "$total" -eq "0" ]
    then
        if [ "$is_ping" == "1" ]; then
            ping_discord "$ready" "$drop"
        else
            restart_srv
        fi
        exit 0 # do not keep restarting on crash or pinging
    else
        printf "%s failed players=%s " "$mode" "$total"
    fi
}

while true;
do
    check_empty
    sleep_m 20
done

