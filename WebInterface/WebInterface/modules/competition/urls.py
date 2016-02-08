from django.conf.urls import patterns
from django.conf.urls import url
from WebInterface.modules.competition.views import management
#from WebInterface.modules.competition.views import orangeteam
from WebInterface.modules.competition.views import whiteteam
from WebInterface.modules.competition.views import blueteam
#from WebInterface.modules.competition.views import redteam

urlpatterns = patterns('',
	# Management pages
	url(r'^(?P<organizationUrl>[\w\-\_]{0,50})/management/summary/$',	management.listCompetitions),
	#url(r'^(?P<organizationUrl>[\w\-\_]{0,50})/management/list/$',		management.listCompetitions),
	url(r'^(?P<organizationUrl>[\w\-\_]{0,50})/management/create/$',	management.createCompetition),

	# Orange Team pages
	#url(r'^(?P<competitionUrl>[\w\-\_]{0,50})/teamorange/$', orangeteam.summary),

	# White Team pages
	url(r'^(?P<competitionId>\d+)/teamwhite/summary/$',										whiteteam.summary),
	url(r'^(?P<competitionId>\d+)/teamwhite/settings/$',									whiteteam.settings),
	url(r'^(?P<competitionId>\d+)/teamwhite/teams/$',										whiteteam.listTeams),
	url(r'^(?P<competitionId>\d+)/teamwhite/teams/create/$',								whiteteam.createTeam),
	url(r'^(?P<competitionId>\d+)/teamwhite/teams/edit/(?P<teamId>[1-9][1-9]*)/$',			whiteteam.editTeam),
	# url(r'^(?P<competitionUrl>[\w\-\_]{0,50})/teamwhite/services/$',									whiteteam.listServices),
	# url(r'^(?P<competitionUrl>[\w\-\_]{0,50})/teamwhite/services/create/$',								whiteteam.createService),
	# url(r'^(?P<competitionUrl>[\w\-\_]{0,50})/teamwhite/services/edit/(?P<serviceId>[1-9][1-9]*)/$',	whiteteam.editService),
	url(r'^(?P<competitionId>\d+)/teamwhite/injects/$',										whiteteam.listInjects),
	url(r'^(?P<competitionId>\d+)/teamwhite/injects/create/$',								whiteteam.createInject),
	url(r'^(?P<competitionId>\d+)/teamwhite/injects/edit/(?P<injectId>[1-9][1-9]*)/$',		whiteteam.editInject),

	# Blue Team pages
	url(r'^(?P<competitionId>\d+)/teamblue/summary/$',										blueteam.summary),
	url(r'^(?P<competitionId>\d+)/teamblue/details/$',										blueteam.details),
	url(r'^(?P<competitionId>\d+)/teamblue/ranking/$',										blueteam.ranking),
	url(r'^(?P<competitionId>\d+)/teamblue/injects/$',										blueteam.injects),
	url(r'^(?P<competitionId>\d+)/teamblue/injects/(?P<ijctid>[1-9][1-9]*)/$', 				blueteam.injects_respond),
	url(r'^(?P<competitionId>\d+)/teamblue/servicestatus/$',								blueteam.servicestatus),
	url(r'^(?P<competitionId>\d+)/teamblue/servicestatistics/$',							blueteam.servicestatistics),
	url(r'^(?P<competitionId>\d+)/teamblue/scoreboard/$',									blueteam.scoreboard),
	url(r'^(?P<competitionId>\d+)/teamblue/incidentresponse/$',								blueteam.incidentresponse),
	url(r'^(?P<competitionId>\d+)/teamblue/incidentresponse/(?P<intrspid>[1-9][1-9]*)/$',	blueteam.incidentresponse_respond),
)
	# Red Team pages
	#url(r'^(?P<competitionUrl>[\w\-\_]{0,50})/teamred/$', redteam.summary),