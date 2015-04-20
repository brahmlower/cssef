from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.shortcuts import RequestContext
from django.core.context_processors import csrf
from django.core.files.uploadedfile import UploadedFile
from django.forms import NumberInput
from django.forms import TextInput
from django.utils import timezone
from WebInterface.forms import CreateInject
from WebInterface.forms import CreateTeam
from WebInterface.forms import CreateService
from WebInterface.forms import CompetitionSettings
from WebInterface import cssefApi
import json

def summary(request, organizationUrl, competitionUrl):
	context = {}
	context['organization'] = cssefApi.getOrganization(organizationUrl)
	context['competition'] = cssefApi.getCompetition(context['organization']['organizationId'], competitionUrl)
	return render_to_response('competition/summary.html', context)

def settings(request, organizationUrl, competitionUrl):
	context = RequestContext(request)
	context.push({'organization': cssefApi.getOrganization(organizationUrl)})
	context.push({'competition': cssefApi.getCompetition(context['organization']['organizationId'], competitionUrl)})
	context.push({'form': CompetitionSettings()})
	return render_to_response('competition/settings.html', context)

def listTeams(request, organizationUrl, competitionUrl):
	context = RequestContext(request)
	context.push({'organization': cssefApi.getOrganization(organizationUrl)})
	context.push({'competition': cssefApi.getCompetition(context['organization']['organizationId'], competitionUrl)})
	context.push({'teams': cssefApi.getTeams(context['competition']['competitionId'])})
	return render_to_response('competition/listTeams.html', context)

def createEditTeam(request, organizationUrl, competitionUrl, teamId = None):
	context = RequestContext(request)
	organization = cssefApi.getOrganization(organizationUrl)
	competition = cssefApi.getCompetition(organization['organizationId'], competitionUrl)
	if not request.method == 'POST':
		context.push({'organization': organization})
		context.push({'competition': competition})
		context.push({'action': 'create'})
		context.push({'form': CreateTeam(competitionId = competition['competitionId'], teamId = teamId)})
		return render_to_response('competition/createEditTeam.html', context)
	formData = CreateTeam(request.POST)
	if not formData.is_valid():
		return render_to_response('competition/createEditTeam.html', context)
	formData.cleaned_data['competitionId'] = competition['competitionId']
	response = cssefApi.post('competitions/%s/teams.json' % competition['competitionId'], formData.cleaned_data)
	return HttpResponseRedirect('/organization/%s/competitions/%s/teams/' % (organization['url'], competition['url']))

def listServices(request, organizationUrl, competitionUrl):
	context = RequestContext(request)
	organization = cssefApi.getOrganization(organizationUrl)
	competition = cssefApi.getCompetition(organization['organizationId'], competitionUrl)
	context.push({'organization': organization})
	context.push({'competition': competition})
	context.push({'pluginsAvailable': len(cssefApi.get('plugins.json')) > 0})
	context.push({'services': cssefApi.getServices(competition['competitionId'])})
	return render_to_response('competition/listServices.html', context)

def createEditService(request, organizationUrl, competitionUrl, serviceId = None):
	context = RequestContext(request)
	organization = cssefApi.getOrganization(organizationUrl)
	competition = cssefApi.getCompetition(organization['organizationId'], competitionUrl)
	if not request.method == 'POST':
		context.push({'organization': organization})
		context.push({'competition': competition})
		context.push({'action': 'create'})
		context.push({'form': CreateService(competitionId = context['competition']['competitionId'], serviceId = serviceId)})
		return render_to_response('competition/createEditService.html', context)
	formData = CreateService(request.POST)
	if not formData.is_valid():
		return render_to_response('competition/createEditService.html', context)
	formData.cleaned_data['competitionId'] = competition['competitionId']
	response = cssefApi.post('competitions/%s/services.json' % competition['competitionId'], formData.cleaned_data)
	return HttpResponseRedirect('/organization/%s/competitions/%s/services/' % (organization['url'], competition['url']))

