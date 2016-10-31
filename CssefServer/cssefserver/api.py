import time
import logging
import tokenlib
from cssefserver import ModelWrapper
from cssefserver.models import User as UserModel
from cssefserver.models import Organization as OrganizationModel
from cssefserver.utils import PasswordHash
from cssefserver.errors import MaxMembersReached
from cssefserver.errors import AuthIncorrectAdminToken
from cssefserver.errors import NoUsernameProvided
from cssefserver.errors import NoOrganizationProvided
from cssefserver.errors import NonexistentUser
from cssefserver.errors import AuthFindsMultipleUsers
from cssefserver.errors import IncorrectCredentials
from cssefserver.errors import PermissionDenied

class User(ModelWrapper):
    """Defines a basic User object.

    This subclasses ModelWrapper, and uses user.models.User as it's database
    model.

    Attributes:
        model_object (UserModel): Defines the model the object is associated
            with
        fields (list): Lists the fields within the associated model to present
            to the client
    """
    model_object = UserModel
    fields = [
        'name',
        'username',
        'password',
        'description',
        'organization']

    @property
    def password(self):
        """Password for the user.

        This wraps the password attribute of the associated model.

        Returns:
            PasswordHash: Contains the hash of the users password. The hash
            itself can be extracted by reading the PasswordHash.hash
            attribute. See PasswordHash for more information.

        Example:
            The following is an example shows instantiating an existing user
            via its pkid, displaying the value type of its password attribute,
            then retrieving the password hash from the PasswordHash object.::

                >>> u = User(pkid = 1)
                >>> type(u.password)
                <type 'PasswordHash'>
                >>> print u.password.hash
                abiglonghashisprintedhere
                >>>

        """
        #return PasswordHash(self.model.password)
        return self.model.password

    @password.setter
    def password(self, value):
        """Sets the password for the User.

        This abstracts the process setting the new value in the database.

        Args:
            value (str): Plaintext value the password should be set to.

        Returns:
            None:

        Example:
            <todo>
        """
        rounds = 10
        pass_hash = PasswordHash.new(value, rounds)
        self.model.password = pass_hash.hash
        self.server.database_connection.commit()

    @classmethod
    def from_dict(cls, server, kw_dict):
        org = Organization.from_database(server, pkid=kw_dict['organization'])
        if not org:
            print "Failed to get organization with pkid '%s'" % kw_dict['organization']
            raise ValueError
        if org.model.num_members >= org.max_members:
            raise MaxMembersReached(org.max_members)
        # Copied right from ModelWrapper.from_dict
        model_object_inst = cls.model_object()
        cls_inst = cls(server, model_object_inst)
        for i in kw_dict:
            if i in cls_inst.fields:
                setattr(cls_inst, i, kw_dict[i])
        server.database_connection.add(cls_inst.model)
        server.database_connection.commit()
        org.set_num_members()
        return cls_inst

    def authorized(self, auth_dict, group):
        # TODO: This is related to RBAC implementation
        return True

    def authenticate(self, auth_dict):
        """Attempt to authenticate with whatever information was provided

        The authdict may contain a token or key. Check if either is present
        and attempt to authenticate with that. It will attempt to authenticate
        with the token first. If that fails and autentication failover is not
        enabled, the function will just return. If authentication failover is
        enabled and the password is provided, it will try to authenticate
        with that. If no valid form of authentication is provided,
        authentication will fail.

        Args:
            auth_dict (dict): A dictionary with a password or token in it.

        Returns:
            bool: True if the passwords match, false if not.
        """
        if 'token' in auth_dict.keys():
            # Do token authentication
            if self.authenticate_token(auth_dict['token']):
                return True
            # Token was provided, but was invalid.
            # if not self.config.auth_failover:
            #     # Authentication failover is disabled.
            #     return False
        elif 'password' in auth_dict.keys():
            # Do password authentication
            return self.authenticate_password(auth_dict['password'])
        else:
            # Cannot authenticate!
            print "Neither a password nor auth token were provided!"
            return False

    def authenticate_token(self, raw_token):
        """Check if the provided token is valid for this user.

        This abstracts the process setting the new value in the database. This
        will eventually require additional processes to authorize the moving
        of an account from one organization to another.

        Args:
            value (int): The organization ID of the organization to put the
                user in.

        Returns:
            bool: True if the token belongs to the user and contains the
            correct user ID and organization ID. False if the token does not
            belong to the user, or contains an incorrect user ID or
            organization ID.

        Example:
            <todo>
        """
        try:
            token = tokenlib.parse_token(raw_token, secret=self.server.config.auth_token_salt, now=time.time())
        except tokenlib.errors.MalformedTokenError:
            return False
        # This is a large comparison, so it's been split into three booleans
        ids_match = token['id'] == self.get_id()
        username_match = token['username'] == self.username #pylint: disable=no-member
        org_match = token['organization'] == self.organization #pylint: disable=no-member
        return ids_match and username_match and org_match

    def authenticate_password(self, password):
        """Check if the provided plaintext password is valid for this user.

        This will check that the provided password matches the users password.
        The actual password comparison is done through the __eq__ attribute of
        the PasswordHash class. A token is created and returned if the
        password is correct, allowing the user to make further requests
        without having to reauthenticate each time.

        Args:
            password (str): Plaintext password candidate

        Returns:
            bool: True if the passwords match, false if not.
        """
        return PasswordHash(self.password) == password

    def get_new_token(self):
        token_dict = {"id": self.get_id(),
                      "username": self.username, #pylint: disable=no-member
                      "organization": self.organization} #pylint: disable=no-member
        token = tokenlib.make_token(token_dict, secret=self.server.config.auth_token_salt)
        return token

