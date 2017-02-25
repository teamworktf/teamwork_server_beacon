# Tools

This folder contains tools/examples to verify a `tw_beacon` for yourself. There is a PHP and Python example, which can both be used to test live gameservers, but also has the ability to test offline.

## Online example

If you do not have the motivation / technical knowledge to run these examples by yourself, you can test any server at [this webpage](https://teamwork.tf/community/beacon/verify).


## PHP example

This example can be run on any system that has PHP on it. Just run PHP with the filename, and follow the instructions on the screen. Note that this also required OpenSSL, which is by default on most Linux systems.

```
php verify_signature.php
```

## Python example

Python 3 required. First install these depencies via PIP:

```
pip3 install pyopenssl
pip3 install python-valve
```

Also make sure you have openssl on your system (by defalt on most Linux systems). Then run it like this and follow the instructions:

```
./verify_signature.py
```