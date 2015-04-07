from django.conf.urls import patterns
from django.conf.urls import include
from django.conf.urls import url
from views import general
from views import organization
from views import administrator
#from views import organization
#from views import competitionWhite
#from views import competitionBlue

urlpatterns = patterns('',
	# General site pages
	url(r'^$',			general.home),
	url(r'^updates/$',	general.updates),
	url(r'^contact/$',	general.contact),

	# Blue Team Competition pages
	# url(r'^competitions/login/$',																		competitionBlue.login),
	# url(r'^competitions/logout/$',																		competitionBlue.logout),
	# url(r'^competitions/(?P<competition>[\w\-\_]{0,50})/summary/$',										competitionBlue.summary),
	# url(r'^competitions/(?P<competition>[\w\-\_]{0,50})/details/$',										competitionBlue.details),
	# url(r'^competitions/(?P<competition>[\w\-\_]{0,50})/ranking/$',										competitionBlue.ranking),
	# url(r'^competitions/(?P<competition>[\w\-\_]{0,50})/injects/$',										competitionBlue.injects),
	# url(r'^competitions/(?P<competition>[\w\-\_]{0,50})/injects/(?P<ijctid>[1-9][1-9]*)/$', 			competitionBlue.injects_respond),
	# url(r'^competitions/(?P<competition>[\w\-\_]{0,50})/servicestatus/$',								competitionBlue.servicestatus),
	# url(r'^competitions/(?P<competition>[\w\-\_]{0,50})/servicestatistics/$',							competitionBlue.servicestatistics),
	# url(r'^competitions/(?P<competition>[\w\-\_]{0,50})/scoreboard/$',									competitionBlue.scoreboard),
	# url(r'^competitions/(?P<competition>[\w\-\_]{0,50})/incidentresponse/$',							competitionBlue.incidentresponse),
	# url(r'^competitions/(?P<competition>[\w\-\_]{0,50})/incidentresponse/(?P<intrspid>[1-9][1-9]*)/$',	competitionBlue.incidentresponse_respond),

	# # Organization pages
	url(r'^organization/(?P<organization>[\w\-\_]{0,50})/home/$',					organization.home),
	url(r'^organization/(?P<organization>[\w\-\_]{0,50})/members/$',				organization.members),
	url(r'^organization/(?P<organization>[\w\-\_]{0,50})/competitions/$',			organization.listCompetitions),
	url(r'^organization/(?P<organization>[\w\-\_]{0,50})/competitions/create/$',	organization.createCompetition),
	url(r'^organization/(?P<organization>[\w\-\_]{0,50})/settings/$',				organization.settings),

	# # White Team Competition pages
	# url(r'^organizations/(?P<organization>[\w\-\_]{0,50})/competitions/(?P<competition>[\w\-\_]{0,50})/$',												competitionWhite.summary),
	# url(r'^organizations/(?P<organization>[\w\-\_]{0,50})/competitions/(?P<competition>[\w\-\_]{0,50})/summary/$',										competitionWhite.summary),
	# url(r'^organizations/(?P<organization>[\w\-\_]{0,50})/competitions/(?P<competition>[\w\-\_]{0,50})/settings/$',										competitionWhite.settings),
	# url(r'^organizations/(?P<organization>[\w\-\_]{0,50})/competitions/(?P<competition>[\w\-\_]{0,50})/teams/$',										competitionWhite.listTeams),
	# url(r'^organizations/(?P<organization>[\w\-\_]{0,50})/competitions/(?P<competition>[\w\-\_]{0,50})/teams/edit/(?P<teamId>[1-9][1-9]*)/$',			competitionWhite.editTeam),
	# url(r'^organizations/(?P<organization>[\w\-\_]{0,50})/competitions/(?P<competition>[\w\-\_]{0,50})/teams/delete/(?P<teamId>[1-9][1-9]*)/$',			competitionWhite.deleteTeam),
	# url(r'^organizations/(?P<organization>[\w\-\_]{0,50})/competitions/(?P<competition>[\w\-\_]{0,50})/teams/create/$',									competitionWhite.createTeam),
	# url(r'^organizations/(?P<organization>[\w\-\_]{0,50})/competitions/(?P<competition>[\w\-\_]{0,50})/services/$',										competitionWhite.listServices),
	# url(r'^organizations/(?P<organization>[\w\-\_]{0,50})/competitions/(?P<competition>[\w\-\_]{0,50})/services/edit/(?P<serviceId>[1-9][1-9]*)/$',		competitionWhite.editService),
	# url(r'^organizations/(?P<organization>[\w\-\_]{0,50})/competitions/(?P<competition>[\w\-\_]{0,50})/services/delete/(?P<serviceId>[1-9][1-9]*)/$',	competitionWhite.deleteService),
	# url(r'^organizations/(?P<organization>[\w\-\_]{0,50})/competitions/(?P<competition>[\w\-\_]{0,50})/services/create/$',								competitionWhite.createService),
	# url(r'^organizations/(?P<organization>[\w\-\_]{0,50})/competitions/(?P<competition>[\w\-\_]{0,50})/injects/$',										competitionWhite.listInjects),
	# url(r'^organizations/(?P<organization>[\w\-\_]{0,50})/competitions/(?P<competition>[\w\-\_]{0,50})/injects/edit/(?P<injectId>[1-9][1-9]*)/$',		competitionWhite.editInject),
	# url(r'^organizations/(?P<organization>[\w\-\_]{0,50})/competitions/(?P<competition>[\w\-\_]{0,50})/injects/delete/(?P<injectId>[1-9][1-9]*)/$',		competitionWhite.deleteInject),
	# url(r'^organizations/(?P<organization>[\w\-\_]{0,50})/competitions/(?P<competition>[\w\-\_]{0,50})/injects/create/$',								competitionWhite.createInject),

	# Administrator pages
	url(r'^admin/$',											administrator.home),
	url(r'^admin/home/$',										administrator.home),
	url(r'^admin/login/$',										administrator.login),
	url(r'^admin/logout/$',										administrator.logout),
	url(r'^admin/siteconfig/$',									administrator.siteConfig),
	url(r'^admin/users/$',										administrator.listUsers),
	url(r'^admin/users/create/$',								administrator.createUser),
	url(r'^admin/users/edit/$',									administrator.editUser),
	url(r'^admin/organizations/$',								administrator.listOrganizations),
	url(r'^admin/organizations/create/$',						administrator.createOrganization),
	url(r'^admin/organizations/edit/$',							administrator.editOrganization),
	url(r'^admin/plugins/$',									administrator.listPlugins),
	url(r'^admin/plugins/create/$',								administrator.createPlugin),
	url(r'^admin/plugins/edit/(?P<servmdulid>[1-9][1-9]*)/$',	administrator.editPlugin),
	url(r'^admin/plugins/test/(?P<servmdulid>[1-9][1-9]*)/$',	administrator.testPlugin),

	# # Uploaded file related urls
	# url(r'^resources/injects/(?P<compid>[1-9][1-9]*)/(?P<ijctid>[1-9][1-9]*)/(?P<filename>[\w\-\_\.\s\#]{0,64})$',	Resources.inject),
	# url(r'^resources/injectresponses/(?P<compid>[1-9][1-9]*)/(?P<teamid>[1-9][1-9]*)/(?P<ijctrespid>[1-9][1-9]*)/(?P<filename>[\w\-\_\.\s\#]{0,64})$',	Resources.injectresponse),
	# url(r'^resources/incidentresponses/(?P<compid>[1-9][1-9]*)/(?P<teamid>[1-9][1-9]*)/(?P<intrspid>[1-9][1-9]*)/(?P<filename>[\w\-\_\.\s\#]{0,64})$',	Resources.incidentresponse)

)
