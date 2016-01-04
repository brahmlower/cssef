from WebInterface.utils import getContext
from WebInterface.modules.competition.context import WhiteteamSummaryContext
from WebInterface.modules.competition.context import WhiteteamSettingsContext
from WebInterface.modules.competition.context import TeamListContext
from WebInterface.modules.competition.context import TeamEditContext
from WebInterface.modules.competition.context import TeamCreateContext
from WebInterface.modules.competition.context import InjectListContext
from WebInterface.modules.competition.context import InjectEditContext
from WebInterface.modules.competition.context import InjectCreateContext

templatePathPrefix = "competition/templates/whiteteam/"

def summary(request, competitionUrl):
	pageTemplate = templatePathPrefix + 'summary.html'
	return getContext(WhiteteamSummaryContext, pageTemplate, request, competitionUrl = competitionUrl)

def settings(request, competitionUrl):
	pageTemplate = templatePathPrefix + 'settings.html'
	return getContext(WhiteteamSettingsContext, pageTemplate, request, competitionUrl = competitionUrl)

# ==================================================
# Team Methods
# ==================================================
def listTeams(request, competitionUrl):
	pageTemplate = templatePathPrefix + 'listTeams.html'
	return getContext(TeamListContext, pageTemplate, request, competitionUrl = competitionUrl)

def createTeam(request, competitionUrl):
	pageTemplate = templatePathPrefix + 'createEditTeam.html'
	return getContext(TeamCreateContext, pageTemplate, request, competitionUrl = competitionUrl)

def editTeam(request, competitionUrl, teamId):
	pageTemplate = templatePathPrefix + 'createEditTeam.html'
	return getContext(TeamEditContext, pageTemplate, request, competitionUrl = competitionUrl, pkid = teamId)

# ==================================================
# Inject Methods
# ==================================================
def listInjects(request, competitionUrl):
	pageTemplate = templatePathPrefix + 'listInjects.html'
	return getContext(InjectListContext, pageTemplate, request, competitionUrl = competitionUrl)

def createInject(request, competitionUrl):
	pageTemplate = templatePathPrefix + 'createEditInject.html'
	return getContext(InjectCreateContext, pageTemplate, request, competitionUrl = competitionUrl)

def editInject(request, competitionUrl, injectId):
	pageTemplate = templatePathPrefix + 'createEditInject.html'
	return getContext(InjectEditContext, pageTemplate, request, competitionUrl = competitionUrl, pkid = injectId)

# def summary(request, competitionUrl):
# 	context = ContextFactory(request)
# 	context.SetCompetition(organizationUrl, competitionUrl)
# 	return render_to_response(templatePathPrefix + 'summary.html', context.General())

# def settings(request, competitionUrl):
# 	context = RequestContext(request)
# 	organization = cssefApi.getOrganization(organizationUrl)
# 	competition = cssefApi.getCompetition(organization['organizationId'], competitionUrl)
# 	context.push({'organization': organization})
# 	context.push({'competition': competition})
# 	if not request.method == 'POST':
# 		context.push({'form': CompetitionSettings(initial = competition)})
# 		return render_to_response(templatePathPrefix + 'settings.html', context)
# 	formData = CompetitionSettings(request.POST)
# 	if not formData.is_valid():
# 		print formData.errors
# 		return render_to_response(templatePathPrefix + 'settings.html', context)
# 	formData.cleaned_data['competitionId'] = competition['competitionId']
# 	formData.cleaned_data['organization'] = organization['organizationId']
# 	response = cssefApi.post('competitions/%s.json' % competition['competitionId'], formData.cleaned_data)
# 	return HttpResponseRedirect('/organization/%s/competitions/%s/settings/' % (organization['url'], competition['url']))

# def listTeams(request, competitionUrl):
# 	context = ContextFactory(request)
# 	context.SetCompetition(organizationUrl, competitionUrl)
# 	context.push({'teams': cssefApi.getTeams(context['competition']['competitionId'])})
# 	return render_to_response(templatePathPrefix + 'listTeams.html', context.General())

