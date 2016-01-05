from WebInterface.utils import getContext
from WebInterface.context import BaseContext
from WebInterface.modules.organization.context import OrganizationContext
from WebInterface.modules.organization.context import ListMemberContext
from WebInterface.modules.organization.context import OrganizationSettingsContext

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
	return getContext(OrganizationContext, pageTemplate, request, organizationId = organizationId)

def members(request, organizationId):
	pageTemplate = templatePathPrefix + 'listMembers.html'
	return getContext(ListMemberContext, pageTemplate, request, organizationId = organizationId)

def settings(request, organizationId):
	pageTemplate = templatePathPrefix + 'settings.html'
	return getContext(OrganizationSettingsContext, pageTemplate, request, organizationId = organizationId)
