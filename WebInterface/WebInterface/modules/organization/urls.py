from django.conf.urls import patterns
from django.conf.urls import url
from WebInterface.modules.organization import views

urlpatterns = patterns('',
	url(r'^(?P<organizationUrl>[\w\-\_]{0,50})/$',						views.home),
	url(r'^(?P<organizationUrl>[\w\-\_]{0,50})/home/$',					views.home),
	url(r'^(?P<organizationUrl>[\w\-\_]{0,50})/members/$',				views.members),
	url(r'^(?P<organizationUrl>[\w\-\_]{0,50})/competitions/$',			views.listCompetitions),
	url(r'^(?P<organizationUrl>[\w\-\_]{0,50})/competitions/create/$',	views.createCompetition),
	url(r'^(?P<organizationUrl>[\w\-\_]{0,50})/settings/$',				views.settings),
)