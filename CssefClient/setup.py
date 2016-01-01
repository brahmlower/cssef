from setuptools import setup
from cssefclient import cssefclient 
setup(
	# Application name:
	name = "cssefclient",
	
	# Version number:
	version = cssefclient.version,

	# Application author details:
	author = "Brahm Lower",
	author_email = "bplower@gmail.com",

	# Packages:
	packages = ["cssefclient"],

	# Details:
	url = "http://github.com/bplower/cssef/",

	# Scripts:
	scripts = [
		'cssefclient/cssef-cli'
	],

	data_files = [
		('/etc/cssef/', ['cssefclient/cssef.conf'],)
	],

	# Description:
	description = "A CSSEF client to interact with CSSEF servers via Celery.",
	long_description = open("README.md").read(),

	# Dependant packages
	install_requires = [
		"prettytable",
		"celery",
	],
)
