from django.views.generic import TemplateView
from django.template import RequestContext
from WebInterface.utils import getContext
from WebInterface.utils import makeApiRequest as make_api_request
from WebInterface.modules.competition import forms
from WebInterface.modules.competition import context

template_path_prefix = "competition/templates/whiteteam/"

class CompetitionTemplateView(TemplateView):
	api_calls = []
	api_data = {}
	forms = {}
	debug = True

	def pack_context(self, context, context_data = None):
		context.push({'debug': self.debug})
		context.push({'debug_error_count': self.count_api_errors()})
		context.push({'api_calls': self.api_calls})
		context.push({'api_data': self.api_data})
		context.push({'forms': self.forms})
		if context_data:
			context.push(context_data)
		return context

	def count_api_errors(self):
		error_count = 0
		for i in self.api_calls:
			if i['value'] != 0:
				error_count += 1
		return error_count

	def make_api_request(self, endpoint, args_dict):
		api_output = make_api_request(endpoint, args_dict)
		self.api_calls.append(api_output)
		return api_output['content']

	def load_competition(self, comp_pkid):
		api_contents = self.make_api_request('competitionget', {'pkid': comp_pkid})
		self.api_data['competition'] = api_contents[0]

	def delete_item(self, request, comp_pkid, endpoint):
		form_inst = forms.DeleteCompetitionObjectForm(self.request.POST)
		if form_inst.errors:
			print '[ERROR] form failed to validate'
			print form_inst.errors
			return self.get(request, comp_pkid)
		form_data = form_inst.cleaned_data
		form_data['competition'] = comp_pkid
		self.make_api_request(endpoint, form_data)
		return self.get(request, comp_pkid)

def summary(request, comp_pkid):
	page_template = template_path_prefix + 'summary.html'
	return getContext(context.WhiteteamSummaryContext, request,
		page_template = page_template, comp_pkid = comp_pkid)

def settings(request, comp_pkid):
	page_template = template_path_prefix + 'settings.html'
	return getContext(context.WhiteteamSettingsContext, request,
		page_template = page_template, comp_pkid = comp_pkid)

# ==================================================
# Service Methods
# ==================================================
def list_services(request, comp_pkid):
	page_template = template_path_prefix + 'list_services.html'
	return getContext(context.ServiceListContext, request,
		page_template = page_template, comp_pkid = comp_pkid)

def create_service(request, comp_pkid):
	return getContext(context.ServiceCreateContext, request,
		redirect_url = '../', comp_pkid = comp_pkid)

def edit_service(request, comp_pkid, service_pkid):
	page_template = template_path_prefix + 'edit_service.html'
	return getContext(context.ServiceEditContext, request,
		page_template = page_template, comp_pkid = comp_pkid, pkid = service_pkid)

# ==================================================
# Team Methods
# ==================================================
class TeamView(CompetitionTemplateView):
	template_name = "competition/templates/whiteteam/list_teams.html"

	def get(self, request, comp_pkid):
		context = RequestContext(request)
		# Prepare forms
		self.forms['form_create'] = forms.CreateTeamForm()
		self.forms['form_delete'] = forms.DeleteCompetitionObjectForm()
		# Make API requests
		self.load_competition(comp_pkid)
		self.api_data['teams'] = self.make_api_request('teamget', {'competition': comp_pkid})
		# Prepare the context
		context = self.pack_context(context)
		return self.render_to_response(context)

	def post(self, request, comp_pkid):
		context = RequestContext(request)
		if request.POST['formtype'] == "delete":
			return self.delete_item(request, comp_pkid, 'teamdel')
		elif request.POST['formtype'] == "create":
			form_inst = forms.CreateTeamForm(self.request.POST)
			if form_inst.errors:
				print '[ERROR] form failed to validate'
			form_data = form_inst.cleaned_data
			form_data['competition'] = comp_pkid
			self.make_api_request('teamadd', form_data)
		return self.get(request, comp_pkid)

def edit_team(request, comp_pkid, team_pkid):
	page_template = template_path_prefix + 'edit_team.html'
	return getContext(context.TeamEditContext, request,
		page_template = page_template, comp_pkid = comp_pkid, pkid = team_pkid)

