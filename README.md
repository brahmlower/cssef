# Development Disclaimer #
The project is being refactored in the branch. The state of this project may change at any time - please do not assume anything here is stable.

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

# Aditional Documentation
Web API documentation is located in the  [README.md](https://github.com/bplower/cssef/blob/refactor/ScoringEngine/WebApi/README.md) file within the Web API folder.<br>
Project Planning is located in the [TODO.MD](https://github.com/bplower/cssef/blob/refactor/TODO.md) file.<br>
Older documentation can be found on the projects github [wiki](https://github.com/bplower/cssef/wiki). This documentation is older and may contain outdated and incomplete information.

# Dependancies #
### WebInterface ###
* Python 2.7.5
* Django 1.7.2

### ScoringEngine/WebAPI ###
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
