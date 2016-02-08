from setuptools import setup
from setuptools import find_packages
#from cssefserver.api import version

setup(
	# Application name:
	name = "cssefserver",

	# Version number:
	version = "0.0.4",

	# Application author details:
	author = "Brahm Lower",
	author_email = "bplower@gmail.com",

	# Packages:
	packages = find_packages(),

	# Details:
	url = "http://github.com/bplower/cssef/",

	# Scripts:
	scripts = [
		"cssefserver/cssefd"
	],

	data_files = [
		('/etc/cssef/', ['cssefserver/cssefd.conf'])
	],

	# Description:
	description = "The CSSEF server.",
	long_description = open("README.md").read(),

	# Dependant packages:
	install_requires = [
		"sqlalchemy",
		"celery"
	],
)
