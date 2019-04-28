#!/usr/bin/env bash
echo "====================="
echo " Teeworlds Econ Mod  "
echo " by ChillerDragon    "
echo "====================="

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

settings_file="tem.settings"

if [ $# -gt 0 ]; then
    echo "settings file=$1"
    settings_file=$1
fi

if [ ! -f $settings_file ]; then
    echo "error $settings_file not found"
    read -p "Do you want to create one? [y/n]" -n 1 -r
    echo 
    if [[ $REPLY =~ ^[Yy]$ ]]
    then
        echo "/path/to/your/teeworlds/directory" > $settings_file
        echo "name_of_teeworlds_srv" >> $settings_file
        echo "econ_password" >> $settings_file
        echo "econ_port" >> $settings_file
        echo "IsDebug (true/false)" >> $settings_file
        echo "StatsMode (file/sql)" >> $settings_file
        echo "/path/to/log/dir (optional)" >> $settings_file
        nano $settings_file
    fi
    exit
fi

setting_lines=()
econ_mod_path=`pwd`
echo "saved current path=$econ_mod_path"
echo "loading settings.."

#crary i/o redirecting more details at: http://tldp.org/LDP/abs/html/x17974.html
exec 6<&0 # Link file descriptor #6 with stdin.
exec < $settings_file
while read line ; do
setting_lines+=($line)
done

echo "Total settings:"
for index in ${!setting_lines[*]}
do
    printf "%4d: %s\n" $index ${setting_lines[$index]}
done

exec 0<&6 6<&- #normalize i/o agian: restore stdin from fd #6, where it had been saved

# Settings:
# - teeworlds path  0
# - binary          1
# - econ_password   2
# - econ_port       3
# - IsDebug         4
# - StatsMode       5
# - log path        6

stats_path="${setting_lines[0]}/stats"

if [ ! -d "$stats_path" ]; then
    echo "No stats/ folder found in your teeworlds directory" 
    echo "should be at: $stats_path"
    read -p "Do you want to create one? [y/n]" -n 1 -r
    echo 
    if [[ $REPLY =~ ^[Yy]$ ]]
    then
        mkdir $stats_path
        echo "created folder at: $stats_path"
    else
        echo "Error Teeworlds Econ Mod can't start without stats folder"
        exit
    fi
fi

nc_os="nc"

if [ "$(uname)" == "Darwin" ]; then
    nc_os="nc_macOS"
    echo "detected macOS"
elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
    echo "detected Linux"
elif [ "$(expr substr $(uname -s) 1 10)" == "MINGW32_NT" ]; then
    echo "warning MINGW support isnt guaranteed"
elif [ "$(expr substr $(uname -s) 1 10)" == "MINGW64_NT" ]; then
    echo "warning MINGW support isnt guaranteed"
fi

twsettings=""
if [ ${setting_lines[6]} ]
then
    if [ -d ${setting_}]
    echo "adding log path: ${setting_lines[6]}"
    twsettings="logfile ${setting_lines[6]}/${setting_lines[1]}_$(date +%F_%H-%M-%S).log;"
fi

echo "navigate to teeworlds path=${setting_lines[0]}"
cd ${setting_lines[0]}

echo "start server | pipe into main.py | pipe into netcat connection: "
echo "executing: ./${setting_lines[1]} \"$twsettings\" | $econ_mod_path/src/main.py --debug ${setting_lines[4]} --stats ${setting_lines[5]} settings=$settings_file | $econ_mod_path/bin/$nc_os.exp ${setting_lines[2]} ${setting_lines[3]} settings=$settings_file"
./${setting_lines[1]} "$twsettings" | $econ_mod_path/src/main.py --debug ${setting_lines[4]} --stats ${setting_lines[5]} settings=$settings_file | $econ_mod_path/bin/$nc_os.exp ${setting_lines[2]} ${setting_lines[3]} settings=$settings_file

