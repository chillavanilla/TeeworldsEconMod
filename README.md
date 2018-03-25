# TeeworldsEconMod
A python script which communicates with teeworlds server log as input and econ connection as output.

# How to use?

create a ``tem.settings`` file and write line by line these configurations:

```
/path/to/your/teeworlds/directory
name_of_teeworlds_srv
econ_password
econ_port
```

To fire things up execute ``./start_tem.sh``.

This will start your teeworlds server pipe the output through the python scripts
and then respond via netcat connection to the teeworlds econ api.

# Dependencies

You need python3 installed and a teeworlds server with an autoexec including:
```
ec_port "port"
ec_password "password"
```
