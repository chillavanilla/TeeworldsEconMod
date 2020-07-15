#!/usr/bin/env bash
shopt -s extglob # used for trailing slashes globbing
echo "========================"
echo "|| Teeworlds Econ Mod ||"
echo "|| by ChillerDragon   ||"
echo "========================"

function log() {
    echo "[TEM] $1"
}

function err() {
    echo "[TEM:ERROR] $1"
}

# check dependencys
command -v expect >/dev/null 2>&1 || {
    echo >&2 "Error: expect is not found please install it!";
    if [ "$(uname)" == "Darwin" ]; then
        echo >&2 "MacOS: brew install expect";
    elif [ -x "$(command -v apt)" ]; then
        echo >&2 "Debian/Ubuntu: sudo apt install expect";
    fi
    exit 1;
}
command -v nc >/dev/null 2>&1 || {
    echo >&2 "Error: netcat is not found please install it!";
    if [ "$(uname)" == "Darwin" ]; then
        echo >&2 "MacOS: brew install netcat";
    elif [ -x "$(command -v apt)" ]; then
        echo >&2 "Debian/Ubuntu: sudo apt install netcat";
    fi
    exit 1;
}

# init variables
settings_file="tem.settings"
aSettStr=();aSettVal=()
aSettStr+=("sh_tw_path");aSettVal+=("/path/to/your/teeworlds/directory")
aSettStr+=("sh_tw_binary");aSettVal+=("name_of_teeworlds_srv")
aSettStr+=("sh_econ_password");aSettVal+=("password")
aSettStr+=("sh_econ_port");aSettVal+=("8203")
aSettStr+=("sh_logs_path");aSettVal+=("/path/to/log/directory")
aSettStr+=("sh_tw_cfg_file");aSettVal+=("")
aSettStr+=("sh_tw_version");aSettVal+=("6")
aSettStr+=("sh_discord_token_verbose");aSettVal+=("")

if [ $# -gt 0 ]; then
    log "settings file=$1"
    settings_file=$1
fi

function check_path() {
    local path=$1
    local warning=$2
    local create=$3
    if [ -d "$path" ]
    then
        return # path found nothing todo
    fi
    if [ -d "$HOME/.teeworlds/dumps/$path" ]
    then
        # https://github.com/teeworlds/teeworlds/commit/c705f048f3f62e0ed92686e19763a61309125d98
        # new logger system
        # should also support other storage.cfg locations
        # not too sure about how that actually should be supported
        # only logs are under dumps/ so hardcoding dumps/ is not good
        # TODO: improve this
        log "Warning: using path $HOME/.teeworlds/dumps/$path"
        return
    fi
    log "$warning"
    log "should be at: $path"
    if [ "$create" != "0" ]
    then
        read -p "Do you want to create the path? [y/N]" -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]
        then
            mkdir -p "$path"
            log "created folder at: $path"
            return
        fi
    fi
    log "PathError: please provide a valid path."
    exit 1
}

function create_settings() {
    if [ -f "$settings_file" ];
    then
        return
    fi
    local i
    log "FileError: '$settings_file' not found"
    read -p "Do you want to create one? [y/N]" -n 1 -r
    echo 
    if [[ $REPLY =~ ^[Yy]$ ]]
    then
        {
            echo "# TeeworldsEconMod (TEM) by ChillerDragon"
            echo "# https://github.com/chillavanilla/TeeworldsEconMod"
            for i in "${!aSettStr[@]}"
            do
                echo "${aSettStr[$i]}=${aSettVal[$i]}"
            done
        } > "$settings_file"
        nano "$settings_file"
    fi
    exit 1
}

function parse_settings_line() {
        local sett=$1
        local val=$2
        local i
        for i in "${!aSettStr[@]}"
        do
            if  [ "$sett" == "${aSettStr[$i]}" ]
            then
                printf "[TEM:setting] (%s)%-16s=  %s\\n" "$i" "${sett:3}" "$val"
                if [[ "${aSettStr[$i]}" =~ path ]]
                then
                    val="${val%%+(/)}" # strip trailing slash
                fi
                aSettVal[$i]="$val"
                return
            fi
        done
        log "SettingsError: unkown setting $sett"
        exit 1
}

