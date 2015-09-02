from django.test import TestCase
from ScoringEngine.endpoints import *

class GeneralEndpoints(TestCase):
	def testGetCompetition(self):
		creationDict = {'name': 'New Org', 'url': 'new_org', 'maxCompetitions': 5}
		org = createOrganization(creationDict)
		org.createCompetition({'name': 'Super Comp', 'url': 'super_comp'})
		comp = getCompetition(name = 'Super Comp')
		self.assertEquals(org.__class__.__name__, 'Organization')

	def testGetCompetitions(self):
		orgDict1 = {'name': 'First Org', 'url': 'first_org', 'maxCompetitions': 5}
		orgDict2 = {'name': 'Second Org', 'url': 'second_org', 'maxCompetitions': 5}
		org1 = createOrganization(orgDict1)
		org2 = createOrganization(orgDict2)
		org1.createCompetition({'name': 'Super Comp', 'url': 'super_comp'})
		org2.createCompetition({'name': 'Mega Comp', 'url': 'mega_comp'})
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
		creationDict = {'name': 'New Org'}
		org = createOrganization(creationDict)
		self.assertEquals(org.__class__.__name__, 'Organization')

	def testCreateOrganizationDefaults(self):
		creationDict = {'name': 'New Org', 'url': 'new_org'}
		org = createOrganization(creationDict)
		self.assertEquals(org.getMaxMembers(), 0)
		self.assertEquals(org.getMaxCompetitions(), 0)

	def testEditOrganization(self):
		creationDict = {'name': 'New Org', 'url': 'new_org', 'maxMembers': 5}
		org = createOrganization(creationDict)
		editOrganization(organizationId = org.getId(), maxMembers = 10, maxCompetitions = 5)
		self.assertEquals(org.getMaxMembers(), 10)
		self.assertEquals(org.getMaxCompetitions(), 5)

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

	def testEditUser(self):
		pass

class DocumentEndpoints(TestCase):
	pass

class OrganizationEndpoints(TestCase):
	def testCantModifyDeletionAtCreation(self):
		creationDict = {'name': 'New Org', 'url': 'new_org', 'deleteable': False}
		org = createOrganization(creationDict)
		self.assertEquals(org.getDeleteable(), True)

	def testCantModifyDeletionAtEdit(self):
		creationDict = {'name': 'New Org', 'url': 'new_org'}
		org = createOrganization(creationDict)
		org.edit(deleteable = False)
		self.assertEquals(org.getDeleteable(), True)

	def testGetName(self):
		creationDict = {'name': 'New Org', 'url': 'new_org'}
		org = createOrganization(creationDict)
		self.assertEquals(org.getName(), creationDict['name'])

	def testSetName(self):
		creationDict = {'name': 'New Org', 'url': 'new_org'}
		org = createOrganization(creationDict)
		org.edit(name = 'New Name')
		self.assertEquals(org.getName(), 'New Name')

	def testGetUrl(self):
		creationDict = {'name': 'New Org', 'url': 'new_org'}
		org = createOrganization(creationDict)
		self.assertEquals(org.getUrl(), creationDict['url'])

	def testSetUrl(self):
		creationDict = {'name': 'New Org', 'url': 'new_org'}
		org = createOrganization(creationDict)
		org.edit(url = 'new_url')
		self.assertEquals(org.getUrl(), 'new_url')

	def testGetDescription(self):
		creationDict = {'name': 'New Org', 'url': 'new_org', 'description': 'New description!'}
		org = createOrganization(creationDict)
		self.assertEquals(org.getDescription(), creationDict['description'])

	def testSetDescription(self):
		creationDict = {'name': 'New Org', 'url': 'new_org'}
		org = createOrganization(creationDict)
		description = 'New different description!'
		org.edit(description = description)
		self.assertEquals(org.getDescription(), description)

	def testGetMaxMembers(self):
		creationDict = {'name': 'New Org', 'url': 'new_org', 'maxMembers': 10}
		org = createOrganization(creationDict)
		self.assertEquals(org.getMaxMembers(), creationDict['maxMembers'])

	def testSetMaxMembers(self):
		creationDict = {'name': 'New Org', 'url': 'new_org'}
		org = createOrganization(creationDict)
		org.edit(maxMembers = 15)
		self.assertEquals(org.getMaxMembers(), 15)

	def testGetMaxCompetitions(self):
		creationDict = {'name': 'New Org', 'url': 'new_org', 'maxCompetitions': 10}
		org = createOrganization(creationDict)
		self.assertEquals(org.getMaxCompetitions(), creationDict['maxCompetitions'])

	def testSetMaxCompetitions(self):
		creationDict = {'name': 'New Org', 'url': 'new_org'}
		org = createOrganization(creationDict)
		org.edit(maxCompetitions = 15)
		self.assertEquals(org.getMaxCompetitions(), 15)

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
		self.assertEquals(len(org.getCompetitions()), 0)
		org.createCompetition({'name': 'New Comp', 'url': 'new_comp'})
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
		org.createCompetition({'name': 'New Comp', 'url': 'new_comp'})
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
		org = createOrganization(creationDict)
		competition = org.createCompetition({'name': 'New Comp', 'url': 'new_comp'})
		self.assertEquals(competition.__class__.__name__, 'Competition')

	def testCreateMember(self):
		creationDict = {'name': 'New Org', 'url': 'new_org', 'maxMembers': 5}
		org = createOrganization(creationDict)
		member = org.createMember({'name': 'Bob', 'password': 'Bobs!password'})
		self.assertEquals(member.__class__.__name__, 'User')

	def testDeleteCompetition(self):
		creationDict = {'name': 'New Org', 'url': 'new_org', 'maxCompetitions': 5}
		org = createOrganization(creationDict)
		competition = org.createCompetition({'name': 'New Comp', 'url': 'new_comp'})
		org.deleteCompetition(competitionId = competition.getId())

	def testDeleteMember(self):
		creationDict = {'name': 'New Org', 'url': 'new_org', 'maxMembers': 5}
		org = createOrganization(creationDict)
		member = org.createMember({'name': 'Bob', 'password': 'Bobs!password'})
		org.deleteMember(userId = member.getId())

	def testEditCompetition(self):
		creationDict = {'name': 'New Org', 'url': 'new_org', 'maxCompetitions': 5}
		org = createOrganization(creationDict)
		competition = org.createCompetition({'name': 'New Comp', 'url': 'new_comp'})
		org.editCompetition(competitionId = competition.getId(), description = 'New description')
		self.assertEquals(competition.getDescription(), 'New description')

	def testEditMember(self):
		creationDict = {'name': 'New Org', 'url': 'new_org', 'maxMembers': 5}
		org = createOrganization(creationDict)
		member = org.createMember({'name': 'Bob', 'password': 'Bobs!password'})
		org.editMember(userId = member.getId(), name = 'Jill')
		self.assertEquals(member.getName(), 'Jill')

