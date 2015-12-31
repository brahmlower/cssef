#!/bin/bash

# Check if the package is already installed. If so, remove it for a clean installation
pip list | grep cssefclient > /dev/null
if [ "$?" -eq "0" ]
then
	echo "[INFO] Cssefclient package already installed. Removing for clean installation."
	echo "y" | sudo pip uninstall cssefclient > /dev/null
fi

# Install the pip package
echo "y" | sudo pip install . > /dev/null
if [ "$?" -ne "0" ]
then
	>&2 echo "[ERROR] The pip package failed to install."
	exit 1
fi
# Verify that cssef-cli was installed to the correct location
which cssef-cli > /dev/null
if [ "$?" -ne "0" ]
then
	>&2 echo "[ERROR] The cssef-cli not in \$PATH. Expected '/usr/local/bin/cssef-cli'."
	exit 1
fi

# Make sure the cli imports the client pacakge correctly 
cssef-cli organization > /dev/null
retCode=$?
if [ "$retCode" -ne "2" ]
then
	>&2 echo "[ERROR] The cssef-cli failed to run. Expected error code '2', but got '$retCode'"
	exit 1
fi

# Test if communication to the server is working
cssef-cli organization get > /dev/null
if [ "$?" -ne "0" ]
then
	>&2 echo "[ERROR] Client could not reach the cssef server."
	exit 1
fi