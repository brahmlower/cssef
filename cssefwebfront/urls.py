from django.conf.urls import patterns, include, url
from . import views
from . import competition
from . import admin_config
#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', views.home),
    url(r'^competitions/$',                                                     competition.list),				# List of the competitions
    url(r'^competitions/(?P<competition>[\w\-\_]{0,25})/$',                     competition.summary),			# Redirects to the summary page
    #url(r'^competitions/(?P<competition>[\w\-\_]{0,25})/login/$',               competition.login),             # Logins!
    url(r'^competitions/(?P<competition>[\w\-\_]{0,25})/summary/$',             competition.summary),           # Summary of the selected competition
    url(r'^competitions/(?P<competition>[\w\-\_]{0,25})/details/$',	            competition.details),			# Details regarding the competition
    url(r'^competitions/(?P<competition>[\w\-\_]{0,25})/ranking/$',             competition.rankings),			# Rankings of teams in that competition
    url(r'^competitions/(?P<competition>[\w\-\_]{0,25})/injects/$',             competition.injects),			# Changes a little after competition is over
    url(r'^competitions/(?P<competition>[\w\-\_]{0,25})/teamlogin/$',			competition.login),             # Sign in page for teams
    url(r'^competitions/(?P<competition>[\w\-\_]{0,25})/servicestatus/$',		competition.servicestatus),		# Shows current status for services
    url(r'^competitions/(?P<competition>[\w\-\_]{0,25})/servicetimeline/$',     competition.servicetimeline),	# Shows status history for each service
    url(r'^competitions/(?P<competition>[\w\-\_]{0,25})/scoreboard/$',          competition.scoreboard),		# Shows itemized list of point awards/penalties
    url(r'^competitions/(?P<competition>[\w\-\_]{0,25})/incidentresponse/$',	competition.incidentresponse),	# Document submission for indicent responses
    url(r'^admin/$',                                                            admin_config.home),					# Admin login
    url(r'^admin/users/$',                                                      admin_config.users),				# Admin user management page
    url(r'^admin/login/$',                                                      admin_config.login),
    url(r'^admin/competitions/$',                                               admin_config.comp_list),    		# Admin competition management page
    url(r'^admin/competitions/(?P<competition>[\w\-\_]{0,25})/$',			    admin_config.comp_config_summary),	# Redirects to the summary page
    url(r'^admin/competitions/(?P<competition>[\w\-\_]{0,25})/summary/$',       admin_config.comp_config_summary),  # Comp Admin competition configuration page
    url(r'^admin/competitions/(?P<competition>[\w\-\_]{0,25})/details/$',       admin_config.comp_config_details),	# Comp Admin competition details configuration page
    url(r'^admin/competitions/(?P<competition>[\w\-\_]{0,25})/injects/$',       admin_config.comp_config_injects),	# Comp Admin competition injects configuration page
    url(r'^admin/competitions/(?P<competition>[\w\-\_]{0,25})/teams/$',         admin_config.comp_config_teams),	# Comp Admin competition teams configuration page
    url(r'^admin/competitions/(?P<competition>[\w\-\_]{0,25})/services/$',      admin_config.comp_config_services),	# Comp Admin competition services configuration page
    url(r'^admin/competitions/(?P<competition>[\w\-\_]{0,25})/services/delete/(?P<servid>[1-9][1-9]*)', admin_config.comp_config_service_delete),
    url(r'^admin/competitions/(?P<competition>[\w\-\_]{0,25})/scoring/$',       admin_config.comp_config_scoring),	# Comp Admin competition scoring configuration page
    url(r'^admin/competitions/(?P<competition>[\w\-\_]{0,25})/createteam/$',    admin_config.teams),
    url(r'^admin/competitions/(?P<competition>[\w\-\_]{0,25})/editteam/$',      admin_config.teams),
    url(r'^admin/competitions/(?P<competition>[\w\-\_]{0,25})/createservice/$', admin_config.services),
    url(r'^admin/competitions/(?P<competition>[\w\-\_]{0,25})/editservice/$',   admin_config.services),
    url(r'^admin/create-competition/$', admin_config.comp_create),   #Admin create comeptition page
)
