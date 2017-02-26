#!/bin/sh
MYDIR="$(dirname "$(realpath "$0")")"
# Examples which you can use to request new beacons via crontab.
# Refresh all beacons that are in the user_config.json file.
python3 $MYDIR/request_beacon.py refresh-all
# Or you can for example set the beacon for 1 server via RCON (ip, port, rcon pass):
#python3 request_beacon.py <IP> <PORT> rcon <RCON_PASS>
# Or you can for example set the beacon for 1 server via a config file (it will add or replace the tw_beacon)
#python3 request_beacon.py <IP> <PORT> file <CONFIG_LOCATION>