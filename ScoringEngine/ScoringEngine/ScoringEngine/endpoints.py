from threading import Thread
from ScoringEngine.endpoints import ModelWrapper
from ScoringEngine.endpoints import getObject
from ScoringEngine.endpoints import getObjects
from models import Service as ServiceModel
from models import Plugin as PluginModel
from serializers import ServiceSerializer
from serializers import PluginSerializer

class Plugin(ModelWrapper):
	serializerObject = PluginSerializer
	modelObject = PluginModel

	def edit(self, **kwargs):
		self.serialized = kwargs.pop('serialized', None)
		for i in kwargs:
			if i == 'name':				self.setName(kwargs.get(i))
			elif i == 'description':	self.setDescription(kwargs.get(i))

	def getName(self):
		return self.model.name

	def setName(self, name):
		self.model.name = name
		self.model.save()

	def getDescription(self):
		return self.model.description

	def setDescription(self, description):
		self.model.description = description
		self.model.save()

	def getModuleName(self):
		#return Document.objects.get(servicemodule = self.servicemodule).filename.split(".")[0]
		pass

	def getImportPath(self, moduleName = None):
		if moduleName:
			#return settings.CONTENT_PLUGGINS_PATH.replace('/','.')[1:] + moduleName
			return ""
		else:
			return self.getImportPath(self.getModuleName())

class Service(ModelWrapper):
	serializerObject = ServiceSerializer
	modelObject = ServiceModel

	def edit(self, **kwargs):
		self.serialized = kwargs.pop('serialized', None)
		for i in kwargs:
			if i == 'name':				self.setName(kwargs.get(i))
			elif i == 'description':	self.setDescription(kwargs.get(i))
			elif i == 'manualStart':	self.setManualStart(kwargs.get(i))
			elif i == 'datetimeStart':	self.setDatetimeStart(kwargs.get(i))
			elif i == 'datetimeFinish':	self.setDatetimeFinish(kwargs.get(i))
			elif i == 'points':			self.setPoints(kwargs.get(i))
			elif i == 'machineIp':		self.setMachineIp(kwargs.get(i))
			elif i == 'machineFqdn':	self.setMachineFqdn(kwargs.get(i))
			elif i == 'defaultPort':	self.setDefaultPort(kwargs.get(i))

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

def getPlugin(**kwargs):
	return getObject(Plugin, **kwargs)

def getPlugins(**kwargs):
	return getObjects(Plugin, **kwargs)

def editPlugin(**kwargs):
	plugin = getPlugin(pluginId = kwargs.pop('pluginId', None))
	return plugin.edit(**kwargs)

def deletePlugin(**kwargs):
	kwargs.pop('serialized', None)
	getPlugin(**kwargs).delete()

def createPlugin(postData, serialized = False):
	return Plugin.create(Plugin, postData, serialized)

def getService(**kwargs):
	return getObject(Service, **kwargs)

def getServices(**kwargs):
	return getObjects(Service, **kwargs)

def editService(**kwargs):
	service = getService(serviceId = kwargs.pop('serviceId', None))
	return service.edit(**kwargs)

def deleteService(**kwargs):
	kwargs.pop('serialized', None)
	getService(**kwargs).delete()

def createService(postData, serialized = False):
	return Service.create(Service, postData, serialized)

def run():
	# This is the function that starts the whole Scoring Engine
	# if competition.isActive():
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

