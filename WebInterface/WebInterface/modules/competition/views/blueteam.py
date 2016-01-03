from django.http import HttpResponseRedirect
from django.http import HttpResponseForbidden
from django.http import HttpResponseBadRequest
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.contrib import auth
from django.core.context_processors import csrf
#from django.core.files.uploadedfile import UploadedFile
from django.utils import timezone
# from models import Competition
# from models import InjectResponse
# from models import IncidentResponse
# from models import Document
# from models import Service
# from models import Inject
# from models import Score
# from models import Team
# from forms import TeamLoginForm
# from forms import InjectResponseForm
# from forms import IncidentResponseForm
# from forms import IncidentResponseReplyForm
# from forms import ServiceSelectionForm
# from utils import get_inject_display_state
# from utils import UserMessages
# from utils import getAuthValues
# from utils import save_document
#from hashlib import md5
#from cssef import LoadServs
#import settings

templatePathPrefix = "organization/templates/"

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
	username = request.POST.get('username')
	password = request.POST.get('password')
	compid = request.POST.get('compid')
	team = auth.authenticate(username = username, password = password, compid = compid)
	if team == None:
		c["messages"].new_info("Incorrect team credentials.", 4321)
		c["form"] = {'login': TeamLoginForm()}
		return HttpResponseBadRequest(render_to_string(templatePathPrefix + 'login.html', c))
	auth.login(request, team)
	competition = Competition.objects.get(compid = compid)
	return HttpResponseRedirect("/competitions/%s/summary/" % competition.compurl)

def logout(request, competition = None):
	"""
	Page for teams to logout of a competition
	"""
	c = getAuthValues(request, {})
	if c["auth_name"] == "auth_team_blue":
		auth.logout(request)
	return HttpResponseRedirect("/")

def summary(request, competition = None):
	"""
	Display summary information for selected competition
	"""
	current_url = request.build_absolute_uri()
	if request.build_absolute_uri()[-8:] != "summary/":
		return HttpResponseRedirect(current_url + "summary/")
	c = getAuthValues(request, {})
	c["comp_obj"] = Competition.objects.get(compurl = competition)
	c["services"] = Service.objects.filter(compid = c["comp_obj"].compid)
	c["teams"] = Team.objects.filter(compid = c["comp_obj"].compid)
	return render_to_response(templatePathPrefix + 'summary.html', c)

def details(request, competition = None):
	"""
	Display details about the selected competition
	"""
	c = getAuthValues(request, {})
	c["comp_obj"] = Competition.objects.get(compurl = competition)
	c["services"] = Service.objects.filter(compid = c["comp_obj"].compid)
	c["teams"] = Team.objects.filter(compid = c["comp_obj"].compid)
	return render_to_response(templatePathPrefix + 'details.html', c)

def ranking(request, competition = None):
	"""
	Display team rankings for selected competition
	"""
	c = getAuthValues(request, {})
	c["comp_obj"] = Competition.objects.get(compurl = competition)
	# If the view is disabled
	if not c["comp_obj"].teams_view_ranking_enabled:
		c["message"] = "This feature is disabled for this competition."
		return HttpResponseForbidden(render_to_string('status_400.html', c))
	c["ranks"] = []
	team_objs = Team.objects.filter(compid = c["comp_obj"].compid)
	for i in team_objs:
		scores_objs = Score.objects.filter(compid = c["comp_obj"].compid, teamid = i.teamid)
		total = 0
		for k in scores_objs:
			total += k.value
		c["ranks"].append({"team": i.teamname, "score": total, "place":0})		
	return render_to_response(templatePathPrefix + 'rankings.html', c)

def injects(request, competition = None):
	"""
	Display inject list for selected competition
	"""
	c = getAuthValues(request, {})
	# If the user isn't authed as a Blue Team
	if c["auth_name"] != "auth_team_blue":
		c["message"] = "You must log in as a Blue Team to view this page."
		return HttpResponseForbidden(render_to_string('status_400.html', c))
	c["comp_obj"] = Competition.objects.get(compurl = competition)
	# If the view is disabled
	if not c["comp_obj"].teams_view_injects_enabled:
		c["message"] = "This feature is disabled for this competition."
		return HttpResponseForbidden(render_to_string('status_400.html', c))
	c["inject_list"] = []
	for i in Inject.objects.filter(compid = request.user.compid, dt_delivery__lte = timezone.now()):
		c["inject_list"].append({
			"inject": i,
			"files": Document.objects.filter(inject = i),
			"display_state": get_inject_display_state(request.user, i)
		})
	return render_to_response(templatePathPrefix + 'injects.html', c)

