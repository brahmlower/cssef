#!/usr/bin/python
from . import CssefTest
from cssefserver.account import tasks

class OrganizationAdd(CssefTest):
    def test_only_name_provided(self):
        # Prepare the admin token
        self.config.admin_token = "abc123"
        # Instantiate the endpoint
        endpoint = tasks.OrganizationAdd(self.config, self.database_connection)
        # Call the endpoint as if it's been requested through flask
        authDict = {'admin-token': self.config.admin_token}
        orgDict = {'name': 'Test Org'}
        returnDict = endpoint(auth = authDict, **orgDict)
        # Verify that the return data is as expected
        self.assertEqual(returnDict['value'], 0)
        content = returnDict['content'][0]
        self.assertEqual(content['name'], 'Test Org')