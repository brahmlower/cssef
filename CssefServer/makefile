
install:
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

reinstall: uninstall install

clean:
	rm -f tests/*.pyc
	rm -f cssefserver/*.pyc
	rm -f .coverage

test:
	nosetests
