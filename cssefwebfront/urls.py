from django.conf.urls import patterns, include, url
from . import views
from . import Comp
from . import CompConfig
from . import AdminConfig

urlpatterns = patterns('',
    url(r'^$', views.home),
    url(r'^competitions/$',                                                     Comp.list),              # List of the competitions
    url(r'^competitions/(?P<competition>[\w\-\_]{0,25})/$',                     Comp.summary),           # Redirects to the summary page
    url(r'^competitions/(?P<competition>[\w\-\_]{0,25})/summary/$',             Comp.summary),           # Summary of the selected competition
    url(r'^competitions/(?P<competition>[\w\-\_]{0,25})/details/$',             Comp.details),           # Details regarding the competition
    url(r'^competitions/(?P<competition>[\w\-\_]{0,25})/ranking/$',             Comp.rankings),          # Rankings of teams in that competition
    url(r'^competitions/(?P<competition>[\w\-\_]{0,25})/injects/$',             Comp.injects),           # Changes a little after competition is over
    url(r'^competitions/(?P<competition>[\w\-\_]{0,25})/teamlogin/$',           Comp.login),             # Sign in page for teams
    url(r'^competitions/(?P<competition>[\w\-\_]{0,25})/servicestatus/$',       Comp.servicestatus),     # Shows current status for services
    url(r'^competitions/(?P<competition>[\w\-\_]{0,25})/servicetimeline/$',     Comp.servicetimeline),   # Shows status history for each service
    url(r'^competitions/(?P<competition>[\w\-\_]{0,25})/scoreboard/$',          Comp.scoreboard),        # Shows itemized list of point awards/penalties
    url(r'^competitions/(?P<competition>[\w\-\_]{0,25})/incidentresponse/$',    Comp.incidentresponse),  # Document submission for indicent responses
    # General administrator pages
    url(r'^admin/$',                AdminConfig.home),
    url(r'^admin/home/$',           AdminConfig.home),
    url(r'^admin/login/$',          AdminConfig.login),
    url(r'^admin/siteconfig/$',     AdminConfig.site_config),
    # User management configurations
    url(r'^admin/users/$',          AdminConfig.users_list),
    url(r'^admin/users/edit/$',     AdminConfig.users_edit),
    url(r'^admin/users/delete/$',   AdminConfig.users_delete),
    url(r'^admin/users/create/$',   AdminConfig.users_create),
    # General competition configurations
    url(r'^admin/competitions/$',                                           CompConfig.list),
    url(r'^admin/competitions/create/$',                                    CompConfig.create),
    url(r'^admin/competitions/(?P<competition>[\w\-\_]{0,25})/$',           CompConfig.summary),
    url(r'^admin/competitions/(?P<competition>[\w\-\_]{0,25})/summary/$',   CompConfig.summary),
    url(r'^admin/competitions/(?P<competition>[\w\-\_]{0,25})/details/$',   CompConfig.details),
    url(r'^admin/competitions/(?P<competition>[\w\-\_]{0,25})/scoring/$',   CompConfig.scoring),
    # Team related competition configurations
    url(r'^admin/competitions/(?P<competition>[\w\-\_]{0,25})/teams/$',                                   CompConfig.teams_list),
    url(r'^admin/competitions/(?P<competition>[\w\-\_]{0,25})/teams/edit/(?P<teamid>[1-9][1-9]*)/$',      CompConfig.teams_edit),
    url(r'^admin/competitions/(?P<competition>[\w\-\_]{0,25})/teams/delete/(?P<teamid>[1-9][1-9]*)/$',    CompConfig.teams_delete),
    url(r'^admin/competitions/(?P<competition>[\w\-\_]{0,25})/teams/create/$',                            CompConfig.teams_create),
    # Service related competition configurations
    url(r'^admin/competitions/(?P<competition>[\w\-\_]{0,25})/services/$',                                CompConfig.services_list),
    url(r'^admin/competitions/(?P<competition>[\w\-\_]{0,25})/services/edit/(?P<servid>[1-9][1-9]*)/$',   CompConfig.services_edit),
    url(r'^admin/competitions/(?P<competition>[\w\-\_]{0,25})/services/delete/(?P<servid>[1-9][1-9]*)/$', CompConfig.services_delete),
    url(r'^admin/competitions/(?P<competition>[\w\-\_]{0,25})/services/create/$',                         CompConfig.services_create),
    # Inject related competition configurations
    url(r'^admin/competitions/(?P<competition>[\w\-\_]{0,25})/injects/$',                                     CompConfig.injects_list),
    url(r'^admin/competitions/(?P<competition>[\w\-\_]{0,25})/injects/edit/(?P<ijctid>[1-9][1-9]*)/$',      CompConfig.injects_edit),
    url(r'^admin/competitions/(?P<competition>[\w\-\_]{0,25})/injects/delete/(?P<ijctid>[1-9][1-9]*)/$',    CompConfig.injects_delete),
    url(r'^admin/competitions/(?P<competition>[\w\-\_]{0,25})/injects/create/$',                              CompConfig.injects_create),
)
