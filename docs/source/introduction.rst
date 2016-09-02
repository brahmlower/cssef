Introduction
============

.. attention::
	The project is still undergoing heavy development. As such, the state of
	the project may change at any time - please do not assume anything here
	is stable.

The Cyber Security Scoring Engine Framework (CSSEF) is an easy to use
framework for hosting security competitions. The primary purpose of the
framework has been to make scoring security competitions as simple as
possible, so that more time and energy may be spent setting up the
competition environment itself. Many of the features and requirements were
determined by the competitions hosted inhouse by the University of Alaska's
Cyber Security Club, which attended the National Cyber Collegdet Defense
Competition several years in a row. While initial development focused on
providing utilities for CCDC-like competitions, the project expanded to
facilitate other types of competitions as well, such as capture the flag
events.

Features
--------
Features include but are certainly not limited to the following. Please see
the respective section of documentation for more inforation on any particular
feature.

- Multiple organization
- Password and token based authentication
- Easy to use command line interface
- Modern(ish) web client
- Plugin interface for multiple types of competitions
- A prebuilt plugin for CCDC-like competitions (see the plugins section)

Framework Components
--------------------

Server
~~~~~~
This is where the bulk of the framework lives. The server provides facilities
to host various types of security related competitions. Those facilities are
consumed by plugins that use then to build some form of competition. This
means you can host a capture the flag competition and a CCDC-like competition
on the same service. The server communicates with the other clients via HTTP
RPC calls, and uses sqlalchemy for databasing. For additional information, see
the `server documentation`_.

.. _server documentation: server.rst

Client
~~~~~~
The client package provides endpoints for client applications (in the event
you want to write your own), as well as a command line tool. If you plan to
install the web client, this package will be a required depenancy. See the
`client documentation`_ for more information, or the `command line`_
documentation for cli reference.

.. _client documentation: client.rst
.. _command line: cli.rst

Web Client
~~~~~~~~~~
The web client is meant to be an easy and painless tool for interacting with
the server, as well as the various features provided by competition plugins-
especially when competitors may be submitting data during competition
environments that don't actually have the cssef client available. The web
client is currently using django, which itself simply consumes endpoints
within the cssef client. For more information about the web client, see the
cssef webui documentation.