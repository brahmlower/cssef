import paramiko

# This requires 'paramiko'
# sudo pip install paramiko
#
# TODO: This should eventually support keys somehow

class SSH:
	def __init__(self, conf_dict):
		self.port = conf_dict["port"]
		self.username = conf_dict["username"]
		self.password = conf_dict["password"]
		self.points = conf_dict["points"]

	def score(self, team):
		host = team.net_addr
		client = paramiko.SSHClient()
		client.load_system_host_keys()
		client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		try:
			client.connect(host, self.port, self.username, self.password)
			client.close()
			return self.points
		except:
			# This should eventually catch only paramiko errors
			return 0
