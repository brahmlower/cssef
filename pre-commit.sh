#!/bin/bash
if [ "$1" == "--no-virtual-env" ]; then
	use_virtual_env=false
else
	use_virtual_env=true
fi

# Set up the virtual environment
if [ "$use_virtual_env" = true ]; then
	virtualenv cssef_test
	source cssef_test/bin/activate
fi

# Install the server and client
pip install -q CssefClient/.
if [ 0 -ne $? ]; then
	echo "The client failed to install. Exiting."
	exit $?
fi
pip install -q CssefServer/.
if [ 0 -ne $? ]; then
	echo "The server failed to install. Exiting."
	exit $?
fi

# Test the server and client
echo "Running client tests"
nosetests CssefClient/.
CLIENTEXIT=$?

echo "Running server tests"
nosetests CssefServer/.
SERVEREXIT=$?

# Set up the virtual environment
if [ "$use_virtual_env" = true ]; then
	deactivate
	rm -r cssef_test
fi

# Now try to exit with the exit values of the failed tests
if [ 0 -ne "$CLIENTEXIT" ]; then
	exit $CLIENTEXIT
fi
if [ 0 -ne "$SERVEREXIT" ]; then
	exit $SERVEREXIT
fi