# def createEditTeam(request, competitionUrl, teamId = None):
# 	context = RequestContext(request)
# 	organization = cssefApi.getOrganization(organizationUrl)
# 	competition = cssefApi.getCompetition(organization['organizationId'], competitionUrl)
# 	if not request.method == 'POST':
# 		context.push({'organization': organization})
# 		context.push({'competition': competition})
# 		context.push({'action': 'create'})
# 		context.push({'form': CreateTeam(competitionId = competition['competitionId'], teamId = teamId)})
# 		return render_to_response(templatePathPrefix + 'createEditTeam.html', context)
# 	formData = CreateTeam(request.POST)
# 	if not formData.is_valid():
# 		return render_to_response(templatePathPrefix + 'createEditTeam.html', context)
# 	formData.cleaned_data['competitionId'] = competition['competitionId']
# 	response = cssefApi.post('competitions/%s/teams.json' % competition['competitionId'], formData.cleaned_data)
# 	return HttpResponseRedirect('/organization/%s/competitions/%s/teams/' % (organization['url'], competition['url']))

# def listServices(request, competitionUrl):
# 	context = ContextFactory(request)
# 	context.SetCompetition(organizationUrl, competitionUrl)
# 	context.push({'pluginsAvailable': len(cssefApi.get('plugins.json')) > 0})
# 	context.push({'services': cssefApi.getServices(context['competition']['competitionId'])})
# 	return render_to_response(templatePathPrefix + 'listServices.html', context.General())

# def createEditService(request, competitionUrl, serviceId = None):
# 	context = RequestContext(request)
# 	organization = cssefApi.getOrganization(organizationUrl)
# 	competition = cssefApi.getCompetition(organization['organizationId'], competitionUrl)
# 	if not request.method == 'POST':
# 		context.push({'organization': organization})
# 		context.push({'competition': competition})
# 		context.push({'action': 'create'})
# 		context.push({'form': CreateService(competitionId = context['competition']['competitionId'], serviceId = serviceId)})
# 		return render_to_response(templatePathPrefix + 'createEditService.html', context)
# 	formData = CreateService(request.POST)
# 	if not formData.is_valid():
# 		return render_to_response(templatePathPrefix + 'createEditService.html', context)
# 	formData.cleaned_data['competitionId'] = competition['competitionId']
# 	response = cssefApi.post('competitions/%s/services.json' % competition['competitionId'], formData.cleaned_data)
# 	return HttpResponseRedirect('/organization/%s/competitions/%s/services/' % (organization['url'], competition['url']))

# def listInjects(request, competitionUrl):
# 	context = RequestContext(request)
# 	context.push({'organization': cssefApi.getOrganization(organizationUrl)})
# 	context.push({'competition': cssefApi.getCompetition(context['organization']['organizationId'], competitionUrl)})
# 	context.push({'injects': cssefApi.getInjects(context['competition']['competitionId'])})
# 	return render_to_response(templatePathPrefix + 'listInjects.html', context)

# def createEditInject(request, competitionUrl, injectId = None):
# 	context = RequestContext(request)
# 	organization = cssefApi.getOrganization(organizationUrl)
# 	competition = cssefApi.getCompetition(organization['organizationId'], competitionUrl)
# 	if not request.method == 'POST':
# 		context.push({'organization': organization})
# 		context.push({'competition': competition})
# 		context.push({'action': 'create'})
# 		context.push({'form': CreateInject(competitionId = context['competition']['competitionId'], injectId = injectId)})
# 		return render_to_response(templatePathPrefix + 'createEditInject.html', context)
# 	formData = CreateInject(request.POST)
# 	if not formData.is_valid():
# 		return render_to_response(templatePathPrefix + 'createEditInject.html', context)
# 	formData.cleaned_data['competitionId'] = competition['competitionId']
# 	response = cssefApi.post('competitions/%s/injects.json' % competition['competitionId'], formData.cleaned_data)
# 	return HttpResponseRedirect('/organization/%s/competitions/%s/injects/' % (organization['url'], competition['url']))
