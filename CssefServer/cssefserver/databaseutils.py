from systemd import journal
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative import declared_attr

class BaseModel(object):
    """A base model for the sqlalchemy models

    I defined a special base model in an attempt to set a prefix on the
    database tables. That functionality was broken at one point and hasn't
    been restored.
    """
    __name__ = ''
    pkid = Column(Integer, primary_key=True)

    @declared_attr
    def __tablename__(self):
        # Hardcoding the tablePrefix breaks the configurable feature
        # introduced in commit 993d87efef98d709209eead4340ff86a1da32f27
        table_prefix = "cssef"#cssefserver.config.database_table_prefix
        module_prefix = "test"
        module_name = self.__name__.lower()
        return "%s_%s_%s" % (table_prefix, module_prefix, module_name)

def get_foreign_key(cls, column="pkid"):
    """Gets foreign key of another model

    Args:
        cls (Model): Model we want to get the foreign key for
        column (string): The specific column to get a key for. Default is
            pkid. I'm not sure if you would even want to change the column.

    Returns:
        ForeignKey: Instantiated with the tablename and column name of the
        provided model.
    """
    key = "%s.%s" % (cls.__tablename__, column)
    return ForeignKey(key)

def create_database_connection(database_path=''):
    """Returns a database session for the specified database"""
    journal.send(message='Initializing database connection') #pylint: disable=no-member
    database_engine = create_engine('sqlite:///' + database_path)
    try:
        BASE.metadata.create_all(database_engine)
    except OperationalError as error:
        journal.send(message='Failed to open or sync database file: %s' % database_path) #pylint: disable=no-member
        raise error
    BASE.metadata.bind = database_engine
    database_session = sessionmaker(bind=database_engine)
    return database_session()

BASE = declarative_base(cls=BaseModel)
