from cssefclient.utils import RPCEndpoint
from cssefclient.utils import save_token_file

class AvailablePlugins(RPCEndpoint):
    def __init__(self, config):
        self.config = config
        self.rpc_name = 'availableplugins'

class RenewToken(RPCEndpoint):
    def __init__(self, config):
        self.config = config
        self.rpc_name = 'renewtoken'

    def execute(self, **kwargs):
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
        self.rpc_name = 'user.login'

    def execute(self, **kwargs):
        if not self.config.token_auth_enabled:
            # Bail if token authentication is disabled
            if self.config.verbose:
                print ("[ERROR] Logging in requires that token "
                    "authentication be enabled. Set 'token_auth_enabled: "
                    "True' in your configuration.")
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
