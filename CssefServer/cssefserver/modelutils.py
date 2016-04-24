from sqlalchemy import ForeignKey

def get_foreign_key(cls, column="pkid"):
    key = "%s.%s" % (cls.__tablename__, column)
    return ForeignKey(key)
