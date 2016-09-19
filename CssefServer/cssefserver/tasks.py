from __future__ import absolute_import
from cssefserver.utils import EndpointOutput
from cssefserver.taskutils import CssefRPCEndpoint

class AvailableEndpoints(CssefRPCEndpoint):
    """Provides a list of endpoint sources

    This will provide the list of raw enpoint source data, that being a list
    of dictionaries, where each dictionary is a single endpoint source
    containing information about the endpoints it provides.
    """
    name = "Available Endpoints"
    rpc_name = "availableendpoints"
    menu_path = None
    def on_request(self, *args):
        """RPC task to get all available celery endpoints.

        Returns:
            ReturnMessage: A return message where the content is a list of
            dictionaries containing information about the available endpoints.
        """
        return EndpointOutput(content=self.config.endpoint_sources)

class AvailablePlugins(CssefRPCEndpoint):
    """Provides a list of registered plugins

    This returns a list of the plugins that the server is using.
    """
    name = "Available Plugins"
    rpc_name = "availableplugins"
    menu_path = "availableplugins"
    def on_request(self, auth):
        """Get the list of plugins when the endpoint is requested

        Returns:
            ReturnMessage: A list of the plugins, where each entry is a result
            of calling ``plugin_instance.as_dict()``.
        """
        output = EndpointOutput()
        for plugin in self.config.installed_plugins:
            output.content.append(plugin.as_dict())
        return output

def endpoint_source():
    """Builds a dictionary defining the endpoints

    This builds an "endpoint dictionary" that defines information about the
    endpoints in this module and where their source, relative to the overall
    project.

    Returns:
        dict: Dictionary with the keys 'name' and 'endpoints'.
    """
    source_dict = {}
    source_dict['name'] = 'base'
    endpoints = []
    # Now add the endpoints to the endpoint_list
    endpoints.append(AvailableEndpoints.info_dict())
    endpoints.append(AvailablePlugins.info_dict())
    source_dict['endpoints'] = endpoints
    return source_dict
