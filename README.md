# teamwork_server_beacon
Source SDK Plugin that provides community server authentication and additional information.

![beacon icon](https://teamwork.tf/images/beacon-ico.png)


[forum support](https://forum.teamwork.tf/t/development) | [teamwork.tf](https://teamwork.tf)

## Introduction

This plugin allows enitites to identify your server as part of a larger community server community. This plugin will publish a unique beacon to the world, and with that beacon, anyone in the world can verify that your server is indeed part of a larger community provider. teamwork.tf will use this for the website, but the techologies are opensource and can be used by anyone.

This plugin can help websites that use TF2 gameserver information in one way or another to securely identify that a gameserver is part of a larger community. This will be for example useful to identify fake community servers, and helps websites provide additional details about these servers (e.g. the URL/Forum/Name/Image of the community provider).

## How to install?
*quick way*

* [Download this repository](https://github.com/teamworktf/teamwork_server_beacon/archive/master.zip) or clone it via GIT.
* Go to your TF2 server folder.
* Navigate to `tf\addons`.
* Copy the contents of the .ZIP under `dist\addons` into the `tf\addons` folder (result: `tf\addons\teamwork_beacon`).
* Open your `server.cfg`, and add the following line: `tw_beacon "<the-signature-you-got-from-the-site>"`
* Restart the gameserver.
* Check if the plugin loaded by typing `tw_version` and `tw_beacon` in the console and see if it returns a value.

## How to build?
*hard way, allows you to verify the code and develop on the plugin*

* Download and install Visual Studio 2013 (2015 not tested).
* Follow [this guide](https://developer.valvesoftware.com/wiki/Source_SDK_2013) to setup Source SDK 2013.
* `cd` to the root folder of the source sdk.
* `cd mp\src\utils\`
* `git clone https://github.com/teamworktf/teamwork_server_beacon.git`
* Now open Visual Studio and navigate to the `teamwork_server_beacon` folder located in `<source-sdk>\mp\src\utils\`.
* Open the solution file (.sln)
* To see the plugin contents, look at `teamwork_beacon.cpp`, other code is mostly boilerplate.
* Right click and choose `Build Solution` to build the plugin.
* The `teamwork_beacon.dll` will appear in the `Debug` folder.
* Copy this dll into the `Dist\addons\teamwork_beacon\bin` folder, replacing the old one.
* Now follow the chapter above on how to install the plugin.
