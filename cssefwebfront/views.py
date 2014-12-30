from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.contrib import auth
from django.core.context_processors import csrf
from utils import UserMessages
from utils import getAuthValues
from models import Competition

def home(request):
	c = {}
	c["messages"] = UserMessages()
	c = getAuthValues(request, c)
	if c["auth_name"] == "auth_team_blue":
		c["competition_object"] = Competition.objects.get(compid = request.user.compid)
	return render_to_response('home.html', c)