def listInjects(request, organizationUrl, competitionUrl):
	context = RequestContext(request)
	context.push({'organization': cssefApi.getOrganization(organizationUrl)})
	context.push({'competition': cssefApi.getCompetition(context['organization']['organizationId'], competitionUrl)})
	context.push({'injects': cssefApi.getInjects(context['competition']['competitionId'])})
	return render_to_response('competition/listInjects.html', context)

def createEditInject(request, organizationUrl, competitionUrl, injectId = None):
	context = RequestContext(request)
	organization = cssefApi.getOrganization(organizationUrl)
	competition = cssefApi.getCompetition(organization['organizationId'], competitionUrl)
	if not request.method == 'POST':
		context.push({'organization': organization})
		context.push({'competition': competition})
		context.push({'action': 'create'})
		context.push({'form': CreateInject(competitionId = context['competition']['competitionId'], injectId = injectId)})
		return render_to_response('competition/createEditInject.html', context)
	formData = CreateInject(request.POST)
	if not formData.is_valid():
		return render_to_response('competition/createEditInject.html', context)
	formData.cleaned_data['competitionId'] = competition['competitionId']
	response = cssefApi.post('competitions/%s/injects.json' % competition['competitionId'], formData.cleaned_data)
	return HttpResponseRedirect('/organization/%s/competitions/%s/injects/' % (organization['url'], competition['url']))




# def requestGetApi(apiPath):
# 	queryUrl = API_URL + apiPath
# 	jsonString = urlopen(queryUrl).read()
# 	return json.loads(jsonString)

# def requestPostApi(apiPath):
# 	pass

# # General competition configuration modules
# def summary(request, organization, competition):
# 	"""
# 	Displays general competitions configurations form
# 	"""
# 	context = {}
# 	context["competition"] = requestGetApi('competition/%s.json' % str(competition))
# 	return render_to_response('CompConfig/summary.html', context)

# def settings(request, organization, competition):
# 	"""
# 	Displays competitions details form
# 	"""
# 	c.update(csrf(request))
# 	c["comp_obj"] = Competition.objects.get(compurl = competition)
# 	form_initial = Competition.objects.filter(compid = c['comp_obj'].compid).values()[0]
# 	c["forms"] = {
# 		#"general_settings": CompetitionSettingsGeneralForm(initial = form_initial),
# 		#"scoring_settings": CompetitionSettingsScoringForm(initial = form_initial),
# 		#"service_settings": CompetitionSettingsServiceForm(initial = form_initial),
# 		#"team_settings": CompetitionSettingsTeamForm(initial = form_initial)
# 	}
# 	if request.POST:
# 		#forms_list = [	#CompetitionSettingsGeneralForm,
# 		#				CompetitionSettingsScoringForm,
# 		#				CompetitionSettingsServiceForm,
# 		#				CompetitionSettingsTeamForm]
# 		f = forms_list[int(request.POST['form_num'])](request.POST)
# 		if f.is_valid():
# 			comp_obj = Competition.objects.filter(compid = c['comp_obj'].compid)
# 			clean_copy = f.cleaned_data
# 			for i in clean_copy:
# 				if clean_copy[i] == u'':
# 					clean_copy[i] = None
# 			comp_obj.update(**clean_copy)
# 			# Schedules the job to start the scoring engine
# 			#sec_until_start = (comp_obj[0].datetime_start - timezone.now()).seconds
# 			#result = run_comp.apply_async((comp_obj[0].compid,), countdown = int(sec_until_start))
# 			#logger.debug('Scheduled competition: Seconds until start: %s, Event UUID: %s' % (str(sec_until_start), str(result.id)))
# 		else:
# 			logger.error("is not valid")
# 		return HttpResponseRedirect('/admin/competitions/%s/settings/' % c["comp_obj"].compurl)
# 	return render_to_response('CompConfig/settings.html', c)

