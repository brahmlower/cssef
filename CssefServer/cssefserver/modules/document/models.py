from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from cssefserver.framework.models import Base
from cssefserver.framework.models import tablePrefix

class Document(Base):
	__tablename__ = tablePrefix + 'document'
	pkid				= Column(Integer, primary_key = True)
	contentType			= Column(String(64))
	fileHash			= Column(String(32))
	filePath			= Column(String(64))
	fileName			= Column(String(64))
	urlEncodedFilename	= Column(String(128))