from django.test import TestCase
from ScoringEngine.framework.core import *

class GeneralEndpoints(TestCase):
	def testGetCompetition(self):
		creationDict = {'name': 'New Org', 'url': 'new_org', 'maxCompetitions': 5}
		org = createOrganization(creationDict)
		se = createScoringEngine({'name':'CSSEF SE', 'packageName':'CssefScoringEngine', 'ownership':1, 'disabled':False})
		org.createCompetition({'name': 'Super Comp', 'url': 'super_comp', 'scoringEngine': se.getId()})
		comp = getCompetition(name = 'Super Comp')
		self.assertEquals(org.__class__.__name__, 'Organization')

	def testGetCompetitions(self):
		se = createScoringEngine({'name':'CSSEF SE', 'packageName':'CssefScoringEngine', 'ownership':1, 'disabled':False})
		orgDict1 = {'name': 'First Org', 'url': 'first_org', 'maxCompetitions': 5}
		orgDict2 = {'name': 'Second Org', 'url': 'second_org', 'maxCompetitions': 5}
		org1 = createOrganization(orgDict1)
		org2 = createOrganization(orgDict2)
		org1.createCompetition({'name': 'Super Comp', 'url': 'super_comp', 'scoringEngine': se.getId()})
		org2.createCompetition({'name': 'Mega Comp', 'url': 'mega_comp', 'scoringEngine': se.getId()})
		users = getCompetitions()
		self.assertEquals(len(users), 2)
		for i in users:
			self.assertEquals(i.__class__.__name__, 'Competition')

	def testGetOrganization(self):
		creationDict = {'name': 'New Org', 'url': 'new_org'}
		createOrganization(creationDict)
		org = getOrganization(name = 'New Org')
		self.assertEquals(org.__class__.__name__, 'Organization')

	def testGetOrganizations(self):
		orgDict1 = {'name': 'First Org', 'url': 'first_org'}
		orgDict2 = {'name': 'Second Org', 'url': 'second_org'}
		createOrganization(orgDict1)
		createOrganization(orgDict2)
		orgs = getOrganizations()
		self.assertEquals(len(orgs), 2)
		for i in orgs:
			self.assertEquals(i.__class__.__name__, 'Organization')

	def testCreateOrganization(self):
		creationDict = {'name': 'New Org', 'url': 'new_org'}
		org = createOrganization(creationDict)
		self.assertEquals(org.__class__.__name__, 'Organization')

	def testCreateOrganizationNoUrl(self):
		# Ultimately though, an error should be thrown rather than returning a dict/returndict
		creationDict = {'name': 'New Org', 'url': 'new_org'}
		org = createOrganization(creationDict)
		self.assertEquals(org.__class__.__name__, 'Organization')

	def testCreateOrganizationDefaults(self):
		creationDict = {'name': 'New Org', 'url': 'new_org'}
		org = createOrganization(creationDict)
		self.assertEquals(org.maxMembers, 0)
		self.assertEquals(org.maxCompetitions, 0)

	# def testEditOrganization(self):
	# 	creationDict = {'name': 'New Org', 'url': 'new_org', 'maxMembers': 5}
	# 	org = createOrganization(creationDict)
	# 	editOrganization(pkid = org.getId(), maxMembers = 10, maxCompetitions = 5)
	# 	self.assertEquals(org.maxMembers, 10)
	# 	self.assertEquals(org.maxCompetitions, 5)

	def testGetUser(self):
		creationDict = {'name': 'New Org', 'url': 'new_org', 'maxMembers': 5}
		org = createOrganization(creationDict)
		member = org.createMember({'name': 'Bob', 'password': 'Bobs!password'})
		user = getUser(name = 'Bob')
		self.assertEquals(user.__class__.__name__, 'User')

	def testGetUsers(self):
		orgDict1 = {'name': 'First Org', 'url': 'first_org', 'maxMembers': 5}
		orgDict2 = {'name': 'Second Org', 'url': 'second_org', 'maxMembers': 5}
		org1 = createOrganization(orgDict1)
		org2 = createOrganization(orgDict2)
		org1.createMember({'name': 'Bob', 'password': 'B0bs!password'})
		org2.createMember({'name': 'Jill', 'password': 'J1lls!password'})
		users = getUsers()
		self.assertEquals(len(users), 2)
		for i in users:
			self.assertEquals(i.__class__.__name__, 'User')

	# def testEditUser(self):
	# 	pass

class DocumentEndpoints(TestCase):
	pass

