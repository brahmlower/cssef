Overview
========

The CSSEF repository is broken into several distinct components, each of which
is represented by directories at the root of the repository. The following is
a brief overview of each component. Continue on for more information about
each section.

CSSEF Server (CssefServer/)
	This is where the server side service and library lives. Like the client,
	all necessary resources for the server pip package are contained here.

CSSEF Client (CssefClient/)
	This is where the client application and library lives. This includes all
	resources needed for the pip package.

CSSEF Web Client (WebInterface/)
	This is a web client that depends on the client library to function. It
	serves the same purpose as the CLI client, but through a web interface. At
	this time, there are no package resources available.

Documentation (docs/)
	This directory contains all documentation resouces for the project.

Competition Plugins (plugins/)
	This directory is for the development of competition plugins to use with
	the CSSEF. At this time, it only houses code for the cssefcdc, which is
	largely composed of old code from the previous itterations of the scoring
	engine framework.
