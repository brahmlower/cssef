from django.conf.urls import patterns
from django.conf.urls import include
from django.conf.urls import url
from views import general
from views import administrator
from views import organization
from views import competitionWhite
from views import competitionBlue

urlpatterns = patterns('',
	# General site pages
	url(r'^$', general.home),

	# Blue Team Competition pages
	url(r'^competitions/login/$',																		competitionBlue.login),
	url(r'^competitions/logout/$',																		competitionBlue.logout),
	url(r'^competitions/(?P<competition>[\w\-\_]{0,50})/$',												competitionBlue.summary),
	url(r'^competitions/(?P<competition>[\w\-\_]{0,50})/summary/$',										competitionBlue.summary),
	url(r'^competitions/(?P<competition>[\w\-\_]{0,50})/details/$',										competitionBlue.details),
	url(r'^competitions/(?P<competition>[\w\-\_]{0,50})/ranking/$',										competitionBlue.ranking),
	url(r'^competitions/(?P<competition>[\w\-\_]{0,50})/injects/$',										competitionBlue.injects),
	url(r'^competitions/(?P<competition>[\w\-\_]{0,50})/injects/(?P<ijctid>[1-9][1-9]*)/$', 			competitionBlue.injects_respond),
	url(r'^competitions/(?P<competition>[\w\-\_]{0,50})/servicestatus/$',								competitionBlue.servicestatus),
	url(r'^competitions/(?P<competition>[\w\-\_]{0,50})/servicestatistics/$',							competitionBlue.servicestatistics),
	url(r'^competitions/(?P<competition>[\w\-\_]{0,50})/scoreboard/$',									competitionBlue.scoreboard),
	url(r'^competitions/(?P<competition>[\w\-\_]{0,50})/incidentresponse/$',							competitionBlue.incidentresponse),
	url(r'^competitions/(?P<competition>[\w\-\_]{0,50})/incidentresponse/(?P<intrspid>[1-9][1-9]*)/$',	competitionBlue.incidentresponse_respond),

	# Organization pages
	url(r'^organizations/(?P<organization>[\w\-\_]{0,50})/competitions/$',																			organization.listCompetitions),
	url(r'^organizations/(?P<organization>[\w\-\_]{0,50})/competitions/create/$',																	organization.createCompetitions),

	# White Team Competition pages
	url(r'^organizations/(?P<organization>[\w\-\_]{0,50})/competitions/(?P<competition>[\w\-\_]{0,50})/$',												competitionWhite.summary),
	url(r'^organizations/(?P<organization>[\w\-\_]{0,50})/competitions/(?P<competition>[\w\-\_]{0,50})/summary/$',										competitionWhite.summary),
	url(r'^organizations/(?P<organization>[\w\-\_]{0,50})/competitions/(?P<competition>[\w\-\_]{0,50})/settings/$',										competitionWhite.settings),
	url(r'^organizations/(?P<organization>[\w\-\_]{0,50})/competitions/(?P<competition>[\w\-\_]{0,50})/teams/$',										competitionWhite.listTeams),
	url(r'^organizations/(?P<organization>[\w\-\_]{0,50})/competitions/(?P<competition>[\w\-\_]{0,50})/teams/edit/(?P<teamId>[1-9][1-9]*)/$',			competitionWhite.editTeam),
	url(r'^organizations/(?P<organization>[\w\-\_]{0,50})/competitions/(?P<competition>[\w\-\_]{0,50})/teams/delete/(?P<teamId>[1-9][1-9]*)/$',			competitionWhite.deleteTeam),
	url(r'^organizations/(?P<organization>[\w\-\_]{0,50})/competitions/(?P<competition>[\w\-\_]{0,50})/teams/create/$',									competitionWhite.createTeam),
	url(r'^organizations/(?P<organization>[\w\-\_]{0,50})/competitions/(?P<competition>[\w\-\_]{0,50})/services/$',										competitionWhite.listServices),
	url(r'^organizations/(?P<organization>[\w\-\_]{0,50})/competitions/(?P<competition>[\w\-\_]{0,50})/services/edit/(?P<serviceId>[1-9][1-9]*)/$',		competitionWhite.editService),
	url(r'^organizations/(?P<organization>[\w\-\_]{0,50})/competitions/(?P<competition>[\w\-\_]{0,50})/services/delete/(?P<serviceId>[1-9][1-9]*)/$',	competitionWhite.deleteService),
	url(r'^organizations/(?P<organization>[\w\-\_]{0,50})/competitions/(?P<competition>[\w\-\_]{0,50})/services/create/$',								competitionWhite.createService),
	url(r'^organizations/(?P<organization>[\w\-\_]{0,50})/competitions/(?P<competition>[\w\-\_]{0,50})/injects/$',										competitionWhite.listInjects),
	url(r'^organizations/(?P<organization>[\w\-\_]{0,50})/competitions/(?P<competition>[\w\-\_]{0,50})/injects/edit/(?P<injectId>[1-9][1-9]*)/$',		competitionWhite.editInject),
	url(r'^organizations/(?P<organization>[\w\-\_]{0,50})/competitions/(?P<competition>[\w\-\_]{0,50})/injects/delete/(?P<injectId>[1-9][1-9]*)/$',		competitionWhite.deleteInject),
	url(r'^organizations/(?P<organization>[\w\-\_]{0,50})/competitions/(?P<competition>[\w\-\_]{0,50})/injects/create/$',								competitionWhite.createInject),

	# Administrator pages
	url(r'^admin/$',													administrator.home),
	url(r'^admin/home/$',												administrator.home),
	url(r'^admin/login/$',												administrator.login),
	url(r'^admin/logout/$',												administrator.logout),
	url(r'^admin/siteconfig/$',											administrator.site_config),
	url(r'^admin/users/$',												administrator.users_list),
	url(r'^admin/users/edit/$',											administrator.users_edit),
	url(r'^admin/users/delete/$',										administrator.users_delete),
	url(r'^admin/users/create/$',										administrator.users_create),
	url(r'^admin/servicemodules/$',										administrator.servicemodule_list),
	url(r'^admin/servicemodules/create/$',								administrator.servicemodule_create),
	url(r'^admin/servicemodules/edit/(?P<servmdulid>[1-9][1-9]*)/$',	administrator.servicemodule_edit),
	url(r'^admin/servicemodules/test/(?P<servmdulid>[1-9][1-9]*)/$',	administrator.servicemodule_test),	
	url(r'^admin/servicemodules/delete/(?P<servmdulid>[1-9][1-9]*)/$',	administrator.servicemodule_delete),

	# Uploaded file related urls
	url(r'^resources/injects/(?P<compid>[1-9][1-9]*)/(?P<ijctid>[1-9][1-9]*)/(?P<filename>[\w\-\_\.\s\#]{0,64})$',	Resources.inject),
	url(r'^resources/injectresponses/(?P<compid>[1-9][1-9]*)/(?P<teamid>[1-9][1-9]*)/(?P<ijctrespid>[1-9][1-9]*)/(?P<filename>[\w\-\_\.\s\#]{0,64})$',	Resources.injectresponse),
	url(r'^resources/incidentresponses/(?P<compid>[1-9][1-9]*)/(?P<teamid>[1-9][1-9]*)/(?P<intrspid>[1-9][1-9]*)/(?P<filename>[\w\-\_\.\s\#]{0,64})$',	Resources.incidentresponse)

)
