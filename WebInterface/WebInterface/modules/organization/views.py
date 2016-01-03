from WebInterface.utils import getContext

templatePathPrefix = "organization/templates/"

# def getContext(contextClass, pageTemplate, request, **kwargs):
# 	context = contextClass(request, **kwargs)
# 	context.processContext()
# 	return render_to_response(pageTemplate, context.getContext())

# def login(request):
# 	context = {}
# 	context["form"] = LoginOrganizationUser()
# 	context.update(csrf(request))
# 	# Checks if the user is submitting the form, or requesting the form
# 	if request.method != "POST":
# 		return render_to_response(templatePathPrefix + 'login.html', context)
# 	username = request.POST.get('username')
# 	password = request.POST.get('password')
# 	# TODO: The following line can throw a MultiValueDictKeyError
# 	admin = auth.authenticate(username = username, password = password)
# 	if admin == None:
# 		return render_to_response(templatePathPrefix + 'login.html', context)
# 	# Checks that the submitted form data is valid
# 	auth.login(request, admin)
# 	organizationName = 'testingorg'
# 	return HttpResponseRedirect("/organization/%s/home" % organizationName)

def home(request, organizationUrl):
	return getContext(BaseContext, templatePathPrefix + "home.html", request)

def members(request, organizationUrl):
	pageTemplate = templatePathPrefix + 'listMembers.html'
	context = getContext(ListMemberContext, pageTemplate, request)
	return context
	# context = {}
	# context['organization'] = cssefApi.getOrganization(organizationUrl)
	# context['members'] = cssefApi.getOrganizationMembers(organizationUrl)
	# users = cssefApi.get('users.json')
	# members = []
	# for i in users:
	# 	if i['organization'] == context['organization']['organizationId']:
	# 		context['members'].append(i)
	# return render_to_response('organization/members.html', context)

def listCompetitions(request, organizationUrl):
	pageTemplate = templatePathPrefix + 'listCompetitions.html'
	context = getContext(ListCompetitionContext, pageTemplate, request)
	return context
	# context = {}
	# context['competitions'] = []
	# context['organization'] = cssefApi.getOrganization(organizationUrl)
	# for i in cssefApi.get('competitions.json'):
	# 	if i['organization'] == context['organization']['organizationId']:
	# 		context['competitions'].append(i)
	# return render_to_response('organization/listCompetitions.html', context)

def createCompetition(request, organizationUrl, competition=None):
	pageTemplate = templatePathPrefix + 'createCompetition.html'
	context = getContext(CreateCompetitionContext, pageTemplate, request)
	return context
	# context = {}
	# context.update(csrf(request))
	# context['organization'] = cssefApi.getOrganization(organizationUrl)
	# context["form"] = CreateCompetition()
	# if request.method != "POST":
	# 	return render_to_response('organization/createCompetition.html', context)
	# formData = CreateCompetition(request.POST)
	# if not formData.is_valid():
	# 	return render_to_response('organization/createCompetition.html', context)
	# formData.cleaned_data['organization'] = context['organization']['organizationId']
	# response = cssefApi.post('competitions.json', formData.cleaned_data)
	# return HttpResponseRedirect('/organization/%s/competitions/' % context['organization']['url'])

def settings(request, organizationUrl):
	pageTemplate = templatePathPrefix + 'settings.html'
	context = getContext(OrganizationSettingsContext, pageTemplate, request)
	return context
	# context = {}
	# context['organization'] = cssefApi.getOrganization(organizationUrl)
	# return render_to_response('organization/settings.html', context)
