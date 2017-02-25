# Examples

This folder contains examples to verify a `tw_beacon` for yourself. There is a PHP and Python example, which can both be used to test live gameservers, but also has the ability to test offline.

## Signature verification

A signature looks like this:
```
tw_beacon "v1:4:redsun:24-04-2018:MDwCHEP6WloptmfHX+ESBMpn38/hl1NJs4LfQtbX/BUCHGIhcUQbKKmNKMtk8/qvo1jPNpiEtwWbE9JZYA4="
```

A signature is made up of the following structure:

```
<version>:<sequence id>:<community provider id>:<valid signature until>:<actual signature>
```

The signature itself (`<actual signature>`) is signed by the public/private keypair of teamwork.tf. This signature has the following structure:

```
<sequence id>:<ip>:<port>:<community provider id>:<valid signature until>
```

The public key to verify, as well as some examples to verify a signature is present in `/tools/`. There is also an online tool available [on this webpage](https://teamwork.tf/community/beacon/verify).

### Revoked signatures

It might be possible that some keys become revoked before their revocation date. To query for these blacklisted signatures, you should send an HTTP GET request to `https://teamwork.tf/community/beacon/revoked` and check if the sequence id and community provider id matches with any of the blacklisted items in the result.

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