# ==================================================
# Inject Methods
# ==================================================
class InjectView(CompetitionTemplateView):
	template_name = "competition/templates/whiteteam/list_injects.html"

	def get(self, request, comp_pkid):
		context = RequestContext(request)
		# Prepare forms
		self.forms['form_create'] = forms.CreateInjectForm()
		self.forms['form_delete'] = forms.DeleteCompetitionObjectForm()
		# Make API requests
		self.load_competition(comp_pkid)
		self.api_data['injects'] = self.make_api_request('injectget', {'competition': comp_pkid})
		# Prepare the context
		context = self.pack_context(context)
		return self.render_to_response(context)

	def post(self, request, comp_pkid):
		context = RequestContext(request)
		if request.POST['formtype'] == "delete":
			return self.delete_item(request, comp_pkid, 'injectdel')
		elif request.POST['formtype'] == "create":
			form_inst = forms.CreateInjectForm(self.request.POST)
			if form_inst.errors:
				print '[ERROR] form failed to validate'
			form_data = form_inst.cleaned_data
			form_data['competition'] = comp_pkid
			self.make_api_request('injectadd', form_data)
		return self.get(request, comp_pkid)

def edit_inject(request, comp_pkid, inject_pkid):
	page_template = template_path_prefix + 'edit_inject.html'
	return getContext(context.InjectEditContext, request,
		page_template = page_template, comp_pkid = comp_pkid, pkid = inject_pkid)

# ==================================================
# Inject Response Methods
# ==================================================
class InjectResponseView(CompetitionTemplateView):
	template_name = "competition/templates/whiteteam/list_injectresponses.html"

	def get(self, request, comp_pkid):
		context = RequestContext(request)
		# Prepare forms
		self.forms['form_create'] = forms.CreateInjectResponseForm(comp_pkid)
		self.forms['form_delete'] = forms.DeleteCompetitionObjectForm()
		# Make API requests
		self.load_competition(comp_pkid)
		self.api_data['injectresponses'] = self.make_api_request('injectresponseget', {'competition': comp_pkid})
		# Prepare the context
		context = self.pack_context(context)
		return self.render_to_response(context)

	def post(self, request, comp_pkid):
		context = RequestContext(request)
		if request.POST['formtype'] == "delete":
			return self.delete_item(request, comp_pkid, 'injectresponsedel')
		elif request.POST['formtype'] == "create":
			form_inst = forms.CreateInjectResponseForm(comp_pkid, self.request.POST)
			if form_inst.errors:
				print '[ERROR] form failed to validate'
			form_data = form_inst.cleaned_data
			form_data['competition'] = comp_pkid
			self.make_api_request('injectresponseadd', form_data)
		return self.get(request, comp_pkid)

def list_injectresponses(request, comp_pkid):
	page_template = template_path_prefix + 'list_injectresponses.html'
	return getContext(context.InjectResponseListContext, request,
		page_template = page_template, comp_pkid = comp_pkid)

def create_injectresponse(request, comp_pkid):
	return getContext(context.InjectResponseCreateContext, request,
		redirect_url = '../', comp_pkid = comp_pkid)

def edit_injectresponse(request, comp_pkid, injectresponse_pkid):
	page_template = template_path_prefix + 'edit_injectresponse.html'
	return getContext(context.InjectResponseEditContext, request,
		page_template = page_template, comp_pkid = comp_pkid, pkid = injectresponse_pkid)

# ==================================================
# Incident Methods
# ==================================================
class IncidentView(CompetitionTemplateView):
	template_name = "competition/templates/whiteteam/list_incidents.html"

	def get(self, request, comp_pkid):
		context = RequestContext(request)
		# Prepare forms
		self.forms['form_create'] = forms.CreateIncidentForm()
		self.forms['form_create'].fields['team'].choices = getTeamChoices(comp_pkid)
		self.forms['form_delete'] = forms.DeleteCompetitionObjectForm()
		# Make API requests
		self.load_competition(comp_pkid)
		self.api_data['incidents'] = self.make_api_request('incidentget', {'competition': comp_pkid})
		# Prepare the context
		context = self.pack_context(context)
		return self.render_to_response(context)

	def post(self, request, comp_pkid):
		context = RequestContext(request)
		if request.POST['formtype'] == "delete":
			return self.delete_item(request, comp_pkid, 'incidentdel')
		elif request.POST['formtype'] == "create":
			form_inst = forms.CreateIncidentForm(self.request.POST)
			if form_inst.errors:
				print '[ERROR] form failed to validate'
			form_data = form_inst.cleaned_data
			form_data['competition'] = comp_pkid
			self.make_api_request('incidentadd', form_data)
		return self.get(request, comp_pkid)

