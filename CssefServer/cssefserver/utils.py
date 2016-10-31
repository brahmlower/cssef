import traceback
import logging
import bcrypt

class PasswordHash(object):
    """
    This code pulled from
    http://variable-scope.com/posts/storing-and-verifying-passwords-with-sqlalchemy
    There are a couple minor changes to it, but most credit goes
    Elmer de Looff - Thank you!
    """
    def __init__(self, hash_):
        """Instantiates a PasswordHash object based on a provided string representing a bcrypt hash.

        Args:
            hash_ (str): The hash string to build the object off of.

        Raises:
            Assertion Error: If `hash_` is not of length 60.

            Assertion Error: If `hash_` does not contain three '$'.
        """
        assert len(hash_) == 60, 'bcrypt hash should be 60 chars.'
        assert hash_.count('$'), 'bcrypt hash should have 3x "$".'
        self.hash = str(hash_)
        self.rounds = int(self.hash.split('$')[2])

    def __eq__(self, candidate):
        """Hashes the candidate string and compares it to the stored hash."""
        if isinstance(candidate, basestring):
            if isinstance(candidate, unicode):
                candidate = candidate.encode('utf8')
            return bcrypt.hashpw(candidate, self.hash) == self.hash
        return False

    def __repr__(self):
        """Simple object representation."""
        return self.hash

    @classmethod
    def new(cls, password, rounds):
        """Creates a PasswordHash from the given password."""
        if isinstance(password, unicode):
            password = password.encode('utf8')
        return cls(bcrypt.hashpw(password, bcrypt.gensalt(rounds)))

class EndpointOutput(object):
    def __init__(self, value=0, message='', content=None):
        self.value = value
        self.message = message
        # Cast the content to a list
        if not content:
            self.content = []
        elif isinstance(content, list):
            self.content = content
        elif isinstance(content, str):
            self.content = [content]
        else:
            raise ValueError("Content must be None, list or string. Got %s instead." % content.__class__.__name__)

    @classmethod
    def from_traceback(cls):
        value = 1
        message = traceback.format_exc()
        instance = cls(value, message)
        instance.log()
        return instance

    def log(self):
        # Check if this was an unexpected error (ID = 1)
        if self.value == 1:
            log_message = "(error {}): Encountered runtime error with given ID {}. Observe the following stack trace:".format(self.value, self.value)
            logging.warning(log_message)
            for i in self.message.splitlines():
                logging.warning("(error {}): {}".format(self.value, i))

    def as_dict(self):
        temp_dict = {}
        temp_dict['value'] = self.value
        temp_dict['message'] = self.message
        temp_dict['content'] = self.content
        return temp_dict
