from framework.api import CssefCeleryApp
from cssefserver.framework.utils import ModelWrapper
from cssefserver.modules.document.models import Document as DocumentModel

class Document(ModelWrapper):
	modelObject = DocumentModel
	fields = [
		'contentType',
		'fileHash',
		'fielPath',
		'fileName',
		'urlEncodedFileName']

	@property
	def contentType(self):
		return self.model.contentType

	@contentType.setter
	def contentType(self, value):
		self.model.contentType = value
		self.db.commit()

	@property
	def fileHash(self):
		return self.model.fileHash

	@fileHash.setter
	def fileHash(self, value):
		self.model.fileHash = value
		self.db.commit()

	@property
	def filePath(self):
		return self.model.filePath

	@filePath.setter
	def filePath(self, value):
		self.model.filePath = value
		self.db.commit()

	@property
	def fileName(self):
		return self.model.fileName

	@fileName.setter
	def fileName(self, value):
		self.model.fileName = value
		self.db.commit()

	@property
	def urlEncodedFileName(self):
		return self.model.urlEncodedFileName

	@urlEncodedFileName.setter
	def setUrlEncodedFileName(self, value):
		self.model.urlEncodedFileName = value
		self.db.commit()