from cssefserver.framework.utils import ModelWrapper
from cssefserver.modules.competition.engines.CssefScoringEngine.models import Plugin as PluginModel
from cssefserver.modules.competition.engines.CssefScoringEngine.models import Service as ServiceModel

class Plugin(ModelWrapper):
	modelObject = PluginModel
	fields = [
		'name',
		'description'
	]

	@property
	def name(self):
		return self.model.name

	@name.setter
	def name(self, value):
		self.model.name = value
		self.db.commit()

	@property
	def description(self):
		return self.model.description

	@description.setter
	def description(self, value):
		self.model.description = value
		self.db.commit()

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
	modelObject = ServiceModel
	fields = [
		'name',
		'description',
		'manualStart',
		'datetimeStart',
		'datetimeFinish',
		'points',
		'machineIp',
		'machineFqdn',
		'defaultPort'
	]

	@property
	def name(self):
		return self.model.name

	@name.setter
	def name(self, value):
		self.model.name = value
		self.db.commit()

	@property
	def description(self):
		return self.model.description

	@description.setter
	def description(self, value):
		self.model.description = value
		self.db.commit()

	@property
	def manualStart(self):
		return self.model.manualStart

	@manualStart.setter
	def manualStart(self, value):
		self.model.manualStart = value
		self.db.commit()

	@property
	def datetimeStart(self):
		return self.model.datetimeStart

	@datetimeStart.setter
	def datetimeStart(self, value):
		self.model.datetimeStart = value
		self.db.commit()

	@property
	def datetimeFinish(self):
		return self.model.datetimeFinish

	@datetimeFinish.setter
	def datetimeFinish(self, value):
		self.model.datetimeFinish = value
		self.db.commit()

	@property
	def points(self):
		return self.model.points

	@points.setter
	def points(self, value):
		self.model.points = value
		self.db.commit()

	@property
	def machineIp(self):
		return self.model.machineIp

	@machineIp.setter
	def machineIp(self, value):
		self.model.machineIp = value
		self.db.commit()

	@property
	def machineFqdn(self):
		return self.model.machineFqdn

	@machineFqdn.setter
	def machineFqdn(self, value):
		self.model.machineFqdn = value
		self.db.commit()

	@property
	def defaultPort(self):
		return self.model.defaultPort

	@defaultPort.setter
	def defaultPort(self, value):
		self.model.defaultPort = value
		self.db.commit()

	def score(self, team):
		instance = self.loadPlugin()
		scoreInstance = instance.score(team)
		scoreInstance.datetime = timezone.now()
		scoreInstance.teamId = team.teamId
		scoreInstance.serviceId = self.serviceId
		scoreInstance.competitionId = self.competitionId
		return score_obj

	# def loadPlugin(self):
	# 	#moduleName = Document.objects.get(servicemodule = self.servicemodule).filename.split(".")[0]
	# 	#module = __import__(settings.CONTENT_PLUGGINS_PATH.replace('/','.')[1:] + moduleName, fromlist=[moduleName])
	# 	moduleName = self.plugin.getModuleName()
	# 	module = __import__(self.plugin.getImportPath(moduleName), fromlist=[moduleName])
	# 	return getattr(module, moduleName)(self)