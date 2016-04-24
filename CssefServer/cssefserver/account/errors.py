class MaxCompetitionsReached(Exception):
    def __init__(self, max_competitions):
        super(MaxCompetitionsReached, self).__init__()
        self.max_competitions = max_competitions
        self.message = "The maximum number of competitions is %d" % self.max_competitions

    def __str__(self):
        return repr(self.message)

class MaxMembersReached(Exception):
    def __init__(self, max_members):
        super(MaxMembersReached, self).__init__()
        self.max_members = max_members
        self.message = "The maximum number of members is %d" % self.max_members
    def __str__(self):
        return repr(self.message)
