class Command(object):
	params_names = None
	params_short_names = None
	params_args = None

	def __init__(self, receiver, *args, **kwargs):
		super(Command, self).__init__()
		self._receiver = receiver

		self.params_names = []
		self.params_short_names = []
		self.params_args = None

	def help(self):
		pass

	def params(self):
		return zip(self.params_names, self.params_short_names)

	def param_short_name(self, param):
		try:
			return self.params_short_names[self.params_names.index(param)]
		except IndexError:
			if type(param) is str:
				raise RuntimeError("Command doesn't support parameter with name \"{}\"".format(param))
			else:
				raise TypeError(
					"Wrong type received as parameter name. Expected a string value. "
					"Got {}, instead.".format(type(param).__name__)
				)

	def set_params(self, *args, **kwargs):
		# Makes sure the arguments received are all either positional or keyword arguments. Mixing the two is not
		# supported. An exception is raised if this condition is not met
		try:
			assert (len(args) == 0 and len(kwargs) > 0) or (len(args) > 0 and len(kwargs) == 0)
		except AssertionError:
			# The method received a mix of positional and keyword arguments. This is not supported to avoid
			# confusion and to simplify the logic in the code.
			raise RuntimeError(
				"Mixing positional and keyword arguments is not supported. Please, refer to the command\'s help"
				"for more information on how the arguments should be delivered to the command."
			)

		try:
			assert len(args) > 0
		except AssertionError:
			# Assume the keyword arguments dictionary contains as many values as the number of necessary parameters
			# for the command.
			self.params_args = {}
			missing_args = []

			for ln, sn in zip(self.params_names, self.params_short_names):
				try:
					self.params_args[ln] = kwargs[ln]
				except KeyError:
					try:
						self.params_args[ln] = kwargs[sn]
					except KeyError:
						# If one parameter is missing, then continue with the rest of the arguments
						continue
		else:
			# Assume the positional arguments list contains as many values as the number of necessary parameters
			# for the command
			self.params_args = dict(zip(self.params_names, args))

		try:
			# If all the necessary arguments were received by this method, then the dictionary created above
			# has to have as many keys as the number of parameters for the command
			assert len(self.params_args.keys()) == len(self.params_names)
		except AssertionError:
			# Some arguments are missing. Therefore, the command has to ask the user to provide the
			# missing arguments
			self.prompt(missing_only=True)

		return self

	def prompt(self, missing_only=False):
		if not missing_only:
			# The inner arguments dictionary has to be reset first and then populate it with the user inputs
			self.params_args = dict.fromkeys(self.params_names)
			missing_arguments = self.params_args.keys()
		else:
			# Find the arguments which have been set, already
			try:
				current_arguments = self.params_args.keys()
			except AttributeError:
				# The inner arguments dictionary is None. This means no arguments have been set at this point.
				# Therefore, the method will have to ask for all of them
				self.params_args = dict.fromkeys(self.params_names)
				missing_arguments = self.params_args.keys()
			else:
				# Extract the arguments missing
				missing_arguments = set(self.params_names).difference(current_arguments)

		for ln in missing_arguments:
			self.params_args[ln] = input("%s:" % ln.capitalize())

		return self

	def execute(self):
		pass
