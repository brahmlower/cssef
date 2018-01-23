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
    license = "MIT",

    # Packages:
    packages = ["cssefclient"],

    # Details:
    url = "http://github.com/bplower/cssef/",

    # Description:
    description = "A CSSEF client to interact with CSSEF servers via rpc.",
    long_description = open("README.md").read(),

    # Dependant packages
    install_requires = ["prettytable", "jsonrpcclient", "PyYAML"],
)
