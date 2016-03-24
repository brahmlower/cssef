#!/bin/bash

# Stop the server in case it's already running
cssefd stop

# Wipe the database
rm db.sqlite3

# Uninstall the CSSEF server package
sudo pip uninstall -y cssefserver

# Now reinstall the CSSEF server package
sudo pip install .
if [ "$?" -ne "0" ]
then
	>&2 echo "[ERROR] The pip package failed to install."
	exit 1
fi

# Fix permissions on the logging directory
# This will eventually be unnecessary, but is only needed now 
# because we're not running the server with any elevated previleges
# (running 'sudo cssefd start' will complain about trunning celery 
# workers as root)
sudo chmod go+w /var/log/cssef

# Change the config file to store the pid file in /tmp/ rather than
# /var/run/. This is for the same reason we changed permissions on
# the log file directory (we're not running with any elevated permissions)
sudo sed -i 's|/var/run/|/tmp/|' /etc/cssef/cssefd.yml

# We're going to set the admin key to use for the initial setup
admintoken=`openssl rand -hex 16`
sudo sed -i "s|admin-token:|admin-token: $admintoken|" /etc/cssef/cssefd.yml

# Now restart the server
cssefd start

# Add an organization to add our user to.
cssef-cli --admin-token $admintoken organization add --name=Administrators --maxMembers=10

# And now our new test admin user!
cssef-cli --admin-token $admintoken user add --organization=1 --name=Admin --username=admin --password=admin