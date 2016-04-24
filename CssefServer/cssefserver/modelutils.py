from sqlalchemy import ForeignKey

def getForeignKey(cls, column = "pkid"):
    key = "%s.%s" % (cls.__tablename__, column)
    return ForeignKey(key)