class OrganizationEndpoints(TestCase):
	def testCantModifyDeletionAtCreation(self):
		creationDict = {'name': 'New Org', 'url': 'new_org', 'deleteable': False}
		org = createOrganization(creationDict)
		self.assertEquals(org.isDeleteable(), True)

	def testCantModifyDeletionAtEdit(self):
		creationDict = {'name': 'New Org', 'url': 'new_org'}
		org = createOrganization(creationDict)
		org.edit(deleteable = False)
		self.assertEquals(org.isDeleteable(), True)

	def testGetName(self):
		creationDict = {'name': 'New Org', 'url': 'new_org'}
		org = createOrganization(creationDict)
		self.assertEquals(org.name, creationDict['name'])

	def testSetName(self):
		creationDict = {'name': 'New Org', 'url': 'new_org'}
		org = createOrganization(creationDict)
		org.edit(name = 'New Name')
		self.assertEquals(org.name, 'New Name')

	def testGetUrl(self):
		creationDict = {'name': 'New Org', 'url': 'new_org'}
		org = createOrganization(creationDict)
		self.assertEquals(org.url, creationDict['url'])

	def testSetUrl(self):
		creationDict = {'name': 'New Org', 'url': 'new_org'}
		org = createOrganization(creationDict)
		org.edit(url = 'new_url')
		self.assertEquals(org.url, 'new_url')

	def testGetDescription(self):
		creationDict = {'name': 'New Org', 'url': 'new_org', 'description': 'New description!'}
		org = createOrganization(creationDict)
		self.assertEquals(org.description, creationDict['description'])

	def testSetDescription(self):
		creationDict = {'name': 'New Org', 'url': 'new_org'}
		org = createOrganization(creationDict)
		description = 'New different description!'
		org.edit(description = description)
		self.assertEquals(org.description, description)

	def testGetMaxMembers(self):
		creationDict = {'name': 'New Org', 'url': 'new_org', 'maxMembers': 10}
		org = createOrganization(creationDict)
		self.assertEquals(org.maxMembers, creationDict['maxMembers'])

	def testSetMaxMembers(self):
		creationDict = {'name': 'New Org', 'url': 'new_org'}
		org = createOrganization(creationDict)
		org.edit(maxMembers = 15)
		self.assertEquals(org.maxMembers, 15)

	def testGetMaxCompetitions(self):
		creationDict = {'name': 'New Org', 'url': 'new_org', 'maxCompetitions': 10}
		org = createOrganization(creationDict)
		self.assertEquals(org.maxCompetitions, creationDict['maxCompetitions'])

	def testSetMaxCompetitions(self):
		creationDict = {'name': 'New Org', 'url': 'new_org'}
		org = createOrganization(creationDict)
		org.edit(maxCompetitions = 15)
		self.assertEquals(org.maxCompetitions, 15)

	def testGetNumMembers(self):
		pass

	def testSetNumMembers(self):
		pass

	def testGetNumCompetitions(self):
		pass

	def testSetNumCompetitions(self):
		pass

	def testGetCompetitions(self):
		creationDict = {'name': 'New Org', 'url': 'new_org', 'maxCompetitions': 5}
		org = createOrganization(creationDict)
		se = createScoringEngine({'name':'CSSEF SE', 'packageName':'CssefScoringEngine', 'ownership':1, 'disabled':False})
		self.assertEquals(len(org.getCompetitions()), 0)
		org.createCompetition({'name': 'New Comp', 'url': 'new_comp', 'scoringEngine': se.getId()})
		self.assertEquals(len(org.getCompetitions()), 1)

	def testGetMembers(self):
		creationDict = {'name': 'New Org', 'url': 'new_org', 'maxMembers': 5}
		org = createOrganization(creationDict)
		self.assertEquals(len(org.getMembers()), 0)
		org.createMember({'name': 'Bob', 'password': 'Bobs!password'})
		self.assertEquals(len(org.getMembers()), 1)

	def testGetCompetition(self):
		creationDict = {'name': 'New Org', 'url': 'new_org', 'maxCompetitions': 5}
		org = createOrganization(creationDict)
		se = createScoringEngine({'name':'CSSEF SE', 'packageName':'CssefScoringEngine', 'ownership':1, 'disabled':False})
		org.createCompetition({'name': 'New Comp', 'url': 'new_comp', 'scoringEngine': se.getId()})
		competition = org.getCompetition(name = 'New Comp')
		self.assertEquals(competition.__class__.__name__, 'Competition')

	def testGetMember(self):
		creationDict = {'name': 'New Org', 'url': 'new_org', 'maxMembers': 5}
		org = createOrganization(creationDict)
		org.createMember({'name': 'Bob', 'password': 'Bobs!password'})
		member = org.getMember(name = 'Bob')
		self.assertEquals(member.__class__.__name__, 'User')

	def testCreateCompetition(self):
		creationDict = {'name': 'New Org', 'url': 'new_org', 'maxCompetitions': 5}
		se = createScoringEngine({'name':'CSSEF SE', 'packageName':'CssefScoringEngine', 'ownership':1, 'disabled':False})
		org = createOrganization(creationDict)
		competition = org.createCompetition({'name': 'New Comp', 'url': 'new_comp', 'scoringEngine': se.getId()})
		self.assertEquals(competition.__class__.__name__, 'Competition')

	def testCreateMember(self):
		creationDict = {'name': 'New Org', 'url': 'new_org', 'maxMembers': 5}
		org = createOrganization(creationDict)
		member = org.createMember({'name': 'Bob', 'password': 'Bobs!password'})
		self.assertEquals(member.__class__.__name__, 'User')

	def testDeleteCompetition(self):
		creationDict = {'name': 'New Org', 'url': 'new_org', 'maxCompetitions': 5}
		org = createOrganization(creationDict)
		se = createScoringEngine({'name':'CSSEF SE', 'packageName':'CssefScoringEngine', 'ownership':1, 'disabled':False})
		competition = org.createCompetition({'name': 'New Comp', 'url': 'new_comp', 'scoringEngine': se.getId()})
		org.deleteCompetition(pkid = competition.getId())

	def testDeleteMember(self):
		creationDict = {'name': 'New Org', 'url': 'new_org', 'maxMembers': 5}
		org = createOrganization(creationDict)
		member = org.createMember({'name': 'Bob', 'password': 'Bobs!password'})
		org.deleteMember(pkid = member.getId())

	def testEditCompetition(self):
		creationDict = {'name': 'New Org', 'url': 'new_org', 'maxCompetitions': 5}
		org = createOrganization(creationDict)
		se = createScoringEngine({'name':'CSSEF SE', 'packageName':'CssefScoringEngine', 'ownership':1, 'disabled':False})
		competition = org.createCompetition({'name': 'New Comp', 'url': 'new_comp', 'scoringEngine': se.getId()})
		org.editCompetition(pkid = competition.getId(), description = 'New description')
		self.assertEquals(competition.description, 'New description')

	def testEditMember(self):
		creationDict = {'name': 'New Org', 'url': 'new_org', 'maxMembers': 5}
		org = createOrganization(creationDict)
		member = org.createMember({'name': 'Bob', 'password': 'Bobs!password'})
		org.editMember(pkid = member.getId(), name = 'Jill')
		self.assertEquals(member.name, 'Jill')

