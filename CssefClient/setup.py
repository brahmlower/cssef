from setuptools import setup

setup(
	# Application name:
	name = "cssef-client",
	
	# Version number:
	version = "0.0.3",

	# Application author details:
	author = "Brahm Lower",
	author_email = "bplower@gmail.com",

	# License
	license = "GPL-3.0",

	# Packages:
	packages = ["cssefclient"],

	# Details:
	url = "http://github.com/bplower/cssef/",

	# Scripts:
	scripts = [
		'cssef-cli'
	],

	data_files = [
		('/etc/cssef/', ['cssef.yml'],)
	],

	# Description:
	description = "A CSSEF client to interact with CSSEF servers via rpc.",
	long_description = open("README.md").read(),

	# Dependant packages
	install_requires = ["prettytable", "jsonrpcclient", "PyYAML"],
)
