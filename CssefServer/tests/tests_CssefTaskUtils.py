import tempfile
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm.session import Session
from . import CssefTest
import cssefserver
from cssefserver import taskutils
from cssefserver.account.api import Organization
from cssefserver.utils import EndpointOutput

class ModelDelTest(CssefTest):
    """ Tests cssefserver.taskutils.model_del
    """
    def test_del_object(self):
        # Make the object first
        org_dict = {"name": "testorg"}
        Organization.from_dict(self.database_connection, org_dict)
        # Now delete the object
        output = cssefserver.taskutils.model_del(Organization, self.database_connection, 1)
        # Make sure the return is what we expected
        self.assertTrue(isinstance(output, EndpointOutput))
        self.assertTrue(isinstance(output.content, list))
        self.assertEquals(len(output.content), 0)
        self.assertEquals(output.value, 0)
        # Now make sure the object is actually removed from the database
        output = cssefserver.taskutils.model_get(Organization, self.database_connection, pkid = 1)
        self.assertTrue(isinstance(output, EndpointOutput))
        self.assertTrue(isinstance(output.content, list))
        self.assertEquals(len(output.content), 0)
        self.assertEquals(output.value, 0)

    def test_del_missing_pkid(self):
        # Delete an object that isn't even there
        output = cssefserver.taskutils.model_del(Organization, self.database_connection, 1)
        # Make sure the return is what we expected
        self.assertTrue(isinstance(output, EndpointOutput))
        self.assertTrue(isinstance(output.content, list))
        self.assertEquals(len(output.content), 0)
        self.assertNotEquals(output.value, 0)

class ModelSetTest(CssefTest):
    """Tests cssefserver.taskutils.model_set
    """
    def test_set_single_field(self):
        # Make the object first
        org_dict = {"name": "testorg"}
        Organization.from_dict(self.database_connection, org_dict)
        # Now set the object
        output = cssefserver.taskutils.model_set(Organization, self.database_connection, 1, name = "testingname")
        # Make sure the return is what we expected
        self.assertTrue(isinstance(output, EndpointOutput))
        self.assertTrue(isinstance(output.content, list))
        self.assertEquals(len(output.content), 1)
        self.assertTrue(isinstance(output.content[0], dict))
        self.assertEquals(output.value, 0)
        self.assertEquals(output.content[0]["name"], "testingname")

    def test_set_multiple_fields(self):
        # Make the object first
        org_dict = {"name": "testorg"}
        Organization.from_dict(self.database_connection, org_dict)
        # Now set the object
        output = cssefserver.taskutils.model_set(Organization, self.database_connection, 1, name = "testingname", max_members = 10)
        # Make sure the return is what we expected
        self.assertTrue(isinstance(output, EndpointOutput))
        self.assertTrue(isinstance(output.content, list))
        self.assertEquals(len(output.content), 1)
        self.assertTrue(isinstance(output.content[0], dict))
        self.assertEquals(output.value, 0)
        self.assertEquals(output.content[0]["name"], "testingname")
        self.assertEquals(output.content[0]["max_members"], 10)

    def test_set_single_field(self):
        # TODO: I may want to change the name of the pkid field for model_set, that way it
        # can actually accept the pkid field. It should be the job of ModelWrapper to
        # specifically raise an error when there is an attempt to change the id.
        # Make the object first
        org_dict = {"name": "testorg"}
        Organization.from_dict(self.database_connection, org_dict)
        # Now set the object
        with self.assertRaises(Exception) as context:
            cssefserver.taskutils.model_set(Organization, self.database_connection, 1, pkid = 5)
        self.assertTrue(isinstance(context.exception, TypeError))

    def test_set_nonreal_field(self):
        # Make the object first
        org_dict = {"name": "testorg"}
        Organization.from_dict(self.database_connection, org_dict)
        # Now make sure an error is raised
        with self.assertRaises(Exception) as context:
            cssefserver.taskutils.model_set(Organization, self.database_connection, 1, name = "testingname", fakefield = "fakevalue")
        self.assertTrue(isinstance(context.exception, Exception))
        # TODO: A new error will need to be defined to to raise when a nonreal
        # value is set, to preserve the object in the event the user is setting
        # values on the wrong type of object. This should be checked *before* setting
        # any values. It should also be checked that each value applies correctly
        # before committing the values to the database

class ModelGetTest(CssefTest):
    """Tests cssefserver.taskutils.model_get
    """
    def test_get_single_object(self):
        # Make the object first
        org_dict = {"name": "testorg"}
        Organization.from_dict(self.database_connection, org_dict)
        output = cssefserver.taskutils.model_get(Organization, self.database_connection)
        # Make sure the return is what we expected
        self.assertTrue(isinstance(output, EndpointOutput))
        self.assertTrue(isinstance(output.content, list))
        self.assertEquals(len(output.content), 1)
        self.assertTrue(isinstance(output.content[0], dict))
        self.assertEquals(output.value, 0)

    def test_get_multiple_objects(self):
        # Make the objects first
        org_dict1 = {"name": "testorg1"}
        org_dict2 = {"name": "testorg2"}
        Organization.from_dict(self.database_connection, org_dict1)
        Organization.from_dict(self.database_connection, org_dict2)
        output = cssefserver.taskutils.model_get(Organization, self.database_connection)
        # Make sure the return is what we expected
        self.assertTrue(isinstance(output, EndpointOutput))
        self.assertTrue(isinstance(output.content, list))
        self.assertEquals(len(output.content), 2)
        self.assertTrue(isinstance(output.content[1], dict))
        self.assertEquals(output.value, 0)

    def test_get_filter_field(self):
        # Make the objects first
        org_dict1 = {"name": "testorg1"}
        org_dict2 = {"name": "testorg2"}
        Organization.from_dict(self.database_connection, org_dict1)
        Organization.from_dict(self.database_connection, org_dict2)
        output = cssefserver.taskutils.model_get(Organization, self.database_connection, name = "testorg1")
        # Make sure the return is what we expected
        self.assertTrue(isinstance(output, EndpointOutput))
        self.assertTrue(isinstance(output.content, list))
        self.assertEquals(len(output.content), 1)
        self.assertTrue(isinstance(output.content[0], dict))
        self.assertEquals(output.value, 0)
        self.assertEquals(output.content[0]["name"], "testorg1")