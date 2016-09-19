import traceback
from systemd import journal
import sqlalchemy.exc
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from cssefserver.modelbase import BASE as Base
from cssefserver import errors
# from cssefserver.errors import CssefException
# from cssefserver.errors import CssefPluginMalformedName
# from cssefserver.errors import CssefPluginInstantiationError

class EndpointOutput(object):
    def __init__(self, value=0, message='', content=None):
        self.value = value
        self.message = message
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

def create_database_connection(database_path=''):
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
    # Todo: this should maybe be called handle_endpoint_exception()
    value = 1
    message = traceback.format_exc().splitlines()
    output = EndpointOutput(value, message)
    # Log the occurance of this error
    journal.send(message="(error %d): Encountered runtime error with given id" #pylint: disable=no-member
                 " %d. Observe the following stack trace:" % (output.value, output.value)) #pylint: disable=no-member
    for i in output.message:
        journal.send(message="(error %d): %s" % (output.value, i)) #pylint: disable=no-member
    return output.as_dict()

def import_plugin(module_string):
    if len(module_string.split(".")) != 2:
        raise errors.CssefPluginMalformedName(module_string)
    module_name = module_string.split(".")[0]
    module_class = module_string.split(".")[1]
    try:
        module = __import__(module_name)
        plugin_class_ref = getattr(module, module_class)
        return plugin_class_ref()
    except:
        raise errors.CssefPluginInstantiationError(module_string)

def import_plugins(plugin_name_list):
    """Instantiates CSSEF competition plugins

    Plugins that were specified within the ``installed-plugins``
    configuration are instantiated here. Successfully loaded plugins are
    listed in ``self.plugins``. If a plugin fails to load, it is
    effectively removed from ``self.config.installed_plugins``.

    Returns:
        list
    """
    journal.send(message='Starting plugin import') #pylint: disable=no-member
    plugin_instance_list = []
    for module_string in plugin_name_list:
        try:
            plugin_instance = import_plugin(module_string)
            plugin_instance_list.append(plugin_instance)
        except errors.CssefException as error:
            journal.send(message=str(error)) #pylint: disable=no-member
    return plugin_instance_list
