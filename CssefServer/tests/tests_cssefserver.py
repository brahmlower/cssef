import tempfile
import unittest
import cssefserver

class ConfigurationTest(unittest.TestCase):
    """Tests cssefserver.Configuration
    """
    def test_set_setting(self):
        # Prepare the settings data to use
        setting_name = 'admin-token'
        setting_value = 'this is a token'
        # Test the settings
        configuration = cssefserver.Configuration()
        configuration.set_setting(setting_name, setting_value)
        self.assertEquals(configuration.admin_token, setting_value)

    def test_set_setting_fails(self):
        setting_name = 'not-real'
        configuration = cssefserver.Configuration()
        with self.assertRaises(ValueError) as context:
            configuration.set_setting(setting_name, 'testvalue')

    def test_from_dict(self):
        # Prepare the settings data to use
        settings_dict = {'admin-token': 'this is a token', "database-table-prefix": "test"}
        # Test the settings
        configuration = cssefserver.Configuration()
        configuration.from_dict(settings_dict)
        self.assertEquals(configuration.admin_token, settings_dict['admin-token'])

    def test_from_dict_setting_fails(self):
        # Prepare the settings data to use
        settings_dict = {'admin-token': 'this is a token', "not-real": "test"}
        # Test the settings
        configuration = cssefserver.Configuration()
        configuration.from_dict(settings_dict)
        self.assertEquals(configuration.admin_token, settings_dict['admin-token'])

    def test_from_file(self):
        # Prepare the settings data to use
        settings_file = tempfile.NamedTemporaryFile()
        settings_file.write("installed-plugins:\n- cssefctf.CaptureTheFlag")
        settings_file.flush()
        # Test the settings
        configuration = cssefserver.Configuration()
        configuration.from_file(settings_file.name)
        self.assertEquals(configuration.installed_plugins, ['cssefctf.CaptureTheFlag'])

class PluginTest(unittest.TestCase):
    def test_as_dict(self):
        golden_dict = {"name": "TestPlugin", "short_name": "tp", "version": ''}
        plugin = cssefserver.Plugin()
        plugin.name = golden_dict['name']
        plugin.short_name = golden_dict['short_name']
        self.assertEquals(golden_dict, plugin.as_dict())

    def test_endpoint_info(self):
        golden_dict = {"name": "Plugin", "endpoints": []}
        endpoint_info = cssefserver.Plugin.endpoint_info()
        self.assertEquals(golden_dict, endpoint_info)

