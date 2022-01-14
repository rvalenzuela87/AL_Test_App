class Command(object):
	params_long_names = None
	params_short_names = None
	params_values = None

	def __init__(self, receiver, *args, **kwargs):
		super(Command, self).__init__()
		self._receiver = receiver

		self.params_long_names = []
		self.params_short_names = []
		self.params_values = []

	def help(self):
		pass

	def prompt(self):
		pass

	def params(self):
		return zip(self.params_long_names, self.params_short_names, self.params_values)

	def param_short_name(self, param):
		try:
			return self.params_short_names[self.params_long_names.index(param)]
		except IndexError:
			if type(param) is str:
				raise RuntimeError("Command doesn't support parameter with name \"{}\"".format(param))
			else:
				raise TypeError(
					"Wrong type received as parameter name. Expected a string value. "
					"Got {}, instead.".format(type(param).__name__)
				)

	def set_params(self, *args, **kwargs):
		try:
			# Assume the args list contains all the necessary values for each of the command's parameters
			assert len(args) == len(self.params_long_names)
		except AssertionError:
			# Assume the kwargs dictionary contains all the necessary values for the command's parameters.
			# The order of the parameters' values list has to follow the order of the parameters long names or
			# short names lists
			for ln, sn in zip(self.params_long_names, self.params_short_names):
				try:
					self.params_values.append(kwargs[ln])
				except KeyError:
					try:
						self.params_values.append(kwargs[sn])
					except KeyError:
						# If one parameter is missing, then reset the values list and raise an exception
						self.params_values = []
						raise RuntimeError("No value received for parameter {}({})".format(ln, sn))
		else:
			self.params_values = [v for v in args]

		return self

	def execute(self):
		pass
