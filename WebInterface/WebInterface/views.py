from django.http import HttpResponseRedirect
from django.contrib import auth

from WebInterface.context import BaseContext
from WebInterface.utils import getContext

def home(request):
	return getContext(BaseContext, request, page_template = "home.html")

def updates(request):
	return getContext(BaseContext, request, page_template = "updates.html")

def contact(request):
	return getContext(BaseContext, request, page_template = "contact.html")

def logout(request):
	auth.logout(request)
	return HttpResponseRedirect("/")
