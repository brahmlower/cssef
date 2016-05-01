from WebInterface.utils import getContext
from WebInterface.context import BaseContext
from WebInterface.modules.organization.context import OrganizationContext
from WebInterface.modules.organization.context import ListMemberContext
from WebInterface.modules.organization.context import OrganizationSettingsContext
from WebInterface.modules.organization.context import CompPluginListContext
from WebInterface.modules.organization.context import CompPluginCreateContext

templatePathPrefix = "organization/templates/"

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

def home(request, organizationId):
	pageTemplate = templatePathPrefix + 'home.html'
	return getContext(OrganizationContext, request, page_template = pageTemplate, organizationId = organizationId)

def members(request, organizationId):
	pageTemplate = templatePathPrefix + 'listMembers.html'
	return getContext(ListMemberContext, request, page_template = pageTemplate, organizationId = organizationId)

def settings(request, organizationId):
	pageTemplate = templatePathPrefix + 'settings.html'
	return getContext(OrganizationSettingsContext, request, page_template = pageTemplate, organizationId = organizationId)

def compplugin_list(request, organizationId, plugin_name):
	pageTemplate = templatePathPrefix + 'plugin_list.html'
	return getContext(CompPluginListContext, request, page_template = pageTemplate, organizationId = organizationId, plugin_name = plugin_name)

def compplugin_create(request, organizationId, plugin_name):
	return getContext(CompPluginCreateContext, request, redirect_url = '/organization/%s/plugin/%s/' % (organizationId, plugin_name), organizationId = organizationId)