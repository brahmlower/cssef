#!/usr/bin/python
import unittest
from . import CssefTest
from cssefserver.account.api import Organization
from cssefserver.account.api import User

class UserTest(CssefTest):
    def test_create_minimal_user(self):
        user_object = create_org_and_user(self.database_connection)
        self.assertTrue(isinstance(user_object, User))

    def test_edit_user(self):
        user_object = create_org_and_user(self.database_connection)
        user_object.edit(name = "Super Bob")
        self.assertEquals(user_object.name, "Super Bob")

    def test_delete_user(self):
        user_object = create_org_and_user(self.database_connection)
        user_object.delete()
        user_object1 = User.from_database(self.database_connection, user_object.get_id())
        self.assertEquals(user_object1, None)

    def test_auth_password_success(self):
        user_object = create_org_and_user(self.database_connection)
        authed = user_object.authenticate_password("bobpass")
        self.assertTrue(authed)

    def test_auth_password_fail(self):
        user_object = create_org_and_user(self.database_connection)
        authed = user_object.authenticate_password("notpass")
        self.assertFalse(authed)

    def test_auth_token_success(self):
        user_object = create_org_and_user(self.database_connection)
        token = user_object.get_new_token()
        authed = user_object.authenticate_token(token)
        self.assertTrue(authed)

    def test_auth_token_fail(self):
        user_object = create_org_and_user(self.database_connection)
        token = "longfaketokenthatisntatoken"
        authed = user_object.authenticate_token(token)
        self.assertFalse(authed)

class OrganizationTest(CssefTest):
    def test_create_minimal_org(self):
        org_dict = { "name": "testorg" }
        org_object = Organization.from_dict(self.database_connection, org_dict)

def create_org_and_user(database_connection):
    org_dict = { "name": "testorg", "max_members": 10 }
    org_object = Organization.from_dict(database_connection, org_dict)
    user_dict = {
        'username': "bob",
        "name": "Bob",
        "password": "bobpass",
        "organization": org_object.get_id()
    }
    return User.from_dict(database_connection, user_dict)
