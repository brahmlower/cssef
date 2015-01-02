from django.utils import timezone
import json
class Pluggin:
	"""
	All pluggins should be children of this class. This ganrantees that each
	pluggin has these core values: 'points', 'net_type', 'subdomain', 'address'
	and 'default_port'. Additionally, 'build_address' is provided to get the
	full address for the team, regardless if they're being scored by dns or
	by an ipv4 address.
	"""
	def __init__(self, service_obj):
		self.service_name = service_obj.name
		self.points = service_obj.points
		self.connectip = service_obj.connectip
		self.networkloc = service_obj.networkloc
		self.port = service_obj.defaultport
		self.networkaddr = ""

	def update_configuration(self, team_obj):
		self.networkaddr = team_obj.networkaddr
		# Set the score configurations
		score_config_dict = json.loads(team_obj.score_configs)
		if self.service_name in score_config_dict:
			for key in score_config_dict[self.service_name]:
				value = score_config_dict[self.service_name][key]
				if (isinstance(value, self.team_config_type_dict[key]) or isinstance(value, unicode)) and len(str(value)) > 0:
					setattr(self, key, score_config_dict[self.service_name][key])

	def build_address(self, withport = None):
		addr = ""
		if self.connectip:
			addr = self.networkaddr + "." + self.networkloc
		else:
			addr = self.networkloc + "." + self.networkaddr
		if withport:
			return addr + ":" + str(self.port)
		return addr

class PlugginTest:
	"""
	This class handles the testing of the pluggin. It asks the user/tester for
	values that should be used for testing. These values are for the pluggin
	configuration overall, as well as specific configurations a team might
	have. Because the Pluggin.score() expects a Team object with score_configs,
	the Team class is emulated. This class provides EmulatedTeam, which only
	has score_configs, which holds the team specific configurations provided by
	the user/tester.
	"""
	def __init__(self, class_obj):
		self.config_list = ["points","net_type","subdomain","address","default_port"]
		self.class_inst = class_obj(self.get_pluggin_configs())
		self.team_config = self.get_team_config(class_obj)
		self.score()

	def get_pluggin_configs(self):
		print "\nGeneral service pluggin configurations."
		tmp_dict = {}
		for i in self.config_list:
			tmp_dict[i] = raw_input("Please enter a value for '%s': " % i)
		return tmp_dict

	def get_team_config(self, class_obj):
		print "\nTeam specific pluggin configurations."
		tmp_dict = {}
		class_dict = class_obj.team_config_type_dict
		for i in class_dict:
			prompt = "Please enter a(n) '%s' for '%s': " % (class_dict[i].__name__, i)
			tmp_dict[i] = class_dict[i](raw_input(prompt))
		# A blank line between the input sections and output
		print ""
		return tmp_dict

	def score(self):
		class_name = self.class_inst.__class__.__name__
		emulated_team = self.EmulatedTeam(class_name, self.team_config)
		score_obj = self.class_inst.score(emulated_team)
		print "[%s] Team:n/a Service:n/a Value:%s Messages:%s" % \
			(timezone.now(), score_obj.value, score_obj.message)

	class EmulatedTeam:
		"""
		Super simple emulation of a Team object, which simply provides
		score_configs. There might be a simpler way of doing this, but this
		seems to be working for now.
		"""
		def __init__(self, class_name, team_config):
			self.score_configs = {class_name: team_config}