class Organization(ModelWrapper):
    model_object = OrganizationModel
    fields = [
        'name',
        'url',
        'description',
        'max_members',
        'max_competitions',
        'can_add_users',
        'can_delete_users',
        'can_add_competitions',
        'can_delete_competitions']

    def as_dict(self):
        """Provides a dictionary representation of the Organization

        Builds and returns a dictionary representing the values in the
        Organizations `fields` attribute. Organization.as_dict() includes the
        readonly attribute `deletable`.

        Returns:
            dict: A dictionary that represents the same values in the object.
        """
        tmp_dict = super(Organization, self).as_dict()
        tmp_dict['deletable'] = self.is_deletable()
        return tmp_dict

    def is_deletable(self):
        """Checks if the organization can be deleted.

        Return:
            bool: True if the organization can be deleted, false if it cannot
            be deleted.
        """
        return self.model.deletable

    def get_num_members(self):
        """Gets the current number of competitions belonging to the organization

        This gets the "cached" count of the current number of competitions
        that belong to the organization.

        Returns:
            int: The number of competitions that are part of the organization
        """
        return self.model.num_members

    def set_num_members(self):
        """Gets the current number of members in the organization

        This gets the "cached" count of the current number of users that are
        part of the organization.

        Returns:
            int: The number of users that are part of the oragnizaiton
        """
        self.model.num_members = User.count(self.server.database_connection, organization=self.get_id())
        self.server.database_connection.commit()

    def get_num_competitions(self):
        return self.model.set_num_competitions

    # def setNumCompetitions(self):
    #     self.model.numCompetitions = Competition.count(self.db, organization = self.get_id())
    #     self.db.commit()

    # def getCompetitions(self, **kwargs):
    #     return Competition.search(Competition, organization = self.get_id(), **kwargs)

    def get_members(self, **kwargs):
        return User.search(User, organization=self.get_id(), **kwargs)

    # def getCompetition(self, **kwargs):
    #     return Competition(**kwargs)

    def get_member(self, **kwargs):
        """Gets a specific member that belongs to the organization

        This will retrieve a specific user that belongs to the organization.

        Args:
            **kwargs: Keyword arguments that define the user to match.

        Returns:
            User: A user that belongs to the organization
        """
        kwargs['organization'] = self.get_id()
        return User(**kwargs)

def authorize_access(server, auth_dict, config):
    # Check if we're doing user authentication, or admin token auth.
    if 'admin-token' in auth_dict:
        # Just check that the auth key matches that of the authkey in the server config file
        if config.admin_token == auth_dict['admin-token']:
            # Auth key matched
            logging.debug("[AUTH INFO] Provided auth-token was correct.")
            return None
        else:
            raise AuthIncorrectAdminToken
    # Importing for this got pretty ugly... :(
    if not auth_dict.get('username', None):
        #print "[AUTH WARNING] No username provided."
        raise NoUsernameProvided
    if not auth_dict.get('organization', None):
        logging.debug("[AUTH WARNING] No organization was provided.")
        raise NoOrganizationProvided
    user_list = User.search(server, \
        username=auth_dict['username'], organization=auth_dict['organization'])
    if len(user_list) < 1:
        # No matching user was found
        raise NonexistentUser
    if len(user_list) > 1:
        # There are multiple users. This is extremely bad
        raise AuthFindsMultipleUsers
    user = user_list[0]
    # Authenticate the user
    if not user.authenticate(auth_dict):
        raise IncorrectCredentials
    # Authorize the user
    if not user.authorized(auth_dict, 'organization'):
        raise PermissionDenied
    return user
