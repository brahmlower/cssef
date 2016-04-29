class CssefException(Exception):
    value = None
    message = None
    def as_return_dict(self):
        return {'value': self.value, 'message': self.message, 'content': []}

class NonExistantCommand(CssefException):
    value = -5
    message = ["Invalid command."]