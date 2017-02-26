# Examples

This folder contains examples to verify a `tw_beacon` for yourself. There is a PHP and Python example, which can both be used to test live gameservers, but also have the ability to test offline.

## Testing a signature

### Online example

If you do not have the motivation / technical knowledge to run these examples by yourself, you can test any server at [this webpage](https://teamwork.tf/community/beacon/verify).


### Binay example - Linux

This example can run on any system without external dependencies (e.g. install PHP/Python). This is a compiled version of the Python script. Open a bash terminal and CD into the `examples/` folder. After this, execute `./verify_signature` and follow the instructions.

### PHP example

This example can be run on any system that has PHP on it. Just run PHP with the filename, and follow the instructions on the screen. Note that this also required OpenSSL, which is by default on most Linux systems.

```
php verify_signature.php
```

### Python example

Python 3 required. First install these depencies via PIP:

```
pip3 install pyopenssl
pip3 install python-valve
```

Also make sure you have OpenSSL on your system (by defalt on most Linux systems). Then run it like this and follow the instructions:

```
./verify_signature.py
```

## Implementing it yourself

### Signature verification

A signature looks like this:
```
"v1:4:redsun:24-04-2018:MDwCHEP6WloptmfHX+ESBMpn38/hl1NJs4LfQtbX/BUCHGIhcUQbKKmNKMtk8/qvo1jPNpiEtwWbE9JZYA4="
```

When the plugin is installed, it will create a ConVar which is exposed to anyone who will query for the server rule list. A signature is made up of the following structure:

```
<version>:<sequence id>:<community provider id>:<valid signature until>:<base64 encoded signature frame>
```

The signature itself (`<base64 encoded signature frame>`) is signed by the [public](https://github.com/teamworktf/teamwork_server_beacon/blob/master/examples/verification_key_teamwork.pem)/private keypair of teamwork.tf. This signature has the following structure:

```
<sequence id>:<ip>:<port>:<community provider id>:<valid signature until>
```

### Verifying yourself

Everything you need to verify a signature, is present in the `/examples/` folder. Here you can find the public key, as well as some code examples to verify a signature (without any intervention of teamwork.tf themselves).

### Revoked signatures

It might be possible that some keys become revoked before their 'valid until' date. To query for these blacklisted signatures, you should send an HTTP GET request to `https://teamwork.tf/community/beacon/revoked` and check if the sequence id and community provider id matches with any of the blacklisted items in the result. Check the PHP or Python script in this folder to see how this is implemented.