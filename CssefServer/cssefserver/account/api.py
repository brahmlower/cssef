import time
import tokenlib
from cssefserver.utils import ModelWrapper
from cssefserver.account.models import User as UserModel
from cssefserver.account.models import Organization as OrganizationModel
from cssefserver.account.utils import PasswordHash
from cssefserver.account.errors import MaxMembersReached

# THIS IS HARDCODED, WHICH IS BAD
SECRET_SALT = "Gv1Z5EYyCJzNuc6hEbj5fd+E2P4+iNFw"

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
    def name(self):
        """Name of the user.

        This wraps the name attribute of the associated model.

        Returns:
            str: String containing the name of the User object.
        """
        return self.model.name

    @name.setter
    def name(self, value):
        """Sets the name of the User.

        This abstracts the process setting the new value in the database.

        Args:
            value (str): The value to set the name to.

        Returns:
            None:

        Example:
            <todo>
        """
        self.model.name = value
        self.db_conn.commit()

    @property
    def username(self):
        """Username for the user.

        This wraps the username attribute of the associated model.

        Returns:
            str: String containing the username of the User object.
        """
        return self.model.username

    @username.setter
    def username(self, value):
        """Sets the username of the User.

        This abstracts the process setting the new value in the database.

        TODO: This will eventually have to check that the username is unique
        to the organization. If it has already been taken, thow an error.

        Args:
            value (str): The value to set the username to.

        Returns:
            None:

        Example:
            <todo>
        """
        self.model.username = value
        self.db_conn.commit()

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
        self.db_conn.commit()

    @property
    def description(self):
        """Description for the user.

        This wraps the description attribute of the associated model.

        Returns:
            str: String containing the description of the User object.
        """
        return self.model.description

    @description.setter
    def description(self, value):
        """Sets the description for the User.

        This abstracts the process setting the new value in the database.

        Args:
            value (str): The value to set the description to.

        Returns:
            None:

        Example:
            <todo>
        """
        self.model.description = value
        self.db_conn.commit()

    @property
    def organization(self):
        """Sets the description for the User.

        This abstracts the process setting the new value in the database. This
        should eventaully instantiate an instance of the Organization with the
        associated ID and then return that, rather than just the ID.

        Returns:
            Int: Represents the Organization ID.

        Example:
            <todo>
        """
        return self.model.organization

    @organization.setter
    def organization(self, value):
        """Sets the organization the User is a part of.

        This abstracts the process setting the new value in the database. This
        will eventually require additional processes to authorize the moving
        of an account from one organization to another.

        Args:
            value (int): The organization ID of the organization to put the
                user in.

        Returns:
            None:

        Example:
            <todo>
        """
        self.model.organization = value
        self.db_conn.commit()

    @classmethod
    def from_dict(cls, db_conn, kw_dict):
        org = Organization.from_database(db_conn, pkid=kw_dict['organization'])
        if not org:
            print "Failed to get organization with pkid '%s'" % kw_dict['organization']
            raise ValueError
        if org.model.num_members >= org.max_members:
            raise MaxMembersReached(org.max_members)
        # Copied right from ModelWrapper.from_dict
        model_object_inst = cls.model_object()
        cls_inst = cls(db_conn, model_object_inst)
        for i in kw_dict:
            if i in cls_inst.fields:
                setattr(cls_inst, i, kw_dict[i])
        db_conn.add(cls_inst.model)
        db_conn.commit()
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

    def authenticate_token(self, token):
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
            parsed_token = tokenlib.parse_token(token, secret=SECRET_SALT, now=time.time())
        except tokenlib.errors.MalformedTokenError:
            return False
        return parsed_token['id'] == self.get_id() and \
            parsed_token['username'] == self.username and \
            parsed_token['organization'] == self.organization

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
        token_dict = {"id": self.get_id(), "username": self.username, "organization": self.organization}
        token = tokenlib.make_token(token_dict, secret=SECRET_SALT)
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

    @property
    def can_add_users(self):
        """If the organization can add their own users

        This wraps the `canAddUsers` attribute of the associated model.

        Returns:
            bool: True if the organization can add its own users, false if not
        """
        return self.model.can_add_users

    @can_add_users.setter
    def can_add_users(self, value):
        self.model.can_add_users = value
        self.db_conn.commit()

    @property
    def can_delete_users(self):
        """If the organization can delete their own users.

        This wraps the `canDeleteUsers` attribute of the associated model.

        Returns:
            str: True if the organization can delete its own users, false if
                not
        """
        return self.model.can_delete_users

    @can_delete_users.setter
    def can_delete_users(self, value):
        self.model.can_delete_users = value
        self.db_conn.commit()

    @property
    def can_add_competitions(self):
        """If the organization can add their own competitions

        This wraps the `canAddCompetitions` attribute of the associated model.

        Returns:
            bool: True if the organization can add its own competitions, false
                if not
        """
        return self.model.can_add_competitions

    @can_add_competitions.setter
    def can_add_competitions(self, value):
        self.model.can_add_competitions = value
        self.db_conn.commit()

    @property
    def can_delete_competitions(self):
        """If the organization can delete their own competitions.

        This wraps the `can_delete_competitions` attribute of the associated model.

        Returns:
            str: True if the organization can delete its own competitions,
                false if not
        """
        return self.model.can_delete_competitions

    @can_delete_competitions.setter
    def can_delete_competitions(self, value):
        self.model.can_delete_competitions = value
        self.db_conn.commit()

    @property
    def name(self):
        """Name of the organization.

        This wraps the `name` attribute of the associated model.

        Returns:
            str: String containing the name of the Organization object.
        """
        return self.model.name

    @name.setter
    def name(self, value):
        self.model.name = value
        self.db_conn.commit()

    @property
    def url(self):
        """URL value for the organization.

        This wraps the `url` attribute of the associated model.

        Returns:
            str: String containing the url of the Organization object.
        """
        return self.model.url

    @url.setter
    def url(self, value):
        self.model.url = value
        self.db_conn.commit()

    @property
    def description(self):
        """Description of the organization.

        This wraps the `description` attribute of the associated model.

        Returns:
            str: String containing the description of the Organization object.
        """
        return self.model.description

    @description.setter
    def description(self, value):
        self.model.description = value
        self.db_conn.commit()

    @property
    def max_members(self):
        """Mamimum number of members of the organization can have.

        Integer value representing the maximum number of members the
        organization may have.This wraps the `maxMembers` attribute of the
        associated model.

        Returns:
            int:
        """
        return self.model.max_members

    @max_members.setter
    def max_members(self, value):
        self.model.max_members = value
        self.db_conn.commit()

    @property
    def max_competitions(self):
        """Mamimum number of competitions of the organization can have.

        Integer value representing the maximum number of members the
        organization may have.This wraps the `maxCompetitions` attribute of
        the associated model.

        Returns:
            int:
        """
        return self.model.max_competitions

    @max_competitions.setter
    def max_competitions(self, value):
        self.model.max_competitions = value
        self.db_conn.commit()

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
        self.model.num_members = User.count(self.db_conn, organization=self.get_id())
        self.db_conn.commit()

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
