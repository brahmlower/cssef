from django.forms import Form
from django.template import RequestContext

class BaseContext(object):
	def __init__(self, request):
		self.api_calls = []
		self.forms = {}
		self.debug = True
		self.debug_error_count = 0
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
		self.api_calls.append(output)
		self.returnValue = output['value']
		if type(output['message']) == list:
			self.errors = "\n".join(output['message'])
		else:
			self.errors = output['message']
		self.apiData = output['content']

	def getContext(self):
		for i in self.api_calls:
			if i['value'] != 0:
				self.debug_error_count += 1
		#print 'utils.getContext - start'
		self.context.push({'debug': self.debug})
		self.context.push({'debug_error_count': self.debug_error_count})
		self.context.push({'api_calls': self.api_calls})
		self.context.push({'forms': self.forms})
		self.context.push({'apiData': self.apiData})
		#print 'utils.getContext - end'
		return self.context

class FormContext(BaseContext):
	CREATE = 'create'
	DELETE = 'delete'
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
		# All things considered, this is not a great way to solve this issue, since an inconsistent
		# state of self.form is bad and makes stack tracing more confusing. Just another item for the
		# todo list...
		if isinstance(self.form, Form):
			self.context.push({'form': self.form})
		else:
			self.context.push({'form': self.form()})
		return self.context