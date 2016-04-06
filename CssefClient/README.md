# CSSEF Client
All documentation is hosted by Read the Docs. Installation and configuration documentation can be found [here](http://cssef.readthedocs.org/en/latest/client.html).

Developer documentation is still a work in progress. Bug me about it if you want it finished faster.

<!----
The CSSEF Client can be intalled through setup.py a pip local installation. Building and installing via pip is suggested as it makes upgrading/removing the package easier.

## Installing
Manually install the package.
```
user@host:~$ git clone https://github.com/bplower/cssef.git
user@host:~$ cd cssef/cssefclient
user@host:~/cssef/cssefclient$ sudo pip install .
```

This will add the cssefclient module to python.
```
user@host:~$ python
Python 2.7.9 (default, Mar  1 2015, 12:57:24) 
[GCC 4.9.2] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> from cssefclient import cssefclient
>>> cssefclient.OrganizationGet
<class 'cssefclient.cssefclient.OrganizationGet'>
>>>
```

Additionally, it will create a client configuration file.
```
user@host:~$ ls /etc/cssef
cssef.conf
```

## Verifying installation
You can use the build tests to make sure the build you've downloaded works. This assumes you've cloned the repo into your home directory.

To make running unittests simple, I'm using nose. It can be installed through pip and provides the 'nosetests' utility.

The tests_cssef-cli.bash script will the functionality of the cssef-cli utility specifically. Please note that part of the script will uninstall any preexisting cssefclient installations and install the cssefclient package you've cloned. Some of the tests will require that the CSSEF server be available using the configurations in the ~/cssef/cssefclient/cssefclient/cssef.conf file (you can change these as needed before running the script).
```
user@host:~$ sudo pip install nose
user@host:~$ cd ~/cssef/cssefclient
user@host:~/cssef/cssefclient$ nosetests tests
user@host:~/cssef/cssefclient$ tests/tests_cssef-cli.bash
```
---->
