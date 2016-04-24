#!/bin/bash

# Lint the project before breaking down the current environment
PYLINT=`which pylint`
if [ 0 -eq $? ]; then
	$PYLINT cssefclient/ 2>/dev/null | grep "E:"
	if [ 0 -eq $? ]; then
		echo ""
		echo "There were errors while linting 'cssefclient'! Pip install aborted."
		exit
	fi

	$PYLINT cssef-cli 2>/dev/null | grep "E:"
	if [ 0 -eq $? ]; then
		echo ""
		echo "There were errors while linting 'cssef-cli'! Pip install aborted."
		exit
	fi
else
	echo "Pylint couldn't be found. Linting was skipped. Please consider installing pylint. :)"
fi

sudo pip uninstall -q -y cssef-client
sudo pip install -q .
