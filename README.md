# Disclaimer #
The project was not written with clean code, making further development difficult and time consuming. I'm refactoring in this branch, which will eventually overwrite the content of the master branch. Refactoring should hopefully make continued and future development easier.

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

# Framework #
The project is now broken into two main pieces: the scoring engine and the web interface.

## Scoring Engine ##
To keep the framework mentality, the scoring engine is strictly the engine tracking scores and points. It provides some other functionality such as inject and incident response tracking and scoring, however these features can be disabled if all you want is the scoring mechanics. Within the ScoringEngine class, there is a WebApi class which provides a semi-RESTful JSON API. If you already have your own frontend interface, or want to write your own, you can use the WebApi bindings to pupulate the content on your interface. Further documentation on the API can be found below.

### Dependancies ###
* Python 2.7.5
* celery 3.1.17
* Django 1.7.2
* django-celery 3.1.16

### Usage ###
#### Development ####
```
python manage.py syncdb
python manage.py runserver 0.0.0.0:8081
```
#### Production ####
Since the project hasn't reached a stable release, there are no instructions for running it in a production grade manner.

## Web Interface ##
The web interface aims to provide an out-of-the-box working tool with which to interact with the scoring engine. The web interface has various pages for site/service administrators, organization users (white team) and competitors (blue team). The web interface will grow to support additional functionality as it's added to the scoring engine.

### Dependancies ###
* Python 2.7.5
* Django 1.7.2

### Usage ###
#### Development ####
```
python manage.py syncdb
python manage.py runserver 0.0.0.0:8080
```
#### Production ####
Since the project hasn't reached a stable release, there are no instructions for running it in a production grade manner.

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
