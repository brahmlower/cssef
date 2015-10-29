from django.apps import AppConfig
from django.db.utils import OperationalError
import pkgutil
from ScoringEngine import engines
from ScoringEngine.framework.core import getScoringEngine
from ScoringEngine.framework.core import createScoringEngine
from ScoringEngine.framework.core import ScoringEngine as ScoringEngineWrapper
import sys

class BackendConfig(AppConfig):
	name = 'ScoringEngine'
	verbose_name = 'Cyber Security Scoring Engine Framework'
	def ready(self):
		package = engines
		for importer, modname, ispkg in pkgutil.iter_modules(package.__path__):
			try:
				#scoringEngineEntry = getScoringEngine(packageName = modname)
				mod = importScoringEngine(modname)
				mod.run()
			except OperationalError:
				return None
			except ScoringEngineWrapper.ObjectDoesNotExist:
				createScoringEngine({'name': modname, 'packageName': modname})

def importScoringEngine(name):
	enginesModule = 'ScoringEngine.engines.%s'#.endpoints'
	scoringEngine = getScoringEngine(name = name)
	package = enginesModule % scoringEngine.packageName
	module = __import__(package)
	for i in package.split('.')[1:]:
		module = getattr(module, i)
	return module

