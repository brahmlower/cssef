# API Documentation

This is reference documentation on the python api for the core framework. The following are links to the various sections documentation.

* [Competition](https://github.com/bplower/cssef/blob/refactor/ScoringEngine/ScoringEngine/README.md#competition)
* [Team](https://github.com/bplower/cssef/blob/refactor/ScoringEngine/ScoringEngine/README.md#team)
* [Inject](https://github.com/bplower/cssef/blob/refactor/ScoringEngine/ScoringEngine/README.md#inject)
* [InjectResponse](https://github.com/bplower/cssef/blob/refactor/ScoringEngine/ScoringEngine/README.md#injectresponse)
* [Incident](https://github.com/bplower/cssef/edit/refactor/ScoringEngine/ScoringEngine/README.md#incident)
* [IncidentResponse](https://github.com/bplower/cssef/edit/refactor/ScoringEngine/ScoringEngine/README.md#incidentresponse)
* [Score](https://github.com/bplower/cssef/blob/refactor/ScoringEngine/ScoringEngine/README.md#score)
* [Organization](https://github.com/bplower/cssef/blob/refactor/ScoringEngine/ScoringEngine/README.md#organization)
* [User](https://github.com/bplower/cssef/blob/refactor/ScoringEngine/ScoringEngine/README.md#user)
* [Document](https://github.com/bplower/cssef/blob/refactor/ScoringEngine/ScoringEngine/README.md#document)

There is a lot of documentation here. If you see any errors or unfinished sections, feel free to submit edits via a pull request.

#### getObjects()
endpoints.**getObjects**(classPointer, \*\*kwargs)
<br>This is more of a utility method used by the other endpoints. It will simply apply the filter defined by the keywork arguments to the database object classPointer. The keyword serialized is poped from kwargs to define how to return the object.
<br>**Input**
<br>**Output**
<br>**Example**
```python
```
* * *

#### getObject()
endpoints.**getObject**(classPointer, \*\*kwargs)
<br>This is more of a utility method used by the other endpoints. It will simply apply the filter defined by the keywork arguments to the database object classPointer. The keyword serialized is poped from kwargs to define how to return the objects.
<br>**Input**
<br>**Output**
<br>**Example**
```python
```
* * *
#### wrappedSearch()
endpoints.**wrappedSearch**(objType, objTypeModel, \*\*kwargs)
<br>This is more of a utility method used by the other endpoints.
<br>**Input**
<br>**Output**
<br>**Example**
```python
```
* * *

#### getCompetition()
endpoints.**getCompetition**(\*\*kwargs)
<br>This will return a single competition matching the filter defined by the provided keywords. The keyword serialized can be provided to specify how the object should be returned.
<br>**Input**
<br>**Output**
<br>**Example**
```python
```
* * *

#### getCompetitions()
endpoints.**getCompetitions**(\*\*kwargs)
<br>This will return all competition objects matching the filter defined by the provided keywords. The keyword serialzied can be provided to specify how the object should be returned.
<br>**Input**
<br>**Output**
<br>**Example**
```python
```
* * *

#### getOrganization()
endpoints.**getOrganization**(\*\*kwargs)
<br>This will return a single organization matching the filter defined by the provided keywords. The keyword serialized can be provided to specify how the object should be returned.
<br>**Input**
<br>**Output**
<br>**Example**
```python
```
* * *

#### getOrganizations()
endpoints.**getOrganizations**(\*\*kwargs)
<br>This will return all organizations objects matching the filter defined by the provided keywords. The keyword serialzied can be provided to specify how the object should be returned.
<br>**Input**
<br>**Output**
<br>**Example**
```python
```
* * *

#### createOrganization()
endpoints.**createOrganization**(postData, serialized = False)
<br>This will create a and return a new organization.
<br>**Input**
<br>**Output**
<br>**Example**
```python
```
* * *

#### editOrganization()
endpoints.**editOrganization**(\*\*kwargs)
<br>This will edit an existing organiztion defined by kwargs.
<br>**Input**
<br>**Output**
<br>**Example**
```python
```
* * *

#### getUsers()
endpoints.**getUsers**(\*\*kwargs)
<br>This will return all users objects matching the filter defined by the provided keywords. The keyword serialzied can be provided to specify how the object should be returned.
<br>**Input**
<br>**Output**
<br>**Example**
```python
```
* * *

#### getUser()
endpoints.**getUser**(\*\*kwargs)
<br>This will return a single user matching the filter defined by the provided keywords. The keyword serialized can be provided to specify how the object should be returned.
<br>**Input**
<br>**Output**
<br>**Example**
```python
```
* * *

#### editUser()
endpoints.**editUser**(\*\*kwargs)
<br>This is used to edit user specific settings like personal preferences. This as not been implemented yet though.
<br>**Input**
<br>**Output**
<br>**Example**
```python
```
* * *

## Competition
#### count()
endpoints.Competition.**count**(\*\*kwarg)
<br>This returns the number of Competition objects that match the provided filter.
<br>**Input**
<br>**Output**
<br>&nbsp;&nbsp;&nbsp;&nbsp;Returns value of type integer
<br>**Example**
```python
>>> from ScoringEngine.endpoints import *
>>> orgData = {'name': 'New Org', 'url':'new_org'}
>>> org = createOrganization(orgData)
>>> org.createCompetition({'name':'First Comp})
>>> org.createCompetition({'name': 'Second Comp})
>>> organizationId = org.getId()
>>> numCompetitions = Competition.count(organization = organizationId)
>>> print numCompetitions
2
>>>
```
* * *

#### getName()
endpoints.Competition.**getName**(self)
<br>This will return the name of the competition as a string.
<br>**Input**
<br>&nbsp;&nbsp;&nbsp;&nbsp;None
<br>**Output**
<br>&nbsp;&nbsp;&nbsp;&nbsp;Returns value of type str
<br>**Example**
```python
>>> from ScoringEngine.endpoints import *
>>> orgData = {'name': 'New Org', 'url':'new_org'}
>>> org = createOrganization(orgData)
>>> competition = org.createCompetition({'name':'First Comp})
>>> name = competition.getName()
>>> print name
New Org
>>>
```
* * *


#### check()
endpoints.Competition.**check**(self)<br>
This should one day perform a consistency check to make sure the competition doesn't have any conflicting values set. This may or may not be necessary depending on how much I implement error checking.
<br>**Input**
<br>**Output**
<br>**Example**
```python
```
* * *

#### createTeam()
endpoints.Competition.**createTeam**(self, objType, serialized = False)
<br>This will create and return a new team in within the competition.
<br>**Input**
* postData (required)
<br>&nbsp;&nbsp;&nbsp;&nbsp;Dictionary containing required keywords for a new Team.
* serialized (optional)
<br>&nbsp;&nbsp;&nbsp;&nbsp;Return as object (False) or as a dictionary (True). If not provided, this value will default to False.

**Output**
<br>**Example**
```python
>>> from ScoringEngine.endpoints import *
>>> orgData = {'name': 'New Org', 'url':'new_org'}
>>> org = createOrganization(orgData)
>>> competition = org.createCompetition({'name':'First Comp})
>>> teamData = {'name':'New Team', 'username':'new_team', 'password':'$3(Ur#!'}
>>> team = competition.createTeam(teamData)
>>>
```
* * *

#### editTeam()
endpoints.Competition.**editTeam**(\*\*kwargs)
<br>Take a dictionary of values for the Team object and applies their values to the team object. This effectively calls getTeam() with the provided teamId, then calls edit() on that team. This would be used in cases where you only wish to apply changes to team, but you don't have the team object.
<br>**Input**
* \*\*kwargs
  * teamId - *Integer* (required)
<br>&nbsp;&nbsp;&nbsp;&nbsp;Specifies the team to edit. Cannot be changed.
  * serialized - *Boolean* (optional)
<br>&nbsp;&nbsp;&nbsp;&nbsp;This defines the type to return. If not provided, this defaults to False.
  * name - *String* (optional)
<br>&nbsp;&nbsp;&nbsp;&nbsp;The team name
  * username - *String* (optional)
<br>&nbsp;&nbsp;&nbsp;&nbsp;The username used to sign in
  * password - *String* (optional)
<br>&nbsp;&nbsp;&nbsp;&nbsp;The password used to sign in
  * networkCidr - *String* (optional)
<br>&nbsp;&nbsp;&nbsp;&nbsp;The CIDR representation of the network associated with the team
  * scoreConfiguration - *String* (optional)
<br>&nbsp;&nbsp;&nbsp;&nbsp;The dictionary for storing scoring configurations

**Output**
<br>&nbsp;&nbsp;&nbsp;&nbsp;None
<br>**Example**
```python
>>> from ScoringEngine.endpoints import *
>>> org = createOrganization({'name': 'New Org', 'url':'new_org'})
>>> competition = org.createCompetition({'name':'First Comp})
>>> teamData = {'name':'New Team', 'username':'new_team', 'password':'$3(Ur#!'}
>>> team = competition.createTeam(teamData)
>>> print team.getName()
New Team
>>> competition.editTeam(teamId = team.getId(), name = 'Super Team')
>>> print team.getName()
Super Team
>>>
```
* * *

#### getTeam()
endpoints.Competition.**getTeam**(self, \*\*kwargs)
<br> Retrieves an existing team object.
<br>**Input**

**Output**
<br>**Example**
```python
>>> from SoringEngine.endpoints import *
>>> org = createOrganization({'name': 'New Org', 'url':'new_org'})
>>> competition = org.createCompetition({'name':'First Comp})
>>> team = competition.createTeam({'name':'New Team', 'username':'new_team', 'password':'$3(Ur#!'})
>>> competition.getTeam(teamId = team.getId())
>>>
```
* * *

#### getTeams()
endpoints.Competition.**getTeams**(self, \*\*kwargs)
<br> Retrieves an existing team object.
<br>**Input**
* objType (required):
<br>&nbsp;&nbsp;&nbsp;&nbsp;This is the class type of the object to search for
* \*\*kwargs (optional):
  * serialized:
<br>&nbsp;&nbsp;&nbsp;&nbsp;This defines the type to return. If not provided, this defaults to False.

**Output**
<br>**Example**
This is a bad example, using a function that doesn't exist. I'll get back to this eventually.
```python
>>> from SoringEngine.endpoints import *
>>> org = createOrganization({'name': 'New Org', 'url':'new_org'})
>>> competition = org.createCompetition({'name':'First Comp})
>>> team = competition.createTeam({'name':'New Team', 'username':'new_team', 'password':'$3(Ur#!'})
>>> team.setScore(100)
>>> teamList = competition.getTeams(score = 100)
>>> len(teamList)
1
>>> 
```
* * *
#### deleteTeam()
endpoints.Competition.**deleteTeam**(self, \*\*kwargs)
<br> Deletes the specified team object.
<br>**Input**
* \*\*kwargs (optional):
  * serialized:
<br>&nbsp;&nbsp;&nbsp;&nbsp;This defines the type to return. If not provided, this defaults to False.
  * teamId:
<br>&nbsp;&nbsp;&nbsp;&nbsp;The ID for the Team object you'd like to delete.

**Output**
<br>&nbsp;&nbsp;&nbsp;&nbsp;None
<br>**Example**
```python
competition = getCompetition(competitionId = 1)
competition.deleteTeam(teamId = 5)
```
* * *

#### createIncident()
endpoints.Competition.**createIncident**(self, postData, serialized = False)
<br> Creates a new incident object.
<br>**Input**
<br>**Output**
<br>**Example**
```python
```
* * *

#### editIncident()
endpoints.Competition.**editIncident**(self, \*\*kwargs)
<br> Edits an existing incident object.
<br>**Input**
<br>**Output**
<br>**Example**
```python
```
* * *

#### getIncident()
endpoints.Competition.**getIncident**(self, \*\*kwargs)
<br> Retrieves an existing incident object.
<br>**Input**
<br>**Output**
<br>**Example**
```python
```
* * *

#### getIncidents()
endpoints.Competition.**getIncidents**(self, \*\*kwargs)
<br> Retrieves multiple existing incident objects.
<br>**Input**
<br>**Output**
<br>**Example**
```python
```
* * *

#### deleteIncident()
endpoints.Competition.**deleteIncident**(self, \*\*kwargs)
<br> Deletes a single incident object.
<br>**Input**
* \*\*kwargs (optional):
  * serialized:
<br>&nbsp;&nbsp;&nbsp;&nbsp;This defines the type to return. If not provided, this defaults to False.
  * teamId:
<br>&nbsp;&nbsp;&nbsp;&nbsp;The ID for the Incident object you'd like to delete.

**Output**
<br>&nbsp;&nbsp;&nbsp;&nbsp;None
<br>**Example**
```python
competition = getCompetition(competitionId = 1)
competition.deleteIncident(incidentId = 5)
```
* * *

#### createIncidentResponse()
endpoints.Competition.**createIncidentResponse**()
<br> Creates a new incident response object.
<br>**Input**
<br>**Output**
<br>**Example**
```python
```
* * *

#### editIncidentResponse()
endpoints.Competition.**editIncidentResponse**(self, \*\*kwargs)
<br> Edits an existing incident response object.
<br>**Input**
<br>**Output**
<br>**Example**
```python
```
* * *

#### getIncidentResponse()
endpoints.Competition.**getIncidentResponse**(self, \*\*kwargs)
<br> Retrieves an existing incident response object.
<br>**Input**
<br>**Output**
<br>**Example**
```python
```
* * *
#### getIncidentResponses()
endpoints.Competition.**getIncidentResponses**(self, \*\*kwargs)
<br> Retrieves multiple existing incident response objects.
<br>**Input**
<br>**Output**
<br>**Example**
```python
```
* * *

#### deleteIncidentResponse()
endpoints.Competition.**deleteIncidentResponse**(self, \*\*kwargs)
<br> Deletes a single specified incident response object.
<br>**Input**
* \*\*kwargs (optional):
  * serialized:
<br>&nbsp;&nbsp;&nbsp;&nbsp;This defines the type to return. If not provided, this defaults to False.
  * teamId:
<br>&nbsp;&nbsp;&nbsp;&nbsp;The ID for the IncidentResponse object you'd like to delete.

**Output**
<br>&nbsp;&nbsp;&nbsp;&nbsp;None
<br>**Example**
```python
competition = getCompetition(competitionId = 1)
competition.deleteIncidentResponse(incidentResponseId = 5)
```
* * *

#### createInject()
endpoints.Competition.**createInject**()
<br> Creates a new inject object.
<br>**Input**
<br>**Output**
<br>**Example**
```python
```
* * *

#### editInject()
endpoints.Competition.**editInject**(self, \*\*kwargs)
<br> Edits an existing inject object.
<br>**Input**
<br>**Output**
<br>**Example**
```python
```
* * *

#### getInject()
endpoints.Competition.**getInject**(self, \*\*kwargs)
<br> Retrieves an existing inject object.
<br>**Input**
<br>**Output**
<br>**Example**
```python
```
* * *

#### getInjects()
endpoints.Competition.**getInjects**(self, \*\*kwargs)
<br> Retrieves existing inject objects.
<br>**Input**
<br>**Output**
<br>**Example**
```python
```
* * *

#### deleteInject()
endpoints.Competition.**deleteInject**(self, \*\*kwargs)
<br> Deletes a single specified inject response.
<br>**Input**
* \*\*kwargs (optional):
  * serialized:
<br>&nbsp;&nbsp;&nbsp;&nbsp;This defines the type to return. If not provided, this defaults to False.
  * teamId:
<br>&nbsp;&nbsp;&nbsp;&nbsp;The ID for the Inject object you'd like to delete.

**Output**
<br>&nbsp;&nbsp;&nbsp;&nbsp;None
<br>**Example**
```python
competition = getCompetition(competitionId = 1)
competition.deleteInject(injectId = 5)
```
* * *

#### createInjectResponse
endpoints.Competition.**createInjectResponse**()
<br> Creates a new inject response object.
<br>**Input**
<br>**Output**
<br>**Example**
```python
```
* * *

#### editInjectResponse()
endpoints.Competition.**editInjectResponse**(self, \*\*kwargs)
<br> Edits an existing inject response object.
<br>**Input**
<br>**Output**
<br>**Example**
```python
```
* * *

#### getInjectResponse()
endpoints.Competition.**getInjectResponse**(self, \*\*kwargs)
<br> Retrieves an existing inject response object.
<br>**Input**
<br>**Output**
<br>**Example**
```python
```
* * *

#### getInjectResponses()
endpoints.Competition.**getInjectResponses**(self, \*\*kwargs)
<br> Retrieves specified existing inject response objects.
<br>**Input**
<br>**Output**
<br>**Example**
```python
```
* * *

#### deleteInjectResponse()
endpoints.Competition.**deleteInjectResponses**(self, \*\*kwargs)
<br> Delete the specified inject response object.
<br>**Input**
* \*\*kwargs (optional):
  * serialized:
<br>&nbsp;&nbsp;&nbsp;&nbsp;This defines the type to return. If not provided, this defaults to False.
  * teamId:
<br>&nbsp;&nbsp;&nbsp;&nbsp;The ID for the InjectResponse object you'd like to delete.

**Output**
<br>&nbsp;&nbsp;&nbsp;&nbsp;None
<br>**Example**
```python
competition = getCompetition(competitionId = 1)
competition.deleteInjectResponse(injectResponseId = 5)
```
* * *

#### createScore()
endpoints.Competition.**createScore**()
<br> Create a new score object.
<br>**Input**
<br>**Output**
<br>**Example**
```python
```
* * *

#### editScore()
endpoints.Competition.**editScore**(self, \*\*kwargs)
<br> Edit an existing score object.
<br>**Input**
<br>**Output**
<br>**Example**
```python
```
* * *

#### getScore()
endpoints.Competition.**getScore**(self, \*\*kwargs)
<br> Retrieves an existing score.
<br>**Input**
<br>**Output**
<br>**Example**
```python
```
* * *

#### getScores()
endpoints.Competition.**getScores**(self, \*\*kwargs)
<br> Retrieves the specified existing score objects.
<br>**Input**
<br>**Output**
<br>**Example**
```python
```
* * *

#### deleteScore()
endpoints.Competition.**deleteScore**(self, \*\*kwargs)
<br> Deletes the specified score object.
<br>**Input**
* \*\*kwargs (optional):
  * serialized:
<br>&nbsp;&nbsp;&nbsp;&nbsp;This defines the type to return. If not provided, this defaults to False.
  * teamId:
<br>&nbsp;&nbsp;&nbsp;&nbsp;The ID for the Score object you'd like to delete.

**Output**
<br>&nbsp;&nbsp;&nbsp;&nbsp;None
<br>**Example**
```python
competition = getCompetition(competitionId = 1)
competition.deleteScore(scoreId = 5)
```
* * *

## Team
#### edit()
endpoints.Competition.Team.**edit**(self, \*\*kwargs)
<br> Applies many changes to the team object. This simply iterates over the provided keyword arguments and calls the corresponding 'set' methods. This does will modify the object directly and will bypass any additional checking or limitations implemented in endpoints.Competition.editTeam().
<br>**Input**
* name - *String* (optional)
* username - *String* (optional)
* password - *String* (optional)
* networkCidr - *String* (optional)
* scoreConfigs - *String* (optional)

**Output**
* endponts.Competition.Team

**Example**
```python
```
* * *
#### getId()
endpoints.Competition.Team.**getId**(self)
<br> Returns the Id of the object as an integer.
<br>**Input**
* None

**Output**
* Integer

**Example**
```python
>>> from ScoringEngine.endpoints import *
>>> org = createOrganization({'name': 'New Org', 'url': 'new_org', 'maxCompetitions': 5})
>>> comp = org.createCompetition({'name': 'Super Comp', 'url': 'super_comp'})
>>> teamData = {'name': 'UAF Team', 'username': 'uafteam', 'password': 'U@fR0(k5', 'networkCidr': '192.168.1.0/24', 'scoreConfigurations': "{'httpService':{'port':80}}"
>>> team = comp.createTeam(teamData)
>>> print team.getId()
1
>>>
```
* * *
#### getUsername()
endpoints.Competition.Team.**getUsername**(self)
<br> Returns the username of the object as a string.
<br>**Input**
* None

**Output**
* String

**Example**
```python
>>> from ScoringEngine.endpoints import *
>>> org = createOrganization({'name': 'New Org', 'url': 'new_org', 'maxCompetitions': 5})
>>> comp = org.createCompetition({'name': 'Super Comp', 'url': 'super_comp'})
>>> teamData = {'name': 'UAF Team', 'username': 'uafteam', 'password': 'U@fR0(k5', 'networkCidr': '192.168.1.0/24', 'scoreConfigurations': "{'httpService':{'port':80}}"
>>> team = comp.createTeam(teamData)
>>> team.getUsername()
uafteam
>>>
```
* * *
#### setUsername()
endpoints.Competition.Team.**setUsername**(self, username)
<br> Sets the username of the object.
<br>**Input**
* username - *String* (required)

**Output**
* Boolean?

**Example**
```python
>>> from ScoringEngine.endpoints import *
>>> org = createOrganization({'name': 'New Org', 'url': 'new_org', 'maxCompetitions': 5})
>>> comp = org.createCompetition({'name': 'Super Comp', 'url': 'super_comp'})
>>> teamData = {'name': 'UAF Team', 'username': 'uafteam', 'password': 'U@fR0(k5', 'networkCidr': '192.168.1.0/24', 'scoreConfigurations': "{'httpService':{'port':80}}"
>>> team = comp.createTeam(teamData)
>>> team.setUsername('newusername')
>>> print team.getUsername()
newusername
>>>
```
* * *
#### getName()
endpoints.Competition.Team.**getName**(self)
<br> Returns the name of the object.
<br>**Input**
* None

**Output**
* String

**Example**
```python
>>> from ScoringEngine.endpoints import *
>>> org = createOrganization({'name': 'New Org', 'url': 'new_org', 'maxCompetitions': 5})
>>> comp = org.createCompetition({'name': 'Super Comp', 'url': 'super_comp'})
>>> teamData = {'name': 'UAF Team', 'username': 'uafteam', 'password': 'U@fR0(k5', 'networkCidr': '192.168.1.0/24', 'scoreConfigurations': "{'httpService':{'port':80}}"
>>> team = comp.createTeam(teamData)
>>> print team.getName()
UAF Team
>>>
```
* * *
#### setName()
endpoints.Competition.Team.**setName**(self, name)
<br> Sets the name of the object.
<br>**Input**
* name - *String* (required)

**Output**
* Boolean?

**Example**
```pythonpython
>>> from ScoringEngine.endpoints import *
>>> org = createOrganization({'name': 'New Org', 'url': 'new_org', 'maxCompetitions': 5})
>>> comp = org.createCompetition({'name': 'Super Comp', 'url': 'super_comp'})
>>> teamData = {'name': 'UAF Team', 'username': 'uafteam', 'password': 'U@fR0(k5', 'networkCidr': '192.168.1.0/24', 'scoreConfigurations': "{'httpService':{'port':80}}"
>>> team = comp.createTeam(teamData)
>>> team.setName('New UAF Team')
>>> print team.getName()
New UAF Team
>>>
```
* * *
#### getPassword()
endpoints.Competition.Team.**getPassword**(self)
<br> Gets the password of the object. I really don't think this should be an available option, butI'm leaving it in for now, since I'm not making design decisions ATM (Sep 2, 2015).
<br>**Input**
* None

**Output**
* String

**Example**
Idealy the password won't be stored in plaintext, so this would actually return a hash of some sort. But even though, I don't like the idea of getting anything related to the password without having to get direct access to the database.
```python
>>> from ScoringEngine.endpoints import *
>>> org = createOrganization({'name': 'New Org', 'url': 'new_org', 'maxCompetitions': 5})
>>> comp = org.createCompetition({'name': 'Super Comp', 'url': 'super_comp'})
>>> teamData = {'name': 'UAF Team', 'username': 'uafteam', 'password': 'U@fR0(k5', 'networkCidr': '192.168.1.0/24', 'scoreConfigurations': "{'httpService':{'port':80}}"
>>> team = comp.createTeam(teamData)
>>> team.getPassword()
U@fR0(k5
>>>
```
* * *
#### setPassword()
endpoints.Competition.Team.**setPassword**(self, password)
<br> Sets the password of the object.
<br>**Input**
* password - *String* (required)

**Output**
* Boolean?

**Example**
```python
>>> from ScoringEngine.endpoints import *
>>> org = createOrganization({'name': 'New Org', 'url': 'new_org', 'maxCompetitions': 5})
>>> comp = org.createCompetition({'name': 'Super Comp', 'url': 'super_comp'})
>>> teamData = {'name': 'UAF Team', 'username': 'uafteam', 'password': 'U@fR0(k5', 'networkCidr': '192.168.1.0/24', 'scoreConfigurations': "{'httpService':{'port':80}}"
>>> team = comp.createTeam(teamData)
>>> team.setPassword('Password123')
>>>
```
* * *
#### getNetworkCidr()
endpoints.Competition.Team.**getNetworkCidr**(self)
<br> Returns the networkCidr of the object as a string.
<br>**Input**
* None

**Output**
* String

**Example**
```python
>>> from ScoringEngine.endpoints import *
>>> org = createOrganization({'name': 'New Org', 'url': 'new_org', 'maxCompetitions': 5})
>>> comp = org.createCompetition({'name': 'Super Comp', 'url': 'super_comp'})
>>> teamData = {'name': 'UAF Team', 'username': 'uafteam', 'password': 'U@fR0(k5', 'networkCidr': '192.168.1.0/24', 'scoreConfigurations': "{'httpService':{'port':80}}"
>>> team = comp.createTeam(teamData)
>>> print team.getNetworkCidr()
192.168.1.0/24
>>>
```
* * *
#### setNetworkCidr()
endpoints.Competition.Team.**setNetworkCidr**(self, networkCidr)
<br> Sets the networkCidr of the object.
<br>**Input**
* networkCidr - *String* (required)

**Output**
* Boolean?

**Example**
```python
>>> from ScoringEngine.endpoints import *
>>> org = createOrganization({'name': 'New Org', 'url': 'new_org', 'maxCompetitions': 5})
>>> comp = org.createCompetition({'name': 'Super Comp', 'url': 'super_comp'})
>>> teamData = {'name': 'UAF Team', 'username': 'uafteam', 'password': 'U@fR0(k5', 'networkCidr': '192.168.1.0/24', 'scoreConfigurations': "{'httpService':{'port':80}}"
>>> team = comp.createTeam(teamData)
>>> team.setNetworkCidr('10.0.0.1/24')
>>> print team.getNetworkCidr()
10.0.0.1./24
>>>
```
* * *
#### getScoreConfigurations()
endpoints.Competition.Team.**getScoreConfiguration**(self)
<br> Gets the scoreConfiguration of the object.
<br>**Input**
* None

**Output**
* String

**Example**
```python
>>> from ScoringEngine.endpoints import *
>>> org = createOrganization({'name': 'New Org', 'url': 'new_org', 'maxCompetitions': 5})
>>> comp = org.createCompetition({'name': 'Super Comp', 'url': 'super_comp'})
>>> teamData = {'name': 'UAF Team', 'username': 'uafteam', 'password': 'U@fR0(k5', 'networkCidr': '192.168.1.0/24', 'scoreConfigurations': "{'someService':{'port':666}}"}
>>> team = comp.createTeam(teamData)
>>> scoreConfigsString = team.getScoreConfigurations()
>>> scoreConfigs = json.loads(scoreConfigsString)
>>> print scoreConfigs['someService']
{'port': 666}
>>> 
```
* * *
#### setScoreConfigurations()
endpoints.Competition.Team.**setScoreConfiguration**(self, scoreConfiguration)
<br> Sets the scoreConfiguration of the object. This gets a little funky, since the string is actualy supposed to be a pickled dictionary. 
<br>**Input**
* scoreConfiguration - *String* (required)

**Output**
* Boolean?

**Example**
```python
>>> from ScoringEngine.endpoints import *
>>> org = createOrganization({'name': 'New Org', 'url': 'new_org', 'maxCompetitions': 5})
>>> comp = org.createCompetition({'name': 'Super Comp', 'url': 'super_comp'})
>>> teamData = {'name': 'UAF Team', 'username': 'uafteam', 'password': 'U@fR0(k5', 'networkCidr': '192.168.1.0/24', 'scoreConfigurations': "{'someService':{'port':666}}"}
>>> team = comp.createTeam(teamData)
>>> team.setScoreConfigurations("{'someService':{'port': 420}}")
>>> scoreConfigsString = team.getScoreConfigurations()
>>> scoreConfigs = json.loads(scoreConfigsString)
>>> print scoreConfigs['someService']
{'port': 420}
>>>
```
* * *
## Inject
#### edit()
endpoints.Competition.Inject.**edit**(self, \*\*kwargs)
<br>**Input**
* \*\*kwargs

**Output**
* Something

**Example**
```python
```
* * *

#### getId()
endpoints.Competition.Inject.**getId**(self)
<br>**Input**
* None

**Output**
* Something

**Example**
```python
```
* * *

#### setRequireResponse()
endpoints.Competition.Inject.**setRequireResponse**(self, requireResponse)
<br>**Input**
* requireResponse - *Boolean* (required)

**Output**
* Something

**Example**
```python
```
* * *

#### getRequireResponse()
endpoints.Competition.Inject.**getRequireResponse**(self)
<br>**Input**
* None

**Output**
* Something

**Example**
```python
```
* * *

#### setManualDelivery()
endpoints.Competition.Inject.**setManualDelivery**(self, manualDelivery)
<br>**Input**
* manualDelivery - *Boolean* (required)

**Output**
* Something

**Example**
```python
```
* * *

#### getManualDelivery()
endpoints.Competition.Inject.**getManualDelivery**(self)
<br>**Input**
* None

**Output**
* Something

**Example**
```python
```
* * *

#### setDatetimeDelivery()
endpoints.Competition.Inject.**setDatetimeDelivery**(self, datetimeDelivery)
<br>**Input**
* datetimeDelivery - *Datetime* (required)

**Output**
* Something

**Example**
```python
```
* * *

#### getDatetimeDelivery()
endpoints.Competition.Inject.**getDatetimeDelivery**(self)
<br>**Input**
* None

**Output**
* Something

**Example**
```python
```
* * *

#### setDatetimeResponseDue()
endpoints.Competition.Inject.**setDatetimeResponseDue**(self, datetimeResponseDue)
<br>**Input**
* datetimeResponseDue - *Datetime* (required)

**Output**
* Something

**Example**
```python
```
* * *

#### getDatetimeResponseDue()
endpoints.Competition.Inject.**getDatetimeResponseDue**(self)
<br>**Input**
* None

**Output**
* Something

**Example**
```python
```
* * *

#### setDatetimeResponseClose()
endpoints.Competition.Inject.**setDatetimeResponseClose**(self, datetimeResponseClose)
<br>**Input**
* datetimeResponseClose - *Datetime* (required)

**Output**
* Something

**Example**
```python
```
* * *

#### getDatetimeResponseClose()
endpoints.Competition.Inject.**getDatetimeResponseClose**(self)
<br>**Input**
* None

**Output**
* Something

**Example**
```python
```
* * *

#### setTitle()
endpoints.Competition.Inject.**setTitle**(self, title)
<br>**Input**
* title - *String* (required)

**Output**
* Something

**Example**
```python
```
* * *

#### getTitle()
endpoints.Competition.Inject.**getTitle**(self)
<br>**Input**
* None

**Output**
* Something

**Example**
```python
```
* * *

#### setBody()
endpoints.Competition.Inject.**setBody**(self, body)
<br>**Input**
* body - *String* (required)

**Output**
* Something

**Example**
```python
```
* * *

#### getBody()
endpoints.Competition.Inject.**getBody**(self)
<br>**Input**
* None

**Output**
* Something

**Example**
```python
```
* * *

#### getDocuments()
endpoints.Competition.Inject.**getDocuments**(self)
<br>**Input**
* None

**Output**
* Something

**Example**
```python
```
* * *

#### getResponses()
endpoints.Competition.Inject.**getResponses**(self)
<br>**Input**
* None

**Output**
* Something

**Example**
```python
```
* * *

## InjectResponse
#### edit()
endpoints.Competition.InjectResponse.**edit**(self, \*\*kwargs)
<br>**Input**
* \*\*kwargs

**Output**
* Boolean?

**Example**
```python
```
* * *

#### getId()
function header
<br>**Input**
* None

**Output**
* Something

**Example**
```python
```
* * *

#### setDatetime()
endpoints.Competition.InjectResponse.**setDatetime**(self, datetime)
<br>**Input**
* datetime - *Datetime* (required)

**Output**
* Something

**Example**
```python
```
* * *

#### getDatetime()
endpoints.Competition.InjectResponse.**getDatetime**(self)
<br>**Input**
* None

**Output**
* Datetime

**Example**
```python
```
* * *

#### setContent()
endpoints.Competition.InjectResponse.**setContent**(self, content)
<br>**Input**
* content - *String* (required)

**Output**
* Something

**Example**
```python
```
* * *

#### getContent()
endpoints.Competition.InjectResponse.**getContent**(self)
<br>**Input**
* None

**Output**
* String

**Example**
```python
```
* * *

## Incident
#### edit()
endpoints.Competition.Incident.**edit**(self, \*\*kwargs)
<br>**Input**
* None

**Output**
* Something

**Example**
```python
```
* * *

#### getId()
endpoints.Competition.Incident.**getId**(self)
<br>**Input**
* None

**Output**
* Integer

**Example**
```python
```
* * *

#### setDatetime()
endpoints.Competition.Incident.**setDatetime**(self, datetime)
<br>**Input**
* datetime - *Datetime* (required)

**Output**
* Something

**Example**
```python
```
* * *

#### getDatetime()
endpoints.Competition.Incident.**getDatetime**(self)
<br>**Input**
* None

**Output**
* Datetime

**Example**
```python
```
* * *

#### setSubject()
endpoints.Competition.Incident.**setSubject**(self, subject)
<br>**Input**
* subject - *String* (required)

**Output**
* Something

**Example**
```python
```
* * *

#### getSubject()
endpoints.Competition.Incident.**getSubject**(self)
<br>**Input**
* None

**Output**
* String

**Example**
```python
```
* * *

#### setContent()
endpoints.Competition.Incident.**setContent**(self, content)
<br>**Input**
* content - *String* (required)

**Output**
* Something

**Example**
```python
```
* * *

#### getContent()
endpoints.Competition.Incident.**getContent**(self)
<br>**Input**
* None

**Output**
* Something

**Example**
```python
```
* * *

## IncidentResponse
#### edit()
endpoints.Competition.IncidentResponse.**edit**(self)
<br>**Input**
* None

**Output**
* Something

**Example**
```python
```
* * *

#### getId()
endpoints.Competition.IncidentResponse.**getId**(self)
<br>**Input**
* None

**Output**
* Something

**Example**
```python
```
* * *

#### setReplyTo()
endpoints.Competition.IncidentResponse.**setReplyTo**(self)
<br>**Input**
* None

**Output**
* Something

**Example**
```python
```
* * *

#### getReplyTo()
endpoints.Competition.IncidentResponse.**getReplyTo**(self)
<br>**Input**
* None

**Output**
* Something

**Example**
```python
```
* * *

#### setDatetime()
endpoints.Competition.IncidentResponse.**setDatetime**(self)
<br>**Input**
* None

**Output**
* Something

**Example**
```python
```
* * *

#### getDatetime()
endpoints.Competition.IncidentResponse.**getDatetime**(self)
<br>**Input**
* None

**Output**
* Something

**Example**
```python
```
* * *

#### setSubject()
endpoints.Competition.IncidentResponse.**setSubject**(self)
<br>**Input**
* None

**Output**
* Something

**Example**
```python
```
* * *

#### getSubject()
endpoints.Competition.IncidentResponse.**getSubject**(self)
<br>**Input**
* None

**Output**
* Something

**Example**
```python
```
* * *

#### setContent()
endpoints.Competition.IncidentResponse.**setContent**(self)
<br>**Input**
* None

**Output**
* Something

**Example**
```python
```
* * *

#### getContent()
endpoints.Competition.IncidentResponse.**getContent**(self)
<br>**Input**
* None

**Output**
* Something

**Example**
```python
```
* * *


## Score
#### edit()
endpoints.Competition.Score.****(self)
<br>**Input**
* None

**Output**
* Something

**Example**
```python
```
* * *

#### getId()
endpoints.Competition.Score.****(self)
<br>**Input**
* None

**Output**
* Something

**Example**
```python
```
* * *

#### setDatetime()
endpoints.Competition.Score.****(self)
<br>**Input**
* None

**Output**
* Something

**Example**
```python
```
* * *

#### getDatetime()
endpoints.Competition.Score.****(self)
<br>**Input**
* None

**Output**
* Something

**Example**
```python
```
* * *

#### setValue()
endpoints.Competition.Score.****(self)
<br>**Input**
* None

**Output**
* Something

**Example**
```python
```
* * *

#### getValue()
endpoints.Competition.Score.****(self)
<br>**Input**
* None

**Output**
* Something

**Example**
```python
```
* * *

#### setMessage()
endpoints.Competition.Score.****(self)
<br>**Input**
* None

**Output**
* Something

**Example**
```python
```
* * *

#### getMessage()
endpoints.Competition.Score.****(self)
<br>**Input**
* None

**Output**
* Something

**Example**
```python
```
* * *

## Organization
#### edit()
function header
<br>**Input**
* None

**Output**
* Something

**Example**
```python
```
* * *

#### getDeleteable()
function header
<br>**Input**
* None

**Output**
* Something

**Example**
```python
```
* * *

#### getName()
function header
<br>**Input**
* None

**Output**
* Something

**Example**
```python
```
* * *

#### setName()
function header
<br>**Input**
* None

**Output**
* Something

**Example**
```python
```
* * *

#### getUrl()
function header
<br>**Input**
* None

**Output**
* Something

**Example**
```python
```
* * *

#### setUrl()
function header
<br>**Input**
* None

**Output**
* Something

**Example**
```python
```
* * *

#### getDescription()
function header
<br>**Input**
* None

**Output**
* Something

**Example**
```python
```
* * *

#### setDescription()
function header
<br>**Input**
* None

**Output**
* Something

**Example**
```python
```
* * *

#### getMaxMembers()
function header
<br>**Input**
* None

**Output**
* Something

**Example**
```python
```
* * *

#### setMaxMembers()
function header
<br>**Input**
* None

**Output**
* Something

**Example**
```python
```
* * *

#### getMaxCompetitions()
function header
<br>**Input**
* None

**Output**
* Something

**Example**
```python
```
* * *

#### setMaxCompetitions()
function header
<br>**Input**
* None

**Output**
* Something

**Example**
```python
```
* * *

#### getNumMembers()
function header
<br>**Input**
* None

**Output**
* Something

**Example**
```python
```
* * *

#### setNumMembers()
function header
<br>**Input**
* None

**Output**
* Something

**Example**
```python
```
* * *

#### getNumCompetitions()
function header
<br>**Input**
* None

**Output**
* Something

**Example**
```python
```
* * *

#### setNumCompetitions()()
function header
<br>**Input**
* None

**Output**
* Something

**Example**
```python
```
* * *

#### getCompetitions()
function header
<br>**Input**
* None

**Output**
* Something

**Example**
```python
```
* * *

#### getCompetition()
function header
<br>**Input**
* None

**Output**
* Something

**Example**
```python
```
* * *

#### createCompetition()
function header
<br>**Input**
* None

**Output**
* Something

**Example**
```python
```
* * *

#### deleteCompetition()
function header
<br>**Input**
* None

**Output**
* Something

**Example**
```python
```
* * *

#### editCompetition()
function header
<br>**Input**
* None

**Output**
* Something

**Example**
```python
```
* * *

#### getMembers()
function header
<br>**Input**
* None

**Output**
* Something

**Example**
```python
```
* * *

#### getMember()
function header
<br>**Input**
* None

**Output**
* Something

**Example**
```python
```
* * *

#### createMember()
function header
<br>**Input**
* None

**Output**
* Something

**Example**
```python
```
* * *

#### deleteMember()
function header
<br>**Input**
* None

**Output**
* Something

**Example**
```python
```
* * *

#### editMember()
function header
<br>**Input**
* None

**Output**
* Something

**Example**
```python
```
* * *



## User
#### count()
function header
<br>**Input**
* None

**Output**
* Something

**Example**
```python
```
* * *

#### edit()
function header
<br>**Input**
* None

**Output**
* Something

**Example**
```python
```
* * *

#### getName()
function header
<br>**Input**
* None

**Output**
* Something

**Example**
```python
```
* * *

#### setName()
function header
<br>**Input**
* None

**Output**
* Something

**Example**
```python
```
* * *

#### getUsername()
function header
<br>**Input**
* None

**Output**
* Something

**Example**
```python
```
* * *

#### setUsername()
function header
<br>**Input**
* None

**Output**
* Something

**Example**
```python
```
* * *

#### getPassword()
function header
<br>**Input**
* None

**Output**
* Something

**Example**
```python
```
* * *

#### setPassword()
function header
<br>**Input**
* None

**Output**
* Something

**Example**
```python
```
* * *

#### getDescription()
function header
<br>**Input**
* None

**Output**
* Something

**Example**
```python
```
* * *

#### setDescription()
function header
<br>**Input**
* None

**Output**
* Something

**Example**
```python
```
* * *

#### getOrganizationId()
function header
<br>**Input**
* None

**Output**
* Something

**Example**
```python
```
* * *

#### setOrganizationId()
function header
<br>**Input**
* None

**Output**
* Something

**Example**
```python
```
* * *


## Document
#### edit()
function header
<br>**Input**
* None

**Output**
* Something

**Example**
```python
```
* * *

#### setContentType()
function header
<br>**Input**
* None

**Output**
* Something

**Example**
```python
```
* * *

#### getContentType()
function header
<br>**Input**
* None

**Output**
* Something

**Example**
```python
```
* * *

#### setFileHash()
function header
<br>**Input**
* None

**Output**
* Something

**Example**
```python
```
* * *

#### getFileHash()
function header
<br>**Input**
* None

**Output**
* Something

**Example**
```python
```
* * *

#### setFilePath()
function header
<br>**Input**
* None

**Output**
* Something

**Example**
```python
```
* * *

#### getfilePath()
function header
<br>**Input**
* None

**Output**
* Something

**Example**
```python
```
* * *

#### setFilename()
function header
<br>**Input**
* None

**Output**
* Something

**Example**
```python
```
* * *

#### getFilename()
function header
<br>**Input**
* None

**Output**
* Something

**Example**
```python
```
* * *

#### setUrlEncodedFilename()
function header
<br>**Input**
* None

**Output**
* Something

**Example**
```python
```
* * *

#### getUrlEncodedFilename()
function header
<br>**Input**
* None

**Output**
* Something

**Example**
```python
```
* * *

