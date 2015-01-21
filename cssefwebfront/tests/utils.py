from django.test import Client
from django.utils import timezone
from datetime import timedelta
from cssefwebfront.models import Competition
from cssefwebfront.models import Team
from cssefwebfront.models import Admin

def create_comp(identifier):
	new_comp = Competition()
	new_comp.compname = "Test Competition"
	new_comp.compurl = "test_competition%s" % str(identifier)
	new_comp.description_short = "short description"
	new_comp.description_full = "full description"
	new_comp.datetime_display = timezone.now()
	new_comp.datetime_start = timezone.now()
	new_comp.datetime_finish = timezone.now() + timedelta(days=1)
	return new_comp

def create_blue(username, password, compid):
	new_blue = Team()
	new_blue.compid = compid
	new_blue.teamname = username
	new_blue.username = username
	new_blue.password = password
	new_blue.networkaddr = "depricated"
	new_blue.save()

def create_white(username, password):
	new_white = Admin()
	new_white.username = username
	new_white.password = password
	new_white.save()

def create_inject(compid, dt_d, dt_rd, dt_rc):
	new_inject = Inject()
	new_inject.compid = compid
	new_inject.dt_delivery = dt_d
	new_inject.dt_response_due = dt_rd
	new_inject.dt_response_close = dt_rc
	new_inject.title = "Test Inject"
	new_inject.body = "Test inject body"
	return new_inject

def prepare_open_inject(compid):
	dt_d = timezone.now()
	dt_rd = timezone.now() + timedelta(hours=1)
	dt_rc = timezone.now() + timedelta(hours=1)
	return create_inject(compid, dt_d, dt_rd, dt_rc)

def prepare_late_inject(compid):
	dt_d = timezone.now()
	dt_rd = timezone.now()
	dt_rc = timezone.now() + timedelta(hours=1)
	return create_inject(compid, dt_d, dt_rd, dt_rc)

def prepare_closed_inject(compid):
	dt_d = timezone.now()
	dt_rd = timezone.now()
	dt_rc = timezone.now()
	return create_inject(compid, dt_d, dt_rd, dt_rc)

def client_blue_login(username, password, compid):
	client = Client()
	post_data = {'username': username, 'password': password, 'compid': compid}
	return (client, client.post('/competitions/login/', post_data))

def client_white_login(username, password):
	client = Client()
	post_data = {'username': username, 'password': password}
	return (client, client.post('/admin/login/', post_data))