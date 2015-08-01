# This should only consume endpoint from the CompetitionEngine
from threading import Thread
from .models import Service as ServiceModel

def run():
	# This is the function that starts the whole Scoring Engine
	# if competition.isActive():
	pass

def test():
	# This should maybe run the tests within the scoring engine?
	pass

def scoringLoop(competition):
	while timezone.now() < competition.datetimeFinish:
		services = competition.getServices()
		teams = competition.getTeams()
		for service in services:
			for team in teams:
				scoreThread = Thread(target = scoreService, args = (competition, service, team))
				scoreThread.run()
		competition.sleepScoreInterval()

def scoreService(competition, service, team):
	print "Thread for scoring service '%s' for team '%s'" % (service.name, team.teamname)
	score = service.score(team)
	score.save()

class Service:
	def __init__(self, serviceModelObj = None, **kwargs):
		self.model = serviceModelObj
		if not self.model:
			self.model = ServiceModel(**kwargs)
			self.model.save()

	def delete(self):
		self.model.delete()

	@staticmethod
	def search(**kwargs):
		return wrappedSearch(Service, ServiceModel, **kwargs)

	def setName(self, name):
		self.model.name = name
		self.model.save()

	def getName(self):
		return self.model.name

	def setDescription(self, description):
		self.model.description = description
		self.model.save()

	def getDescription(self):
		return self.model.description

	def setManualStart(self, manualStart):
		self.model.manualStart = manualStart
		self.model.save()

	def getManualStart(self):
		return self.model.manualStart

	def setDatetimeStart(self, datetimeStart):
		self.model.datetimeStart = datetimeStart
		self.model.save()

	def getDatetimeStart(self):
		return self.model.datetimeStart

	def setDatetimeFinish(self, datetimeFinish):
		self.model.datetimeFinish = datetimeFinish
		self.model.save()

	def getDatetimeFinish(self):
		return self.model.datetimeFinish

	def setPoints(self, points):
		self.model.points = points
		self.model.save()

	def getPoints(self):
		return self.model.points

	def setMachineIp(self, machineIp):
		self.model.machineIp = machineIp
		self.model.save()

	def getMachineIp(self):
		return self.model.machineIp

	def setMachineFqdn(self, machineFqdn):
		self.model.machineFqdn = machineFqdn
		self.model.save()

	def getMachineFqdn(self):
		return self.model.machineFqdn

	def setDefaultPort(self, defaultPort):
		self.model.defaultPort = defaultPort
		self.model.save()

	def getDefaultPort(self):
		return self.model.defaultPort

	def score(team):
		# not yet updated for current code
		score = service.score(team)
		score.save()


# Copied from CompetitionEngine
# Service modules
# NOTE: These will very like be moved over to the scoring engine
def newService(self):
	pass

def getService(self):
	pass

def getServices(self):
	pass

def delService(self):
	pass


	# ULTIMATE SPEGETTHI (because fuck spelling) CODE