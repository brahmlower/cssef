from unittest import TestCase
from framework.utils import databaseConnection
from framework.core import Organization
from framework.core import User
from datetime import datetime

dbPath = '/home/sk4ly/Documents/cssef/Cssef/db.sqlite3'
dictOrganization = {
	'name': 'T Org',
	'url': 't_org',
	'maxCompetitions': 1}
dictUser = {
	'name': 'Test User',
	'username': 'tuser',
	'password': 'tpass'
}

class UserEndpoints(TestCase):
	def testUser_fromDict(self):
		dbConn = databaseConnection(dbPath)
		organization = Organization.fromDict(dbConn, dictOrganization)
		x = dictUser.copy()
		x['organization'] = organization.getId()
		user = User.fromDict(dbConn, x)
		self.assertTrue(isinstance(user, User))

	def testUser_fromDatabase(self):
		dbConn = databaseConnection(dbPath)
		organization = Organization.fromDict(dbConn, dictOrganization)
		x = dictUser.copy()
		x['organization'] = organization.getId()
		user = User.fromDict(dbConn, x)
		user = User.fromDatabase(dbConn, user.getId())
		self.assertTrue(isinstance(user, User))

	def testUser_delete(self):
		dbConn = databaseConnection(dbPath)
		organization = Organization.fromDict(dbConn, dictOrganization)
		x = dictUser.copy()
		x['organization'] = organization.getId()
		user = User.fromDict(dbConn, x)
		pkid = user.getId()
		user.delete()
		user = User.fromDatabase(dbConn, pkid)
		self.assertEqual(None, user)

# 	def testGetOrganizationId(self):
# 		org = createOrganization({'name': 'New Org', 'url': 'new_org', 'maxMembers': 1})
# 		user = org.createMember({'name': 'Bob', 'password': 'Bobs!password', 'username': 'b'})
# 		self.assertEquals(user.organization, org.getId())

# 	def testSetOrganizationId(self):
# 		org1 = createOrganization({'name': 'First Org', 'url': 'first_org', 'maxMembers': 1})
# 		org2 = createOrganization({'name': 'Second Org', 'url': 'second_org', 'maxMembers': 1})
# 		user = org1.createMember({'name': 'Bob', 'password': 'Bobs!password', 'username': 'b'})
# 		user.organization = org2.getId()
# 		self.assertEquals(user.organization, org2.getId())