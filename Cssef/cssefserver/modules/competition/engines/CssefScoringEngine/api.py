
scoringEngineEndpoints = {
	"name": "Scoring Engines",
	"author": "",
	"menuName": ["engines"],
	"endpoints": [
		{	"name": "Add Scoring Engine",
			"celeryName": "scoringEngineAdd",
			"menu": ["add"],
			"arguments": [
				{	"name": "Name",
					"argument": "name",
					"keyword": True,
					"optional": False
				},
				{	"name": "Package name",
					"argument": "packageName",
					"keyword": True,
					"optional": False
				}
			]
		},
		{	"name": "Delete Scoring Engine",
			"celeryName": "scoringEngineDel",
			"menu": ["del"],
			"arguments": [
				{	"name": "Scoring Engine",
					"argument": "scoringEngine",
					"keyword": True,
					"optional": False
				}
			]
		},
		{	"name": "Set Scoring Engine",
			"celeryName": "scoringEngineSet",
			"menu": ["set"],
			"arguments": [
				{	"name": "Name",
					"argument": "name",
					"keyword": True,
					"optional": True
				},
				{	"name": "Package name",
					"argument": "packageName",
					"keyword": True,
					"optional": True
				},
				{	"name": "Disabled",
					"argument": "disabled",
					"keyword": True,
					"optional": True
				}
			]
		},
		{	"name": "Get Scoring Engine",
			"celeryName": "scoringEngineGet",
			"menu": ["get"],
			"arguments": [
				{	"name": "Name",
					"argument": "name",
					"keyword": True,
					"optional": True
				},
				{	"name": "Package name",
					"argument": "packageName",
					"keyword": True,
					"optional": True
				},
				{	"name": "Disabled",
					"argument": "disabled",
					"keyword": True,
					"optional": True
				}
			]
		}
	]
}

# ==================================================
# Scoring Engine Endpoints
# ==================================================
@CssefCeleryApp.task(name = 'scoringEngineAdd')
def scoringengineAdd(**kwargs):
	try:
		db = databaseConnection(dbPath)
		scoringEngine = ScoringEngine.fromDict(db, kwargs)
		returnDict = getEmptyReturnDict()
		returnDict['content'].append(scoringEngine.asDict())
		return returnDict
	except Exception as e:
		return handleException(e)

@CssefCeleryApp.task(name = 'scoringEngineDel')
def scoringengineDel(scoringEngine = None):
	try:
		if not scoringEngine:
			raise Exception
		return modelDel(ScoringEngine, scoringEngine)
	except Exception as e:
		return handleException(e)

@CssefCeleryApp.task(name = 'scoringEngineSet')
def scoringengineSet(scoringEngine = None, **kwargs):
	try:
		if not scoringEngine:
			raise Exception
		return modelSet(ScoringEngine, scoringEngine, **kwargs)
	except Exception as e:
		return handleException(e)

@CssefCeleryApp.task(name = 'scoringEngineGet')
def scoringengineGet(**kwargs):
	try:
		return modelGet(ScoringEngine, **kwargs)
	except Exception as e:
		return handleException(e)