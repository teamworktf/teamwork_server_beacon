# teamwork_server_beacon
Source SDK Plugin for providing server beacon.

## How to install?

* [Download this repository](https://github.com/teamworktf/teamwork_server_beacon/archive/master.zip) or check it out via git.
* Go to your TF2 server folder.
* Navigate to `tf\addons`.
* Copy the contents of the .ZIP under `Dist\addons` into the `tf\addons` folder.
* Open your `server.cfg`, and add the following line: `tw_beacon "<the-signature-you-got-from-the-site>"`
* Restart server.

## How to build?

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