# # Team related configuration modules
# def listTeams(request, organization, competition):
# 	"""
# 	Lists the teams in the competition
# 	"""
# 	context = {}
# 	context["competition"] = requestGetApi('competition/%s.json' % competition)
# 	context["teams"] = requestGetApi('competition/%s/teams.json' % competition)
# 	return render_to_response('CompConfig/teams_list.html', context)

# def editTeam(request, organization, competition, teamId = None):
# 	"""
# 	Edit the team in the competition
# 	"""
# 	c["action"] = "edit"
# 	c["comp_obj"] = Competition.objects.get(compurl = competition)
# 	c.update(csrf(request))
# 	if request.method != "POST":
# 		team_obj = Team.objects.filter(compid = c["comp_obj"].compid, teamId = int(teamId))
# 		c["teamId"] = team_obj[0].teamId
# 		#c["form"] = CreateTeamForm(initial = team_obj.values()[0])
# 		c["service_configs_list"] = buildTeamServiceConfigForms(c["comp_obj"].compid, team_obj[0].score_configs)
# 		return render_to_response('CompConfig/teams_create-edit.html', c)
# 	form_dict = request.POST.copy().dict()
# 	form_dict.pop('csrfmiddlewaretoken', None)
# 	form_dict["compid"] = c["comp_obj"].compid
# 	form_dict["score_configs"] = buildTeamServiceConfigDict(c["comp_obj"].compid, form_dict)
# 	# Clean network address
# 	if form_dict['networkaddr'][-1] == ".":
# 		form_dict['networkaddr'] = form_dict['networkaddr'][:-1]
# 	if form_dict['networkaddr'][0] == ".":
# 		form_dict['networkaddr'] = form_dict['networkaddr'][1:]
# 	team_obj = Team.objects.filter(compid = c["comp_obj"].compid, teamId = int(teamId))
# 	team_obj.update(**form_dict)
# 	return HttpResponseRedirect('/admin/competitions/%s/teams/' % competition)

# def createTeam(request, organization, competition):
# 	"""
# 	Create the team in the competition
# 	"""
# 	c={}
# 	c["action"] = "create"
# 	c["comp_obj"] = Competition.objects.get(compurl = competition)
# 	c.update(csrf(request))
# 	if request.method != "POST":
# 		#c['form'] = buildTeamServiceConfigForms(c["comp_obj"].compid, CreateTeamForm())
# 		c["depend_list"] = buildTeamServiceDependencyList(c["comp_obj"].compid)
# 		return render_to_response('CompConfig/teams_create-edit.html', c)
# 	form_dict = request.POST.copy()
# 	form_dict["compid"] = c["comp_obj"].compid
# 	form_dict["score_configs"] = buildTeamServiceConfigDict(c["comp_obj"].compid, form_dict)
# 	# Clean network address
# 	if form_dict['networkaddr'][-1] == ".":
# 		form_dict['networkaddr'] = form_dict['networkaddr'][:-1]
# 	if form_dict['networkaddr'][0] == ".":
# 		form_dict['networkaddr'] = form_dict['networkaddr'][1:]
# 	#team = CreateTeamForm(form_dict)
# 	if not team.is_valid():
# 		#c['form'] = buildTeamServiceConfigForms(c["comp_obj"].compid, CreateTeamForm(), form_dict)
# 		return render_to_response('CompConfig/teams_create-edit.html', c)
# 	team.save()
# 	return HttpResponseRedirect("/admin/competitions/%s/teams/" % competition)

# # Service related configuration modules
# def listServices(request, organization, competition):
# 	"""
# 	Lists the services in the competition
# 	"""
# 	c["comp_obj"] = Competition.objects.get(compurl = competition)
# 	c["service_list"] = Service.objects.filter(compid = c["comp_obj"].compid)
# 	c["available_modules"] = bool(len(ServiceModule.objects.all()))
# 	return render_to_response('CompConfig/services_list.html', c)

