"""
This list of CSSEF errors will be expanded and modified as more errors are
added.

Authentication Errors:
----------------------
Allotted error codes: 30 - 49

- 30 - IncorrectCredentials
- 31 - TokenDisallowed
- 32 - TokenExpired
- 33 - BadAuthSource

General User Errors:
--------------------
Allotted error codes: 50 - 150

- 50 - InvalidPkidValue

"""
import traceback
from systemd import journal
#from cssefserver.utils import EndpointOutput

class CssefException(Exception):
    """A basic CSSEF exception to be subclassed

    This class is meant to be subclassed by actual errors, setting the value
    for 'value' and 'message'. Any CssefExcption can be easily prepared for
    the user by calling ``as_return_dict()``.
    """
    value = None
    message = None

    def log(self):
        journal.send(message="(error %d): Caught a CSSEF error" % self.value) #pylint: disable=no-member
        for i in self.message:
            journal.send(message="(error %d): %s" % (self.value, i)) #pylint: disable=no-member

    def as_return_dict(self):
        """Return the error as a return dictionary

        This returns a "return_dict", which is just a dictionary containing
        the keys 'value', 'message', and 'content'. This will just create the
        return dict based on the properties value and message. There is no
        content. The error is also logged via journal.send().

        Returns:
            dict: A dictionary with the keys 'value' and 'message' with
            values of the corresponding properties. An example dict:

            ``{'value': 1, 'message': ['Example message'], 'content': []}``
        """
        # Log everything we need first
        self.log()
        # journal.send(message="(error %d): Caught a CSSEF error" % self.value) #pylint: disable=no-member
        # for i in self.message:
        #     journal.send(message="(error %d): %s" % (self.value, i)) #pylint: disable=no-member

        # Now build the return object
        return {"value": self.value, "message": self.message}
        # The following is commented because importing EndpointOutput here
        # causes some *really* bad cyclical import errors
        # TODO: Maybe this method shoudln't be a thing. I have a function to handle
        # exceptions that are thrown- so CssefExeptions shouldn't be any different.
        # let them be thrown, then let them be handled by the handle_exception method
        # like everything else.
        # output = EndpointOutput(self.value, self.message)
        # return output.as_dict()

    def __repr__(self):
        return str(self.message)

class CssefPluginMalformedName(CssefException):
    value = 9000
    message = ["Incorrectly formatted plugin entry."]

    def __init__(self, plugin_value):
        self.message.append("The provided plugin value was: '%s'." % plugin_value)

class CssefPluginInstantiationError(CssefException):
    value = 9001
    message = ["Module failed to instantiate."]

    def __init__(self, plugin_value):
        self.message.append("The provided plugin value was: '%s'." % plugin_value)
        for i in traceback.format_exc().splitlines():
            self.message.append(i)

class CssefObjectDoesNotExist(Exception):
    """Expection for model instantiation errors

    This is the base exception that is subclassed as ObjectDoesNotExist in the
    ModelWrapper class. It is thrown when one tries to instantiate the model
    with data identifying a particular database record that does not exist. I
    may eventually change this to subclass CssefException rather than
    Exception, but there may be some unintended consequences to that.
    """
    def __init__(self, message):
        super(CssefObjectDoesNotExist, self).__init__()
        self.message = message

    def __str__(self):
        return repr(self.message)

class IncorrectCredentials(CssefException):
    """Generic authentication failure exection

    This is used in cases where enough authentication information was provided
    but some part of it was incorrect.
    """
    value = 30
    message = ['Bad username or password']

class TokenDisallowed(CssefException):
    """Error returned when token authentication is disabled

    If the server has token authentication disabled, then this error will be
    returned to the user indicating that they must provide a password rather
    than using a token.
    """
    value = 31
    message = ['Token may not be used during login.']

class NoUsernameProvided(CssefException):
    """Username field was missing

    Used when the username is missing from the provided authentication
    information.
    """
    value = 32
    message = ['No username provided.']

class NoOrganizationProvided(CssefException):
    """Organization field was missing

    Used when the organization is missing from the provided authentication
    information.
    """
    value = 33
    message = ['No organization provided.']

class NonexistentUser(CssefException):
    """Error returned when the username does not exist

    This error is returned when a specified user does not exist. This should
    not be used within the authentication process, as it gives information
    about what users do and don't exist.
    """
    value = 34
    message = ['Unable to find user with provided username.']

class PermissionDenied(CssefException):
    value = 35
    message = ['Permission id denied.']

class AuthFindsMultipleUsers(CssefException):
    """Error returned when multiple users have the same name

    This error is thrown when there are multiple users with the same username
    within the same organization. This is extremely bad, and will idealy never
    be seen.
    """
    value = 36
    message = ['Username + Organization returned multiple users.']

class AuthIncorrectAdminToken(CssefException):
    """Error return when an invalid token was provided

    This error is thrown when the authentication token is invalid in some way.
    """
    value = 37
    message = ['Provided auth-token was incorrect.']


class InvalidPkidValue(CssefException):
    """Indicates the provided PKID value was bad

    This error indicates that there was a problem interpreting the value
    provided for the pkid of some object.
    """
    value = 50
    message = ['Provided pkid was not valid.']