def edit_incident(request, comp_pkid, incident_pkid):
	page_template = template_path_prefix + 'edit_incident.html'
	return getContext(context.IncidentEditContext, request,
		page_template = page_template, comp_pkid = comp_pkid, pkid = incident_pkid)

# ==================================================
# Incident Response Methods
# ==================================================
class IncidentResponseView(CompetitionTemplateView):
	template_name = "competition/templates/whiteteam/list_incidentresponses.html"

	def get(self, request, comp_pkid):
		context = RequestContext(request)
		# Prepare forms
		self.forms['form_create'] = forms.CreateIncidentResponseForm(comp_pkid)
		self.forms['form_delete'] = forms.DeleteCompetitionObjectForm()
		# Make API requests
		self.load_competition(comp_pkid)
		self.api_data['incidentresponses'] = self.make_api_request('incidentresponseget', {'competition': comp_pkid})
		# Prepare the context
		context = self.pack_context(context)
		return self.render_to_response(context)

	def post(self, request, comp_pkid):
		context = RequestContext(request)
		if request.POST['formtype'] == "delete":
			return self.delete_item(request, comp_pkid, 'incidentresponsedel')
		elif request.POST['formtype'] == "create":
			form_inst = forms.CreateIncidentResponseForm(comp_pkid, self.request.POST)
			if form_inst.errors:
				print '[ERROR] form failed to validate'
			form_data = form_inst.cleaned_data
			form_data['competition'] = comp_pkid
			self.make_api_request('incidentresponseadd', form_data)
		return self.get(request, comp_pkid)

def edit_incidentresponse(request, comp_pkid, incidentresponse_pkid):
	page_template = template_path_prefix + 'edit_incidentresponse.html'
	return getContext(context.IncidentResponseEditContext, request,
		page_template = page_template, comp_pkid = comp_pkid, pkid = incidentresponse_pkid)

# ==================================================
# Score Methods
# ==================================================
class ScoreView(CompetitionTemplateView):
	template_name = "competition/templates/whiteteam/list_scores.html"

	def get(self, request, comp_pkid):
		context = RequestContext(request)
		# Prepare forms
		self.forms['form_create'] = forms.CreateScoreForm(comp_pkid)
		#self.forms['form_create'].fields['team'].choices = getTeamChoices(comp_pkid)
		self.forms['form_delete'] = forms.DeleteCompetitionObjectForm()
		# Make API requests
		self.load_competition(comp_pkid)
		self.api_data['scores'] = self.make_api_request('scoreget', {'competition': comp_pkid})
		# Prepare the context
		context = self.pack_context(context)
		return self.render_to_response(context)

	def post(self, request, comp_pkid):
		context = RequestContext(request)
		if request.POST['formtype'] == "delete":
			return self.delete_item(request, comp_pkid, 'scoredel')
		elif request.POST['formtype'] == "create":
			form_inst = forms.CreateScoreForm(comp_pkid, self.request.POST)
			#form_inst.clean()
			#form_inst(self.request.POST)
			#form_inst = forms.CreateScoreForm(self.request.POST)
			if form_inst.errors:
				print '[ERROR] form failed to validate'
			form_data = form_inst.cleaned_data
			form_data['competition'] = comp_pkid
			self.make_api_request('scoreadd', form_data)
		return self.get(request, comp_pkid)

def list_scores(request, comp_pkid):
	page_template = template_path_prefix + 'list_scores.html'
	return getContext(context.ScoreListContext, request,
		page_template = page_template, comp_pkid = comp_pkid)

def create_score(request, comp_pkid):
	return getContext(context.ScoreCreateContext, request,
		redirect_url = '../', comp_pkid = comp_pkid)

def edit_score(request, comp_pkid, score_pkid):
	page_template = template_path_prefix + 'edit_score.html'
	return getContext(context.ScoreEditContext, request,
		page_template = page_template, comp_pkid = comp_pkid, pkid = score_pkid)

def getTeamChoices(comp_pkid):
	teamChoices = []
	output = make_api_request('teamget', {'competition': comp_pkid})
	for i in output['content']:
		teamChoices.append((i['id'], i['name']))
	return teamChoices