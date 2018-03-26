#!/bin/bash
echo "====================="
echo " Teeworlds Econ Mod  "
echo " by ChillerDragon    "
echo "====================="

if [ ! -f tem.settings ]; then
    echo "error tem.settings file not found"
    read -p "Do you want to create one? [y/n]" -n 1 -r
    echo 
    if [[ $REPLY =~ ^[Yy]$ ]]
    then
        echo "/path/to/your/teeworlds/directory" > tem.settings
        echo "name_of_teeworlds_srv" >> tem.settings
        echo "econ_password" >> tem.settings
        echo "econ_port" >> tem.settings
        nano tem.settings
    fi
    exit
fi

setting_lines=()
econ_mod_path=`pwd`
echo "saved current path=$econ_mod_path"
echo "loading settings.."

#crary i/o redirecting more details at: http://tldp.org/LDP/abs/html/x17974.html
exec 6<&0 # Link file descriptor #6 with stdin.
exec < tem.settings
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
# - teeworlds path
# - binary
# - econ_password
# - econ_port 

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

echo "navigate to teeworlds path=${setting_lines[0]}"
cd ${setting_lines[0]}

echo "start server | pipe into main.py | pipe into netcat connection: "
echo "executing: ./${setting_lines[1]} | $econ_mod_path/src/main.py | $econ_mod_path/bin/nc.exp ${setting_lines[2]} ${setting_lines[3]}"
./${setting_lines[1]} | $econ_mod_path/src/main.py | $econ_mod_path/bin/nc.exp ${setting_lines[2]} ${setting_lines[3]}

