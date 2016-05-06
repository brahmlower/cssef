from django.conf.urls import patterns
from django.conf.urls import url
from WebInterface.modules.competition.views import management
#from WebInterface.modules.competition.views import orangeteam
from WebInterface.modules.competition.views import whiteteam
from WebInterface.modules.competition.views import blueteam
#from WebInterface.modules.competition.views import redteam

urlpatterns = patterns('',
	# Orange Team pages
	#url(r'^(?P<competitionUrl>[\w\-\_]{0,50})/teamorange/$', orangeteam.summary),

	# White Team pages
	# Summary
	url(r'^(?P<comp_pkid>\d+)/teamwhite/summary/$', whiteteam.summary),
	# URLs for configuration related pages
	# General Settings
	url(r'^(?P<comp_pkid>\d+)/teamwhite/settings/$', whiteteam.settings),
	# Services
	url(r'^(?P<comp_pkid>\d+)/teamwhite/services/$', whiteteam.list_services),
	url(r'^(?P<comp_pkid>\d+)/teamwhite/services/create/$', whiteteam.create_service),
	url(r'^(?P<comp_pkid>\d+)/teamwhite/services/edit/(?P<service_pkid>\d+)/$', whiteteam.edit_service),
	# Teams
	url(r'^(?P<comp_pkid>\d+)/teamwhite/teams/$', whiteteam.TeamView.as_view()),
	url(r'^(?P<comp_pkid>\d+)/teamwhite/teams/edit/(?P<team_pkid>\d+)/$', whiteteam.edit_team),
	# Injects
	url(r'^(?P<comp_pkid>\d+)/teamwhite/injects/$', whiteteam.InjectView.as_view()),
	url(r'^(?P<comp_pkid>\d+)/teamwhite/injects/edit/(?P<inject_pkid>\d+)/$', whiteteam.edit_inject),
	# URLs for review related pages
	# Inject Responses
	url(r'^(?P<comp_pkid>\d+)/teamwhite/injectresponses/$', whiteteam.InjectResponseView.as_view()),
	url(r'^(?P<comp_pkid>\d+)/teamwhite/injectresponses/edit/(?P<injectresponse_pkid>\d+)$', whiteteam.edit_injectresponse),
	# Incidents
	url(r'^(?P<comp_pkid>\d+)/teamwhite/incidents/$', whiteteam.IncidentView.as_view()),
	url(r'^(?P<comp_pkid>\d+)/teamwhite/incidents/edit/(?P<incident_pkid>\d+)$', whiteteam.edit_incident),
	# Incident Responses
	url(r'^(?P<comp_pkid>\d+)/teamwhite/incidentresponses/$', whiteteam.IncidentResponseView.as_view()),
	url(r'^(?P<comp_pkid>\d+)/teamwhite/incidentresponses/edit/(?P<incidentresponse_pkid>\d+)$', whiteteam.edit_incidentresponse),
	# Scores
	url(r'^(?P<comp_pkid>\d+)/teamwhite/scores/$', whiteteam.ScoreView.as_view()),
	url(r'^(?P<comp_pkid>\d+)/teamwhite/scores/edit/(?P<score_pkid>\d+)/$', whiteteam.edit_score),

	# Blue Team pages
	url(r'^(?P<competitionId>\d+)/teamblue/summary/$',										blueteam.summary),
	url(r'^(?P<competitionId>\d+)/teamblue/details/$',										blueteam.details),
	url(r'^(?P<competitionId>\d+)/teamblue/ranking/$',										blueteam.ranking),
	url(r'^(?P<competitionId>\d+)/teamblue/injects/$',										blueteam.injects),
	url(r'^(?P<competitionId>\d+)/teamblue/injects/(?P<ijctid>\d+)/$', 						blueteam.injects_respond),
	url(r'^(?P<competitionId>\d+)/teamblue/servicestatus/$',								blueteam.servicestatus),
	url(r'^(?P<competitionId>\d+)/teamblue/servicestatistics/$',							blueteam.servicestatistics),
	url(r'^(?P<competitionId>\d+)/teamblue/scoreboard/$',									blueteam.scoreboard),
	url(r'^(?P<competitionId>\d+)/teamblue/incidentresponse/$',								blueteam.incidentresponse),
	url(r'^(?P<competitionId>\d+)/teamblue/incidentresponse/(?P<intrspid>\d+)/$',			blueteam.incidentresponse_respond),
)
	# Red Team pages
	#url(r'^(?P<competitionUrl>[\w\-\_]{0,50})/teamred/$', redteam.summary),