# def editService(request, organization, competition, serviceId = None):
# 	"""
# 	Edits the service in the competitions
# 	"""

# 	c["action"] = "edit"
# 	c["comp_obj"] = Competition.objects.get(compurl = competition)
# 	c.update(csrf(request))
# 	if request.method != "POST":
# 		serv_obj = Service.objects.filter(compid = c["comp_obj"].compid, serviceId = int(serviceId))
# 		c["serviceId"] = serv_obj[0].serviceId
# 		initial_dict = serv_obj.values()[0]
# 		initial_dict["connectip"] = int(initial_dict["connectip"])
# 		initial_dict["servicemodule"] = serv_obj[0].servicemodule.servmdulid
# 		#c["form"] = CreateServiceForm(initial = initial_dict)
# 		return render_to_response('CompConfig/services_create-edit.html', c)
# 	# TODO: This part is super gross. I should improve efficiency at some point
# 	form_dict = request.POST.copy().dict()
# 	form_dict.pop('csrfmiddlewaretoken', None)
# 	# Set network connection display
# 	if int(form_dict["connectip"]) == 1:
# 		form_dict["connect_display"] = "IP Address"
# 		form_dict["connectip"] = True
# 	else:
# 		form_dict["connect_display"] = "Domain Name"
# 		form_dict["connectip"] = False
# 	# Clean machine address value
# 	if form_dict['networkloc'][0] == ".":
# 		form_dict['networkloc'] = form_dict['networkloc'][1:]
# 	if form_dict['networkloc'][-1] == ".":
# 		form_dict['networkloc'] = form_dict['networkloc'][:-1]
# 	serv_obj = Service.objects.filter(compid = c["comp_obj"].compid, serviceId = int(serviceId))
# 	serv_obj.update(**form_dict)
# 	return HttpResponseRedirect('/admin/competitions/%s/services/' % competition)

# def createService(request, organization, competition):
# 	"""
# 	Create services in the competition
# 	"""
# 	c["comp_obj"] = Competition.objects.get(compurl = competition)
# 	if not bool(len(ServiceModule.objects.all())):
# 		return HttpResponseRedirect("/admin/competitions/%s/services/" % c["comp_obj"].compurl)
# 	if request.method != "POST":
# 		# Serve empty form without acting on any data
# 		c.update(csrf(request))
# 		#c["form"] = CreateServiceForm()
# 		c["action"] = "create"
# 		return render_to_response('CompConfig/services_create-edit.html', c)
# 	# Prepare post data for validation
# 	form_dict = request.POST.copy().dict()
# 	#serv_form = CreateServiceForm(form_dict)
# 	if not serv_form.is_valid():
# 		print serv_form.errors
# 		return render_to_response('CompConfig/services_create-edit.html', c)
# 	# Now prepare post data for service object instantiation
# 	form_dict.pop('csrfmiddlewaretoken', None)
# 	form_dict["compid"] = c["comp_obj"].compid
# 	form_dict["servicemodule"] = ServiceModule.objects.get(servmdulid = form_dict["servicemodule"])
# 	# Set network connection display
# 	if int(form_dict["connectip"]) == 1:
# 		form_dict['connectip'] = True
# 		form_dict["connect_display"] = "IP Address"
# 	else:
# 		form_dict['connectip'] = False
# 		form_dict["connect_display"] = "Domain Name"
# 	# Clean machine address value
# 	if form_dict['connectip'] and form_dict['networkloc'][0] == ".":
# 		form_dict['networkloc'] = form_dict['networkloc'][1:]
# 	elif not form_dict['connectip'] and form_dict['networkloc'][-1] == ".":
# 		form_dict['networkloc'] = form_dict['networkloc'][:-1]
# 	serv_obj = Service(**form_dict)
# 	serv_obj.save()
# 	return HttpResponseRedirect("/admin/competitions/%s/services/" % competition)

