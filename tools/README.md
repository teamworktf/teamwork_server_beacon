# Tools

This folder contains scripts/binaries to automate the beacon retrieval.

## Requesting a beacon

CD into `tools/` and execute `python request_beacon.py` (Windows/Linux, Python 3+ required, make sure you have `python-valve` installed, `pip install python-valve`) or `./request_beacon` (Linux, without Python). Remember to set your PATH variable to your Python installation if you've just installed Python on Windows.

After entering  your API key you got from teamwork.tf, you will be presented with three options:

* `request` : Request a beacon, which you need to copy/paste into your `server.cfg`.
* `request-file` : Request a beacon, and automatically insert this beacon into your `server.cfg`, make sure you restart your TF2 gameserver (CONFIG WILL BE STORED).
* `request-rcon` : Request a beacon, and automatically set this on your server **warning:** this is not permanent, the beacon will be lost on server restart.
* `refresh-all` : Refresh all beacons, that you requested via `request-file` or `request-rcon`.

It is important you refresh your beacons at least once a year! Beacons that are no longer valid, means that your server will not be authenticated towards this service. Either set a reminder in your calendar, or automate the retrieval. Note that your signature is bound to your IP:PORT; if you run the gameserver on a non-static IP adress, you need to update the beacon everytime your IP changes.


## Automation

To make sure that your server have valid signatures, you need to periodicly refresh your beacons. I'd advise using `crontab` to trigger this Python script, and afterwards to restart your server.

1. Add all your servers (IP:PORT, and location of the `server.cfg`) to the request tool by executing `request-file` for all of those servers.
2. Verify that all the servers are stored in the tools config (`user_config.json`).
3. Open crontab (`crontab -e`) and add something like this:
```
# at 5 a.m every week with:
0 5 * * 1 <location-to-tools-dir>/automated_beacon_refresh.sh
```
4. Make sure to also restart your TF2 server after changing the config file. To do this you can add ` && <restart-server-cmd>` to the last line from above.
