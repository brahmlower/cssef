import os
import re
import sys
import stat

class CommandOutput(object):
    def __init__(self, value, message, content):
        self.value = value
        self.message = message
        # Cast the content to a list
        if isinstance(content, list):
            self.content = content
        elif isinstance(content, str):
            self.content = [content]
        else:
            raise ValueError
        # Get the keys of the content if it's a dict
        if len(self.content) > 0 and isinstance(self.content[0], dict):
            self.table_headers = self.content[0].keys()
        else:
            self.table_headers = None

    def __nonzero__(self):
        return self.value == 0

    def as_dict(self):
        temp_dict = {}
        temp_dict['value'] = self.value
        temp_dict['message'] = self.message
        temp_dict['content'] = self.content
        return temp_dict

class RPCEndpoint(object):
    """Base class to represent an endpoint task on the server.

    This class gets subclassed by other classes to define a specific
    task on the cssef server.
    """
    def __init__(self, config, rpc_name):
        """
        Args:
            config (Configuration): The current configuration to use
            rpc_name (str): The task name as defined by the rpc server
            args (list): Arguments that are available to the task

        Attributes:
            config (Configuration): The current configuration to use
            rpc_name (str): The task name as defined by the rpc server
            args (list): Arguments that are available to the task
        """
        self.config = config
        self.rpc_name = rpc_name

    def execute(self, **kwargs):
        """Calls the rpc endpoint on the remote server

        Args:
            **kwargs: Keyword arguments to pass to the rpc endpoint on the
                server.

        Returns:
            CommandOutput: The task data is cast to a CommandOutput object if
            the task completed successfully. If the task experiences an
            unhandled error, it is caught and a CommandOutput object is
            created with values describing the encountered exception.
        """
        if self.config.verbose:
            print "[LOGGING] Calling rpc with name '%s'."  % self.rpc_name
        try:
            # This is a hint at a larger issue- If I don't cast this to an
            # integer, it is passed to send_task() and get() as a string
            # rather than an expected integer. This means all values read
            # from the configuration object are strings, which may be
            # problematic if a value MUST be an integer.
            #task_timeout = int(self.config.task_timeout)
            #self.task = self.config.apiConn.send_task(self.endpointName,
            #    args = args, kwargs = kwargs, expires = task_timeout)
            #result = self.task.get(timeout = task_timeout)
            output_dict = self.config.server_connection.request(self.rpc_name, **kwargs)
            if output_dict:
                return CommandOutput(**output_dict)
            else:
                return CommandOutput(value=-1, content=[], \
                    message=['Call to endpoint returned "None".'])
        except Exception as err:
            return CommandOutput(value=-1, content=[], message=[str(err)])

def load_token_file(token_file):
    """Load token from a file

    This will try to load the token from the token cache file. If
    successful, it will save the token it finds in the `token` attribute
    for use while sending requests to the server.

    Returns:
        bool: True if token was successfully loaded, otherwise False.
    """
    # Make sure the file exists
    if not os.path.isfile(token_file):
        sys.stderr.write("[WARNING] Token file not found. Cannot use token authentication.\n")
        sys.stderr.flush()
        return None
    # Now make sure that only we have access to it
    file_permissions = os.stat(token_file).st_mode
    permissions_denied = [stat.S_IRGRP, stat.S_IWGRP, stat.S_IXGRP,
                          stat.S_IROTH, stat.S_IWOTH, stat.S_IXOTH]
    for i in permissions_denied:
        if bool(file_permissions & i):
            sys.stderr.write("Token file may not have any permissions for group or other.\n")
            sys.stderr.flush()
            return None
    # Now actually read in the file
    token = open(token_file, 'r').read()
    if len(token) > 0:
        return token
    return None

def save_token_file(token_file_path, token):
    # Save the returned token
    if not os.path.exists(token_file_path):
        # The file doesn't exist yet, make it
        open(token_file_path, 'a').close()
    os.chmod(token_file_path, stat.S_IRUSR | stat.S_IWUSR)
    open(token_file_path, 'w').write(token)

def parse_time_notation(value):
    value_notation_list = [
        {"value": 1, "alias": ["s", "second", "seconds"]},
        {"value": 60, "alias": ["m", "minute", "minutes"]},
        {"value": 3600, "alias": ["h", "hour", "hours"]},
        {"value": 86400, "alias": ["d", "day", "days"]}]
    strings = filter(None, re.split('(\d+)', value))
    time_value = strings[0]
    time_metric = strings[1]
    for i in value_notation_list:
        if time_metric in i['alias']:
            return i['value'] * time_value
    # Reaching this point means the metric is not a known alias
    raise ValueError