class UserEndpoints(TestCase):
	def testGetId(self):
		org = createOrganization({'name': 'New Org', 'url': 'new_org', 'maxMembers': 1})
		user = org.createMember({'name': 'Bob', 'password': 'Bobs!password', 'username': 'b'})
		self.assertEquals(user.getId(), 1)

	def testGetName(self):
		org = createOrganization({'name': 'New Org', 'url': 'new_org', 'maxMembers': 1})
		user = org.createMember({'name': 'Bob', 'password': 'Bobs!password', 'username': 'b'})
		self.assertEquals(user.getName(), 'Bob')

	def testSetName(self):
		org = createOrganization({'name': 'New Org', 'url': 'new_org', 'maxMembers': 1})
		user = org.createMember({'name': 'Bob', 'password': 'Bobs!password', 'username': 'b'})
		user.setUsername('Billy')
		self.assertEquals(user.getName(), 'Billy')

	def testGetUsername(self):
		org = createOrganization({'name': 'New Org', 'url': 'new_org', 'maxMembers': 1})
		user = org.createMember({'name': 'Bob', 'password': 'Bobs!password', 'username': 'b'})
		self.assertEquals(user.getUsername(), 'b')

	def testSetUsername(self):
		org = createOrganization({'name': 'New Org', 'url': 'new_org', 'maxMembers': 1})
		user = org.createMember({'name': 'Bob', 'password': 'Bobs!password', 'username': 'b'})
		user.setUsername('bb')
		self.assertEquals(user.getUsername(), 'bb')

	def testGetPassword(self):
		org = createOrganization({'name': 'New Org', 'url': 'new_org', 'maxMembers': 1})
		user = org.createMember({'name': 'Bob', 'password': 'Bobs!password', 'username': 'b'})
		self.assertEquals(user.getPassword(), 'Bobs!password')

	def testSetPassword(self):
		org = createOrganization({'name': 'New Org', 'url': 'new_org', 'maxMembers': 1})
		user = org.createMember({'name': 'Bob', 'password': 'Bobs!password', 'username': 'b'})
		user.setPassword('b0bsBurg3rz')
		self.assertEquals(user.getPassword(), 'b0bsBurg3rz')

	def testGetDescription(self):
		org = createOrganization({'name': 'New Org', 'url': 'new_org', 'maxMembers': 1})
		user = org.createMember({'name': 'Bob', 'password': 'Bobs!password', 'username': 'b', 'description': "Super security expert!"})
		self.assertEquals(user.getDescription(), "Super security expert!")

	def testSetDescription(self):
		org = createOrganization({'name': 'New Org', 'url': 'new_org', 'maxMembers': 1})
		user = org.createMember({'name': 'Bob', 'password': 'Bobs!password', 'username': 'b', 'description': "Super security expert!"})
		user.setDescription("He actually sucks at security...")
		self.assertEquals(user.getDescription(), "He actually sucks at security...")

	def testGetOrganizationId(self):
		org = createOrganization({'name': 'New Org', 'url': 'new_org', 'maxMembers': 1})
		user = org.createMember({'name': 'Bob', 'password': 'Bobs!password', 'username': 'b'})
		self.assertEquals(user.getOrganizationId(), org.getId())

	def testSetOrganizationId(self):
		org1 = createOrganization({'name': 'First Org', 'url': 'first_org', 'maxMembers': 1})
		org2 = createOrganization({'name': 'Second Org', 'url': 'second_org', 'maxMembers': 1})
		user = org1.createMember({'name': 'Bob', 'password': 'Bobs!password', 'username': 'b'})
		user.setOrganizationId(org2.getId())
		self.assertEquals(user.getOrganizationId(), org2.getId())

class CompetitionEndpoints(TestCase):
	pass

class TeamEndpoints(TestCase):
	pass

class InjectEndpoints(TestCase):
	pass

class InjectResponseEndpoints(TestCase):
	pass

class IncidentEndpoints(TestCase):
	pass

class IncidentResponseEndpoints(TestCase):
	pass

class ScoreEndpoints(TestCase):
	pass
