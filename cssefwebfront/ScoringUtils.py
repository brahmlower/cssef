from django.utils import timezone
import pickle
class Plugin:
	"""
	All plugins should be children of this class. This ganrantees that each
	plugin has these core values: 'points', 'net_type', 'subdomain', 'address'
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
		score_configs = pickle.loads(team_obj.score_configs)
		# Return none if there are no specific configurations for the service in this team
		if not self.service_name in score_configs:
			return None
		# Make all fields of the configurations members of this class
		for field_id in score_configs[self.service_name]:
			field_name = score_configs[self.service_name][field_id]["name"]
			field_instance = score_configs[self.service_name][field_id]["instance"]
			field_value = field_instance.get_value() # Does this mean that this istance is what holds the value set on a per team basis?
			if isinstance(field_value, field_instance.value_type):
				setattr(self, field_name, field_value)

	def build_address(self, machineaddr = None, withport = None):
		addr = ""
		if self.connectip:
			if not machineaddr:
				addr = self.networkaddr + "." + self.networkloc
			else:
				addr = machineaddr + "." + self.networkloc
		else:
			if not machineaddr:
				addr = self.networkloc + "." + self.networkaddr
			else:
				addr = machineaddr + "." + self.networkaddr
		if withport:
			return addr + ":" + str(self.port)
		return addr

class Integer:
	value_type = int
	def __init__(self, label=None, default_value=None, depends=None, required=False):
		self.label = label
		self.default_value = default_value
		self.required = required
		self.depends = depends
		self.value = None

	def get_value(self):
		if self.value:
			return self.value
		return self.default_value

	def set_value(self, value):
		if value != '':
			try:
				self.value = int(value)
			except ValueError:
				print "GOT A VALUE ERROR while trying to convert the string '%s'" % value
		else:
			self.value = None

	def __str__(self):
		return "label='%s' required='%s' depends='%s' default_value='%s' value='%s'" % (self.label, str(self.required), str(self.depends), str(self.default_value), str(self.value))

class Boolean:
	value_type = bool
	def __init__(self, label=None, default_value=None, depends=None, required=False):
		self.label = label
		self.default_value = default_value
		self.required = required
		self.depends = depends
		self.value = None

	def get_value(self):
		if self.value != None:
			return self.value
		return self.default_value

	def set_value(self, value):
		if value == 'False' or value == 'True':
			self.value = value
		else:
			self.value = None

	def __str__(self):
		return "label='%s' required='%s' depends='%s' default_value='%s' value='%s'" % (self.label, str(self.required), str(self.depends), str(self.default_value), str(self.value))

class String:
	value_type = str
	def __init__(self, label=None, default_value=None, depends=None, required=False):
		self.label = label
		self.default_value = default_value
		self.required = required
		self.depends = depends
		self.value = None

	def get_value(self):
		if self.value:
			return self.value
		return self.default_value

	def set_value(self, value):
		if value != '':
			self.value = value
		else:
			self.value = None

	def __str__(self):
		return "label='%s' required='%s' depends='%s' default_value='%s' value='%s'" % (self.label, str(self.required), str(self.depends), self.default_value, self.value)

class EmulatedTeam:
	"""
	Super simple emulation of a Team object, which simply provides
	score_configs. There might be a simpler way of doing this, but this
	seems to be working for now.
	"""
	def __init__(self, networkaddr):
		self.networkaddr = networkaddr
		self.score_configs = pickle.dumps({})

	def add_service(self, serv_obj, config_dict):
		tmp_score_configs = pickle.loads(self.score_configs)
		tmp_score_configs[serv_obj.name] = config_dict
		self.score_configs = pickle.dumps(tmp_score_configs)
