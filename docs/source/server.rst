Server Installation and Configuration
=====================================
.. _server-server_installation:

Server Installation
-------------------
The server requires systemd, python and pip.

Install the prerequisets
::

	user@debian:~$ sudo apt-get install -y git python-pip python-dev systemd libsystemd-dev

Install the CSSEF server
::

	user@debian:~$ git clone https://github.com/bplower/cssef.git
	user@debian:~$ cd cssef/CssefServer
	user@debian:~/cssef/CssefServer$ sudo make install

Verify the installation was successful
::

	user@debian:~/cssef/CssefServer$ sudo systemctl is-enabled cssef-server.service
	enabled
	user@debian:~/cssef/CssefServer$ sudo systemctl start cssef-server.service
	user@debian:~/cssef/CssefServer$ sudo systemctl status cssef-server.service | grep Active:
	Active: active (running) since Thu 2016-09-01 22:00:49 AKDT; 6s ago

.. _server-server_configuration:

Server Configuration
--------------------

Configurations can be loaded from several different sources, where values
loaded later will overwrite previously set values. The order configuration
values are loaded is as follows:

1. Default (hard coded)
2. Global config file
4. Command line configs

Please consider the following example:

	`The default client cache time for available endpoints is 24 hours, but
	is overwritten to a value of 12 hours in the global config file. However,
	you are troublshooting something related to plugins, so you've started the
	daemon with the cache time value set to 0 meaning the cache will be
	refreshed on each client request.`

The value of the client cache time was overwritten twice in this example:
once by the global configuration, and once by the value provided on the
command line. Any configuration option may be set through any of the
configuration sources (excluding the default configs for obvious reasons).

Available Options
~~~~~~~~~~~~~~~~~
admin-token
	This should only be used for initial setup, but may be used in the event
	you are locked out of administrator accounts. The client may provide the
	token to authorize requests by completely bypassing username and password
	checks. If you are not actively using this, the value should be left
	blank, meaning admin-token auth is disabled.

	Default:

	Example config file
	::

		# Setting a weak admin token for initial setup
		admin-token: abc123def456

	Example command line
	::

		user@debian ~$ cssefd start --admin-token abc123def456

database-path
	While using sqlite as the backend database, this option will be for the
	absolute path to store the database file at.

	Default: ``/var/opt/cssef/db.sqlite3``

	Example config file
	::

		# Hold the database in memory for performance while testing
		database-path: ''

	Example command line
	::

		user@debian ~$ cssefd start --database-path ''

database-table-prefix

	.. attention::
	This feature is broken as of `commit 993d87e`_. The prefix is hardcoded to
	"cssef" for the time being.

	.. _commit 993d87e: https://github.com/bplower/cssef/commit/993d87efef98d709209eead4340ff86a1da32f27

	This value will be the prefix for every table in the database. Depending
	on your database backend, this may not be as important. The default will
	result in tables that look similar to "cssef_users".

	Default: ``cssef``

	Example config file
	::

		# Table prefix for production cssef installation
		database-table-prefix: cssef-prod

	Example command line
	::

		user@debian ~$ cssefd start --database-table-prefix cssef-prod

logging
	I've completely skipped the logging values because they're all basically
	useless right now...

installed-plugins
	This is a list of plugins that conform to the CSSEF plugin model that
	should be imported. Those plugins must already be installed, and the
	entries in this list must be the names of the modules.

	Default:

	Example config file
	::

		# Include the default CCDC like competition and CTF competition
		installed-plugins:
		- cssef-ccdc
		- cssef-ctf

	Example command line
	::

		user@debian ~$ cssefd start --installed-plugins cssef-ccdc,cssef-ctf