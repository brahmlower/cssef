class Pluggin:
	"""
	All pluggins should be children of this class. This ganrantees that each
	pluggin has these core values: 'points', 'net_type', 'subdomain', 'address'
	and 'default_port'. Additionally, 'build_address' is provided to get the
	full address for the team, regardless if they're being scored by dns or
	by an ipv4 address.
	"""
	def __init__(self, conf_dict):# points, net_type, subdomain, address, default_port):
		self.points = conf_dict["points"]
		self.net_type = conf_dict["net_type"]
		self.subdomain = conf_dict["subdomain"]
		self.address = conf_dict["address"]
		self.default_port = conf_dict["default_port"]

	def build_address(self, team_config):
		if self.net_type == "domainname":
			sd = self.subdomain
			dn = team_config["domainname"]
			return ".".join([str(sd), str(dn)])
		elif self.net_type == "ipaddress":
			nm = team_config["network"]
			na = self.address
			return ".".join([str(nm), str(na)])
		raise Exception("Bad Programming/User Error: no such '%s'. Should be {domain|ipaddress}" % self.net_type)


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
		print "" # To put a blank line between the input sections and output
		return tmp_dict

	def score(self):
		class_name = self.class_inst.__class__.__name__
		emulated_team = self.EmulatedTeam(class_name, self.team_config)
		score_obj = self.class_inst.score(emulated_team)
		print score_obj

	class EmulatedTeam:
		"""
		Super simple emulation of a Team object, which simply provides
		score_configs. There might be a simpler way of doing this, but this
		seems to be working for now.
		"""
		def __init__(self, class_name, team_config):
			self.score_configs = {class_name: json.dumps(team_config)}

class Score:
	"""
	The score object should be returned by score(). This provides basic
	information that may be useful for loggin and scoring. This currently
	only provides the score (as 'value'), a boolean indicating if the score was
	successfull, as well as a success or error message. If an error was thrown,
	it will be included in 'error_msg'.
	"""
	def __init__(self, success, value, error_msg=None, success_msg=None):
		self.success = success
		self.value = value
		self.error_msg = error_msg
		self.success_msg = success_msg

	def __str__(self):
		if self.success:
			return "Succeeded with value '%s' and message '%s'" % (str(self.value), self.success_msg)
		else:
			return "Failed with value '%s' and error '%s'" % (str(self.value), self.error_msg)