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
The webfrontend is written using Django14. Starting the webserver (currently) requires running 'python manage.py runserver'. As of this writing, the scoring engine component must be started separately, at the time you wish to begin scoring.

## Web Interface ##
<pre></code>python manage.py syncdb
python runserver 0.0.0.0</code></pre>

Administrator authentication doesn't use the builtin user database yet. To create an administroator user, run the create_admin script in the projects root directory. The first argument is the admin username and the second argument is the admins password (plaintext right now, I know...)
<pre><code>./create_admin admin admin</code></pre>

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
* 'points' is a nonnegative integer value. Keep in mind 0 indicates the service failed the scoring criteria.
* 'net_type' indicates how the service should be scored: via ipaddress or by domain name. The two accepted values are 'ipaddress' and 'domainname'
* 'subdomain' is the subdomain to use to reach the service. In the case of testing a webserver at www.example.com, the subdomain value would be set to 'www'
* 'address' is the eqivalent of subdomain, but for the ipaddress. If you expected to reach the service at 192.168.1.100, the value of address would be '100'
* 'default_port' is the port number you would by default expect to find the service on. When scoring a website, this would be set to 80. This can be overwritten by the team configs, should a team change the port on which they serve the site.

#####PlugginTest#####
This class handles the testing of the pluggin. It asks the user/tester for values that should be used for testing. These values are for the pluggin configuration overall, as well as specific configurations a team might have. Because the Pluggin.score() expects a Team object with score_configs, the Team class is emulated. This class provides EmulatedTeam, which only has score_configs, which holds the team specific configurations provided by the user/tester.

To run a test, start a python shell from the projects root directory. Import the pluggin you'd like to test, then call its Test class. Answer the prompted questions, and and then it will test the pluggin

<pre></code>$ python
Python 2.7.5 (default, Mar  9 2014, 22:15:05) 
[GCC 4.2.1 Compatible Apple LLVM 5.0 (clang-500.0.68)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> import pluggins.HTTP as HTTP
>>> HTTP.Test()

General service pluggin configurations.
Please enter a value for 'points': 100
Please enter a value for 'net_type': ipaddress
Please enter a value for 'subdomain': www
Please enter a value for 'address': 109
Please enter a value for 'default_port': 80

Team specific pluggin configurations.
Please enter a(n) 'int' for 'port': 80
Please enter a(n) 'int' for 'timeout': 2
Please enter a(n) 'str' for 'network': 192.168.0

[2014-12-29 09:53:56.579363+00:00] Team:n/a Service:n/a Value:100 Messages:
</code></pre>

# TODO #
#####Long Term#####
* Add Orange Team support
* Add Red Team support

#####Medium Term#####
* Seperate White Team and Site Admin pages and accounts
* View and score inject responses as white team
* Implement better error notification when user attempt to access blocked pages
* Test scoring a service from a White Team interface

#####Short Term#####
* Add interface to edit competition details
* Add interface to modify general site information/content
* Add content to Service Timeline view for Blue Team
 * General statistics
* Finish content for Summary pages (Blue and White Teams)
* Finish content for Details pages (Blue and White Teams)
* Change networkaddr field in Team model (and surrounding code) to be CIDR or domain name
