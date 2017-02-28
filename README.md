# teamwork_server_beacon
Source SDK Plugin that provides community server authentication and additional information.

![beacon icon](https://teamwork.tf/images/beacon-ico.png)


[forum section](https://forum.teamwork.tf/t/development) | [teamwork.tf](https://teamwork.tf)

## Introduction

This plugin allows anyone to identify your server as part of a larger community. This plugin will publish a unique beacon to the world, and with that beacon, anyone in the world can verify that your server is indeed part of a community provider. teamwork.tf will use this for the website, but the techologies are opensource and can be used by anyone.

This plugin can help websites that use TF2 gameserver information in one way or another to securely identify that a gameserver is part of a community with multiple servers. This will be for example useful to identify fake community servers, and helps websites provide additional details about these servers (e.g. the URL/Forum/Name/Image of the community provider/group).

## Verify a server

If you want to verify a server, you can do so with [this online tool](https://teamwork.tf/community/beacon/verify), or look at the `examples/` folder for some programming examples and useful local tools.

## Community server providers

This sections is only relevant to people who run TF2 servers. In order for a server to emit a beacon, which others can verify, the server needs a plugin. The only function the plugin has, is that it allows you to set the `tw_beacon` ConVar in your server config. It does not do anything else!

### How to install the plugin?

1. Clone this repository on your server (`git clone https://github.com/teamworktf/teamwork_server_beacon.git`).
2. Alternatively you can [download](https://github.com/teamworktf/teamwork_server_beacon/archive/master.zip) this repository and unzip it somewhere on your server.
3. CD to `teamwork_server_beacon\dist\addons` and copy the contents of that folder.
4. Natigate to your TF2 server folder and CD into `tf\addons`. Paste the contents here.
5. Restart the TF2 server and verify the plugin has loaded (type in console: `tw_version`, this should return a version number).
6. Now you can start requesting beacons for your sever. Read the next chapter below.

### Requesting beacons

By default, a beacon is valid for 1 year and 2 months. This means that you need to request a beacon for each server at least once a year to keep the beacons valid.

1. Make sure you are a community provider on teamwork.tf. [Click here](https://teamwork.tf/community/beacon) to apply.
2. Log in with your Steam account on the website, and copy the API key that is under "Manage Community Provider".
3. Now CD into the location where you unpacked/cloned this repository.
4. CD into `tools/`.
5. Execute `python request_beacon.py` (Windows/Linux, Python 3+ required, make sure you have `python-valve` installed, `pip install python-valve`) or `./request_beacon` (Linux). *Click [here to download python for Windows](https://www.python.org/ftp/python/3.4.4/python-3.4.4.amd64.msi), this only takes a minute.*
6. Set the API key, and choose `request-file`, to set the beacon permanently (RCON is gone after a server restart).
7. Enter IP/Port of your server, and give the location of your `server.cfg` once it asks for the .cfg file.
7. Make sure you restart the server.
8. Learn here how to [verify/check a signature](https://github.com/teamworktf/teamwork_server_beacon/tree/master/examples) *(wait at least 10 minutes for the online tool)*.
9. Learn how to automate the beacon refreshing [here](https://github.com/teamworktf/teamwork_server_beacon/tree/master/tools), or just make a reminder a year from now that you need to refresh the beacon (outdated beacons are invalid).

As said before, the beacon will only be valid for 1y2m, if the validity expires the beacon will be no longer valid. At this point the specification will ignore your beacon. Note that your signature is bound to your IP:PORT; if you run the gameserver on a non-static IP adress, you need to update the beacon everytime your IP changes.

### How to build the plugin?
*OPTIONAL STEP, only recommended if you want to verify the code itself.*

** Windows **

1. Download and install Visual Studio 2013.
2. Follow [this guide](https://developer.valvesoftware.com/wiki/Source_SDK_2013) to setup Source SDK 2013.
3. CD to the root folder of the source sdk.
4. `cd mp\src\utils\`
5. `git clone https://github.com/teamworktf/teamwork_server_beacon.git`
6. Now open Visual Studio and navigate to the `teamwork_server_beacon` folder located in `<source-sdk>\mp\src\utils\`.
7. Open the solution file (.sln)
8. To see the plugin contents, look at `teamwork_beacon.cpp`.
9. Right click and choose `Build Solution` to build the plugin.
10. The `teamwork_beacon.dll` will appear in the `debug` folder.
11. Copy this `teamwork_beacon.dll` into the `dist\addons\teamwork_beacon\bin` folder, replacing the old one.
12. Now follow the chapter above on how to install the plugin.

** Linux **

1. Download and install CodeLite.
2. Follow [this guide](https://developer.valvesoftware.com/wiki/Source_SDK_2013) to setup Source SDK 2013.
3. CD to the root folder of the source sdk.
4. `cd mp\src\utils\`
5. `git clone https://github.com/teamworktf/teamwork_server_beacon.git`
6. Now open Code Lite and navigate to the `teamwork_server_beacon` folder located in `<source-sdk>\mp\src\utils\`.
7. Open the project file (.project)
8. To see the plugin contents, look at `teamwork_beacon.cpp`.
9. Build the solution to check if its working.
10. The `teamwork_beacon.so` will appear in the `../../game/bin/` folder.
11. Copy this `teamwork_beacon.so` into the `dist\addons\teamwork_beacon\bin` folder, replacing the old one.
12. Now follow the chapter above on how to install the plugin.