def injects_respond(request, competition = None, ijctid = None):
	"""
	Displays a specific inject and provides either upload or text entry for inject response
	"""
	c = getAuthValues(request, {})
	# If the user isn't authed as a Blue Team
	if c["auth_name"] != "auth_team_blue":
		c["message"] = "You must log in as a Blue Team to view this page."
		return HttpResponseForbidden(render_to_string('status_400.html', c))
	c["comp_obj"] = Competition.objects.get(compurl = competition)
	# If the view is disabled
	if not c["comp_obj"].teams_view_injects_enabled:
		c["message"] = "This feature is disabled for this competition."
		return HttpResponseForbidden(render_to_string('status_400.html', c))
	c.update(csrf(request))
	# If we're not getting POST data, serve the page normally
	if request.method != "POST":
		ijct_obj = Inject.objects.get(compid = c["comp_obj"].compid, ijctid = ijctid)
		if not ijct_obj.require_response:
			return HttpResponseRedirect('/competitions/%s/injects/' % (competition))
		c["inject"] = {
			"ijct_obj": ijct_obj,
			"files": Document.objects.filter(inject = ijctid),
			"display_state": get_inject_display_state(request.user, ijct_obj)
		}
		c["response_list"] = []
		for i in InjectResponse.objects.filter(compid = c["comp_obj"].compid, teamid = request.user.teamid, ijctid = ijctid):
			c["response_list"].append({
				"response": i,
				"files": Document.objects.filter(injectresponse = i)
			})
		if c["inject"]["ijct_obj"].dt_response_close <= timezone.now():
			c["response_locked"] = True
		else:
			c["response_locked"] = False
			c["responseform"] = InjectResponseForm()
		return render_to_response(templatePathPrefix + 'injects_view_respond.html', c)
	# Check if we're allowed to take the submission (time restrictions)
	ijct_obj = Inject.objects.get(compid = c["comp_obj"].compid, ijctid = ijctid)
	if not ijct_obj.require_response:
		return HttpResponseRedirect('/competitions/%s/injects/' % (competition))
	if ijct_obj.dt_response_close <= timezone.now():
		# Very clever person - submission form was closed, but they're attempting to POST anyway
		return HttpResponseRedirect('/competitions/%s/injects/%s/' % (competition, ijctid))
	# Determine if we're handling text entry or file upload
	tmp_dict = request.POST.copy().dict()
	tmp_dict.pop('csrfmiddlewaretoken', None)
	tmp_dict.pop('docfile', None)
	tmp_dict['compid'] = request.user.compid
	tmp_dict['teamid'] = request.user.teamid
	tmp_dict['ijctid'] = int(ijctid)
	ijct_resp_obj = InjectResponse(**tmp_dict)
	ijct_resp_obj.save()
	# Checks if we were given a file
	if 'docfile' in request.FILES:
		save_document(request.FILES['docfile'], settings.CONTENT_INJECT_REPONSE_PATH, ijct_resp_obj)
	return HttpResponseRedirect('/competitions/%s/injects/%s/' % (competition, ijctid))

def servicestatus(request, competition = None):
	"""
	Display current service status for selected team in selected competition
	"""
	c = getAuthValues(request, {})
	# If the user isn't authed as a Blue Team
	if c["auth_name"] != "auth_team_blue":
		c["message"] = "You must log in as a Blue Team to view this page."
		return HttpResponseForbidden(render_to_string('status_400.html', c))
	c["comp_obj"] = Competition.objects.get(compurl = competition)
	# If the view is disabled
	if not c["comp_obj"].teams_view_servicestatus_enabled:
		c["message"] = "This feature is disabled for this competition."
		return HttpResponseForbidden(render_to_string('status_400.html', c))
	c["status_list"] = []
	service_objs = Service.objects.filter(compid = c["comp_obj"].compid, datetime_start__lte = timezone.now(), datetime_finish__gt = timezone.now())
	for i in service_objs:
		c["status_list"].append({
			"service": i,
			"score": i.score(request.user)
		})
	return render_to_response(templatePathPrefix + 'servicestatus.html', c)

