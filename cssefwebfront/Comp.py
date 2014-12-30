from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth import authenticate
from django.core.context_processors import csrf
from django.core.files.uploadedfile import UploadedFile
from models import Competition
from models import InjectResponse
from models import Service
from models import Inject
from models import Score
from models import Team
from forms import TeamLoginForm
from forms import InjectResponseForm
import settings
from utils import UserMessages
from utils import getAuthValues
from django.utils import timezone

def login(request):
	"""
	Page for teams to login to for a competition
	"""
	c = {}
	c["messages"] = UserMessages()
	c = getAuthValues(request, c)
	c.update(csrf(request))
	# Checks if the user is submitting the form, or requesting the form
	if request.method != "POST":
		c["form"] = {'login': TeamLoginForm()}
		return render_to_response('Comp/login.html', c)
	teamname = request.POST.get('teamname')
	password = request.POST.get('password')
	compid = request.POST.get('compid')
	team = authenticate(teamname = teamname, password = password, compid = compid)
	if team == None:
		c["messages"].new_info("Incorrect team credentials.", 4321)
		return render_to_response('Comp/login.html', c)
	auth.login(request, team)
	competition = Competition.objects.get(compid = compid)
	print competition.compurl
	return HttpResponseRedirect("/competitions/%s/summary/" % competition.compurl)

def logout(request, competition = None):
	"""
	Page for teams to logout of a competition
	"""
	c = {}
	c["messages"] = UserMessages()
	c = getAuthValues(request, c)
	if c["auth_name"] != "auth_team_blue":
		print "Cannot sign you out of something you're not logged in as."
	else:
		auth.logout(request)
	return HttpResponseRedirect("/")

def list(request):
	"""
	Display list of competitions
	"""
	c = {}
	c["messages"] = UserMessages()
	c = getAuthValues(request, c)
	c["competition_list"] = Competition.objects.all()
	return render_to_response('Comp/list.html', c)

def summary(request, competition = None):
	"""
	Display summary information for selected competition
	"""
	current_url = request.build_absolute_uri()
	if request.build_absolute_uri()[-8:] != "summary/":
		return HttpResponseRedirect(current_url + "summary/")
	c = {}
	c["messages"] = UserMessages()
	c["competition_object"] = Competition.objects.get(compurl = competition)
	c = getAuthValues(request, c)
	return render_to_response('Comp/summary.html', c)

def details(request, competition = None):
	"""
	Display details about the selected competition
	"""
	c = {}
	c["messages"] = UserMessages()
	c["competition_object"] = Competition.objects.get(compurl = competition)
	c = getAuthValues(request, c)
	c["services"] = Service.objects.filter(compid = c["competition_object"].compid)
	c["teams"] = Team.objects.filter(compid = c["competition_object"].compid)
	return render_to_response('Comp/details.html', c)

def rankings(request, competition = None):
	"""
	Display team rankings for selected competition
	"""
	c = {}
	c["messages"] = UserMessages()
	c["competition_object"] = Competition.objects.get(compurl = competition)
	c = getAuthValues(request, c)
	c["ranks"] = []
	team_objs = Team.objects.filter(compid = c["competition_object"].compid)
	for i in team_objs:
		scores_objs = Score.objects.filter(compid = c["competition_object"].compid, teamid=i.teamid)
		total = 0
		for k in scores_objs:
			total += k.value
		c["ranks"].append({"team": i.teamname, "score": total, "place":0})		
	return render_to_response('Comp/rankings.html', c)

def injects(request, competition = None):
	"""
	Display inject list for selected competition
	"""
	c = {}
	c["messages"] = UserMessages()
	c["competition_object"] = Competition.objects.get(compurl = competition)
	c = getAuthValues(request, c)
	if c["auth_name"] != "auth_team_blue":
		return render_to_response('Comp/injects.html', c)
	c["injects"] = Inject.objects.filter(compid = c["competition_object"].compid, dt_delivery__lte = timezone.now())
	return render_to_response('Comp/injects.html', c)

