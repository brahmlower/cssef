Documentation
=============

Sphinx is used for documentation, and is hosted through Read The Docs. New
commits to the repository will update the live documentation.

The autodoc extension for Sphinx is used to create reference documentation
from docstrings throughout the code. This helps to enforce proper code
documentation practices.

Local Review
------------

Documentation can be automatically built and hosted using `sphinx-autobuild`_.
I've set up an option in the makefile to watch the whole project (excluding
the documentation build directory, and the autodocs directory), that way we
don't have to remember how to propery run sphinx-autobuild. All you have to do
is run the following command:

.. _sphinx-autobuild: https://pypi.python.org/pypi/sphinx-autobuild

::

	user@debian:~/cssef/docs$ make livehtml
