from cssefclient.utils import RPCEndpoint
from cssefclient.utils import save_token_file

class AvailableEndpoints(RPCEndpoint):
    def __init__(self, config):
        """Instiantiates a new instance of AvailableEndpoints.

        This is hardcoded because this task/endpoint will be available on all
        configurations of the server.

        Args:
            config (Configuration): The current configuration to use

        Attributes:
            config (Configuration): The current configuration to use
            endpointName (str): The rpc endpoint name
            args (list): The required arguments while calling the rpc endpoint
        """
        self.config = config
        self.rpc_name = 'availableendpoints'

class RenewToken(RPCEndpoint):
    def __init__(self, config):
        self.config = config
        self.rpc_name = 'renewtoken'

    def execute(self, **kwargs):
        print kwargs
        # # Populate the arguments to pass to the login
        # # Here we only need the username and the token
        # if not kwargs.get('username'):
        #     kwargs['username'] = self.config.username
        # if not kwargs.get('organization'):
        #     kwargs['organization'] = self.config.organization
        # if not kwargs.get('token'):
        #     kwargs['token'] = self.config.token
        # Attempt to log in
        return_dict = super(RenewToken, self).execute(**kwargs.get('auth'))
        if return_dict.value != 0:
            return return_dict
        token = return_dict.content[0]
        save_token_file(self.config.token_file, token)
        return_dict.content = ["Token rewnewal was successful."]
        return return_dict

class Login(RPCEndpoint):
    def __init__(self, config):
        self.config = config
        self.rpc_name = 'login'

    def execute(self, **kwargs):
        if not self.config.token_auth_enabled:
            # Bail if token authentication is disabled
            if self.config.verbose:
                print "[ERROR] Logging in requires that token authentication be \
                    enabled. Set 'token_auth_enabled: True' in your \
                    configuration."
            return None
        # Attempt to log in
        return_dict = super(Login, self).execute(**kwargs.get('auth'))
        if return_dict.value != 0:
            return return_dict
        # Save the returned token
        token = return_dict.content[0]
        save_token_file(self.config.token_file, token)
        return_dict.content = ["Authentication was successful."]
        return return_dict

class Logout(RPCEndpoint):
    def __init__(self, config):
        self.rpc_name = 'logout'
        self.config = config

    def execute(self):
        pass
