import tempfile
import unittest
import cssefserver

class CssefServerTest(unittest.TestCase):
    """Tests cssefserver.CssefServer
    """
    def test_server(self):
        server = cssefserver.CssefServer()
        user_object = create_org_and_user(self.database_connection)
        self.assertTrue(isinstance(user_object, User))

    def test_edit_user(self):
        user_object = create_org_and_user(self.database_connection)
        user_object.edit(name = "Super Bob")
        self.assertEquals(user_object.name, "Super Bob")

class ConfigurationTest(unittest.TestCase):
    """Tests cssefserver.Configuration
    """
    def test_settings_via_direct(self):
        # Prepare the settings data to use
        setting = 'admin-token'
        value = 'this is a token'
        # Test the settings
        configuration = cssefserver.Configuration()
        configuration.set_setting(setting, value)
        self.assertEquals(configuration.admin_token, value)

    def test_settings_via_dict(self):
        # Prepare the settings data to use
        settings_dict = {'admin-token': 'this is a token'}
        # Test the settings
        configuration = cssefserver.Configuration()
        configuration.load_settings_dict(settings_dict)
        self.assertEquals(configuration.admin_token, settings_dict['admin-token'])

    def test_settings_via_file(self):
        # Prepare the settings data to use
        settings_file = tempfile.NamedTemporaryFile()
        settings_file.write("installed-plugins:\n- cssefctf.CaptureTheFlag")
        settings_file.flush()
        # Test the settings
        configuration = cssefserver.Configuration()
        configuration.load_settings_file(settings_file.name)
        self.assertEquals(configuration.installed_plugins, ['cssefctf.CaptureTheFlag'])

    def test_multiple_settings_via_dict(self):
        # Prepare the settings data to use
        settings_dict = { "admin-token": "abcd", "database-table-prefix": "test" }
        # Test the settings
        configuration = cssefserver.Configuration()
        configuration.load_settings_dict(settings_dict)
        self.assertEquals(configuration.admin_token, settings_dict['admin-token'])
        self.assertEquals(configuration.database_table_prefix, settings_dict['database-table-prefix'])
