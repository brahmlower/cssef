from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import cssefserver

def establishDatabaseConnection():
	'Returns a database session for the specified database'
	dbEngine = create_engine('sqlite:///' + cssefserver.config.database_path)
	cssefserver.modelbase.Base.metadata.create_all(dbEngine)
	cssefserver.modelbase.Base.metadata.bind = dbEngine
	DBSession = sessionmaker(bind = dbEngine)
	return DBSession()