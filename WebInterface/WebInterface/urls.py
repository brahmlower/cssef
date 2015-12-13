from django.conf.urls import patterns
from django.conf.urls import url
from views import general
from views import organization
from views import administrator
#from views.competition import blueteam
from views.competition import whiteteam

urlpatterns = patterns('',
	# General site pages
	url(r'^$',			general.home),
	url(r'^updates/$',	general.updates),
	url(r'^contact/$',	general.contact),

	# Login/logout pages
	url(r'^login/admin/$',			administrator.login),
	url(r'^login/organization/$',	organization.login),
	#url(r'^login/competitions/$',	blueteam.login),
	url(r'^logout/$',				general.logout),

	# Blue Team Competition pages
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
	url(r'^organization/(?P<organizationUrl>[\w\-\_]{0,50})/$',						organization.home),
	url(r'^organization/(?P<organizationUrl>[\w\-\_]{0,50})/home/$',				organization.home),
	url(r'^organization/(?P<organizationUrl>[\w\-\_]{0,50})/members/$',				organization.members),
	url(r'^organization/(?P<organizationUrl>[\w\-\_]{0,50})/competitions/$',		organization.listCompetitions),
	url(r'^organization/(?P<organizationUrl>[\w\-\_]{0,50})/competitions/create/$',	organization.createCompetition),
	url(r'^organization/(?P<organizationUrl>[\w\-\_]{0,50})/settings/$',			organization.settings),

	# # White Team Competition pages
	url(r'^organization/(?P<organizationUrl>[\w\-\_]{0,50})/competitions/(?P<competitionUrl>[\w\-\_]{0,50})/$',												whiteteam.summary),
	url(r'^organization/(?P<organizationUrl>[\w\-\_]{0,50})/competitions/(?P<competitionUrl>[\w\-\_]{0,50})/summary/$',										whiteteam.summary),
	url(r'^organization/(?P<organizationUrl>[\w\-\_]{0,50})/competitions/(?P<competitionUrl>[\w\-\_]{0,50})/settings/$',									whiteteam.settings),
	url(r'^organization/(?P<organizationUrl>[\w\-\_]{0,50})/competitions/(?P<competitionUrl>[\w\-\_]{0,50})/teams/$',										whiteteam.listTeams),
	url(r'^organization/(?P<organizationUrl>[\w\-\_]{0,50})/competitions/(?P<competitionUrl>[\w\-\_]{0,50})/teams/create/$',								whiteteam.createEditTeam),
	url(r'^organization/(?P<organizationUrl>[\w\-\_]{0,50})/competitions/(?P<competitionUrl>[\w\-\_]{0,50})/teams/edit/(?P<teamId>[1-9][1-9]*)/$',			whiteteam.createEditTeam),
	url(r'^organization/(?P<organizationUrl>[\w\-\_]{0,50})/competitions/(?P<competitionUrl>[\w\-\_]{0,50})/services/$',									whiteteam.listServices),
	url(r'^organization/(?P<organizationUrl>[\w\-\_]{0,50})/competitions/(?P<competitionUrl>[\w\-\_]{0,50})/services/create/$',								whiteteam.createEditService),
	url(r'^organization/(?P<organizationUrl>[\w\-\_]{0,50})/competitions/(?P<competitionUrl>[\w\-\_]{0,50})/services/edit/(?P<serviceId>[1-9][1-9]*)/$',	whiteteam.createEditService),
	url(r'^organization/(?P<organizationUrl>[\w\-\_]{0,50})/competitions/(?P<competitionUrl>[\w\-\_]{0,50})/injects/$',										whiteteam.listInjects),
	url(r'^organization/(?P<organizationUrl>[\w\-\_]{0,50})/competitions/(?P<competitionUrl>[\w\-\_]{0,50})/injects/create/$',								whiteteam.createEditInject),
	url(r'^organization/(?P<organizationUrl>[\w\-\_]{0,50})/competitions/(?P<competitionUrl>[\w\-\_]{0,50})/injects/edit/(?P<injectId>[1-9][1-9]*)/$',		whiteteam.createEditInject),

	# Site Administrator pages
	url(r'^admin/$',											administrator.home),
	url(r'^admin/home/$',										administrator.home),
	url(r'^admin/siteconfigs/$',								administrator.siteConfig),
	url(r'^admin/users/$',										administrator.listUsers),
	url(r'^admin/users/create/$',								administrator.createUser),
	url(r'^admin/users/edit/(?P<userId>[\w\-\_]{0,50})/$',		administrator.editUser),
	url(r'^admin/organizations/$',								administrator.listOrganizations),
	url(r'^admin/organizations/create/$',						administrator.createOrganization),
	url(r'^admin/organizations/edit/(?P<organizationId>[\w\-\_]{0,50})/$',	administrator.editOrganization),
	url(r'^admin/plugins/$',									administrator.listPlugins),
	url(r'^admin/plugins/create/$',								administrator.createEditPlugin),
	url(r'^admin/plugins/edit/(?P<pluginId>[1-9][1-9]*)/$',		administrator.createEditPlugin),
	url(r'^admin/plugins/test/(?P<pluginId>[1-9][1-9]*)/$',		administrator.testPlugin),

	# # Uploaded file related urls
	# url(r'^resources/injects/(?P<compid>[1-9][1-9]*)/(?P<ijctid>[1-9][1-9]*)/(?P<filename>[\w\-\_\.\s\#]{0,64})$',	Resources.inject),
	# url(r'^resources/injectresponses/(?P<compid>[1-9][1-9]*)/(?P<teamid>[1-9][1-9]*)/(?P<ijctrespid>[1-9][1-9]*)/(?P<filename>[\w\-\_\.\s\#]{0,64})$',	Resources.injectresponse),
	# url(r'^resources/incidentresponses/(?P<compid>[1-9][1-9]*)/(?P<teamid>[1-9][1-9]*)/(?P<intrspid>[1-9][1-9]*)/(?P<filename>[\w\-\_\.\s\#]{0,64})$',	Resources.incidentresponse)

)