# # Inject related configuration modules
# def listInjects(request, organization, competition):
# 	"""
# 	Lists the injects in the competition
# 	"""
# 	c["comp_obj"] = Competition.objects.get(compurl = competition)
# 	c["inject_list"] = []
# 	for i in Inject.objects.filter(compid = c["comp_obj"].compid):
# 		c["inject_list"].append({
# 			"inject": i,
# 			"files": Document.objects.filter(inject = i)
# 		})
# 	return render_to_response('CompConfig/injects_list.html', c)

# def editInject(request, organization, competition, injectId = None):
# 	"""
# 	Edit the inject in the competition
# 	"""
# 	c["action"] = "edit"
# 	c["comp_obj"] = Competition.objects.get(compurl = competition)
# 	c.update(csrf(request))
# 	if request.method != "POST":
# 		# Have to use filter here, otherwise we get 'Inject object is not iterable' errors
# 		ijct_obj = Inject.objects.filter(compid = c["comp_obj"].compid, injectId = int(injectId))
# 		c["injectId"] = ijct_obj[0].injectId
# 		#c["form"] = CreateInjectForm(initial = ijct_obj.values()[0])
# 		return render_to_response('CompConfig/injects_create-edit.html', c)
# 	# Note this will only work when there are no lists
# 	form_dict = request.POST.copy().dict()
# 	form_dict.pop('csrfmiddlewaretoken', None)
# 	form_dict.pop('docfile', None)
# 	if 'require_response' in form_dict:
# 		form_dict['require_response'] = True
# 	else:
# 		form_dict['require_response'] = False
# 		form_dict['dt_response_due'] = None
# 		form_dict['dt_response_close'] = None
# 	ijct_obj = Inject.objects.filter(compid = c["comp_obj"].compid, injectId = int(injectId))
# 	ijct_obj.update(**form_dict)
# 	# Was there a file? If so, save it!
# 	if 'docfile' in request.FILES:
# 		save_document(request.FILES['docfile'], settings.CONTENT_INJECT_PATH, ijct_obj)
# 	return HttpResponseRedirect('/admin/competitions/%s/injects/' % competition)

# def createInject(request, organization, competition):
# 	"""
# 	Create injects in the competition
# 	"""
# 	c["action"] = "create"
# 	c["comp_obj"] = Competition.objects.get(compurl = competition)
# 	c.update(csrf(request))
# 	# Just displays the form if we're not handling any input
# 	if request.method != "POST":
# 		#c["form"] = CreateInjectForm()
# 		return render_to_response('CompConfig/injects_create-edit.html', c)
# 	form_dict = request.POST.copy().dict()
# 	form_dict["compid"] = c["comp_obj"].compid
# 	form_dict.pop('csrfmiddlewaretoken', None)
# 	form_dict.pop('docfile', None)
# 	if 'require_response' in form_dict:
# 		form_dict['require_response'] = True
# 	else:
# 		form_dict['require_response'] = False
# 		form_dict['dt_response_due'] = None
# 		form_dict['dt_response_close'] = None
# 	#form_obj = CreateInjectForm(form_dict)
# 	if not form_obj.is_valid():
# 		#c["messages"].new_info("Invalid field data in inject form: %s" % form_obj.errors, 1001)
# 		return render_to_response('CompConfig/injects_create-edit.html', c)
# 	# Start saving the inject!
# 	print form_dict
# 	ijct_obj = Inject(**form_dict)
# 	ijct_obj.save()
# 	# Was there a file? If so, save it!
# 	if 'docfile' in request.FILES:
# 		save_document(request.FILES['docfile'], settings.CONTENT_INJECT_PATH, ijct_obj)
# 	return HttpResponseRedirect("/admin/competitions/%s/injects/" % competition)
