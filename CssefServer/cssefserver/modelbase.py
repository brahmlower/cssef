from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative import declared_attr

class BaseModel(object):
    __name__ = ''

    @declared_attr
    def __tablename__(self):
        # Hardcoding the tablePrefix breaks the configurable feature
        # introduced in commit 993d87efef98d709209eead4340ff86a1da32f27
        table_prefix = "cssef"#cssefserver.config.database_table_prefix
        module_prefix = "test"
        module_name = self.__name__.lower()
        return "%s_%s_%s" % (table_prefix, module_prefix, module_name)

    pkid = Column(Integer, primary_key=True)

BASE = declarative_base(cls=BaseModel)
