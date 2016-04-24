class MaxCompetitionsReached(Exception):
    def __init__(self, maxCompetitions):
        self.maxCompetitions = maxCompetitions
        self.message = "The maximum number of competitions is %d" % self.maxCompetitions

    def __str__(self):
        return repr(self.message)

class MaxMembersReached(Exception):
    def __init__(self, maxMembers):
        self.maxMembers = maxMembers
        self.message = "The maximum number of members is %d" % self.maxMembers
    def __str__(self):
        return repr(self.message)