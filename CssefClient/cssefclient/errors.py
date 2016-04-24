class CssefException(Exception):
	value = None
	message = None
	def asReturnDict(self):
		return {'value': self.value, 'message': self.message, 'content': []}

class NonExistantCommand(CssefException):
	value = -5
	message = ["Invalid command."]