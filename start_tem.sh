#!/bin/bash
echo "====================="
echo " Teeworlds Econ Mod  "
echo " by ChillerDragon    "
echo "====================="

if [ ! -f tem.settings ]; then
    echo "error tem.settings file not found"
    exit
fi

setting_lines=()
econ_mod_path=`pwd`
echo "saved current path=$econ_mod_path"
echo "loading settings.."

exec < tem.settings
while read line ; do
setting_lines+=($line)
done


echo "Total settings:"
for index in ${!setting_lines[*]}
do
    printf "%4d: %s\n" $index ${setting_lines[$index]}
done

# Settings:
# - teeworlds path
# - binary
# - econ_password
# - econ_port 

echo "navigate to teeworlds path=${setting_lines[0]}"
cd ${setting_lines[0]}

echo "start server | pipe into main.py | pipe into netcat connection: "
echo "executing: ./${setting_lines[1]} | $econ_mod_path/src/main.py | $econ_mod_path/bin/nc.exp ${setting_lines[2]} ${setting_lines[3]}"
./${setting_lines[1]} | $econ_mod_path/src/main.py | $econ_mod_path/bin/nc.exp ${setting_lines[2]} ${setting_lines[3]}

