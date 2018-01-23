from setuptools import setup

setup(
    # Application name:
    name = "cssef-server",

    # Version number:
    version = "0.0.6",

    # Application author details:
    author = "Brahm Lower",
    author_email = "bplower@gmail.com",

    # License
    license = "MIT",

    # Packages:
    packages = ["cssefserver"],

    # Details:
    url = "http://github.com/bplower/cssef/",

    # Description:
    description = "The CSSEF server.",
    long_description = open("README.md").read(),

    # Dependant packages:
    install_requires = [
        "bcrypt",
        "sqlalchemy",
        "tokenlib",
        "jsonrpcserver",
        "PyYAML"
    ],
)
