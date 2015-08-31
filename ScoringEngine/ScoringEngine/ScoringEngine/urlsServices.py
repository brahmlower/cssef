from django.conf.urls import patterns
from django.conf.urls import include
from django.conf.urls import url

import views

urlpatterns = patterns('',
	url(r'^services.json', views.services),
	url(r'^services/(?P<serviceId>[0-9]+).json', views.service),
)