def injects_respond(request, competition = None, ijctid = None):
	"""
	Displays a specific inject and provides either upload or text entry for inject response
	"""
	c = {}
	c["messages"] = UserMessages()
	c["competition_object"] = Competition.objects.get(compurl = competition)
	c = getAuthValues(request, c)
	if c["auth_name"] != "auth_team_blue":
		return render_to_response('Comp/injects.html', c)
	c.update(csrf(request))
	# If we're not getting POST data, serve the page normally
	if request.method != "POST":
		c["inject"] = Inject.objects.get(compid = c["competition_object"].compid, ijctid = ijctid)
		c["responses"] = InjectResponse.objects.filter(compid = c["competition_object"].compid, teamid = request.user.teamid, ijctid = ijctid)
		c["responseform"] = InjectResponseForm()
		return render_to_response('Comp/injects_view_respond.html', c)
	# Determine if we're handling text entry or file upload
	ijct_resp_obj = InjectResponse()
	ijct_resp_obj.compid = c["competition_object"].compid
	ijct_resp_obj.teamid = request.user.teamid
	ijct_resp_obj.ijctid = int(ijctid)
	# Checks if we were given a file
	try:
		# Handle necessary file manipulation
		print request.FILES
		uf = UploadedFile(request.FILES['docfile'])
		dest_filepath = settings.BASE_DIR + "/" + uf.name
		wfile = open(dest_filepath, "w")
		wfile.write(uf.read())
		wfile.close()
		# Fill out file related parts of the model
		ijct_resp_obj.isfile = True
		ijct_resp_obj.filename = uf.name
		ijct_resp_obj.filepath = dest_filepath
	except KeyError:
		print "no file was uploaded"
	# Checks if we were given text
	form = InjectResponseForm(request.POST)
	if  form.is_valid():
		ijct_resp_obj.istext = True
		ijct_resp_obj.textentry = form.cleaned_data['textentry']
	#TODO: Have some way of telling user they need to add input before they may submit
	if ijct_resp_obj.istext or ijct_resp_obj.isfile:
		ijct_resp_obj.save()
	return HttpResponseRedirect('/competitions/%s/injects/%s/' % (competition, ijctid))


def servicestatus(request, competition = None):
	"""
	Display current service status for selected team in selected competition
	"""
	c = {}
	c["messages"] = UserMessages()
	c["competition_object"] = Competition.objects.get(compurl = competition)
	c = getAuthValues(request, c)
	if c["auth_name"] != "auth_team_blue":
		return render_to_response('Comp/servicestatus.html', c)
	return render_to_response('Comp/servicestatus.html', c)

def servicetimeline(request, competition = None):
	"""
	Display status timeline of services for selected team in selected competition
	"""
	c = {}
	c["messages"] = UserMessages()
	c["competition_object"] = Competition.objects.get(compurl = competition)
	c = getAuthValues(request, c)
	if c["auth_name"] != "auth_team_blue":
		return render_to_response('Comp/servicetimeline.html', c)
	return render_to_response('Comp/servicetimeline.html', c)

def scoreboard(request, competition = None):
	"""
	Display the list of scores for the selected team of the selected competition
	"""
	c = {}
	c["messages"] = UserMessages()
	c["competition_object"] = Competition.objects.get(compurl = competition)
	c = getAuthValues(request, c)
	if c["auth_name"] != "auth_team_blue":
		return render_to_response('Comp/scoreboard.html', c)
	c["scores"] = []
	score_obj_list = Score.objects.filter(compid = c["competition_object"].compid, teamid = request.user.teamid)
	for i in score_obj_list:
		score_obj_dict = {}
		score_obj_dict["time"] = i.datetime
		score_obj_dict["name"] = Service.objects.get(servid = i.servid).name
		score_obj_dict["value"] = i.value
		c["scores"].append(score_obj_dict)
	return render_to_response('Comp/scoreboard.html', c)

def incidentresponse(request, competition = None):
	"""
	Provides a submission portal for selected team of selected competition to submit incident responses
	"""
	c = {}
	c["messages"] = UserMessages()
	c["competition_object"] = Competition.objects.get(compurl = competition)
	c = getAuthValues(request, c)
	if c["auth_name"] != "auth_team_blue":
		return render_to_response('Comp/incidentresponse.html', c)
	return render_to_response('Comp/incidentresponse.html', c)
