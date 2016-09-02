
install:
	#pip install cssef-server
	pip install .
	mkdir -p /etc/cssef/
	mkdir -p /var/opt/cssef
	cp cssef-server /usr/local/bin/.
	cp cssef-server.yml /etc/cssef/.
	cp cssef-server.service /lib/systemd/system/.
	systemctl enable cssef-server.service

uninstall:
	systemctl stop cssef-server.service
	systemctl disable cssef-server.service
	rm /lib/systemd/system/cssef-server.service
	rm /usr/local/bin/cssef-server
	pip uninstall cssef-server -y

test:
	pylint cssefserver/ --errors-only
	pylint cssef-server --errors-only
	nosetests .