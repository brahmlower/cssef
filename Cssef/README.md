# CSSEF Server/Client

## Server Setup
Set up a user within rabbitmq for the framework:
```
rabbitmqctl add_user cssefd cssefd-pass
rabbitmqctl set_user_tags cssefd administrator
rabbitmqctl set_permissions cssefd ".*" ".*" ".*"
```

Set the celery configurations accordingly in the cssefd.conf file:
```
rpc_username = cssefd
rpc_password = cssefd-pass
rpc_host = localhost

amqp_username = cssefd
amqp_password = cssefd-pass
amqp_host = localhost
```

Start the service:
```
./cssefd.py start
```

## Client Setup
