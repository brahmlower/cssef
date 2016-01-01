# CSSEF Server

## Installation and Setup
### Rabbitmq
Install the server and make sure it is enabled and running
```
user@host:~$ sudo apt-get install rabbitmq-server
user@host:~$ sudo systemctl enable rabbitmq-server.service
Executing /usr/sbin/update-rc.d rabbitmq-server defaults
Executing /usr/sbin/update-rc.d rabbitmq-server enable
user@host:~$ sudo systemctl status rabbitmq-servier.service | grep Active:
   Active: active (running) since Fri 2016-01-01 00:33:07 AKST; 13min ago
```

Now add a new user within rabbitmq for the cssef server and clients
```
user@host:~$ rabbitmqctl add_user cssefd-user cssefd-pass
user@host:~$ rabbitmqctl set_user_tags cssefd-user administrator
user@host:~$ rabbitmqctl set_permissions cssefd-user ".*" ".*" ".*"
```

### CSSEF Server
Now clone the cssef repo and install the server via pip. The pip package is called 'cssefserver'.
```
user@host:~$ git clone https://github.com/bplower/cssef.git
user@host:~$ cd cssef/Cssef
user@host:~/cssef/Cssef$ sudo pip install .
```

If you see an error "fatal error: Python.h: No such file or directory" while the package is installing sqlalchemy, it's most likely because you don't have the python headers installed.
```
sudo pip uninstall sqlalchemy
sudo apt-get install python-dev
sudo pip install .
```

Be sure to set the rabbitmq username and password in the celery section of the config file located at /etc/cssef/cssefd.conf.
```
rpc_username = cssefd-user
rpc_password = cssefd-pass
rpc_host = localhost

amqp_username = cssefd-user
amqp_password = cssefd-pass
amqp_host = localhost
```

# Usage
Installing the cssefserver package will provide the 'cssefd' utility, which can be used to start and stop the server.

Start the service:
```
user@host:~$ cssefd
usage: cssefd start|stop|restart|status
user@host:~$ ssefd start
user@host:~$ cssefd status
Running with pid 11231
```