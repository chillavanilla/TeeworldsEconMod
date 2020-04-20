#!/bin/bash
# discord_bot.sh
# a helper/launcher for the bot.py discord bot
# has to be executed from the tool/ directory
# ./discord_bot.sh

# init variables
settings_file="../tem.settings"
name="nameless"
aSettStr=();aSettVal=()
aSettStr+=("sh_logs_path");aSettVal+=("/path/to/log/directory")
aSettStr+=("sh_discord_token_verbose");aSettVal+=("")
aSettStr+=("py_discord_token");aSettVal+=("")
aSettStr+=("sh_tw_path");aSettVal+=("/path/to/your/teeworlds/directory")
aSettStr+=("sh_tw_binary");aSettVal+=("name_of_teeworlds_srv")
aSettStr+=("sh_econ_password");aSettVal+=("password")
aSettStr+=("sh_econ_port");aSettVal+=("8203")
aSettStr+=("sh_tw_cfg_file");aSettVal+=("")
aSettStr+=("sh_tw_version");aSettVal+=("0.6")

function kill_bot() {
    pkill -f " --universal-id=tem-bot"
}
function log() {
    echo "$1"
}

if [ "$1" == "--help" ]
then
    echo "usage: $0 [<bot_name>] [<settings_file>]"
    exit 0
elif [ "$1" == "--kill" ] || [ "$1" == "--stop" ]
then
    kill_bot
fi
if ! [ -x "$(command -v openssl)" ]; then
  echo 'Error: openssl is not installed.' >&2
  exit 1
fi

if [ $# -gt 0 ]; then
    log "name=$1"
    name=$1
fi
if [ $# -gt 1 ]; then
    log "settings file=$2"
    settings_file=$2
fi

# TODO: remove duplicates from start_tem.sh
# and move them to a lib.sh
function parse_settings_line() {
        local sett=$1
        local val=$2
        local i
        for i in "${!aSettStr[@]}"
        do
            if  [ "$sett" == "${aSettStr[$i]}" ]
            then
                printf "[TEM:setting] (%s)%-16s=  %s\n" "$i" "${sett:3}" "$val"
                aSettVal[$i]="$val"
                return
            fi
        done
        log "SettingsError: unkown setting $sett"
        exit 1
}

function read_settings_file() {
    local i
    while read line
    do
        if [ "${line:0:1}" == "#" ]
        then
            continue # ignore comments
        # TODO: make this less ugly
        elif [[ "${line:0:3}" == "py_" ]] && [[ ! $line =~ ^py_discord_token ]]
        then
            continue # ignore python settings
        elif [ -z "$line" ]
        then
            continue # ignore empty lines
        fi
        line_set=""
        line_val=""
        IFS='=' read -ra split_line <<< "$line"
        for i in "${!split_line[@]}"
        do
            # split by '=' and then join all the elements bigger than 0
            # thus we allow using '=' inside the value
            if [ "$i" == "0" ]
            then
                line_set="${split_line[$i]}"
            else
                if [ $i -gt 1 ]
                then
                    line_val+="="
                fi
                line_val+="${split_line[$i]}"
            fi
        done
        # echo "config: $line_set value: $line_val"
        parse_settings_line $line_set $line_val
    done < $settings_file
}

id="invalid-tem-bot"
function start_bot() {
    id=$(openssl rand -base64 32)
    echo "[+] starting bot.py logfile=$logfile id=$id"
    $(tail -fn1 $log | PYTHONIOENCODING="UTF-8" ./bot.py $token $name --id=$id --universal-id=tem-bot) &
}

function stop_bot() {
    echo "[-] stopping bot.py with id=$id"
    pkill -f $id
}

read_settings_file

logpath="${aSettVal[0]}"
token="${aSettVal[1]}"

if [[ ${logpath:0:1} != "/" ]] && [[ ! -d $logpath ]]
then
    echo "Invalid logpath '$logpath'"
    dumpspath=$HOME/.teeworlds/dumps/$logpath
    if [ -d $dumpspath ]
    then
        logpath=$dumpspath
        echo "Using dumps path: $logpath"
    else
        exit 1
    fi
fi

echo "token=${token:0:10}..."
echo "logpath=$logpath"
echo "name=$name"
cd ../src/discord/

while [ true ]
do
    logfile=`ls $logpath | tail -1`
    latest_log="$logpath$logfile"
    if [ "$log" != "$latest_log" ]
    then
        echo "logs differ old=$log new=$latest_log"
        echo "restaring bot..."
        log=$latest_log
        stop_bot
        start_bot
    fi
    sleep 3
done

