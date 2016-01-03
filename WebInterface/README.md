# CSSEF WebInterface
## Installation and Setup
This django project doesn't have any sort of proper installer yet. For the time being (while it's in development), just run it as a development django site. The following packages are required to run the django site:
* Django 1.7.9
* cssefclient 0.0.2 (see installation instructions [here](https://github.com/bplower/cssef/tree/refactor/CssefClient#installing))

NOTE: While installing the client, verify that you are able to talk to the cssefserver. If you have not set up the cssef server, follow the installation proceedure [here](https://github.com/bplower/cssef/tree/refactor/Cssef#installation-and-setup).

Sync the local database and then start the server.
```
user@host:~$ git clone https://github.com/bplower/cssef.git
user@host:~$ cd cssef/WebInterface
user@host:~/cssef/WebInterface$ python manage.py syncdb
user@host:~/cssef/WebInterface$ python runserver 0.0.0.0:8000
```

You should see the following once you browse to the site.
![Home page](http://i.imgur.com/Fx4sjyb.png)

## Usage
For the time being, there is no authentication - this is simply due to the unfinished project refactoring. You will have to browse directly to the various pages. To start, go to the /admin page and create an organization. Once created, you will be able to browse to the organization at /organization/your_org_url. From there, you can begin to see how members and competitions can be managed.