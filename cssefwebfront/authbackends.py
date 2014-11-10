from django.conf import settings
from django.contrib.auth.models import check_password

from models import Team
from models import Admins

class TeamAuth(object):
	def authenticate(self, teamname=None, password=None, compid=None):
		try:
			team = Team.objects.get(teamname = teamname, password = password, compid = compid)
			return team
		except:
			return None

	def get_user(self, teamname):
		try:
			return Team.objects.get(teamname = teamname)
		except Team.DoesNotExist:
			return None

# class Admins(object):
# 	def authenticate():
# 		pass