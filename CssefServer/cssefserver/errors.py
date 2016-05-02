"""
Authentication Errors:
Allotted error codes: 30 - 49
30 - IncorrectCredentials
31 - TokenDisallowed
32 - TokenExpired
33 - BadAuthSource

General User Errors:
Allotted error codes: 50 - 150
50 - InvalidPkidValue
"""

class CssefException(Exception):
    value = None
    message = None
    def as_return_dict(self):
        return {'value': self.value, 'message': self.message, 'content': []}

class CssefObjectDoesNotExist(Exception):
    'An exception for when the requested object does not exist - not needed I think'
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return repr(self.message)

class IncorrectCredentials(CssefException):
    value = 30
    message = ['Bad username or password']

class TokenDisallowed(CssefException):
    value = 31
    message = ['Token may not be used during login.']

class NoUsernameProvided(CssefException):
    value = 32
    message = ['No username provided.']

class NoOrganizationProvided(CssefException):
    value = 33
    message = ['No organization provided.']

class NonexistentUser(CssefException):
    value = 34
    message = ['Unable to find user with provided username.']

class PermissionDenied(CssefException):
    value = 35
    message = ['Permission id denied.']

class AuthFindsMultipleUsers(CssefException):
    value = 36
    message = ['Username + Organization returned multiple users.']

class AuthIncorrectAdminToken(CssefException):
    value = 37
    message = ['Provided auth-token was incorrect.']


class InvalidPkidValue(CssefException):
    value = 50
    message = ['Provided pkid was not valid.']
