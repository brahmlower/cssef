from django.conf.urls import patterns
from django.conf.urls import url
from WebInterface.modules.organization import views

urlpatterns = patterns('',
	url(r'^(?P<organizationUrl>[\w\-\_]{0,50})/$',						views.home),
	url(r'^(?P<organizationUrl>[\w\-\_]{0,50})/home/$',					views.home),
	url(r'^(?P<organizationUrl>[\w\-\_]{0,50})/members/$',				views.members),
	url(r'^(?P<organizationUrl>[\w\-\_]{0,50})/members/edit/(?P<username>[\w\-\_]{0,50})/$',	views.members),
	url(r'^(?P<organizationUrl>[\w\-\_]{0,50})/members/delete/(?P<username>[\w\-\_]{0,50})/$',	views.members),
	url(r'^(?P<organizationUrl>[\w\-\_]{0,50})/settings/$',				views.settings),
)