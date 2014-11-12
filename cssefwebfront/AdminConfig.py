from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.contrib import auth
from django.core.context_processors import csrf

from forms import CreateCompetitionForm
from forms import AdminLoginForm
from forms import CreateTeamForm
from forms import CreateServiceForm
from models import Competition
from models import Service
from models import Team

class UserMessages:
	def __init__(self):
		self.info = []
		self.error = []
		self.success = []
	def new_info(self, string, num):
		self.info.append({"string":string, "num":num})

	def new_error(self, string, num):
		self.error.append({"string":string, "num":num})

	def new_success(self, string, num):
		self.success.append({"string":string, "num":num})

	def clear(self):
		self.info = []
		self.error = []
		self.success = []

def home(request):
	"""
	Page displayed after loggin in
	"""
	return render_to_response('AdminConfig/home.html')

def login(request):
	"""
	Page for admins to login to for competition management
	"""
	c = {}
	c["messages"] = UserMessages()
	c["form"] = {'login': AdminLoginForm()}
	# Checks if the user is submitting the form, or requesting the form
	if request.method != "POST":
		c.update(csrf(request))
		return render_to_response('AdminConfig/login.html', c)
	login = AdminLoginForm(request.POST)
	# Checks that the submitted form data is valid
	if not login.is_valid():
		c["messages"].new_error("Invalid field data in competition form.", 1003)
		return render(request, 'AdminConfig/login.html', c)

	# Lol I don't actually check the creds :P
	return render_to_response('AdminConfig/home.html', c)

def site_config(request):
	"""
	Displays configuration options for the overall site
	"""
	c = {}
	c["messages"] = UserMessages()
	return render_to_response('AdminConfig/home.html', c)

def users_list(request):
	"""
	Displays site or competition administrative users
	"""
	return render_to_response('AdminConfig/users_list.html')

def users_edit(request):
	"""
	Edit a site or competition administrative user
	"""
	return render_to_response('AdminConfig/users_edit.html')

def users_delete(request):
	"""
	Delete site or competition administrative users
	"""
	return HttpResponseRedirect('/admin/users/')

def users_create(request):
	"""
	Create site or competition administrative users
	"""
	return render_to_response('AdminConfig/users_create.html')

