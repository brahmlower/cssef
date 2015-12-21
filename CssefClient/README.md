# CSSEF Client

The CSSEF Client can be intalled through setup.py or a pip local installation. Building and installing via pip is suggested as it makes upgrading/removing the package easier.

## Installing
Currently, you will have to manually build and install the package.
```
user@host:~$ git clone https://github.com/bplower/cssef.git
user@host:~$ cd cssef/cssefclient
user@host:~/cssef/cssefclient$ python setup.py bdist_wheel
user@host:~/cssef/cssefclient$ sudo pip install dist/CssefClient-0.0.1-py2-none-any.whl
```

## Verifying installation
Installing the package will provide the 'cssef-cli' utility and a corresponding configuration file in /etc/cssef/.
```
user@host:~$ which cssef-cli
/usr/local/bin/cssef-cli
user@host:~$ ls /etc/cssef/
cssef.conf
```

Additionally this will add the CssefClient module to python.
```
user@host:~$ python
Python 2.7.9 (default, Mar  1 2015, 12:57:24) 
[GCC 4.9.2] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> from CssefClient import cssefclient
>>> cssefclient.OrganizationGet
<class 'CssefClient.cssefclient.OrganizationGet'>
>>>
```