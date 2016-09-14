CSSEF Server
============

Lets start with a quick overview of what everything in this directory is for,
since most of it hasn't been formally organized.

cssefserver/
	This directory contains the source for the pip package 'cssef-server'.

tests/
	Directory for tests for the 'cssef-server' package.

readme.md
	A readme file for github.

cssef-server
	An executable file to host a CSSEF server. This is what is started by
	systemd.

cssef-server.service
	A systemd service file, used to define the 'cssef-server' service.

cssef-server.yml
	A service configuration file, which is read in when the cssef server
	is started.

makefile
	Used to make running several tasks related to installation and testing
	easier.

setup.py
	A setup script that defines the 'cssef-server' python package for pip.

Makefile
--------

At this time, the makefile must be run from the current directory
(.../CssefServer) since resources are pathed referentially.

install
	The actions of the install process are divided into four steps:

	1. Install the 'cssef-server' package via pip.
	2. Create necessary directories.
	3. Copy service and config files.
	4. Enable (but not start) the service within systemd.

uninstall
	Uninstall does most of the install process, but will leave the
	configuration files and database files, in case those are still needed
	afterward.

	1. Stop and disabled the the service within systemd.
	2. Remove the .service file and service executable
	3. Remove the python package via pip

reinstall
	This simply calls the `uninstall` and `install` portions of the make file.
	It is important to note here that the contents of 
	`/etc/cssef/cssef-server.yml` will be overwritten.

test
	This will run pylint and nosetests  on the library and the cssef-server
	executable.
