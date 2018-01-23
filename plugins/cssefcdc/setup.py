from setuptools import setup
from setuptools import find_packages

setup(
	# Application name:
	name = "cssef-cdc",

	# Version number:
	version = "0.0.1",

	# Application author details:
	author = "Brahm Lower",
	author_email = "bplower@gmail.com",

	# License
	license = "MIT",

	# Packages:
	packages = ['cssefcdc'],

	# Details:
	url = "http://github.com/bplower/cssef/",

	# Scripts:
	scripts = [],
	data_files = [],

	# Description:
	description = "A CSSEF plugin for CCDC-like competitions.",
	long_description = open("README.md").read(),

	# Dependant packages:
	install_requires = ["ipaddr", "sqlalchemy", "cssef-server"],
)
