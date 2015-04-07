from django.conf.urls import patterns
from django.conf.urls import include
from django.conf.urls import url
import views

urlpatterns = patterns('',
    url(r'^competitions.json', views.competitions),
    url(r'^competitions/(?P<competitionId>[0-9]+).json',  views.competition),
    url(r'^competitions/(?P<competitionId>[0-9]+)/teams.json', views.teams),
    url(r'^competitions/(?P<competitionId>[0-9]+)/teams/(?P<teamId>[0-9]+).json', views.team),
    url(r'^competitions/(?P<competitionId>[0-9]+)/services.json', views.services),
    url(r'^competitions/(?P<competitionId>[0-9]+)/services/(?P<serviceId>[0-9]+).json', views.service),
    url(r'^competitions/(?P<competitionId>[0-9]+)/scores.json', views.scores),
    url(r'^competitions/(?P<competitionId>[0-9]+)/scores/(?P<scoreId>[0-9]+).json', views.score),
    url(r'^competitions/(?P<competitionId>[0-9]+)/injects.json', views.injects),
    url(r'^competitions/(?P<competitionId>[0-9]+)/injects/(?P<injectId>[0-9]+).json', views.inject),
    url(r'^competitions/(?P<competitionId>[0-9]+)/injectresponses.json', views.injectresponses),
    url(r'^competitions/(?P<competitionId>[0-9]+)/injectresponses/(?P<injectResponseId>[0-9]+).json', views.injectresponse),
    url(r'^competitions/(?P<competitionId>[0-9]+)/incidentresponses.json', views.incidentresponses),
    url(r'^competitions/(?P<competitionId>[0-9]+)/incidentresponses/(?P<incidentResponseId>[0-9]+).json', views.incidentresponse),
    url(r'^plugins.json', views.plugins),
    url(r'^plugins/(?P<pluginId>[0-9]+).json', views.plugin),
    url(r'^users.json', views.users),
    url(r'^users/(?P<userId>[0-9]+).json', views.user),
    url(r'^organizations.json', views.organizations),
    url(r'^organizations/(?P<organizationId>[0-9]+).json', views.organization)
)
