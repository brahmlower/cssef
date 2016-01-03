from django.conf.urls import patterns
from django.conf.urls import url
#from modules.competition.views import orangeteam
from WebInterface.modules.competition.views import whiteteam
from WebInterface.modules.competition.views import blueteam
#from modules.competition.views import redteam

urlpatterns = patterns('',
	# Orange Team pages
	#url(r'^(?P<competitionUrl>[\w\-\_]{0,50})/teamorange/$', orangeteam.summary),

	# White Team pages
	url(r'^(?P<competitionUrl>[\w\-\_]{0,50})/teamwhite/summary/$',										whiteteam.summary),
	url(r'^(?P<competitionUrl>[\w\-\_]{0,50})/teamwhite/settings/$',									whiteteam.settings),
	url(r'^(?P<competitionUrl>[\w\-\_]{0,50})/teamwhite/teams/$',										whiteteam.listTeams),
	url(r'^(?P<competitionUrl>[\w\-\_]{0,50})/teamwhite/teams/create/$',								whiteteam.createEditTeam),
	url(r'^(?P<competitionUrl>[\w\-\_]{0,50})/teamwhite/teams/edit/(?P<teamId>[1-9][1-9]*)/$',			whiteteam.createEditTeam),
	url(r'^(?P<competitionUrl>[\w\-\_]{0,50})/teamwhite/services/$',									whiteteam.listServices),
	url(r'^(?P<competitionUrl>[\w\-\_]{0,50})/teamwhite/services/create/$',								whiteteam.createEditService),
	url(r'^(?P<competitionUrl>[\w\-\_]{0,50})/teamwhite/services/edit/(?P<serviceId>[1-9][1-9]*)/$',	whiteteam.createEditService),
	url(r'^(?P<competitionUrl>[\w\-\_]{0,50})/teamwhite/injects/$',										whiteteam.listInjects),
	url(r'^(?P<competitionUrl>[\w\-\_]{0,50})/teamwhite/injects/create/$',								whiteteam.createEditInject),
	url(r'^(?P<competitionUrl>[\w\-\_]{0,50})/teamwhite/injects/edit/(?P<injectId>[1-9][1-9]*)/$',		whiteteam.createEditInject),

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