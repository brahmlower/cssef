import traceback
from systemd import journal
from cssefserver import errors

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
            log_message = "(error %d): Encountered runtime error with given ID %d. Observe the following stack trace:" % (self.value, self.value)
            journal.send(message=log_message) #pylint: disable=no-member 
            for i in self.message.splitlines():
                journal.send(message="(error %d): %s" % (self.value, i)) #pylint: disable=no-member 

    def as_dict(self):
        temp_dict = {}
        temp_dict['value'] = self.value
        temp_dict['message'] = self.message
        temp_dict['content'] = self.content
        return temp_dict

