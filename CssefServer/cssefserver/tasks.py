from __future__ import absolute_import
import ast
import logging
from cssefserver.utils import get_empty_return_dict
from cssefserver.utils import CssefRPCEndpoint

class AvailableEndpoints(CssefRPCEndpoint):
    name = "Available Endpoints"
    rpc_name = "availableendpoints"
    menu_path = None
    def on_request(self, *args):
        """RPC task to get all available celery endpoints.

        Returns:
            A return_dict dictionary containing the results of the API call. The
            content is a list of dictionaries containing information about the
            available endpoints.
        """
        return_dict = get_empty_return_dict()
        return_dict['content'] = self.config.endpoint_sources
        return return_dict

class AvailablePlugins(CssefRPCEndpoint):
    name = "Available Plugins"
    rpc_name = "availableplugins"
    menu_path = "availableplugins"
    def on_request(self, auth):
        """RPC task to get all available competition plugins.

        Returns:
            A return_dict dictionary containing the results of the API call. The
            content is a list of dictionaries containing information about the
            available endpoints.
        """
        return_dict = get_empty_return_dict()
        plugin_dict_list = []
        for i in self.config.installed_plugins:
            plugin_dict_list.append(i.as_dict())
        return_dict['content'] = plugin_dict_list
        return return_dict

def endpoint_source():
    source_dict = {}
    source_dict['name'] = 'base'
    endpoints = []
    # Now add the endpoints to the endpoint_list
    endpoints.append(AvailableEndpoints.info_dict())
    endpoints.append(AvailablePlugins.info_dict())
    source_dict['endpoints'] = endpoints
    return source_dict
