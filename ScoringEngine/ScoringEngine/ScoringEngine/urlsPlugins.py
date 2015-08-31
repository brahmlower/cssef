from django.conf.urls import patterns
from django.conf.urls import include
from django.conf.urls import url

import views

urlpatterns = patterns('',
	url(r'^plugins.json', views.plugins),
	url(r'^plugins/(?P<pluginId>[0-9]+).json', views.plugin),
)