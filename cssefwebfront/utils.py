import json
from models import Service
from models import Team

def getAuthValues(request, c):
	c["auth"] = request.user.is_authenticated
	if request.user.is_authenticated:
		team = request.user.__class__.__name__
		if team == "Team":
			c["auth_name"] = "auth_team_blue"
			c["auth_name_display"] = "Blue Team"
		elif team == "Admin":
			c["auth_name"] = "auth_team_white"
			c["auth_name_display"] = "White Team"
		else:
			c["auth_name"] = "auth_team_red"
			c["auth_name_display"] = "Red Team"
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