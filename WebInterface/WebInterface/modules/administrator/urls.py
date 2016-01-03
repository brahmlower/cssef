from django.conf.urls import patterns
from django.conf.urls import url
from WebInterface.modules.administrator import views

urlpatterns = patterns('',
	url(r'^$',											views.home),
	url(r'^home/$',										views.home),
	url(r'^siteconfigs/$',								views.siteConfig),
	url(r'^users/$',									views.listUsers),
	url(r'^users/create/$',								views.createUser),
	url(r'^users/edit/(?P<userId>[\w\-\_]{0,50})/$',	views.editUser),
	url(r'^organizations/$',							views.listOrganizations),
	url(r'^organizations/create/$',						views.createOrganization),
	url(r'^organizations/edit/(?P<organizationId>[\w\-\_]{0,50})/$',	views.editOrganization),
	# url(r'^plugins/$',									administrator.listPlugins),
	# url(r'^plugins/create/$',								administrator.createEditPlugin),
	# url(r'^plugins/edit/(?P<pluginId>[1-9][1-9]*)/$',		administrator.createEditPlugin),
	# url(r'^plugins/test/(?P<pluginId>[1-9][1-9]*)/$',		administrator.testPlugin),
)