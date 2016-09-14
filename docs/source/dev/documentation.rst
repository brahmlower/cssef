Documentation
=============

Sphinx is used for documentation, and is hosted through Read The Docs. New
commits to the repository will update the live documentation.

The autodoc extension for Sphinx is used to create reference documentation
from docstrings throughout the code. This helps to enforce proper code
documentation practices.

Building the docs
-----------------

Building the documentation relies on sphinx and the sphinx rtd theme, but I
also highly recommend installing sphinx-autobuild.
::

	user@debian:~$ pip install sphinx sphinx-rtd-theme sphinx-autobuild

The documentation can be built manually or automatically. I'm lazy so I
suggest using the automatic method, but I'll cover the manual process anyway.

Building Manually
-----------------

The makefile in the root of the ``docs`` folder is a lightly modified version
of the standard makefile that comes with sphinx, so if you're familiar with
sphinx, the process is the same.
::

	user@debian:~/cssef/docs$ make html

And that's it! The resulting html files will be located within docs/build/html.
From time to time, you may want to run a ``make clean`` before rebuilding the
documentation, just to make sure everything is fresh and up to date.

Building Automatically
----------------------

Documentation can be automatically built and locally served using
`sphinx-autobuild`_. I've set up an option in the makefile to watch the whole
project (excluding the documentation build directory, and the autodocs
directory), that way we don't have to remember how to propery run
sphinx-autobuild. All you have to do is run the following command:

.. _sphinx-autobuild: https://pypi.python.org/pypi/sphinx-autobuild

::

	user@debian:~/cssef/docs$ make livehtml
