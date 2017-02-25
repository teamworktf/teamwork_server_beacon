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
5. Execute `python request_beacon.py` (Linux) or `request_beacon.exe` (Windows).
6. Follow the steps, it will automaticly write the signature into your server's config file.
7. Make sure you restart the server.
8. Check with the [online tool](https://teamwork.tf/community/beacon/verify), if it worked (wait at least 10 minutes before trying).
9. Add a new item to your personal agenda, exactly one year from now with the title `REQUEST NEW TW TOKENS FOR SERVERS!!`.

As said before, the beacon will only be valid for 1y2m, if the validity expires the token will be no longer valid. At this point the specification will ignore your beacon.

### How to build the plugin?
*OPTIONAL STEP, only recommended if you want to verify the code itself.*

1. Download and install Visual Studio 2013.
2. Follow [this guide](https://developer.valvesoftware.com/wiki/Source_SDK_2013) to setup Source SDK 2013.
3. CD to the root folder of the source sdk.
4. `cd mp\src\utils\`
5. `git clone https://github.com/teamworktf/teamwork_server_beacon.git`
6. Now open Visual Studio and navigate to the `teamwork_server_beacon` folder located in `<source-sdk>\mp\src\utils\`.
7. Open the solution file (.sln)
8. To see the plugin contents, look at `teamwork_beacon.cpp`.
9. Right click and choose `Build Solution` to build the plugin.
10. The `teamwork_beacon.dll` will appear in the `Debug` folder.
11. Copy this `teamwork_beacon.dll` into the `Dist\addons\teamwork_beacon\bin` folder, replacing the old one.
12. Now follow the chapter above on how to install the plugin.