function read_settings_file() {
    local i
    while read -r line
    do
        if [ "${line:0:1}" == "#" ]
        then
            continue # ignore comments
        elif [ "${line:0:3}" == "py_" ]
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
                if [ "$i" -gt "1" ]
                then
                    line_val+="="
                fi
                line_val+="${split_line[$i]}"
            fi
        done
        # echo "config: $line_set value: $line_val"
        parse_settings_line "$line_set" "$line_val"
    done < "$settings_file"
}

create_settings # create fresh if null
aSettVal[6]="" # overwrite defualt used for sample config by create_settings()
econ_mod_path="$(pwd)"
log "saved current path=$econ_mod_path"
log "loading settings.."
read_settings_file

# Settings:
# - teeworlds path  0
# - binary          1
# - econ_password   2
# - econ_port       3
# - log path        4
# - cfg path        5
# - tw version      6
# - discord token   7 ( NOT USED BY THIS SCRIPT ONLY BY tools/discord_bot.sh )

twsettings=""

check_path "${aSettVal[0]}" "The teeworlds path is invalid" "0" # 0=dont create on fail
check_path "${aSettVal[0]}/stats" "No stats/ folder found in your teeworlds directory" "1" # 1=create on fail
if [ "${aSettVal[4]}" ]
then
    check_path "${aSettVal[4]}" "The logpath is invalid" "1" # 1=create on fail
    log "adding log path: ${aSettVal[4]}"
    extension=".log"
    if [ "${aSettVal[6]}" == "7" ] || [ "${aSettVal[6]}" == "0.7" ]
    then
        # 0.7 appends .txt anyways
        extension=""
    fi
    twsettings="logfile ${aSettVal[4]}/${aSettVal[1]}_$(date +%F_%H-%M-%S)$extension;"
fi

log "navigate to teeworlds path=${aSettVal[0]}"
cd "${aSettVal[0]}" || { err "invalid path '${aSettVal[0]}'"; exit 1; }

tw_settings_file=""
if [ "${aSettVal[5]}" ]
then
    if [ ! -f "${aSettVal[5]}" ]
    then
        log "Invalid config file '${aSettVal[5]}'"
        exit 1
    fi
    log "settings path: ${aSettVal[5]}"
    tw_settings_file="-f ${aSettVal[5]}"
fi

function teeworlds_srv() {
    ./${aSettVal[1]} "$twsettings" "$tw_settings_file"
}

function main_py() {
    local path="$1"
    local settingsfile="$2"
    cd "$path" || { err "invalid econ path '$path'"; exit 1; }
    ./src/main.py --settings="$settingsfile"
}

function netcat() {
    local path="$1"
    local ec_pw="$2"
    local ec_port="$3"
    local settingsfile="$4"
    local nc_os
    nc_os="nc"
    if [ "$(uname)" == "Darwin" ]; then
        nc_os="nc_macOS"
        log "detected macOS"
    elif [ "$(uname -s)" == "Linux" ]; then
        log "detected Linux"
    elif [ "$(uname -s)" == "MINGW32_NT" ]; then
        log "warning MINGW support isnt guaranteed"
    elif [ "$(uname -s)" == "MINGW64_NT" ]; then
        log "warning MINGW support isnt guaranteed"
    fi
    cd "$path" || { err "invalid netcat path '$path'"; exit 1; }
    ./bin/$nc_os.exp "$ec_pw" "$ec_port" settings="$settingsfile"
}

cmd="(teeworlds_srv \"$twsettings\" $tw_settings_file) | (main_py \"$econ_mod_path\" \"$settings_file\") | (netcat \"$econ_mod_path\" \"${aSettVal[2]}\" \"${aSettVal[3]}\" \"$settings_file\")"
log "run server | pipe into main.py | pipe into netcat connection: "
log "executing: $cmd"
eval "$cmd"

