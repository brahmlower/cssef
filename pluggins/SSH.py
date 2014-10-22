import paramiko

# TODO: This should eventually support keys somehow (I think)

class SSH:
	def __init__(self, conf_dict):
		self.name = conf_dict["name"]
		self.port = 22
		self.username = conf_dict["username"]
		self.password = conf_dict["password"]

	def score(self, team):
		host = team.net_addr
		client = paramiko.SSHClient()
		client.load_system_host_keys()
		client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		try:
			client.connect(host, self.port, self.username, self.password)
			client.close()
			return True
		except:
			return False
