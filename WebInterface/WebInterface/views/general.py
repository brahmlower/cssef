from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response as renderToResponse
from django.shortcuts import render
from django.contrib import auth
from django.core.context_processors import csrf

def home(request):
	context = {}
	return renderToResponse('general/home.html', context)

def updates(request):
	context = {}
	return renderToResponse('general/updates.html', context)

def contact(request):
	context = {}
	return renderToResponse('general/contact.html', context)
