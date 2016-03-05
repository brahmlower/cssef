# Development Plans

The project is going through a refactory period. The refactory process is broken into four seperate stages. Each stage will receive a minor release. The stages are outlined below.
## Refactoring
### Stage 1 (release 0.01) [DONE]
The project is current in stage 1 of development/refactoring. The project is not operational and tasks are not optimally divided. The scoring engine core and web api are reliant on each other, and cannot be separated. The Web UI is also entirely dependant on the Web API, and cannot directly interface with the scoring engine core.

#### Final State Goals
Most initial features will be implemented along with necessary unit and integration tests. The scoring engine core and Web API will still be reliant on one another, and the Web UI will still rely on the Web API to interact with the scoring engine core. The project will be stable and semi-robust at this point.

The following is a diagram of how this stage will operate. The SQL database is consumed directly by the Scoring Engine Core + Web API. The Web UI interacts with the Scoring Engine Core by communicating with the Web API.
Red Lines: Database traffic (can be networked)
Purple Lines: Traffic between the Scoring Engine Core + Web API service and the Web UI service
![Stage 1](http://i.imgur.com/8y3nj13.png)

### Stage 2 (release 0.02) [DONE]
#### Final State Goals
The Web API will be separated from the Scoring Engine. They will be able to run independant of each other. The scoring engine will need the rest of its service support (daemon-ness, ports, database handling/connections), since it is currently held up entirely by Django. The Web API won't require much further changing than settings and configurations for pointing to the Scoring Engine.

The following diagram is a high level representation of data flow for Stage 2.
Red Line: Database traffice
Blue Lines: Traffic as client to a Scoring Engine Endpoint
![Stage 2](http://i.imgur.com/z4TYaDq.png)

### Stage 3 (release 0.03)
#### Final State Goals
A standalone command line client will be created to interact with the Scoring Engine. This should support everything the ~~Web UI~~ and Web API supports.

The following diagram is a high level representation of data flow for Stage 3.
* Red Line: Database traffice
* Blue Lines: Traffic as client to a Scoring Engine Endpoint
![Stage 3](http://i.imgur.com/K7Rdx71.png)

### Stage 4 (release 0.04)
#### Final State Goals
The Web API is expaned to act as both a Scoring Engine Endpoint and a client. This means the Web API will act as a proxy for other scoring engine clients (such as the Web UI and CLI). This means a Scoring Engine can be configured such that it is not directly accessible by some clients. All clients (~~Web API~~, Web UI, CLI) will have settings to specify the address of the host to consume. The clients will auto negotiate if the host it's consuming is a Scoring Engine or a Web API, and submit requests accordingly.

The following diagram is a high level representation of data flow for Stage 4.
* Red Line: Database traffice
* Blue Lines: Traffic as client to a Scoring Engine Endpoint
* Yellow Lines: Traffic as a client to a Web API
![Stage 4](http://i.imgur.com/ZVt6VGP.png)

## Post Refactoring
I hope to have a list of features and fixes to implement by this point. Those changes will be implemented. Once proper tests have been written for the changes, the project will be ready for it's first official release (maybe 0.10?)
