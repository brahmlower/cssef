# Description #
The Cyber Security Scoring Engine Framework (cssef) is meant to provide an easy to use framework with which to score cyber security competitions. There are two main components: the web frontend, and the backend scoring engine. The goal of the frontend is to give users (including competitors, competitions admins, and site admins) an easy to interface to interact with the the competitions white-team infrustrcture. For competitiors, this might extend only as far as viewing injects. Competition admins will be able to track competitor scores (and service status').

# Usage #
The webfrontend is written using Django14. Starting the webserver (currently) requires running 'python manage.py runserver'. There are plans to create proper SystemV and SystemD service scripts. As of this writing, the scoring engine component must be started separately, at the time you wish to begin scoring (this will also change in the future).

## cssef.py ##
Please note that this has a very underdeveloped help menu.
<pre><code>./cssef.py
Must provide an action {run|team|competition|service}</code></pre>
This is the output provided when cssef is run without any arguments. The run option will begin running the scoring engine. The rest of the options deal with interacting with the database. These extra actions were added before I finished writing the basic web frontend, that way I could test the scoring engine against objects stored in the database. These options may eventually be removed.
<pre><code>./cssef.py team
Did not match {dump|delete|create}</code></pre>
Providing team, competition or service as a first argument, with not further arguments will result in this output. Dump will show all the items in that table. Delete will delete an entry with the specified ID. Create will create a new entry in that table. The value for each column must be provided like <code>columnname=value</code>.

# Pluggins #
Pluggins are the modules that actually score the services you plan to score in your competition. Pluggins are just simple python modules, in which you write how to score the desired service. Each pluggin requires a 'score' method, that returns an integer of 0 or greater. If the service is scored as down, return 0 and if it's up, return some positive value.
# TODO #
* Improve current pluggins
* Implement Team and Site Admin authentication
* Create/Delete/List site and competition administrators
* Make teams deletable
* Make teams editable
* Make services editable
* Create inject display interface
* Interface to modify homepage content
* Non-hardcoded site link in top-right corner
