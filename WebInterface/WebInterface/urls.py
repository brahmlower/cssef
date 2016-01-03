from django.conf.urls import patterns
from django.conf.urls import include
from django.conf.urls import url
import views

urlpatterns = patterns('',
	# General site pages
	url(r'^$',			views.home),
	url(r'^updates/$',	views.updates),
	url(r'^contact/$',	views.contact),

	# Login/logout pages
	# url(r'^login/admin/$',		administrator.login),
	# url(r'^login/organization/$',	organization.login),
	# url(r'^logout/$',				general.logout),

	# Include urls for the various modules
	url(r'^admin/',			include('WebInterface.modules.administrator.urls')),
	url(r'^organization/',	include('WebInterface.modules.organization.urls')),
	url(r'^competition/',	include('WebInterface.modules.competition.urls')),
)
