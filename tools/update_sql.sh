#!/bin/bash
# this script adds a new column to the stats database
# only use this script if you know what you are doing
# it is needed to update the stats.db table on a new update where a new value gets added

if [ ! -f stats.db ]; then
    echo "'stats.db' not found"
    exit
fi

echo "Column name: "
read col
echo "Datatype (INTEGER, TEXT, REAL): "
read datatype
if [ "$datatype" == "INTEGER" ]; then
    echo "INTEGER is an valid option"
elif [ "$datatype" == "TEXT" ]; then
    echo "TEXT is an valid option"
elif [ "$datatype" == "REAL" ]; then
    echo "REAL is an valid option"
else
    echo "ERROR $datatype is not an allowed datatype"
    exit
fi
echo "Default ('', 0): "
read default

echo "ALTER TABLE Players ADD $col $datatype DEFAULT $default;" | sqlite3 stats.db
