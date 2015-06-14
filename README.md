# Disclaimer #
This branch is for refactoring the project. Refactoring should hopefully make continued and future development easier.

# Description #
The Cyber Security Scoring Engine Framework (CSSEF) is meant to provide an easy to use framework with which to score cyber security competitions. Cyber security competitions are increasing in popularity, however preparation for such competitions can be difficult. The UAF CSC decided to make practice competitions to give members a feeling of what regional or national CCDC competitions would feel like. We were missing a feedback mechanism though, which is where the CSSEF comes in.

The CSSEF is meant to provide an easy to use interface for the competition managers and competitors (white and blue team respectively). Some of the features include:
* Automatic and/or manual inject delivery to blue teams
* Automatic or manual start of service scoring
* Blue team incident response field
* Blue team score board
* Team rankings by points
* Blue team service status (checks services each time the pages is loaded)
* Support for custom service plugins (write your own modules for services)

Future goals include the addition of interfaces for Red and Orange teams.

# Dependancies #
### WebInterface ###
* Python 2.7.5
* Django 1.7.2

### ScoringEngine ###
* Python 2.7.5
* Django 1.7.2
* celery 3.1.17
* django-celery 3.1.16

# Running for Development #
### Easy Run ###
For convienence, the script 'start_cssef' will start the web interface as well as the backend scoring engine. It assumes you are in the root level directory of the cssef project.
```
cd ~/cssef/
./start_cssef
```
### Running Manually ###
Starting everything manualy requires that the web interface and scoring engine be started seperately. Starting each component is similar to how you would start a normal django project that is still in development. As it stands, the port numbers are hardcoded into the settings files for each component, so if you change these, be sure the changes are reflected in the respective ```settings.py``` file.
```
cd ~/cssef/ScoringEngine/
python manage.py syncdb
python manage.py runserver 0.0.0.0:8000
```
Then open a new shell and and start the web frontend:
```
cd ~/cssef/WebInterface/
python manage.py syncdb
python manage.py runserver 0.0.0.0:8080
```

# Additional Documentation #
Further project documentation, including development documentation can be found on the projects wiki: https://github.com/bplower/cssef/wiki

# TODO #
#####Long Term#####
* Add Orange Team support
* Add Red Team support

#####Medium Term#####
* Seperate White Team and Site Admin pages and accounts
* View and score inject responses as white team
* Implement better error notification when user attempt to access blocked pages
* Test scoring a service from a White Team interface
* Add celery support
* Refactor to be a proper django site (too much stuff in the django root directory)

#####Short Term#####
* Add interface to modify general site information/content
* Add content to Service Statistics view for Blue Team
 * General statistics
* Finish content for Summary pages (Blue and White Teams)
* Finish content for Details pages (Blue and White Teams)
* Change networkaddr field in Team model (and surrounding code) to be CIDR or domain name
* Add unit tests
* Add integration tests