def servicestatistics(request, competition = None):
	"""
	Display status timeline of services for selected team in selected competition
	"""
	c = getAuthValues(request, {})
	# If the user isn't authed as a Blue Team
	if c["auth_name"] != "auth_team_blue":
		c["message"] = "You must log in as a Blue Team to view this page."
		return HttpResponseForbidden(render_to_string('status_400.html', c))
	c["comp_obj"] = Competition.objects.get(compurl = competition)
	# If the view is disabled
	if not c["comp_obj"].teams_view_servicestatistics_enabled:
		c["message"] = "This feature is disabled for this competition."
		return HttpResponseForbidden(render_to_string('status_400.html', c))
	# Prepare page for statistics view selector
	c.update(csrf(request))
	c["form"] = ServiceSelectionForm(compid = c["comp_obj"].compid)
	score_obj_list = []
	if request.POST and request.POST['service'] != u'-1':
		c["form"] = ServiceSelectionForm(initial = {"service": request.POST['service']}, compid = c["comp_obj"].compid)
		comp_seconds = int((c["comp_obj"].datetime_finish - c["comp_obj"].datetime_start).total_seconds())
		score_obj_list = Score.objects.filter(compid = request.user.compid, teamid = request.user.teamid, servid = request.POST['service'])
		if len(score_obj_list) > 0:
			prev_date = score_obj_list[0].datetime
			total_percent = 0
			c["score_vals"] = []
			for i in score_obj_list[1:]:
				diff = int((i.datetime - prev_date).total_seconds())
				percentage = 100 * float(diff) / float(comp_seconds)
				if total_percent + percentage > 100:
					percentage = 100 - total_percent
				total_percent += percentage
				prev_date = i.datetime
				c["score_vals"].append({"value":i.value,"percentage": percentage})
	else:
		score_obj_list = Score.objects.filter(compid = request.user.compid, teamid = request.user.teamid)
	# Prepare data for chart_overall_uptime
	chart_score_up = 0
	chart_score_down = 0
	for i in score_obj_list:
		if i.value == 0:
			chart_score_down += 1
		else:
			chart_score_up += 1
	c["score_pie_chart"] = [
		{"value":chart_score_up,"color":"#46BFBD","highlight":"#5AD3D1","label":"Scored Up"},
		{"value":chart_score_down,"color":"#F7464A","highlight":"#FF5A5E","label":"Scored Down"}
	]
	total_scores = chart_score_up + chart_score_down
	return render_to_response(templatePathPrefix + 'servicestatistics.html', c)

def scoreboard(request, competition = None):
	"""
	Display the list of scores for the selected team of the selected competition
	"""
	c = getAuthValues(request, {})
	# If the user isn't authed as a Blue Team
	if c["auth_name"] != "auth_team_blue":
		c["message"] = "You must log in as a Blue Team to view this page."
		return HttpResponseForbidden(render_to_string('status_400.html', c))
	c["comp_obj"] = Competition.objects.get(compurl = competition)
	# If the view is disabled
	if not c["comp_obj"].teams_view_scoreboard_enabled:
		c["message"] = "This feature is disabled for this competition."
		return HttpResponseForbidden(render_to_string('status_400.html', c))
	c.update(csrf(request))
	c["scores"] = []
	if request.POST and request.POST['service'] != u'-1' :
		c["form"] = ServiceSelectionForm(initial = {"service": request.POST['service']}, compid = request.user.compid)
		scores_obj_list = Score.objects.filter(compid = request.user.compid, teamid = request.user.teamid, servid = request.POST['service'])
		for i in scores_obj_list:
			c["scores"].append({
				"time": i.datetime,
				"name": Service.objects.get(servid = i.servid).name,
				"value": i.value
			})
	else:
		c["form"] = ServiceSelectionForm(compid = request.user.compid)
		scores_obj_list = Score.objects.filter(compid = request.user.compid, teamid = request.user.teamid)
		for i in scores_obj_list:
			c["scores"].append({
				"time": i.datetime,
				"name": Service.objects.get(servid = i.servid).name,
				"value": i.value
			})
	return render_to_response(templatePathPrefix + 'scoreboard.html', c)

