import sys
import unittest
try:
    from unittest.mock import MagicMock
except ImportError:
    from mock import MagicMock
import cssefserver

class EndpointOutputTest(unittest.TestCase):
    """Tests cssefserver.utils.EndpointOutput
    """
    def test_blank(self):
        end_out = cssefserver.utils.EndpointOutput()
        self.assertEquals(end_out.value, 0)
        self.assertEquals(end_out.message, '')
        self.assertEquals(end_out.content, [])

    def test_as_dict(self):
        golden_dict = {"value": 1, "message": "It broke", "content": []}
        end_out = cssefserver.utils.EndpointOutput( \
            golden_dict['value'], \
            golden_dict['message'], \
            golden_dict['content'])
        self.assertEquals(end_out.as_dict(), golden_dict)

    def test_content_list(self):
        content = [1,2,3]
        end_out = cssefserver.utils.EndpointOutput(content = content)
        self.assertEquals(end_out.content, content)

    def test_content_str(self):
        content = "This is content."
        end_out = cssefserver.utils.EndpointOutput(content = content)
        self.assertEquals(end_out.content, [content])

    def test_from_traceback(self):
        try:
            raise Exception('test_from_traceback')
        except:
            end_out = cssefserver.utils.EndpointOutput().from_traceback()
            self.assertTrue(isinstance(end_out, cssefserver.utils.EndpointOutput))
            self.assertEquals(end_out.value, 1)
            self.assertEquals(end_out.content, [])
            print end_out.message
            self.assertTrue(end_out.message.endswith("Exception: test_from_traceback\n"))

class ImportPluginManagerTest(unittest.TestCase):
    """ Tests cssefserver.PluginManager
    """
    def test_import_from_string_malformed_no_period(self):
        module_string = "doesntExist"
        plugin_manager = cssefserver.PluginManager()
        with self.assertRaises(Exception) as context:
            plugin_manager.import_from_string(module_string)
        self.assertTrue(isinstance(context.exception, \
            cssefserver.errors.CssefPluginMalformedName))

    def test_import_from_string_malformed_non_alpha(self):
        module_string = "doesnt.Ex'ist"
        plugin_manager = cssefserver.PluginManager()
        with self.assertRaises(Exception) as context:
            plugin_manager.import_from_string(module_string)
        self.assertTrue(isinstance(context.exception, \
            cssefserver.errors.CssefPluginInstantiationError))

    def test_instantiation_error(self):
        module_string = "csseftest.TestMissingPlugin"
        with self.assertRaises(Exception) as context:
            cssefserver.utils.import_plugin(module_string)
        self.assertTrue(isinstance(context.exception, \
            cssefserver.errors.CssefPluginInstantiationError))

    def test_import_from_string_success(self):
        module_string = "csseftest.TestPlugin"
        sys.modules[module_string.split(".")[0]] = MagicMock(spec=cssefserver.Plugin)
        plugin_manager = cssefserver.PluginManager()
        plugin_manager.import_from_string(module_string)
        self.assertEquals(len(plugin_manager.available_plugins), 1)
        plugin_instance = plugin_manager.available_plugins[0]
        self.assertTrue(isinstance(plugin_instance, cssefserver.Plugin))

    def test_import_from_list_success(self):
        module_list = ["csseftest1.TestPlugin1", "csseftest2.TestPlugin2"]
        for i in module_list:
            sys.modules[i.split(".")[0]] = MagicMock(spec=cssefserver.Plugin)
        plugin_manager = cssefserver.PluginManager(module_list)
        self.assertEquals(len(plugin_manager.available_plugins), 2)
        for plugin_instance in plugin_manager.available_plugins:
            self.assertTrue(isinstance(plugin_instance, cssefserver.Plugin))
