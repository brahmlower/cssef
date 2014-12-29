import json
from models import Service
from models import Team

def isAuthAdmin(request, c):
	user = request.user
	if user.is_authenticated() and user.__class__.__name__ == "Admin":
		c["admin_auth"] = True
	else:
		c["admin_auth"] = False
	return c

def isAuthBlueTeam(request, c):
	user = request.user
	if user.is_authenticated and user.__class__.__name__ == "Team":
		c["blue_team_auth"] = True
	else:
		c["blue_team_auth"] = False
	return c

class UserMessages:
	def __init__(self):
		self.info = []
		self.error = []
		self.success = []
	def new_info(self, string, num):
		self.info.append({"string":string, "num":num})

	def new_error(self, string, num):
		self.error.append({"string":string, "num":num})

	def new_success(self, string, num):
		self.success.append({"string":string, "num":num})

	def clear(self):
		self.info = []
		self.error = []
		self.success = []

def add_teams_scoreconfigs(compid):
	# Add service scoring configuration objects to each team
	services = Service.objects.filter(compid = compid)
	teams = Team.objects.filter(compid = compid)
	for t in teams:
		score_configs = json.loads(t.score_configs)
		for s in services:
			try:
				x = score_configs[s.module]
			except KeyError:
				score_configs[s.module] = {}
		target_team = Team.objects.filter(compid = compid, teamid = t.teamid)
		target_team.update(score_configs = json.dumps(score_configs))

def clean_teams_scoreconfigs(compid, module_str):
	# Removes the scoring configuration object from teams for services
	# that have been deleted
	services = Service.objects.filter(compid = compid)
	teams = Team.objects.filter(compid = compid)
	for t in teams:
		score_configs = json.loads(t.score_configs)
		score_configs.pop(module_str, None)
		target_team = Team.objects.filter(compid = compid, teamid = t.teamid)
		target_team.update(score_configs = score_configs)