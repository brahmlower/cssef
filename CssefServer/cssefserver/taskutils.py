import abc
from cssefserver.utils import EndpointOutput
from cssefserver.utils import handle_exception
from cssefserver.errors import CssefException
from cssefserver.errors import InvalidPkidValue

class CssefRPCEndpoint(object):
    """Base class for RPC endpoints

    This class provides the functionality and utilities to create new RPC
    endpoints, consumable by clients.
    """
    name = None
    rpc_name = None
    menu_path = None
    takes_kwargs = True
    on_request_args = []
    def __init__(self, server):
        self.server = server

    def __call__(self, **kwargs):
        args_list = []
        # This builds the list of arguments we were told are expected
        # by the overloaded on_request() method
        for i in self.on_request_args:
            args_list.append(kwargs.get(i))
        for i in self.on_request_args:
            try:
                kwargs.pop(i)
            except KeyError:
                value = 1
                message = ["Missing required argument '%s'." % i]
                output = EndpointOutput(value, message)
                return output.as_dict()
        # Now call the on_request method that actually handles the request.
        # Here we're determining if we should pass it kwargs or not (the
        # subclass tells us yes or no). This is surrounded by a catch
        # to handle various errors that may crop up
        try:
            output = self.on_request(*args_list, **kwargs)
            return output.as_dict()
            # if self.takes_kwargs:
            #     output = self.on_request(*args_list, **kwargs)
            #     return output.as_dict()
            # else:
            #     output = self.on_request(*args_list)
            #     return output.as_dict()
        except CssefException as err:
            return err.as_return_dict()
        except Exception as err:
            return handle_exception()

    @classmethod
    def info_dict(cls):
        tmp_dict = {}
        tmp_dict['name'] = cls.name
        tmp_dict['rpc_name'] = cls.rpc_name
        tmp_dict['menu_path'] = cls.menu_path
        tmp_dict['reference'] = cls
        return tmp_dict

    @abc.abstractmethod
    def on_request(self, *args, **kwargs):
        """Abstract method for endpoint work

        This method is where work specifically for fufilling requests goes.
        When the RPC class is called, on_request() is called and wrapped in
        error handling and message passing so the subclass doesn't need to
        deal with it.

        This method **must** return a dictionary. For best results (for the
        client), that dictionary should conform to the "return_dict" structure
        losely defined in the code base. That structure being ``{'value': int,
        'message': [string], content: [string]}``
        """
        pass

# TODO: Split this function up. It's horribly by every measure...
def model_del(cls, database_connection, pkid):
    """Genaric function to delete models

    Args:
        cls (Model): The class type the pkid is refering to.
        database_connection (sqlalchemy.orm.Session): The existing database
            connection to use.
        pkid (int): The ID of the model instance to be deleted.

    Return:
        dict: A return dict indicating the result of the operation.
    """
    if pkid == "*":
        # todo: implement a wildcard
        value = 1
        message = ["Wildcards are not implemented yet."]
        return EndpointOutput(value, message)
    elif isinstance(pkid, str) and "-" in pkid:
        range_values = pkid.split("-")
        if len(range_values) == 2:
            try:
                for pkid in range(int(range_values[0]), int(range_values[1])+1):
                    model_obj = cls.from_database(database_connection, pkid)
                    if model_obj:
                        model_obj.delete()
                        return EndpointOutput()
            except ValueError:
                # One of the ranges provided could not be cast as an integer.
                # Return error.
                value = 1
                message = [("Range value could not be cast to integer. Expected"
                            " integer range like 1-4. Got '%s' instead." % pkid)]
                return EndpointOutput(value, message)
        else:
            value = 1
            message = [("Expected integer range like 1-4. Got '%s' instead." % pkid)]
            return EndpointOutput(value, message)
    elif isinstance(pkid, str) or isinstance(pkid, unicode):
        try:
            pkid = str(pkid)
        except ValueError:
            raise InvalidPkidValue
        model_obj = cls.from_database(database_connection, pkid)
        if model_obj:
            model_obj.delete()
            return EndpointOutput()
    elif isinstance(pkid, int):
        model_obj = cls.from_database(database_connection, pkid)
        model_obj.delete()
        return EndpointOutput()

    # We don't know what the hell we were given. Disregard it and thow
    # an error :(
    value = 1
    message = [("Expected integer value (5) or range (2-7). Got '%s' of type "
                "%s instead." % (str(pkid), str(type(pkid))))]
    return EndpointOutput(value, message)

def model_set(cls, database_connection, pkid, **kwargs):
    """Genaric function to modify model values

    Args:
        cls (Model): The class type the pkid is refering to.
        database_connection (sqlalchemy.orm.Session): The existing database
            connection to use.
        pkid (int): The ID of the model instance to be modified.

    Return:
        dict: A return dict indicating the result of the operation.
    """
    model_obj = cls.from_database(database_connection, pkid)
    model_obj.edit(**kwargs)
    content = [model_obj.as_dict()]
    return EndpointOutput(content=content)

def model_get(cls, database_connection, **kwargs):
    """Genaric function to get models

    Args:
        cls (Model): The class type to get entries from.
        database_connection (sqlalchemy.orm.Session): The existing database
            connection to use.

    Return:
        dict: A return dict indicating the result of the operation.
    """
    model_objs = cls.search(database_connection, **kwargs)
    output = EndpointOutput()
    # TODO: We're itterating here because model_objs is not a list, it's a querylist (iirc)
    # and really we need to find a clean way to convert that to a list, that way we don't
    # have to itterate over EVERY item returned.... Think smart, not hard.
    for i in model_objs:
        output.content.append(i.as_dict())
    return output
