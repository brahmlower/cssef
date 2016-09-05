
install:
	pip install .
	mkdir -p /etc/cssef/
	cp cssef-cli /usr/local/bin/.
	cp cssef-client.yml /etc/cssef/.

uninstall:
	rm /usr/local/bin/cssef-cli
	pip uninstall cssef-client -y

reinstall: uninstall install

test:
	pylint cssefclient/ --errors-only
	pylint cssef-cli --errors-only
	nosetests .