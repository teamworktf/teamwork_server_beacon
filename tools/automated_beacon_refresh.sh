#!/bin/sh
# Refresh all beacons that are in the user_config.json file.
python3 request_beacon.py request-rcon-all
# Or you can for example set the beacon for 1 server (ip, port, rcon pass):
#python3 request_beacon.py 0.0.0.0 27015 test
