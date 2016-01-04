from django.conf.urls import patterns
from django.conf.urls import url
from WebInterface.modules.competition.views import management
#from WebInterface.modules.competition.views import orangeteam
from WebInterface.modules.competition.views import whiteteam
from WebInterface.modules.competition.views import blueteam
#from WebInterface.modules.competition.views import redteam

urlpatterns = patterns('',
	# Management pages
	url(r'^(?P<organizationUrl>[\w\-\_]{0,50})/management/summary/$',	management.summary),
	url(r'^(?P<organizationUrl>[\w\-\_]{0,50})/management/list/$',		management.listCompetitions),
	url(r'^(?P<organizationUrl>[\w\-\_]{0,50})/management/create/$',	management.createCompetition),

	# Orange Team pages
	#url(r'^(?P<competitionUrl>[\w\-\_]{0,50})/teamorange/$', orangeteam.summary),

	# White Team pages
	url(r'^(?P<competitionUrl>[\w\-\_]{0,50})/teamwhite/summary/$',										whiteteam.summary),
	url(r'^(?P<competitionUrl>[\w\-\_]{0,50})/teamwhite/settings/$',									whiteteam.settings),
	url(r'^(?P<competitionUrl>[\w\-\_]{0,50})/teamwhite/teams/$',										whiteteam.listTeams),
	url(r'^(?P<competitionUrl>[\w\-\_]{0,50})/teamwhite/teams/create/$',								whiteteam.createTeam),
	url(r'^(?P<competitionUrl>[\w\-\_]{0,50})/teamwhite/teams/edit/(?P<teamId>[1-9][1-9]*)/$',			whiteteam.editTeam),
	# url(r'^(?P<competitionUrl>[\w\-\_]{0,50})/teamwhite/services/$',									whiteteam.listServices),
	# url(r'^(?P<competitionUrl>[\w\-\_]{0,50})/teamwhite/services/create/$',								whiteteam.createService),
	# url(r'^(?P<competitionUrl>[\w\-\_]{0,50})/teamwhite/services/edit/(?P<serviceId>[1-9][1-9]*)/$',	whiteteam.editService),
	url(r'^(?P<competitionUrl>[\w\-\_]{0,50})/teamwhite/injects/$',										whiteteam.listInjects),
	url(r'^(?P<competitionUrl>[\w\-\_]{0,50})/teamwhite/injects/create/$',								whiteteam.createInject),
	url(r'^(?P<competitionUrl>[\w\-\_]{0,50})/teamwhite/injects/edit/(?P<injectId>[1-9][1-9]*)/$',		whiteteam.editInject),

	# Blue Team pages
	url(r'^(?P<competitionUrl>[\w\-\_]{0,50})/teamblue/summary/$',										blueteam.summary),
	url(r'^(?P<competitionUrl>[\w\-\_]{0,50})/teamblue/details/$',										blueteam.details),
	url(r'^(?P<competitionUrl>[\w\-\_]{0,50})/teamblue/ranking/$',										blueteam.ranking),
	url(r'^(?P<competitionUrl>[\w\-\_]{0,50})/teamblue/injects/$',										blueteam.injects),
	url(r'^(?P<competitionUrl>[\w\-\_]{0,50})/teamblue/injects/(?P<ijctid>[1-9][1-9]*)/$', 				blueteam.injects_respond),
	url(r'^(?P<competitionUrl>[\w\-\_]{0,50})/teamblue/servicestatus/$',								blueteam.servicestatus),
	url(r'^(?P<competitionUrl>[\w\-\_]{0,50})/teamblue/servicestatistics/$',							blueteam.servicestatistics),
	url(r'^(?P<competitionUrl>[\w\-\_]{0,50})/teamblue/scoreboard/$',									blueteam.scoreboard),
	url(r'^(?P<competitionUrl>[\w\-\_]{0,50})/teamblue/incidentresponse/$',								blueteam.incidentresponse),
	url(r'^(?P<competitionUrl>[\w\-\_]{0,50})/teamblue/incidentresponse/(?P<intrspid>[1-9][1-9]*)/$',	blueteam.incidentresponse_respond),
)
	# Red Team pages
	#url(r'^(?P<competitionUrl>[\w\-\_]{0,50})/teamred/$', redteam.summary),