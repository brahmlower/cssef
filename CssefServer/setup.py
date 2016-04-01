from setuptools import setup

setup(
	# Application name:
	name = "cssef-server",

	# Version number:
	version = "0.0.6",

	# Application author details:
	author = "Brahm Lower",
	author_email = "bplower@gmail.com",

	# Packages:
	packages = ["cssefserver"],

	# Details:
	url = "http://github.com/bplower/cssef/",

	# Scripts:
	scripts = [
		"cssefd"
	],

	data_files = [
		('/etc/cssef/', ['cssefd.yml']),
		('/var/log/cssef/', [])
	],

	# Description:
	description = "The CSSEF server.",
	long_description = open("README.md").read(),

	# Dependant packages:
	install_requires = [
		"sqlalchemy",
		"celery",
		"tokenlib"
	],
)
