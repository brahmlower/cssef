# API Documentation
## Organization
Endpoints:
* [/organizations.json](https://github.com/bplower/cssef/blob/refactor/ScoringEngine/WebApi/README.md#resource-list)
* [/organizations/\<id\>.json](https://github.com/bplower/cssef/blob/refactor/ScoringEngine/WebApi/README.md#resource-details)
* [/organizations/\<id\>/members.json](https://github.com/bplower/cssef/blob/refactor/ScoringEngine/WebApi/README.md#resource-list-1)
* [/organizations/\<id\>/members/\<id\>.json](https://github.com/bplower/cssef/blob/refactor/ScoringEngine/WebApi/README.md#resource-details-1)
* [/organizations/\<id\>/competitions.json](https://github.com/bplower/cssef/blob/refactor/ScoringEngine/WebApi/README.md#resource-list-2)
* [/organizations/\<id\>/competitions/\<id\>.json](https://github.com/bplower/cssef/blob/refactor/ScoringEngine/WebApi/README.md#resource-details-2)

### Organizations
#### Resource List
URL: /organizations.json
<br> Description: Lists all organizations
<br> Methods: GET, POST
<br> Example Output:
<pre>[
	{
		"organizationId": 1,
		"name": "Example Organization Name 1",
		"url": "example_organization_name_1",
		"maxMembers": 10,
		"maxCompetitions": 10
	},
	{
		"organizationId": 2,
		"name": "Example Organization Name 2",
		"url": "example_organization_name_2",
		"maxMembers": 10,
		"maxCompetitions": 10
	}
]</pre>
#### Resource Details
URL: /organizations/1.json
<br> Description: Lists extended details about the organization with the id of 1
<br> Methods: GET, PUT, PATCH, DELETE
<br> Example Output:
<pre>{
	"organizationId": 1,
	"name": "Example Organization Name 1",
	"url": "example_organization_name_1",
	"maxMembers": 10,
	"maxCompetitions": 10
	"members": [
		{
			"userId": 1,
			"name": "John Doe",
			"username": "johnd",
			"password": "somehashhere"
		},
		{
			"userId": 2,
			"name": "Jane Doe",
			"username": "janed",
			"password": "somehashhere"
		}
	],
	"competitions": [
		{
			"competitionId": 1,
			"name": "Example Competition 1",
			"url": "example_competition_1",
			"description": "This is an example description."
		},
		{
			"competitionId": 2,
			"name": "Example Competition 2",
			"url": "example_competition_2",
			"description": "This is another example description."
		}
	]
}</pre>

### Organizations - Members
#### Resource List
URL: /organizations/1/members.json
<br> Description: Lists the members of the organization with the id of 1
<br> Methods: GET, POST
<br> Example Output:
<pre>[
	{
		"userId": 1,
		"name": "John Doe",
		"username": "johnd",
		"password": "somehashhere"
	},
	{
		"userId": 2,
		"name": "Jane Doe",
		"username": "janed",
		"password": "somehashhere"
	}
]</pre>

#### Resource Details
URL: /organizations/1/members/1.json
<br>Description: This provides details for the member with id 1 within organization with id 1
<br>Methods: GET, PUT, PATCH, DELETE
<br>Example Output:
<pre>{
	"userId": 2,
	"name": "Jane Doe",
	"username": "janed",
	"password": "somehashhere"
}</pre>

### Organizations - Competitions
#### Resource List
URL: /organizations/1/competitions.json
<br> Description: Lists the competitions of the organization with the id of 1
<br> Methods: GET, POST
<br> Example Output:
<pre>[
	{
		"competitionId": 1,
		"name": "Example Competition 1",
		"url": "example_competition_1",
		"description": "This is an example description."
	},
	{
		"competitionId": 2,
		"name": "Example Competition 2",
		"url": "example_competition_2",
		"description": "This is another example description."
	}
]</pre>
#### Resource Details
URL: /organizations/1/competitions/2.json
<br> Description: Lists the competitions of the organization with the id of 1
<br> Methods: GET, PUT, PATCH, DELETE
<br> Example Output:
<pre>{
	"competitionId": 2,
	"name": "Example Competition 2",
	"url": "example_competition_2",
	"description": "This is another example description."
}</pre>

## Competitions
Endpoints:
* [/competitions.json](https://github.com/bplower/cssef/blob/refactor/ScoringEngine/WebApi/README.md#resource-list-3)
* [/competitions/\<id\>.json](https://github.com/bplower/cssef/blob/refactor/ScoringEngine/WebApi/README.md#resource-details-3)
* [/competitions/\<id\>/services.json](https://github.com/bplower/cssef/blob/refactor/ScoringEngine/WebApi/README.md#resource-list-4)
* [/competitions/\<id\>/services/\<id\>.json](https://github.com/bplower/cssef/blob/refactor/ScoringEngine/WebApi/README.md#resource-details-4)
* /competitions/\<id\>/services/\<id\>/plugin.json
* [/competitions/\<id\>/teams.json](https://github.com/bplower/cssef/blob/refactor/ScoringEngine/WebApi/README.md#resource-list-5)
* [/competitions/\<id\>/teams/\<id\>.json](https://github.com/bplower/cssef/blob/refactor/ScoringEngine/WebApi/README.md#resource-details-5)
* [/competitions/\<id\>/injects.json](https://github.com/bplower/cssef/blob/refactor/ScoringEngine/WebApi/README.md#resource-list-6)
* [/competitions/\<id\>/injects/\<id>.json](https://github.com/bplower/cssef/blob/refactor/ScoringEngine/WebApi/README.md#resource-details-6)
* /competitions/\<id\>/injects/\<id\>/files.json
* /competitions/\<id\>/injects/\<id\>/files/\<id\>.json
* /competitions/\<id\>/injects/\<id\>/responses.json
* /competitions/\<id\>/injects/\<id\>/responses/\<id\>.json
* /competitions/\<id\>/injects/\<id\>/responses/\<id\>/files.json
* /competitions/\<id\>/injects/\<id\>/responses/\<id\>/files/\<id\>.json
* [/competitions/\<id\>/incidents.json](https://github.com/bplower/cssef/blob/refactor/ScoringEngine/WebApi/README.md#resource-list-7)
* [/competitions/\<id\>/incidents/\<id\>.json](https://github.com/bplower/cssef/blob/refactor/ScoringEngine/WebApi/README.md#resource-details-7)
* /competitions/\<id\>/incidents/\<id\>/responses.json
* /competitions/\<id\>/incidents/\<id\>/responses/\<id\>.json
* /competitions/\<id\>/incidents/\<id\>/responses/\<id\>/files.json
* /competitions/\<id\>/incidents/\<id\>/responese/\<id\>/files/\<id\>.json
* [/competitions/\<id\>/scores.json](https://github.com/bplower/cssef/blob/refactor/ScoringEngine/WebApi/README.md#resource-list-8)
* [/competitions/\<id\>/scores/\<id\>.json](https://github.com/bplower/cssef/blob/refactor/ScoringEngine/WebApi/README.md#resource-details-8)

### Competitions
#### Resource List
URL: /compeititons.json
<br>Description: Lists all competitions
<br>Methods: GET, POST
<br>Example Output:
<pre>[
	{
		"competitionId": 1,
		"name": "Example Competition 1",
		"url": "example_competition_1",
		"description": "This is an example description."
	},
	{
		"competitionId": 2,
		"name": "Example Competition 2",
		"url": "example_competition_2",
		"description": "This is another example description."
	}
]</pre>

#### Resource Details
URL: /compeititons/2.json
<br> Description: Lists the competition with the id of 2
<br> Methods: GET, PUT, PATCH, DELETE
<br> Example Output:
<pre>{
	"competitionId": 2,
	"name": "Example Competition 2",
	"url": "example_competition_2",
	"description": "This is another example description."
}</pre>

### Competitions - Services
#### Resource List
URL: /compeititons/2/services.json
<br> Description: Lists the services within the competition with the id of 2
<br> Methods: GET, POST
<br> Example Output:
<pre>[
	{
		"serviceId": 1,
		"competitionId": 2,
		"name": "SSH Service",
		"description": "This is an example service description."
	},
	{
		"serviceId": 2,
		"competitionId": 2,
		"name": "HTTP Service",
		"description": "This is another example service description."
	}
]</pre>
#### Resource Details
URL: /compeititons/2/services/1.json
<br> Description: Lists the services within the competition with the id of 2
<br> Methods: GET, POST
<br> Example Output:
<pre>{
	"serviceId": 2,
	"competitionId": 2,
	"name": "HTTP Service",
	"description": "This is another example service description."
}</pre>

### Competitions - Teams
#### Resource List
URL: /compeititons/2/teams.json
<br> Description: Lists the teams within the competition with the id of 2
<br> Methods: GET, POST
<br> Example Output:
<pre>[
	{
		"teamId": 1,
		"competitionId": 2,
		"name": "Example Team 1",
		"username": "exampleteam1",
		"password": "password-ex1",
		"description": "This is an example service description."
	},
	{
		"teamId": 2,
		"competitionId": 2,
		"name": "Example Team 2",
		"username": "exampleteam2"
		"password": "password-ex2"
		"description": "This is another example service description."
	}
]</pre>
#### Resource Details
URL: /compeititons/2/teams/2.json
<br> Description: Lists the services within the competition with the id of 2
<br> Methods: GET, POST
<br> Example Output:
<pre>{
	"teamId": 2,
	"competitionId": 2,
	"name": "Example Team 2",
	"username": "exampleteam2"
	"password": "password-ex2"
	"description": "This is another example service description."
}</pre>

### Competitions - Injects
#### Resource List
#### Resource Details
### Competitions - Injects - Files
#### Resource List
#### Resource Details
### Competitions - Injects - Responses
#### Resource List
#### Resource Details
### Competitions - Injects - Responses - Files
#### Resource List
#### Resource Details
### Competitions - Incidents
#### Resource List
#### Resource Details
### Competitions - Incidents - Responses
#### Resource List
#### Resource Details
### Competitions - Incidents - Responses - Files
#### Resource List
#### Resource Details
### Competitions - Scores
#### Resource List
#### Resource Details

## Plugins
Endpoints:
* [/plugins.json](https://github.com/bplower/cssef/blob/refactor/ScoringEngine/WebApi/README.md#resource-list-9)
* [/plugins/\<id\>.json](https://github.com/bplower/cssef/blob/refactor/ScoringEngine/WebApi/README.md#resource-details-9)
* [/plugins/\<id\>/files.json](https://github.com/bplower/cssef/blob/refactor/ScoringEngine/WebApi/README.md#resource-list-10)
* [/plugins/\<id\>/files/\<id\>.json](https://github.com/bplower/cssef/blob/refactor/ScoringEngine/WebApi/README.md#resource-details-10)

### Plugins
#### Resource List
#### Resource Details
### Plugins - Files
#### Resource List
#### Resource Details

## Files
Endpoints:
* [/files.json](https://github.com/bplower/cssef/blob/refactor/ScoringEngine/WebApi/README.md#resource-list-11)
* [/files/\<id\>.json](https://github.com/bplower/cssef/blob/refactor/ScoringEngine/WebApi/README.md#resource-details-11)

### Files
#### Resource List
#### Resource Details
