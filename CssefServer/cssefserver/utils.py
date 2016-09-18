import abc
import traceback
from systemd import journal
# Database related imports
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sqlalchemy.exc
from cssefserver.modelbase import BASE as Base
from cssefserver.errors import CssefException
from cssefserver.errors import CssefObjectDoesNotExist

class CssefRPCEndpoint(object):
    """Base class for RPC endpoints

    This class provides the functionality and utilities to create new RPC
    endpoints, consumable by clients.
    """
    name = None
    rpc_name = None
    menu_path = None
    takesKwargs = True
    onRequestArgs = []
    def __init__(self, config, database_connection):
        self.config = config
        self.database_connection = database_connection

    def __call__(self, **kwargs):
        args_list = []
        # This builds the list of arguments we were told are expected
        # by the overloaded on_request() method
        for i in self.onRequestArgs:
            args_list.append(kwargs.get(i))
        for i in self.onRequestArgs:
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
            if self.takesKwargs:
                output = self.on_request(*args_list, **kwargs)
                return output.as_dict()
            else:
                output = self.on_request(*args_list)
                return output.as_dict()
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

class ModelWrapper(object):
    """ The base class for wrapping SQLAlchemy model objects

    This class provides utilities for interacting with SQLAlchemy models
    in a clean manner. This should be subclassed by any other objects that
    will need to wrap a SQLAlchemy model object.
    """
    __metaclass__ = abc.ABCMeta
    class ObjectDoesNotExist(CssefObjectDoesNotExist):
        def __init__(self, message):
            super(self.__class__, self).__init__(message)

    model_object = None
    fields = []

    def __init__(self, db_conn, model):
        self.db_conn = db_conn
        self.model = model
        self.define_properties()

    def define_properties(self):
        for i in self.fields:
            if not hasattr(self, i):
                attribute_get = self.__class__.dec_get(self, i)
                attribute_set = self.__class__.dec_set(self, i)
                prop = property(attribute_get, attribute_set)
                setattr(self.__class__, i, prop)

    def dec_get(self, attribute):
        def default_get(self):
            return getattr(self.model, attribute)

        return default_get

    def dec_set(self, attribute):
        def default_set(self, value):
            setattr(self.model, attribute, value)
            self.db_conn.commit()
        return default_set

    def get_id(self):
        return self.model.pkid

    def edit(self, **kwargs):
        for i in kwargs:
            if i in self.fields:
                setattr(self, i, kwargs[i])

    def delete(self):
        self.db_conn.delete(self.model)
        self.db_conn.commit()

    def as_dict(self):
        tmp_dict = {}
        tmp_dict['id'] = self.get_id()
        for i in self.fields:
            try:
                tmp_dict[i] = getattr(self, i)
            except AttributeError:
                # The field is not an attribute of the subclassed model wrapper
                # We'll try to find it in the classes model
                tmp_dict[i] = getattr(self.model, i)
        return tmp_dict

    @classmethod
    def count(cls, db_conn, **kwargs):
        return db_conn.query(cls.model_object).filter_by(**kwargs).count()

    @classmethod
    def search(cls, db_conn, **kwargs):
        model_object_list = db_conn.query(cls.model_object).filter_by(**kwargs)
        cls_list = []
        for i in model_object_list:
            cls_list.append(cls(db_conn, i))
        return cls_list

    @classmethod
    def from_database(cls, db_conn, pkid):
        try:
            return cls.search(db_conn, pkid=pkid)[0]
        except IndexError:
            return None

    @classmethod
    def from_dict(cls, db_conn, kw_dict):
        model_object_inst = cls.model_object() #pylint: disable=not-callable
        cls_inst = cls(db_conn, model_object_inst)
        for i in kw_dict:
            if i in cls_inst.fields:
                setattr(cls_inst, i, kw_dict[i])
        db_conn.add(cls_inst.model)
        db_conn.commit()
        return cls_inst

class EndpointOutput(object):
    def __init__(self, value=0, message=None, content=None):
        self.value = value
        self.message = message
        if not message:
            self.message = []
        # Cast the content to a list
        if not content:
            self.content = []
        elif isinstance(content, list):
            self.content = content
        elif isinstance(content, str):
            self.content = [content]
        else:
            raise ValueError

    def __nonzero__(self):
        return self.value == 0

    def as_dict(self):
        temp_dict = {}
        temp_dict['value'] = self.value
        temp_dict['message'] = self.message
        temp_dict['content'] = self.content
        return temp_dict

def create_database_connection(database_path):
    """Returns a database session for the specified database"""
    journal.send(message='Initializing database connection') #pylint: disable=no-member
    database_engine = create_engine('sqlite:///' + database_path)
    try:
        Base.metadata.create_all(database_engine)
    except sqlalchemy.exc.OperationalError as error:
        journal.send(message='Failed to open or sync database file: %s' % database_path) #pylint: disable=no-member
        raise error
    Base.metadata.bind = database_engine
    database_session = sessionmaker(bind=database_engine)
    return database_session()

def handle_exception():
    value = 1
    message = traceback.format_exc().splitlines()
    output = EndpointOutput(value, message)
    # Log the occurance of this error
    journal.send(message="(error %d): Encountered runtime error with given id" #pylint: disable=no-member
                 " %d. Observe the following stack trace:" % (output.value, output.value)) #pylint: disable=no-member
    for i in output.message:
        journal.send(message="(error %d): %s" % (output.value, i)) #pylint: disable=no-member
    return output.as_dict()
