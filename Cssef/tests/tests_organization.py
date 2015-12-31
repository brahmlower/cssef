from unittest import TestCase
from framework.utils import databaseConnection
from framework.core import Organization
from datetime import datetime

dbPath = '/home/sk4ly/Documents/cssef/Cssef/db.sqlite3'
dictOrganization = {
	'name': 'T Org',
	'url': 't_org',
	'maxCompetitions': 1}

class OrganizationEndpoints(TestCase):
	pass

	# def testCantModifyDeletionAtCreation(self):
	# 	creationDict = {'name': 'New Org', 'url': 'new_org', 'deleteable': False}
	# 	org = createOrganization(creationDict)
	# 	self.assertEquals(org.isDeleteable(), True)

	# def testCantModifyDeletionAtEdit(self):
	# 	creationDict = {'name': 'New Org', 'url': 'new_org'}
	# 	org = createOrganization(creationDict)
	# 	org.edit(deleteable = False)
	# 	self.assertEquals(org.isDeleteable(), True)

	# def testGetNumMembers(self):
	# 	pass

	# def testSetNumMembers(self):
	# 	pass

	# def testGetNumCompetitions(self):
	# 	pass

	# def testSetNumCompetitions(self):
	# 	pass

	# def testGetCompetitions(self):
	# 	creationDict = {'name': 'New Org', 'url': 'new_org', 'maxCompetitions': 5}
	# 	org = createOrganization(creationDict)
	# 	se = createScoringEngine({'name':'CSSEF SE', 'packageName':'CssefScoringEngine', 'ownership':1, 'disabled':False})
	# 	self.assertEquals(len(org.getCompetitions()), 0)
	# 	org.createCompetition({'name': 'New Comp', 'url': 'new_comp', 'scoringEngine': se.getId()})
	# 	self.assertEquals(len(org.getCompetitions()), 1)

	# def testGetMembers(self):
	# 	creationDict = {'name': 'New Org', 'url': 'new_org', 'maxMembers': 5}
	# 	org = createOrganization(creationDict)
	# 	self.assertEquals(len(org.getMembers()), 0)
	# 	org.createMember({'name': 'Bob', 'password': 'Bobs!password'})
	# 	self.assertEquals(len(org.getMembers()), 1)

	# def testGetCompetition(self):
	# 	creationDict = {'name': 'New Org', 'url': 'new_org', 'maxCompetitions': 5}
	# 	org = createOrganization(creationDict)
	# 	se = createScoringEngine({'name':'CSSEF SE', 'packageName':'CssefScoringEngine', 'ownership':1, 'disabled':False})
	# 	org.createCompetition({'name': 'New Comp', 'url': 'new_comp', 'scoringEngine': se.getId()})
	# 	competition = org.getCompetition(name = 'New Comp')
	# 	self.assertEquals(competition.__class__.__name__, 'Competition')

	# def testGetMember(self):
	# 	creationDict = {'name': 'New Org', 'url': 'new_org', 'maxMembers': 5}
	# 	org = createOrganization(creationDict)
	# 	org.createMember({'name': 'Bob', 'password': 'Bobs!password'})
	# 	member = org.getMember(name = 'Bob')
	# 	self.assertEquals(member.__class__.__name__, 'User')

	# def testCreateCompetition(self):
	# 	creationDict = {'name': 'New Org', 'url': 'new_org', 'maxCompetitions': 5}
	# 	se = createScoringEngine({'name':'CSSEF SE', 'packageName':'CssefScoringEngine', 'ownership':1, 'disabled':False})
	# 	org = createOrganization(creationDict)
	# 	competition = org.createCompetition({'name': 'New Comp', 'url': 'new_comp', 'scoringEngine': se.getId()})
	# 	self.assertEquals(competition.__class__.__name__, 'Competition')

	# def testCreateMember(self):
	# 	creationDict = {'name': 'New Org', 'url': 'new_org', 'maxMembers': 5}
	# 	org = createOrganization(creationDict)
	# 	member = org.createMember({'name': 'Bob', 'password': 'Bobs!password'})
	# 	self.assertEquals(member.__class__.__name__, 'User')

	# def testDeleteCompetition(self):
	# 	creationDict = {'name': 'New Org', 'url': 'new_org', 'maxCompetitions': 5}
	# 	org = createOrganization(creationDict)
	# 	se = createScoringEngine({'name':'CSSEF SE', 'packageName':'CssefScoringEngine', 'ownership':1, 'disabled':False})
	# 	competition = org.createCompetition({'name': 'New Comp', 'url': 'new_comp', 'scoringEngine': se.getId()})
	# 	org.deleteCompetition(pkid = competition.getId())

	# def testDeleteMember(self):
	# 	creationDict = {'name': 'New Org', 'url': 'new_org', 'maxMembers': 5}
	# 	org = createOrganization(creationDict)
	# 	member = org.createMember({'name': 'Bob', 'password': 'Bobs!password'})
	# 	org.deleteMember(pkid = member.getId())