from cssefserver.framework.utils import databaseConnection
from cssefserver.framework.utils import handleException
from cssefserver.framework.utils import getEmptyReturnDict
from cssefserver.framework.utils import modelDel
from cssefserver.framework.utils import modelSet
from cssefserver.framework.utils import modelGet
from cssefserver.framework import CssefCeleryApp
from cssefserver.framework import dbPath
from cssefserver.modules.document import Document

@CssefCeleryApp.task(name = 'documentAdd')
def documentAdd(**kwargs):
	try:
		db = databaseConnection(dbPath)
		document = Document.fromDict(db, kwargs)
		returnDict = getEmptyReturnDict()
		returnDict['content'].append(document.asDict())
		return returnDict
	except Exception as e:
		return handleException(e)

@CssefCeleryApp.task(name = 'documentDel')
def documentDel(document = None):
	try:
		if not document:
			raise Exception
		return modelDel(Document, document)
	except Exception as e:
		return handleException(e)

@CssefCeleryApp.task(name = 'documentSet')
def documentSet(document = None, **kwargs):
	try:
		if not document:
			raise Exception
		return modelSet(Document, document, **kwargs)
	except Exception as e:
		return handleException(e)

@CssefCeleryApp.task(name = 'documentGet')
def documentGet(**kwargs):
	try:
		return modelGet(Document, **kwargs)
	except Exception as e:
		return handleException(e)

endpointsDict = {
	"name": "Document",
	"author": "",
	"menuName": ["document"],
	"endpoints": [
		{	"name": "Add Document",
			"celeryName": "documentAdd",
			"menu": ["add"],
			"arguments": []
		},
		{	"name": "Del Document",
			"celeryName": "documentDel",
			"menu": ["del"],
			"arguments": []
		},
		{	"name": "Set Document",
			"celeryName": "documentSet",
			"menu": ["set"],
			"arguments": []
		},
		{	"name": "Get Document",
			"celeryName": "documentGet",
			"menu": ["get"],
			"arguments": []
		}
	]
}