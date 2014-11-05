# from cssef import Score
import paramiko

# TODO: This should eventually support keys somehow (I think)

# class Score:
#     def __init__(self, val_type, val):
#         # val_type should be either 'boolean' or 'integer'
#         # boolean: 1 is true, 0 is false
#         # integer is any integer value
#         self.val_type = val_type
#         self.val = val

class SSH:
	def __init__(self, conf_dict):
		self.id = conf_dict["id"]
		self.name = conf_dict["name"]
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
			return self.points
