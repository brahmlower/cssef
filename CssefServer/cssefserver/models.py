from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from cssefserver.databaseutils import BASE as ModelBase
from cssefserver.databaseutils import get_foreign_key

class Organization(ModelBase):
    """This is a base User SQLAlchemy model.
    """
    deletable = Column(Boolean, default=True)
    can_add_users = Column(Boolean, default=True)
    can_delete_users = Column(Boolean, default=True)
    can_add_competitions = Column(Boolean, default=True)
    can_delete_competitions = Column(Boolean, default=True)
    name = Column(String(256))
    url = Column(String(256), default="")
    description = Column(String(1000), default="")
    max_members = Column(Integer, default=1)
    max_competitions = Column(Integer, default=1)
    num_members = Column(Integer)
    num_competitions = Column(Integer)

class User(ModelBase):
    """This is a base User SQLAlchemy model.
    """
    organization = Column(Integer, get_foreign_key(Organization))
    last_login = Column(DateTime)
    name = Column(String(20))
    username = Column(String(20))
    password = Column(String(64))
    description = Column(String(256), default="")
