from cssefserver.utils import get_empty_return_dict
from cssefserver.errors import InvalidPkidValue

def model_del(cls, database_connection, pkid):
    if pkid == "*":
        # todo: implement a wildcard
        return_dict = get_empty_return_dict()
        return_dict['value'] = 1
        return_dict['message'] = ["Wildcards are not implemented yet."]
        return return_dict
    elif isinstance(pkid, str) and "-" in pkid:
        range_values = pkid.split("-")
        if len(range_values) == 2:
            try:
                for pkid in range(int(range_values[0]), int(range_values[1])+1):
                    model_obj = cls.from_database(database_connection, pkid)
                    if model_obj:
                        model_obj.delete()
                        return get_empty_return_dict()
            except ValueError:
                # One of the ranges provided could not be cast as an integer.
                # Return error.
                return_dict = get_empty_return_dict()
                return_dict['value'] = 1
                return_dict['message'] = [("Range value could not be cast to integer. Expected integer range like 1-4. Got '%s' instead." % pkid)]
                return return_dict
        else:
            print range_values
            return_dict = get_empty_return_dict()
            return_dict['value'] = 1
            return_dict['message'] = [("Expected integer range like 1-4. Got '%s' instead." % pkid)]
            return return_dict
    elif isinstance(pkid, str) or isinstance(pkid, unicode):
        try:
            pkid = str(pkid)
        except ValueError:
            raise InvalidPkidValue
        model_obj = cls.from_database(database_connection, pkid)
        if model_obj:
            model_obj.delete()
            return get_empty_return_dict()
    elif isinstance(pkid, int):
        model_obj = cls.from_database(database_connection, pkid)
        model_obj.delete()
        return get_empty_return_dict()

    # We don't know what the hell we were given. Disregard it and thow
    # an error :(
    return_dict = get_empty_return_dict()
    return_dict['value'] = 1
    return_dict['message'] = [("Expected integer value (5) or range (2-7). Got '%s' of type %s instead." % (str(pkid), str(type(pkid))))]
    return return_dict

def model_set(cls, database_connection, pkid, **kwargs):
    model_obj = cls.from_database(database_connection, pkid)
    model_obj.edit(**kwargs)
    return_dict = get_empty_return_dict()
    return_dict['content'].append(model_obj.as_dict())
    return return_dict

def model_get(cls, database_connection, **kwargs):
    model_objs = cls.search(database_connection, **kwargs)
    return_dict = get_empty_return_dict()
    for i in model_objs:
        return_dict['content'].append(i.as_dict())
    return return_dict
