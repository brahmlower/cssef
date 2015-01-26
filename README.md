# Disclaimer #
This project is still under heavy development. Feel free to use it, but know that it's state of operation may vary drastically from one commit to another. Once the project has reached a stable state, I'll create a stable branch for it.

# Description #
The Cyber Security Scoring Engine Framework (cssef) is meant to provide an easy to use framework with which to score cyber security competitions. There are two main components: the web frontend, and the backend scoring engine. The goal of the frontend is to give users (including competitors, competitions admins, and site admins) an easy to use interface to interact with the white-team infrastructure.

##Dependancies ##
Web Interface:
* Python 2.7.5
* Django 1.7.2

Pluggins:
* SSH - paramiko 1.15.1
* SMB - pysmb 1.1.13

# Usage #
The web frontend is written using Django. Starting the webserver (currently) requires running 'python manage.py runserver'. As of this writing, the scoring engine component must be started separately.

## Web Interface ##
<pre></code>
# These are paths set in settings.py
# These directories will eventually have to be created/verified at first run
mkdir -p cssefwebfront/resources/content/injects
mkdir cssefwebfront/resources/content/incidentresponse
mkdir cssefwebfront/resources/content/injectresponses
python manage.py syncdb
python runserver 0.0.0.0:80</code></pre>

Administrator authentication doesn't use the builtin user database yet. To create an administrator user, run the create_admin script in the projects root directory. The first argument is the admin username and the second argument is the admins password (plaintext right now...)
<pre><code>./create_admin admin admin</code></pre>

## Scoring Engine ##
To start the scoring engine, simply provide the competition ID or competition name for the competition you'd like to begin scoring.

Providing the competition ID:
<pre>$ ./cssef.py 1</pre>

Providing the competition name:
<pre>$ ./cssef.py "Test Cyber Security Competition"</pre>

Running the script with no arguments or incorrect arguments will present the usage:
<pre>$ ./cssef.py 
Usage:
	./cssef.py [competition id (integer)]
	./cssef.py [competition name (string)]
</pre>

As this project is developed, the scoring engine will check and react to various competition settings. There are currently 5 main aspects to the competition that are checked:
 * The competition has scoring enabled
  * Fails if if scoring is disabled
 * The competition has teams
  * Fails if there are no teams
 * The competition has services
  * Fails if there are no services
 * Checks if the competition start time has been reached
  * Will sleep until the datetime the competition is set to start, then begin scoring
 * Checks if the competition finish time has been reached
  * Stops scoring services and exits

Once celery support has been implemented, the scoring engine won't have to be manually started. In that case, the scoring engine will automatically start once the competitions start time has been reached, and score for the duration of the competition.

# Pluggins #
Pluggins are the modules that score the services you plan to track in your competition. Pluggins are just simple python modules containing the code to score the desired service. Each pluggin requires a 'score' method, that returns an integer of 0 or greater. If the service is scored as down, return 0 and if it's up, return some predefined value.

ScoringUtils.py has been written to simplify the development of pluggins. The following are the two classes it provides.
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
