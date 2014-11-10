from urllib2 import urlopen

# This requires 'paramiko'
# sudo pip install paramiko
#
# TODO: This should eventually support keys somehow

class HTTP:
	def __init__(self, conf_dict):
		self.port = conf_dict["port"]
		self.points = conf_dict["points"]
		self.subdomain = conf_dict["subdomain"]

	def score(self, team):
		host = "http://" + self.subdomain + "." + team.domainname
		try:
			request = urlopen(host)
			html = request.read()
			return self.points
		except:
			return 0
