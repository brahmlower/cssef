from django.template import RequestContext

class BaseContext(object):
	def __init__(self, request):
		self.debug = True
		self.returnValue = 0
		self.errors = []
		self.apiData = None
		self.request = request
		self.context = RequestContext(self.request)
		self.httpMethodActions = {}

	def isValid(self):
		return self.returnValue == 0

	def processContext(self):
		try:
			return self.httpMethodActions[self.request.method]()
		except KeyError:
			# the http method isn't supported by the context processor
			return None

	def translateApiReturn(self, output):
		self.returnValue = output['value']
		if type(output['message']) == list:
			self.errors = "\n".join(output['message'])
		else:
			self.errors = output['message']
		self.apiData = output['content']

	def getContext(self):
		print 'utils.getContext - start'
		self.context.push({'debug': self.debug})
		self.context.push({'returnValue': self.returnValue})
		self.context.push({'errors': self.errors})
		self.context.push({'apiData': self.apiData})
		print 'utils.getContext - end'
		return self.context

class FormContext(BaseContext):
	CREATE = 'create'
	EDIT = 'edit'
	def __init__(self, request):
		super(FormContext, self).__init__(request)
		self.debug = True
		self.formData = None
		self.form = None

	def validateFormData(self, **kwargs):
		formData = self.form(self.request.POST, **kwargs)
		self.errors = formData.errors
		if self.errors:
			self.returnValue = 1
			self.form = self.form(initial = self.request.POST, **kwargs)
		self.formData = formData.cleaned_data
		return self.isValid()

	def getContext(self):
		super(FormContext, self).getContext()
		self.context.push({'action': self.action})
		self.context.push({'form': self.form})
		return self.context