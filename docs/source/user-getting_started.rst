Getting Started
===============

There are 3 primary components to framework.

Server Installation
-------------------
The server requires python, pip, rabbitmq, and celery. 

Install the prerequisets
::
	user@debian:~$ sudo apt-get install -y git python-pip python-dev rabbitmq-server

Configure the rabbitmq server
::
	user@debian:~$ sudo rabbitmqctl add_user cssefd-user cssefd-pass
	user@debian:~$ sudo rabbitmqctl set_user_tags cssefd-user administrator
	user@debian:~$ sudo rabbitmqctl set_permissions ".*" ".*" ".*"

Install the CSSEF server
::
	user@debian:~$ git clone https://github.com/bplower/cssef.git
	cd cssef/CssefServer
	user@debian:~/cssef/CssefServer$ sudo pip install .

Verify the installation was successful
::
	user@debian:~/cssef/CssefServer$ cssefd start
	user@debian:~/cssef/CssefServer$ cssefd status
	Running with pid 26351

Client Installation
-------------------
The client requires python and pip.

If you don't have the repo cloned yet, clone it.
::
	user@debian:~$ git clone https://github.com/bplower/cssef.git

Move to the client package directory and install it via pip.
::
	user@debian:~$ cd cssef/CssefClient
	user@debian:~/cssef/CssefClient$ sudo pip install .

Admin Configuration
-------------------
Initially, there are no users or organization, so we will have to make them by using an administrator token. Set the 'admintoken' in the server configuration field to a secure passphrase to use for the initial configuration. Note that this will be provided in plain text several times, but will be revoked after the configuration is complete.

Here we're creating the token and assigning it to an environment variable. We're changing the configuration file via sed, however you may use the text editor of your choice. Afterward, restart the server to apply the configuration changes.
::
	user@debian:~$ admintoken=`openssl rand -hex 16`
	user@debian:~$ sudo sed -i "s|admin-token:|admin-token: $admintoken|" /etc/cssef/cssefd.yml
	user@debian:~$ cssefd restart

We can now provide the admintoken while executing commands. This will allow us to bypass authentication checks and limits. First create an administrator organization for the admin account to exist within.
::
	user@debian:~$ cssef-cli --admin-token $admintoken organization add --name=Administrators --maxMembers=10
	+------------+-------------+----------------+------+----+-----------------+-----------------------+----------------+--------------------+-------------+-----------+
	| maxMembers | description |      name      | url  | id | maxCompetitions | canDeleteCompetitions | canDeleteUsers | canAddCompetitions | canAddUsers | deletable |
	+------------+-------------+----------------+------+----+-----------------+-----------------------+----------------+--------------------+-------------+-----------+
	|     10     |     None    | Administrators | None | 1  |       None      |          True         |      True      |        True        |     True    |    True   |
	+------------+-------------+----------------+------+----+-----------------+-----------------------+----------------+--------------------+-------------+-----------+

And now, create an administrator user to use.
::
	user@debian:~$ cssef-cli --admin-token $admintoken user add --organization=1 --name=Admin --username=admin --password=admin
	+----------+-------------+--------------+--------------------------------------------------------------+----+-------+
	| username | description | organization |                           password                           | id |  name |
	+----------+-------------+--------------+--------------------------------------------------------------+----+-------+
	|  admin   |     None    |      1       | $2b$10$cHzkaFpT3va5LoTyjV4gHuxd3MZQpvm5OUQCGcSiwbxYmsI74j9a6 | 1  | Admin |
	+----------+-------------+--------------+--------------------------------------------------------------+----+-------+

Disable admintoken access by removing the admin token from the server configuration file.
::
	user@debian:~$ sudo sed -i "s|admin-token:*|admin-token:|" /etc/cssef/cssefd.yml
	user@debian:~$ cssefd restart

This can be verified by attempting to list availble users using the admin token we used. At this point in time, the server doesn't explicitly deny the use of the admin-token, so it will continue to attempt to authenticate the user as normal. Since we haven't provided a valid username or password, access is not granted.
::
	user@debian:~$ cssef-cli --admin-token $admintoken user get
	An error was encountered:
	['No username provided.']
	No username provided.

Lastly, we can verify that authorization IS working by logging in. Here we are not specifying the password, so we are prompted for it. Since the authentication is successful, we received an authentication token, which will be automatically provided by the client in future requests.
::
	user@debian:~$ cssef-cli login --username admin
	Password: 
	Authentication was successful.

Now that we've been authenticated, we can list the available users.
::
	user@debian:~$ cssef-cli user get
	+----------+-------------+--------------+--------------------------------------------------------------+----+-------+
	| username | description | organization |                           password                           | id |  name |
	+----------+-------------+--------------+--------------------------------------------------------------+----+-------+
	|  admin   |     None    |      1       | $2b$10$cHzkaFpT3va5LoTyjV4gHuxd3MZQpvm5OUQCGcSiwbxYmsI74j9a6 | 1  | Admin |
	+----------+-------------+--------------+--------------------------------------------------------------+----+-------+
