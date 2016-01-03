from django.http import HttpResponseRedirect
from django.contrib import auth

from WebInterface.context import BaseContext
from WebInterface.utils import getContext

def home(request):
	return getContext(BaseContext, "home.html", request)

def updates(request):
	return getContext(BaseContext, "updates.html", request)

def contact(request):
	return getContext(BaseContext, "contact.html", request)

def logout(request):
	auth.logout(request)
	return HttpResponseRedirect("/")
