from django.conf.urls import patterns
from django.conf.urls import url
from WebInterface.modules.organization import views

urlpatterns = patterns('',
	url(r'^(?P<organizationId>\d+)/$',						views.home),
	url(r'^(?P<organizationId>\d+)/home/$',					views.home),
	url(r'^(?P<organizationId>\d+)/members/$',				views.members),
	url(r'^(?P<organizationId>\d+)/members/edit/(?P<username>[\w\-\_]{0,50})/$',	views.members),
	url(r'^(?P<organizationId>\d+)/members/delete/(?P<username>[\w\-\_]{0,50})/$',	views.members),
	url(r'^(?P<organizationId>\d+)/settings/$',				views.settings),
	url(r'^(?P<organizationId>\d+)/plugin/(?P<plugin_name>[\w\-\_]{0,50})/$', views.compplugin_list),
	url(r'^(?P<organizationId>\d+)/plugin/(?P<plugin_name>[\w\-\_]{0,50})/create/$', views.compplugin_create),
	#url(r'^(?P<organizationId>\d+)/plugin/(?P<plugin_name>[\w\-\_]{0,50})/delete/$', views.compplugin_delete),
)