# TeeworldsEconMod

A python script which communicates with teeworlds server log as input and econ connection as output.

# Setup

on debian based systems do:
```
sudo apt install python3 python3-pip git expect
git clone https://github.com/ChillaVanilla/TeeworldsEconMod.git
cd TeeworldsEconMod
pip3 install -r requirements.txt
./start_tem.sh
```

# How to use?

create a ``tem.settings`` file and write line by line these configurations:

```
sh_tw_path=/path/to/your/teeworlds/directory/
sh_tw_binary=name_of_teeworlds_srv
sh_logs_path=/path/to/log/directory/
sh_econ_password=password
sh_econ_port=8203
py_debug=0
py_stats_mode=file
py_file_database=stats/
```
a sample config could look like:
```
sh_tw_path=/home/chiller/teeworlds/
sh_tw_binary=teeworlds_srv
sh_logs_path=/home/chiller/logs/
sh_econ_password=7h9had8a9
sh_econ_port=8203
py_debug=1
py_stats_mode=sql
py_sql_database=stats.db
```


To fire things up execute ``./start_tem.sh``.

This will start your teeworlds server pipe the output through the python scripts
and then respond via netcat connection to the teeworlds econ api.

# Dependencies

You need python3 and expect installed. And a teeworlds server with an autoexec.cfg including:
```
ec_port "port"
ec_password "password"
```

# Advanced config

Additional config variables can be found in
```
src/global_settings.py
```

You can also lock names and only allow connections from specific regions.
This is to combat player faking and can be used to protect kill/death ratio.

Create a file called ``locked_names.json`` that contains an array of locked names in this format:

```json
[
  { "name": "ChillerDragon", "region": "Bavaria" }
]
```

Then create a [ipinfo](https://ipinfo.io/) account and set the api token in your tem.settings file:
```
py_ipinfo_token=exampletoken
```

# Testing

To make sure everything runs fine on your system you can try running the tests.
It runs tem against a few sample logs.
```
# install bc which is a dependency of test.sh
# also works without but you get a few warnings
sudo apt install bc
cd test
./test.sh

# for more information check the help page
./test.sh --help
```

# Logs

Currently the logs have some weird binary chunks in it and ``grep`` doesn't work well with it.

If you want to convert the logs to text only you could use a command like:

```
for f in logs/*; do echo "[`basename $f`]... (`wc -l $f`)"; strings $f > txt_logs/`basename $f`; done
```

# Bugs

``sv_scorelimit 1000`` is strongly recommended
if scorelimit is lower the wins and looses will be calculated on new round start.
So all players who leave during end screen won't be tracked.
If the scorelimit is 1000 the wins and looses will be saved instantly on the 10th capture.

Keep in mind the script just parses the logs. So everything messing with the logs can be dangerous.
Things like ``restart`` and ``reload`` are untested and not recommended. Also using the rcon command ``say`` to create fake game messages like ``say 'nameless tee' has left the game`` is most likely crashing the server.
