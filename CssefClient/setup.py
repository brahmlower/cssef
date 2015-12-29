from setuptools import setup
from CssefClient import cssefclient 
setup(
	# Application name:
	name = "CssefClient",
	
	# Version number:
	version = cssefclient.version,

	# Application author details:
	author = "Brahm Lower",
	author_email = "bplower@gmail.com",

	# Packages:
	packages = ["CssefClient"],

	# Details:
	url = "http://github.com/bplower/cssef/",

	# Scripts:
	scripts=[
		'CssefClient/cssef-cli'],

	data_files=[
		('/etc/cssef/', ['CssefClient/conf/cssef.conf'],)
	],

	# Description:
	description = "A CSSEF client to interact with CSSEF servers via Celery.",
	long_description = open("README.md").read(),

	# Dependant packages
	install_requires=[
		"prettytable",
		"celery",
	],
)
