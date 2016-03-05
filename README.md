# Cyber Security Scoring Engine Framework 

[![Build Status](https://travis-ci.org/bplower/cssef.svg?branch=refactor)](https://travis-ci.org/bplower/cssef)
[![Join the chat at https://gitter.im/bplower/cssef](https://badges.gitter.im/bplower/cssef.svg)](https://gitter.im/bplower/cssef?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)


## Development Disclaimer
The project is being refactored in this branch. The state of this project may change at any time - please do not assume anything here is stable. The master branch contains a slightly more stable build, but it is seriously outdated, and considerably more convoluted.

## Description
The Cyber Security Scoring Engine Framework (CSSEF) is meant to provide an easy to use framework with which to score cyber security competitions. Cyber security competitions are increasing in popularity, however preparation for such competitions can be difficult. The UAF CSC decided to make practice competitions to give members a feeling of what regional or national CCDC competitions would feel like. We were missing a feedback mechanism though, which is where the CSSEF comes in.

The CSSEF is meant to provide an easy to use interface for the competition managers and competitors (white and blue team respectively). Some of the features include:
* Automatic and/or manual inject delivery to blue teams
* Automatic or manual start of service scoring
* Blue team incident response field
* Blue team score board
* Team rankings by points
* Blue team service status (checks services each time the pages is loaded)
* Support for custom service plugins (write your own modules for services)

Future goals include the addition of interfaces for Red and Orange teams.

## Documentation
Project Planning is located in the [TODO.MD](https://github.com/bplower/cssef/blob/refactor/TODO.md) file.<br>

The project is broken up into several main parts:
* CssefServer
* CssefClient
* WebApi
* WebInterface

### CssefServer
This is the primary backend for the framework. It receives messages via rabbitmq and celery. It is a standalone service and can operate without any other parts of the project being installed. For more information, see the CssefServer Documentation.

### CssefClient
This is the primary python and command line client for the framework. This package provides the python client, as well as a command line client. Once installed, you will be able to interact with the server through the commandline utility, or install and run the WebApi or WebInterface. For more information, see the CssefClient Documentation.

### WebApi
The webapi provides a json api to interact with the server through. For more information, see the [WebApi Documentation](https://github.com/bplower/cssef/blob/refactor/ScoringEngine/WebApi/README.md).

### WebInterface
The webinterface is the primary interface for interacting with the cssef server. For more information, see the WebInterface Documentation.
