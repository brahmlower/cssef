from django.test import TestCase
from django.test import Client
from django.utils import timezone
from datetime import timedelta
from cssefwebfront.models import Competition
from cssefwebfront.models import Team
from cssefwebfront.models import Admin
from cssefwebfront.tests.utils import *

"""
Unit tests for Comp.py:
login
	test_login_success					Tests a legitimate blue team can log in to the competition
	test_login_fail_password			Auth attempt is denied if the password is wrong
	test_login_fail_username			Auth attempt is denied if the username is wrong
	test_login_fail_competition_exist	Auth attempt denied if competition does not exist
	test_login_fail_competition_start	Auth attempt denied if the competition hasn't started yet
	test_login_fail_competition_finish	Auth attempt denied if the competition has already finished
logout
	test_logout							Tests logout will redirect user to /home
summary
	test_auth_success
	test_unauth_success
details
	test_auth_success
	test_unauth_success
ranking
	test_auth_success
	test_unauth_success
injects
	test_blue_authed_success			Page will be provided if user is authed as a blue team
	test_white_authed_fail				Page will not be provided if user is authed as white team
	test_not_authed_fail				Page will not be provided if user is not authed at all
injects_respond
	TODO
servicestatus
	test_blue_authed_success
	test_white_authed_fail
	test_not_authed_fail
servicestatistics
	test_blue_authed_success
	test_white_authed_fail
	test_not_authed_fail
scoreboard
	test_blue_authed_success
	test_white_authed_fail
	test_not_authed_fail
incidentresponse
	test_blue_authed_success
	test_white_authed_fail
	test_not_authed_fail
incidentresponse_respond
	TODO
"""

class LoginTest(TestCase):
	def setUp(self):
		create_comp('1').save()
		create_blue('team1', 'team1', 1)

	def test_login_success(self):
		client, response = client_blue_login('team1', 'team1', 1)
		self.assertEqual(response.status_code, 302)

	def test_login_fail_password(self):
		client, response = client_blue_login('team1', 'team2', 1)
		self.assertEqual(response.status_code, 400)

	def test_login_fail_username(self):
		client, response = client_blue_login('team2', 'team2', 1)
		self.assertEqual(response.status_code, 400)

	def test_login_fail_competition_exist(self):
		client, response = client_blue_login('team1', 'team1', 2)
		self.assertEqual(response.status_code, 400)

	def test_login_fail_competition_start(self):
		pass

	def test_login_fail_competition_finish(self):
		pass

class LogoutTest(TestCase):
	def setUp(self):
		"""
		Creates a competition and a team
		"""
		create_comp('1').save()
		create_blue('team1', 'team1', 1)

	def test_logout(self):
		client, response = client_blue_login('team1', 'team1', 1)
		response = client.get('/competitions/logout/')
		self.assertEqual(response.status_code, 302)

class SummaryTest(TestCase):
	def setUp(self):
		create_comp('1').save()
		create_blue('team1', 'team1', 1)

	def test_auth_success(self):
		client, response = client_blue_login('team1', 'team1', 1)
		response = client.get('/competitions/test_competition1/summary/')
		self.assertEqual(response.status_code, 200)

	def test_unauth_success(self):
		client = Client()
		response = client.get('/competitions/test_competition1/summary/')
		self.assertEqual(response.status_code, 200)

class DetailsTest(TestCase):
	def setUp(self):
		create_comp('1').save()
		create_blue('team1', 'team1', 1)

	def test_auth_success(self):
		client, response = client_blue_login('team1', 'team1', 1)
		response = client.get('/competitions/test_competition1/details/')
		self.assertEqual(response.status_code, 200)

	def test_unauth_success(self):
		client = Client()
		response = client.get('/competitions/test_competition1/details/')
		self.assertEqual(response.status_code, 200)

class RankingTest(TestCase):
	def setUp(self):
		create_comp('1').save()
		create_blue('team1', 'team1', 1)

	def test_auth_success(self):
		client, response = client_blue_login('team1', 'team1', 1)
		response = client.get('/competitions/test_competition1/ranking/')
		self.assertEqual(response.status_code, 200)

	def test_unauth_success(self):
		client = Client()
		response = client.get('/competitions/test_competition1/ranking/')
		self.assertEqual(response.status_code, 200)

