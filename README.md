# Description #
The Cyber Security Scoring Engine Framework (cssef) is meant to provide an easy to use framework with which to score cyber security competitions. There are two main components: the web frontend, and the backend scoring engine. The goal of the frontend is to give users (including competitors, competitions admins, and site admins) an easy to interface to interact with the the competitions white-team infrustrcture. For competitiors, this might extend only as far as viewing injects. Competition admins will be able to track competitor scores (and service status').

##Dependancies ##
Web Interface:
* Python 2.7.5
* Django 1.6.5

Pluggins:
* SSH - paramiko 1.15.1
* SMB - pysmb 1.1.13

# Usage #
The webfrontend is written using Django14. Starting the webserver (currently) requires running 'python manage.py runserver'. There are plans to create proper SystemV and SystemD service scripts. As of this writing, the scoring engine component must be started separately, at the time you wish to begin scoring (this will also change in the future).

## Web Interface ##
python manage.py syncdb
python runserver 0.0.0.0

## Scoring Engine ##
Please note that this has a very underdeveloped help menu.
The "help" menu id displayed when the first argument is invalid or not provided:
<pre><code>./cssef.py
Must provide an action {run|team|competition|service}</code></pre>
Run: Starts scoring the competition specified by ID (currently hardcoded)<br>
Team: team related actions<br>
Competition: Competition related actions<br>
Service: Service related actions<br>

Note that the actions were written before much of the web interface was written/functional, so some of it will be relatively redundant.

<pre><code>./cssef.py team
Did not match {dump|delete|create}</code></pre>
Dump: will list all ove the entries, showing the entries id and name<br>
Delete: Will delete an entrie based on the ID provided as the next argument<br>
Create: Will create an entry based on the arguments provided - all values must be provided on the same line (crazy weird, I know). The value for each column must be provided like <code>columnname=value</code>.

# Pluggins #
Pluggins are the modules that actually score the services you plan to score in your competition. Pluggins are just simple python modules, in which you write how to score the desired service. Each pluggin requires a 'score' method, that returns an integer of 0 or greater. If the service is scored as down, return 0 and if it's up, return some predefined value.

ScoringUtils.py has been written to simplify the development of pluggins. The following are the three classes it provides.
#####Pluggin#####
All pluggins should be children of this class. This ganrantees that each pluggin has these core values: 'points', 'net_type', 'subdomain', 'address' and 'default_port'. Additionally, 'build_address' is provided to get the full address for the team, regardless if they're being scored by dns or by an ipv4 address.

#####PlugginTest#####
This class handles the testing of the pluggin. It asks the user/tester for values that should be used for testing. These values are for the pluggin configuration overall, as well as specific configurations a team might have. Because the Pluggin.score() expects a Team object with score_configs, the Team class is emulated. This class provides EmulatedTeam, which only has score_configs, which holds the team specific configurations provided by the user/tester.

#####Score (being depricated mega-soon)#####
The score object should be returned by score(). This provides basic information that may be useful for loggin and scoring. This currently only provides the score (as 'value'), a boolean indicating if the score was successfull, as well as a success or error message. If an error was thrown, it will be included in 'error_msg'.

# TODO #
* pluggins/ScoringUtils should not have its over Score object (use cssefwebfront.models.Score)
* Add "organizations", which own competition objects
* Site administrators
 * authentication
 * login
 * logoff
* Organization administrators
 * authentication
 * login
 * logoff
* Make competitions deletable
* Make competitions editable (surprised I haven't already done this)
* Create inject display interface for competitors
 * Submit button for uploading inject responses
 * Handle and view responses via white team interface
* Genaric site modifications interface
 * Modify homepage content
 * Site link (top right corner)
* Improve documentation (it sorta sucks right?)
