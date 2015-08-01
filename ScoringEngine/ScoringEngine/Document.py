from models import Document as DocumentModel

class Document:
	def __init__(self, document = None, **kwargs):
		self.model = document
		if not self.model:
			self.model = DocumentModel(**kwargs)

	def delete(self):
		self.model.delete()

	@staticmethod
	def search(**kwargs):
		return wrappedSearch(Document, DocumentModel, **kwargs)

	def setContentType(self, contentType):
		self.model.contentType = contentType
		self.model.save()

	def getContentType(self):
		return self.model.contentType

	def setFileHash(self, fileHash):
		self.model.fileHash = fileHash
		self.model.save()

	def getFileHash(self):
		return self.model.fileHash

	def setFilePath(self, filePath):
		self.model.filePath = filePath
		self.model.save()

	def getFilePath(self):
		return self.model.filePath

	def setFilename(self, filename):
		self.model.filename = filename
		self.model.save()

	def getFilename(self):
		return self.model.filename

	def setUrlEncodedFilename(self, urlEncodedFilename):
		self.model.urlEncodedFilename = urlEncodedFilename
		self.model.save()

	def getUrlEncodedFilename(self):
		return self.model.urlEncodedFilename