class InjectsTest(TestCase):
	def setUp(self):
		"""
		Creates a competition, a blue team, a white team user, and an inject
		"""
		create_comp('1').save()
		create_blue('team1', 'team1', 1)
		create_white('admin', 'admin')
		comp_obj = create_comp('2')
		comp_obj.teams_view_injects_enabled = False
		comp_obj.save()
		create_blue('teamZ', 'teamZ', 2)
		#prepare_open_inject(1).save()
		#prepare_late_inject(1).save()
		#prepare_closed_inject(1).save()

	def test_blue_authed_success(self):
		"""
		Tests that being successfully authenticated as blue team will return the page
		"""
		client, response = client_blue_login('team1', 'team1', 1)
		response = client.get('/competitions/test_competition1/injects/')
		self.assertEqual(response.status_code, 200)

	def test_white_authed_fail(self):
		"""
		Tests that being successfully authenticated as white team will not return the page
		"""
		client, response = client_white_login('admin', 'admin')
		response = client.get('/competitions/test_competition1/injects/')
		self.assertEqual(response.status_code, 403)

	def test_not_authed_fail(self):
		"""
		Tests that not being authenticated will not return the page
		"""
		client = Client()
		response = client.get('/competitions/test_competition1/injects/')
		self.assertEqual(response.status_code, 403)

	def test_injects_disabled(self):
		client, response = client_blue_login('teamZ', 'teamZ', 2)
		response = client.get('/competitions/test_competition2/injects/')
		self.assertEqual(response.status_code, 403)

class ServiceStatusTest(TestCase):
	def setUp(self):
		create_comp('1').save()
		create_blue('team1', 'team1', 1)
		create_white('admin', 'admin')

	def test_blue_authed_success(self):
		"""
		Tests that being successfully authenticated as blue team will return the page
		"""
		client, response = client_blue_login('team1', 'team1', 1)
		response = client.get('/competitions/test_competition1/injects/')
		self.assertEqual(response.status_code, 200)

	def test_white_authed_fail(self):
		"""
		Tests that being successfully authenticated as white team will not return the page
		"""
		client, response = client_white_login('admin', 'admin')
		response = client.get('/competitions/test_competition1/injects/')
		self.assertEqual(response.status_code, 403)

	def test_not_authed_fail(self):
		"""
		Tests that not being authenticated will not return the page
		"""
		client = Client()
		response = client.get('/competitions/test_competition1/injects/')
		self.assertEqual(response.status_code, 403)

class ServiceStatisticsTest(TestCase):
	def setUp(self):
		create_comp('1').save()
		create_blue('team1', 'team1', 1)
		create_white('admin', 'admin')

	def test_blue_authed_success(self):
		"""
		Tests that being successfully authenticated as blue team will return the page
		"""
		client, response = client_blue_login('team1', 'team1', 1)
		response = client.get('/competitions/test_competition1/injects/')
		self.assertEqual(response.status_code, 200)

	def test_white_authed_fail(self):
		"""
		Tests that being successfully authenticated as white team will not return the page
		"""
		client, response = client_white_login('admin', 'admin')
		response = client.get('/competitions/test_competition1/injects/')
		self.assertEqual(response.status_code, 403)

	def test_not_authed_fail(self):
		"""
		Tests that not being authenticated will not return the page
		"""
		client = Client()
		response = client.get('/competitions/test_competition1/injects/')
		self.assertEqual(response.status_code, 403)

class ScoreboardTest(TestCase):
	def setUp(self):
		create_comp('1').save()
		create_blue('team1', 'team1', 1)
		create_white('admin', 'admin')

	def test_blue_authed_success(self):
		"""
		Tests that being successfully authenticated as blue team will return the page
		"""
		client, response = client_blue_login('team1', 'team1', 1)
		response = client.get('/competitions/test_competition1/scoreboard/')
		self.assertEqual(response.status_code, 200)

	def test_white_authed_fail(self):
		"""
		Tests that being successfully authenticated as white team will not return the page
		"""
		client, response = client_white_login('admin', 'admin')
		response = client.get('/competitions/test_competition1/scoreboard/')
		self.assertEqual(response.status_code, 403)

	def test_not_authed_fail(self):
		"""
		Tests that not being authenticated will not return the page
		"""
		client = Client()
		response = client.get('/competitions/test_competition1/scoreboard/')
		self.assertEqual(response.status_code, 403)

class IncidentResponseTest(TestCase):
	def setUp(self):
		create_comp('1').save()
		create_blue('team1', 'team1', 1)
		create_white('admin', 'admin')

	def test_blue_authed_success(self):
		"""
		Tests that being successfully authenticated as blue team will return the page
		"""
		client, response = client_blue_login('team1', 'team1', 1)
		response = client.get('/competitions/test_competition1/incidentresponse/')
		self.assertEqual(response.status_code, 200)

	def test_white_authed_fail(self):
		"""
		Tests that being successfully authenticated as white team will not return the page
		"""
		client, response = client_white_login('admin', 'admin')
		response = client.get('/competitions/test_competition1/incidentresponse/')
		self.assertEqual(response.status_code, 403)

	def test_not_authed_fail(self):
		"""
		Tests that not being authenticated will not return the page
		"""
		client = Client()
		response = client.get('/competitions/test_competition1/incidentresponse/')
		self.assertEqual(response.status_code, 403)

