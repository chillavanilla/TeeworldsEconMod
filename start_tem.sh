#!/usr/bin/env bash
echo "========================"
echo "|| Teeworlds Econ Mod ||"
echo "|| by ChillerDragon   ||"
echo "========================"

function log() {
    echo "[TEM] $1"
}

# check dependencys
command -v expect >/dev/null 2>&1 || {
  echo >&2 "Error: expect is not found please install it!";
  if [ "$(uname)" == "Darwin" ]; then
    echo >&2 "MacOS: brew install expect";
  elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
    echo >&2 "Debian/Ubuntu: sudo apt install expect";
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
    log "$warning"
    log "should be at: $path"
    if [ "$create" != "0" ]
    then
        read -p "Do you want to create the path? [y/n]" -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]
        then
            mkdir $path
            log "created folder at: $path"
            return
        fi
    fi
    log "PathError: please provide a valid path."
    exit
}

function create_settings() {
    if [ -f $settings_file ];
    then
        return
    fi
    local i
    log "FileError: '$settings_file' not found"
    read -p "Do you want to create one? [y/n]" -n 1 -r
    echo 
    if [[ $REPLY =~ ^[Yy]$ ]]
    then
        echo "# TeeworldsEconMod (TEM) by ChillerDragon" > $settings_file
        echo "# https://github.com/chillavanilla/TeeworldsEconMod" >> $settings_file
        for i in "${!aSettStr[@]}"
        do
            echo "${aSettStr[$i]}=${aSettVal[$i]}" >> $settings_file
        done
        nano $settings_file
    fi
    exit
}

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
        exit
}

function read_settings_file() {
    local i
    while read line
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

create_settings # create fresh if null
aSettVal[6]="" # overwrite defualt used for sample config by create_settings()
econ_mod_path=`pwd`
log "saved current path=$econ_mod_path"
log "loading settings.."
read_settings_file

# Settings:
# - teeworlds path  0
# - binary          1
# - econ_password   2
# - econ_port       3
# - log path        4

twsettings=""

check_path "${aSettVal[0]}" "The teeworlds path is invalid" "0" # 0=dont create on fail
check_path "${aSettVal[0]}/stats" "No stats/ folder found in your teeworlds directory" "1" # 1=create on fail
if [ "${aSettVal[4]}" ]
then
    check_path "${aSettVal[4]}" "The logpath is invalid" "1" # 1=create on fail
    log "adding log path: ${aSettVal[4]}"
    twsettings="logfile ${aSettVal[4]}/${aSettVal[1]}_$(date +%F_%H-%M-%S).log;"
fi

nc_os="nc"

if [ "$(uname)" == "Darwin" ]; then
    nc_os="nc_macOS"
    log "detected macOS"
elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
    log "detected Linux"
elif [ "$(expr substr $(uname -s) 1 10)" == "MINGW32_NT" ]; then
    log "warning MINGW support isnt guaranteed"
elif [ "$(expr substr $(uname -s) 1 10)" == "MINGW64_NT" ]; then
    log "warning MINGW support isnt guaranteed"
fi

log "navigate to teeworlds path=${aSettVal[0]}"
cd ${aSettVal[0]}

log "run server | pipe into main.py | pipe into netcat connection: "
log "executing: ./${aSettVal[1]} \"$twsettings\" | cd $econ_mod_path;./src/main.py --settings=$settings_file | ./bin/$nc_os.exp ${aSettVal[2]} ${aSettVal[3]} settings=$settings_file"
(./${aSettVal[1]} "$twsettings") | (cd $econ_mod_path;./src/main.py --settings=$settings_file) | (cd $econ_mod_path;./bin/$nc_os.exp ${aSettVal[2]} ${aSettVal[3]} settings=$settings_file)

