from django.conf.urls import patterns, include, url
from . import views
from . import Comp
from . import CompConfig
from . import AdminConfig
from . import Resources
import WebApi

urlpatterns = patterns('',
	url(r'^api/v1/', include('WebApi.urls')),
	url(r'^$', views.home),
	url(r'^competitions/login/$',												Comp.login),			# Sign in page for teams
	url(r'^competitions/logout/$',												Comp.logout),			# Sign out 'page' for teams
	url(r'^competitions/(?P<competition>[\w\-\_]{0,50})/$',						Comp.summary),			# Redirects to the summary page
	url(r'^competitions/(?P<competition>[\w\-\_]{0,50})/summary/$',				Comp.summary),			# Summary of the selected competition
	url(r'^competitions/(?P<competition>[\w\-\_]{0,50})/details/$',				Comp.details),			# Details regarding the competition
	url(r'^competitions/(?P<competition>[\w\-\_]{0,50})/ranking/$',				Comp.ranking),			# Rankings of teams in that competition
	url(r'^competitions/(?P<competition>[\w\-\_]{0,50})/injects/$',				Comp.injects),			# Changes a little after competition is over
	url(r'^competitions/(?P<competition>[\w\-\_]{0,50})/injects/(?P<ijctid>[1-9][1-9]*)/$', Comp.injects_respond), # Respond to a specific inject
	url(r'^competitions/(?P<competition>[\w\-\_]{0,50})/servicestatus/$',		Comp.servicestatus),	# Shows current status for services
	url(r'^competitions/(?P<competition>[\w\-\_]{0,50})/servicestatistics/$',	Comp.servicestatistics),# Shows status history for each service
	url(r'^competitions/(?P<competition>[\w\-\_]{0,50})/scoreboard/$',			Comp.scoreboard),		# Shows itemized list of point awards/penalties
	url(r'^competitions/(?P<competition>[\w\-\_]{0,50})/incidentresponse/$',	Comp.incidentresponse),	# Document submission for indicent responses
	url(r'^competitions/(?P<competition>[\w\-\_]{0,50})/incidentresponse/(?P<intrspid>[1-9][1-9]*)/$',	Comp.incidentresponse_respond), # LOL!
	# General administrator pages
	url(r'^admin/$',						AdminConfig.home),
	url(r'^admin/home/$',					AdminConfig.home),
	url(r'^admin/login/$',					AdminConfig.login),
	url(r'^admin/logout/$',					AdminConfig.logout),
	url(r'^admin/siteconfig/$',				AdminConfig.site_config),
	# User management pages
	url(r'^admin/users/$',					AdminConfig.users_list),
	url(r'^admin/users/edit/$',				AdminConfig.users_edit),
	url(r'^admin/users/delete/$',			AdminConfig.users_delete),
	url(r'^admin/users/create/$',			AdminConfig.users_create),
	# Service module pages
	url(r'^admin/servicemodules/$',			AdminConfig.servicemodule_list),
	url(r'^admin/servicemodules/create/$',	AdminConfig.servicemodule_create),
	url(r'^admin/servicemodules/edit/(?P<servmdulid>[1-9][1-9]*)/$',	AdminConfig.servicemodule_edit),
	url(r'^admin/servicemodules/test/(?P<servmdulid>[1-9][1-9]*)/$',	AdminConfig.servicemodule_test),	
	url(r'^admin/servicemodules/delete/(?P<servmdulid>[1-9][1-9]*)/$',	AdminConfig.servicemodule_delete),
	# Competition management pages
	url(r'^admin/competitions/$',			AdminConfig.comp_list),
	url(r'^admin/competitions/create/$',	AdminConfig.comp_create),
	url(r'^admin/competitions/(?P<competition>[\w\-\_]{0,50})/delete/$',	AdminConfig.comp_delete),
	# General competition configurations
	url(r'^admin/competitions/(?P<competition>[\w\-\_]{0,50})/$',			CompConfig.comp_summary),
	url(r'^admin/competitions/(?P<competition>[\w\-\_]{0,50})/summary/$',	CompConfig.comp_summary),
	url(r'^admin/competitions/(?P<competition>[\w\-\_]{0,50})/settings/$',	CompConfig.comp_settings),
	# Team related competition configurations
	url(r'^admin/competitions/(?P<competition>[\w\-\_]{0,50})/teams/$',									CompConfig.teams_list),
	url(r'^admin/competitions/(?P<competition>[\w\-\_]{0,50})/teams/edit/(?P<teamid>[1-9][1-9]*)/$',	CompConfig.teams_edit),
	url(r'^admin/competitions/(?P<competition>[\w\-\_]{0,50})/teams/delete/(?P<teamid>[1-9][1-9]*)/$',	CompConfig.teams_delete),
	url(r'^admin/competitions/(?P<competition>[\w\-\_]{0,50})/teams/create/$',							CompConfig.teams_create),
	# Service related competition configurations
	url(r'^admin/competitions/(?P<competition>[\w\-\_]{0,50})/services/$',									CompConfig.services_list),
	url(r'^admin/competitions/(?P<competition>[\w\-\_]{0,50})/services/edit/(?P<servid>[1-9][1-9]*)/$',		CompConfig.services_edit),
	url(r'^admin/competitions/(?P<competition>[\w\-\_]{0,50})/services/delete/(?P<servid>[1-9][1-9]*)/$',	CompConfig.services_delete),
	url(r'^admin/competitions/(?P<competition>[\w\-\_]{0,50})/services/create/$',							CompConfig.services_create),
	# Inject related competition configurations
	url(r'^admin/competitions/(?P<competition>[\w\-\_]{0,50})/injects/$',									CompConfig.injects_list),
	url(r'^admin/competitions/(?P<competition>[\w\-\_]{0,50})/injects/edit/(?P<ijctid>[1-9][1-9]*)/$',		CompConfig.injects_edit),
	url(r'^admin/competitions/(?P<competition>[\w\-\_]{0,50})/injects/delete/(?P<ijctid>[1-9][1-9]*)/$',	CompConfig.injects_delete),
	url(r'^admin/competitions/(?P<competition>[\w\-\_]{0,50})/injects/create/$',							CompConfig.injects_create),
	# Uploaded file related urls
	url(r'^resources/injects/(?P<compid>[1-9][1-9]*)/(?P<ijctid>[1-9][1-9]*)/(?P<filename>[\w\-\_\.\s\#]{0,64})$',	Resources.inject),
	url(r'^resources/injectresponses/(?P<compid>[1-9][1-9]*)/(?P<teamid>[1-9][1-9]*)/(?P<ijctrespid>[1-9][1-9]*)/(?P<filename>[\w\-\_\.\s\#]{0,64})$',	Resources.injectresponse),
	url(r'^resources/incidentresponses/(?P<compid>[1-9][1-9]*)/(?P<teamid>[1-9][1-9]*)/(?P<intrspid>[1-9][1-9]*)/(?P<filename>[\w\-\_\.\s\#]{0,64})$',	Resources.incidentresponse)

)
