import unittest
import cssefserver

class EndpointOutputTest(unittest.TestCase):
    """Tests cssefserver.utils.EndpointOutput
    """
    def test_blank(self):
        end_out = cssefserver.utils.EndpointOutput()
        self.assertEquals(end_out.value, 0)
        self.assertEquals(end_out.message, [])
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

class HandleExceptionTest(unittest.TestCase):
    """Tests cssefserver.utils.handle_exception
    """
    def test_generic_exception(self):
        try:
            raise Exception
        except:
            end_out = cssefserver.utils.handle_exception()
            self.assertTrue(isinstance(end_out, dict))
            self.assertEquals(end_out['value'], 1)
            self.assertEquals(end_out['content'], [])

class ImportPluginTest(unittest.TestCase):
    """ Tests cssefserver.utils.import_plugin
    """
    def test_malformed_name_no_period(self):
        module_string = "doesntExist"
        with self.assertRaises(Exception) as context:
            cssefserver.utils.import_plugin(module_string)
        self.assertTrue(isinstance(context.exception, \
            cssefserver.errors.CssefPluginMalformedName))

    def test_malformed_name_non_alpha(self):
        module_string = "doesnt.Ex'ist"
        with self.assertRaises(Exception) as context:
            cssefserver.utils.import_plugin(module_string)
        self.assertTrue(isinstance(context.exception, \
            cssefserver.errors.CssefPluginMalformedName))

    def test_instantiation_error(self):
        module_string = "csseftest.TestPlugin"
        with self.assertRaises(Exception) as context:
            cssefserver.utils.import_plugin(module_string)
        self.assertTrue(isinstance(context.exception, \
            cssefserver.errors.CssefPluginInstantiationError))

    # This method is still under development...
    # def test_successful_import(self):
    #     class ExamplePlugin(cssefserver.Plugin):
    #         name = "ExamplePlugin"
    #         short_name = "ep"
    #     module_string = ".ExamplePlugin"
    #     instance = cssefserver.utils.import_plugin(module_string)
    #     self.assertTrue(isinstance(instance, cssefserver.Plugin))
