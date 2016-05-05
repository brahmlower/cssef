from WebInterface.utils import getContext
from WebInterface.modules.competition import context

template_path_prefix = "competition/templates/whiteteam/"

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
def list_teams(request, comp_pkid):
	page_template = template_path_prefix + 'list_teams.html'
	return getContext(context.TeamListContext, request,
		page_template = page_template, comp_pkid = comp_pkid)

def create_team(request, comp_pkid):
	return getContext(context.TeamCreateContext, request,
		redirect_url = '../', comp_pkid = comp_pkid)

def edit_team(request, comp_pkid, team_pkid):
	page_template = template_path_prefix + 'edit_team.html'
	return getContext(context.TeamEditContext, request,
		page_template = page_template, comp_pkid = comp_pkid, pkid = team_pkid)

def delete_team(request, comp_pkid):
	return getContext(context.TeamDeleteContext, request, redirect_url = '../')

# ==================================================
# Inject Methods
# ==================================================
def list_injects(request, comp_pkid):
	page_template = template_path_prefix + 'list_injects.html'
	return getContext(context.InjectListContext, request,
		page_template = page_template, comp_pkid = comp_pkid)

def create_inject(request, comp_pkid):
	return getContext(context.InjectCreateContext, request,
		redirect_url = '../', comp_pkid = comp_pkid)

def edit_inject(request, comp_pkid, inject_pkid):
	page_template = template_path_prefix + 'edit_inject.html'
	return getContext(context.InjectEditContext, request,
		page_template = page_template, comp_pkid = comp_pkid, pkid = inject_pkid)

def delete_inject(request, comp_pkid):
	return getContext(context.InjectDeleteContext, request, redirect_url = '../')

# ==================================================
# Inject Response Methods
# ==================================================
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
def list_incidents(request, comp_pkid):
	page_template = template_path_prefix + 'list_incidents.html'
	return getContext(context.IncidentListContext, request,
		page_template = page_template, comp_pkid = comp_pkid)

def create_incident(request, comp_pkid):
	return getContext(context.IncidentCreateContext, request,
		redirect_url = '../', comp_pkid = comp_pkid)

def edit_incident(request, comp_pkid, incident_pkid):
	page_template = template_path_prefix + 'edit_incident.html'
	return getContext(context.IncidentEditContext, request,
		page_template = page_template, comp_pkid = comp_pkid, pkid = incident_pkid)

# ==================================================
# Incident Response Methods
# ==================================================
def list_incidentresponses(request, comp_pkid):
	page_template = template_path_prefix + 'list_incidentresponses.html'
	return getContext(context.IncidentResponseListContext, request,
		page_template = page_template, comp_pkid = comp_pkid)

def create_incidentresponse(request, comp_pkid):
	return getContext(context.IncidentResponseCreateContext, request,
		redirect_url = '../', comp_pkid = comp_pkid)

def edit_incidentresponse(request, comp_pkid, incidentresponse_pkid):
	page_template = template_path_prefix + 'edit_incidentresponse.html'
	return getContext(context.IncidentResponseEditContext, request,
		page_template = page_template, comp_pkid = comp_pkid, pkid = incidentresponse_pkid)

# ==================================================
# Score Methods
# ==================================================
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