def incidentresponse(request, competition = None):
	"""
	Provides a submission portal for selected team of selected competition to submit incident responses
	"""
	c = getAuthValues(request, {})
	# If the user isn't authed as a Blue Team
	if c["auth_name"] != "auth_team_blue":
		c["message"] = "You must log in as a Blue Team to view this page."
		return HttpResponseForbidden(render_to_string('status_400.html', c))
	c["comp_obj"] = Competition.objects.get(compurl = competition)
	# If the view id disabled
	if not c["comp_obj"].teams_view_incidentresponse_enabled:
		c["message"] = "This feature is disabled for this competition."
		return HttpResponseForbidden(render_to_string('status_400.html', c))
	c.update(csrf(request))
	# Get any already opened intrusion responses
	c["responseform"] = IncidentResponseForm()
	# If we're not getting POST data, serve the page normally
	if request.method != "POST":
		c["responseform"] = IncidentResponseForm()
		c["response_list"] = []
		for i in IncidentResponse.objects.filter(compid = c["comp_obj"].compid, teamid = request.user.teamid, replyto = -1):
			c["response_list"].append({
				"response": i,
				"files": Document.objects.filter(incidentresponse = i)
			})
		return render_to_response(templatePathPrefix + 'incidentresponse.html', c)
	# Checks if form is valid, and if so, builds model
	form = IncidentResponseForm(request.POST)
	if not form.is_valid():
		#TODO: This is technically failing without raising an error for the user
		return render_to_response(templatePathPrefix + 'incidentresponse.html', c)
	intresp_obj = IncidentResponse()
	intresp_obj.compid = c["comp_obj"].compid
	intresp_obj.teamid = request.user.teamid
	intresp_obj.datetime = timezone.now()
	intresp_obj.subject = form.cleaned_data['subject']
	intresp_obj.textentry = form.cleaned_data['textentry']
	intresp_obj.replyto = -1
	intresp_obj.save()
	# Was there a file? If so, save it!
	if 'docfile' in request.FILES:
		save_document(request.FILES['docfile'], settings.CONTENT_INCIDENT_REPONSE_PATH, intresp_obj)
	return HttpResponseRedirect('/competitions/%s/incidentresponse/' % c["comp_obj"].compurl)

def incidentresponse_respond(request, competition = None, intrspid = None):
	c = getAuthValues(request, {})
	# If the user isn't authed as a Blue Team
	if c["auth_name"] != "auth_team_blue":
		c["message"] = "You must log in as a Blue Team to view this page."
		return HttpResponseForbidden(render_to_string('status_400.html', c))
	c["comp_obj"] = Competition.objects.get(compurl = competition)
	# If the view is disabled
	if not c["comp_obj"].teams_view_incidentresponse_enabled:
		c["message"] = "This feature is disabled for this competition."
		return HttpResponseForbidden(render_to_string('status_400.html', c))
	c.update(csrf(request))
	# Get any already opened intrusion responses
	c["responseform"] = IncidentResponseReplyForm()
	c["firstpost"] = {
		"response": IncidentResponse.objects.get(intrspid = intrspid),
		"files": Document.objects.filter(incidentresponse = intrspid)
		}
	c["response_list"] = []
	for i in IncidentResponse.objects.filter(compid = request.user.compid, teamid = request.user.teamid, replyto = intrspid):
		c["response_list"].append({
			"response": i,
			"files": Document.objects.filter(incidentresponse = i)
		})
	# If we're not getting POST data, serve the page normally
	if request.method != "POST":
		c["responseform"] = IncidentResponseReplyForm()
		return render_to_response(templatePathPrefix + 'incidentresponse_view_respond.html', c)
	# Checks if form is valid, and if so, builds model
	form = IncidentResponseReplyForm(request.POST)
	if not form.is_valid():
		print form.errors
		#TODO: This is technically failing without raising an error for the user
		return render_to_response(templatePathPrefix + 'incidentresponse_view_respond.html', c)
	intresp_obj = IncidentResponse()
	intresp_obj.compid = c["comp_obj"].compid
	intresp_obj.teamid = request.user.teamid
	intresp_obj.datetime = timezone.now()
	intresp_obj.textentry = form.cleaned_data['textentry']
	intresp_obj.replyto = intrspid
	intresp_obj.save()
	# Was there a file? If so, save it!
	if 'docfile' in request.FILES:
		save_document(request.FILES['docfile'], settings.CONTENT_INCIDENT_REPONSE_PATH, intresp_obj)
	return HttpResponseRedirect('/competitions/%s/incidentresponse/%s/' % (c["comp_obj"].compurl, str(intrspid)))

