from sqlalchemy import ForeignKey

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