class UserEndpoints(TestCase):
	def testGetId(self):
		org = createOrganization({'name': 'New Org', 'url': 'new_org', 'maxMembers': 1})
		user = org.createMember({'name': 'Bob', 'password': 'Bobs!password', 'username': 'b'})
		self.assertEquals(user.getId(), 1)

	def testGetName(self):
		org = createOrganization({'name': 'New Org', 'url': 'new_org', 'maxMembers': 1})
		user = org.createMember({'name': 'Bob', 'password': 'Bobs!password', 'username': 'b'})
		self.assertEquals(user.name, 'Bob')

	def testSetName(self):
		org = createOrganization({'name': 'New Org', 'url': 'new_org', 'maxMembers': 1})
		user = org.createMember({'name': 'Bob', 'password': 'Bobs!password', 'username': 'b'})
		user.name = 'Billy'
		self.assertEquals(user.name, 'Billy')

	def testGetUsername(self):
		org = createOrganization({'name': 'New Org', 'url': 'new_org', 'maxMembers': 1})
		user = org.createMember({'name': 'Bob', 'password': 'Bobs!password', 'username': 'b'})
		self.assertEquals(user.username, 'b')

	def testSetUsername(self):
		org = createOrganization({'name': 'New Org', 'url': 'new_org', 'maxMembers': 1})
		user = org.createMember({'name': 'Bob', 'password': 'Bobs!password', 'username': 'b'})
		user.username = 'bb'
		self.assertEquals(user.username, 'bb')

	def testGetPassword(self):
		org = createOrganization({'name': 'New Org', 'url': 'new_org', 'maxMembers': 1})
		user = org.createMember({'name': 'Bob', 'password': 'Bobs!password', 'username': 'b'})
		self.assertEquals(user.password, 'Bobs!password')

	def testSetPassword(self):
		org = createOrganization({'name': 'New Org', 'url': 'new_org', 'maxMembers': 1})
		user = org.createMember({'name': 'Bob', 'password': 'Bobs!password', 'username': 'b'})
		user.password = 'b0bsBurg3rz'
		self.assertEquals(user.password, 'b0bsBurg3rz')

	def testGetDescription(self):
		org = createOrganization({'name': 'New Org', 'url': 'new_org', 'maxMembers': 1})
		user = org.createMember({'name': 'Bob', 'password': 'Bobs!password', 'username': 'b', 'description': "Super security expert!"})
		self.assertEquals(user.description, "Super security expert!")

	def testSetDescription(self):
		org = createOrganization({'name': 'New Org', 'url': 'new_org', 'maxMembers': 1})
		user = org.createMember({'name': 'Bob', 'password': 'Bobs!password', 'username': 'b', 'description': "Super security expert!"})
		user.description = "He actually sucks at security..."
		self.assertEquals(user.description, "He actually sucks at security...")

	def testGetOrganizationId(self):
		org = createOrganization({'name': 'New Org', 'url': 'new_org', 'maxMembers': 1})
		user = org.createMember({'name': 'Bob', 'password': 'Bobs!password', 'username': 'b'})
		self.assertEquals(user.organization, org.getId())

	def testSetOrganizationId(self):
		org1 = createOrganization({'name': 'First Org', 'url': 'first_org', 'maxMembers': 1})
		org2 = createOrganization({'name': 'Second Org', 'url': 'second_org', 'maxMembers': 1})
		user = org1.createMember({'name': 'Bob', 'password': 'Bobs!password', 'username': 'b'})
		user.organization = org2.getId()
		self.assertEquals(user.organization, org2.getId())