class CssefException(Exception):
    value = None
    message = None
    def as_return_dict(self):
        return {'value': self.value, 'message': self.message, 'content': []}

# Authentication Errors:
# Allotted error codes: 30 - 50
# 30 - IncorrectCredentials
# 31 - TokenDisallowed
# 32 - TokenExpired
# 33 - BadAuthSource

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
