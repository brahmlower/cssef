CSSEF Client
============
.. _client-client_installation:

Client Installation
-------------------
The client requires python and pip.

If you don't have the repo cloned yet, clone it.
::

	user@debian:~$ git clone https://github.com/bplower/cssef.git

Move to the client package directory and install the python package and
execuables via make. The required pip dependancies are ``prettytable``,
``jsonrpcclient``, and ``PyYAML``.
::

	user@debian:~$ cd cssef/CssefClient
	user@debian:~/cssef/CssefClient$ sudo make install

.. _client-client_configuration:

Client Configuration
--------------------

General
~~~~~~~

verbose
	This is by default false, but when set to true, will allow additional
	output to be printed detailing events and actions that are happening.

	Default: ``False``

	Example config file
	::

		# I want to know EXACTLY what the client is doing all the time!
		verbose: True

	Example command line
	::

		user@debian:~$ cssef-cli --verbose organization get

task-timeout
	The time in seconds to wait for a task to be completed. This is in case
	the server is not running, or has crashed while handling your request.

	Default: 5

	Example config file
	::

		# My server is super fast so I should never have to wait.
		task-timeout: 1

	Example command line
	::

		user@debian:~$ cssef-cli --task-timeout 30 organization get

Server Connection
~~~~~~~~~~~~~~~~~

rpc-hostname
	This is the hostname or IP address for the CSSEF server.

	Default: localhost

	Example config file
	::

		# The CSSEF server for the practice competition
		rpc-hostname: 10.0.0.50

	Example command line
	::

		user@debian:~$ cssef-cli --rpc-hostname cssef.example.com login

rpc-port
	This is the port the CSSEF server is using on the remote host.

	Default: 5000

	Example config file
	::

		# Running the service on a non-standard port
		rpc-port: 9001

	Example command line
	::

		user@debian:~$ cssef-cli --rpc-port 1234 login

Authentication
~~~~~~~~~~~~~~

organization
	This is the organization you belong to. At this stage of development, the 
	value is the ID of the organization, but this will eventually be updated
	to be the organizations name.

	Defaut:

	Example config file
	::

		# Setting the organization so that we don't have to provide it each
		# time we authenticate
		organization: 1

	Example command line
	::

		user@debian:~$ cssef-cli --organization 1 organization get

username
	This is the username for your account.

	Default:

	Example config file:
	::

		# I'm getting sick of reintroducing myself all the time
		username: admin

	Example command line
	::

		user@debian:~$ cssef-cli --username admin organization get

password
	The password for your account. If you do not provide your password in a
	situation where it is required (assuming you provide the rest of your
	credentials), you will be prompted for your password. This is exemplified
	in the command line examples section. 

	.. warning::
		It is an extremely bad idea to leave your password in plain text in a
		file. Please don't set this in a configuration file.

	Default:

	Example config file:
	::

		# I make very bad decisions in life. This is one of them.
		password: mypassword

	Example command line
	::

		user@debian:~$ cssef-cli --password mypassword organization get
		...
		user@debian:~$ cssef-cli organization get
		Password:

Token
~~~~~

token-auth-enabled
	This simply enables or disables the token authentication system. Setting
	this to 'False' makes the login command useless since the login command
	is only used to retrieve an authentication token.

	Default: True

	Example config file
	::

		# I was once bullied by tokens in school, so I don't want them on my
		# client at all. This will disable token authentication.
		token-auth-enabled: False

	Example command line
	::

		user@debian:~$ cssef-cli --token-auth-enabled false organization get

token-file
	This is the file to store your current token in. This is a configuration
	you will most often set within your local configuration file, since this
	tells the client where to find your token file.

	Default: ~/.cssef/token

	Example config file
	::

		# I don't like file names less than two words in length, so I'm
		# renaming the token file
		token-file: ~/.cssef/auth-token-file

	Example command line
	::

		user@debian:~$ cssef-cli --token-file ~/.cssef/tmp-token login

token-renewal-enabled
	Most tokens have expirations. When you log in, your token will expire
	after some period of time, after which you will have to login again.
	Token renewal will request a new token each time you execute a command.
	If the token expiration time is 'T', this means you won't have to log in
	again unless it has been T time since you last executed a cssef-cli
	request.

Endpoint Caching
~~~~~~~~~~~~~~~~

endpoint-cache-enabled
	The client gets a list of available commands the server provides. This
	allows the server to add and remove plugins (thus changing the available
	commands) without requiring the client to install or uninstall additional
	components. Endpoint caching lets the client retain that list of endpoints
	so that it doesn't have to ask the server for it each time.

	Default: True

	Example config file
	::

		# I'm a bleeding edge kind of guy- I have to make sure I have the
		# updated list as soon as it's availble, therefore I've disabled
		# endpoint caching.
		endpoint-cache-enabled: False

	Example command line
	::

		user@debian:~$ cssef-cli --endpoint-cache-enabled False organization get

force-endpoint-cache
	In some cases, you may want to force the the client to use the cached
	endpoint data. If you already had cached data and decided that you never
	wanted to check available endpoints again, you could set this a
	configuration file- but that is not recommended.

	Default: False

	Example config file
	::

		# I will only ever be using the core endpoints, which I already have cached, so I don't want to check updated endpoint EVER.
		force-endpoint-cache: True

	Example command line
	::

		user@debian:~$ cssef-cli --force-endpoint-cache True organization get

force-endpoint-server
	In some cases, you may want to force the client to check the server for
	available endpoints. It is rather senseless to set this in a configuration
	file, since that would effectively act the same as setting
	``enpoint-cache-enabled: False``.

	Default: False

	Example config file
	::

		# I'm not a rationable human, so I want endpoint caching enabled, but I never want to use my cached copy of the data.
		force-enpoint-server: True

	Example command line
	::

		user@debian:~$ cssef-cli --force-endpoint-server True organization get

endpoint-cache-file
	This is the path to the file to cache the available endpoint data.

	Default: ~/.cssef/endpoint-cache

	Example config file
	::

		# I have a super secret hiding place for special data like this
		endpoint-cache-file: /dev/null

	Example command line
	::

		user@debian:~$ cssef-cli --endpoint-cache-file ~/.caches/cssef_endpoint-cache organization get

endpoint-cache-time
	This is the maximum amount of time that may pass before the client will
	check for available endpoints. This is based on the last time the file
	specified by ``endpoint-cache-file`` was modified. You can see when a
	file was last modified by using stat. There isn't much point to specifying
	this via command line, unless to induce the same functionality as
	``force-endpoint-server``.

	If an integer with no metric is provided, it will be assumed to be
	seconds. For simplicity, you may provide metrics for seconds, minutes,
	hours, and days using one of the following:
	
	- The first letter of the metric (example: 'd' for days)
	- The singlular of the metric (example: 'hour')
	- The plurl of the metric (example: 'minutes')

	Default: 12h

	Example config file
	::

		# My server is pretty fluid, and gets new/different plugins quite often, and I want to be sure I get those updates in a reasonable amount of time.
		endpoint-cache-time: 5minutes

	Example command line
	::

		user@debian:~$ cssef-cli --endpoint-cache-time 5s organization get
