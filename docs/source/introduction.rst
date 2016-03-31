Cyber Security Scoring Engine Framework 
=======================================

.. attention::
	The project is still undergoing heavy development. As such, the state of the project may change at any time - please do not assume anything here is stable.

The Cyber Security Scoring Engine Framework (CSSEF) is an easy to use framework for hosting security competitions. The primary purpose of the framework has been to make scoring security competitions as simple as possible, so that more time and energy may be spent setting up the competition environment itself. Many of the features and requirements were determined by the competitions hosted inhouse by the University of Alaska's Cyber Security Club, which attended the National Cyber Collegdet Defense Competition several years in a row. While initial development focused on providing utilities for CCDC-like competitions, the project expanded to facilitate other types of competitions as well, such as capture the flag events.

Features
--------
Features include but are certainly not limited to the following. Please see the respective section of documentation for more inforation on any particular feature.

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
This is where the bulk of the framework lives. The server provides facilities to host various types of security related competitions. Those facilities are consumed by additional modules that use them to build some form of competitions. This means you can host a capture the flag competition right next to a CCDC-like competition. The server communicates with the other clients via rabbitmq, and uses sqlalchemy for databasing. It is a standalone service and can operate without any other parts of the project being installed. For additional information, see the cssefserver documentation.

Client
~~~~~~
The client package provides endpoints for client applications (in the event you want to write your own), as well as a command line tool. If you plan to install the web client, this package will be required beforehand. For more information on using the command line utility, see the cssef-cli documentation.

Web Client
~~~~~~~~~~
The web client is meant to be an easy and painless tool for interacting with the server, as well as the various features provided by competition plugins- especially when competitors may be submitting data during competition environments that don't actually have the cssef client available. The web client is currently using django, which itself simply consumes endpoints within the cssef client. For more information about the web client, see the cssef webui documentation.

Web API
~~~~~~~
..note::
	Work on the web API has been halted until the server and client have reached a decently stable state.

The web API is intended to be provided in situations where one may want to provide a proxy to the cssef server for another frontend application that cannot itself have the client application installed on it. Eventually, the CSSEF client will be able to consume endpoints provided by the web API.