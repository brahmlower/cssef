import abc
from cssefserver.utils import EndpointOutput
from cssefserver.errors import CssefException

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
        except CssefException as err:
            return err.as_dict()
        except Exception as err:
            return EndpointOutput.from_traceback().as_dict()

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
        pass # pragma: no cover

def model_del(cls, server, pkid):
    """Genaric function to delete models

    Args:
        cls (Model): The class type the pkid is refering to.
        server (sqlalchemy.orm.Session): The existing database
            connection to use.
        pkid (int): The ID of the model instance to be deleted.

    Return:
        dict: A return dict indicating the result of the operation.
    """
    model_obj = cls.from_database(server, pkid)
    if model_obj:
        model_obj.delete()
    return EndpointOutput()

def model_set(cls, server, pkid, **kwargs):
    """Genaric function to modify model values

    Args:
        cls (Model): The class type the pkid is refering to.
        server (sqlalchemy.orm.Session): The existing database
            connection to use.
        pkid (int): The ID of the model instance to be modified.

    Return:
        dict: A return dict indicating the result of the operation.
    """
    model_obj = cls.from_database(server, pkid)
    model_obj.edit(**kwargs)
    content = [model_obj.as_dict()]
    return EndpointOutput(content=content)

def model_get(cls, server, **kwargs):
    """Genaric function to get models

    Args:
        cls (Model): The class type to get entries from.
        server (sqlalchemy.orm.Session): The existing database
            connection to use.

    Return:
        dict: A return dict indicating the result of the operation.
    """
    model_objs = cls.search(server, **kwargs)
    output = EndpointOutput()
    # TODO: We're looping over the whole list because we need to cast it all
    # to a dictionary. Really we should just define a proper way to serialize
    # the objects in model_objs
    for i in model_objs:
        output.content.append(i.as_dict())
    return output
