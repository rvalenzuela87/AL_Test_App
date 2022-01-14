from commands.command import Command

CLASS_NAME = "ListCommand"


class ListCommand(Command):
	def __init__(self, receiver, *args, **kwargs):
		super(ListCommand, self).__init__(receiver, *args, **kwargs)

		self.params_long_names = ["filter"]
		self.params_short_names = ["f"]

		if len(kwargs) == 0 and len(args) == 0:
			# Enter prompt mode
			self.prompt()
			self.execute()
		else:
			params_values = dict.fromkeys(self.params_long_names)

			for ln, sn in zip(self.params_long_names, self.params_short_names):
				# Assume the kwargs dictionary has a key  equal to the parameter's long or short name
				try:
					params_values[ln] = kwargs[ln]
				except KeyError:
					try:
						params_values[ln] = kwargs[sn]
					except KeyError:
						params_values[ln] = None


	def help(self):
		return "Help for List command"

	def set_params(self, *args, **kwargs):
		super(ListCommand, self).set_params(*args, **kwargs)

		# Validate values set
		return self

	def prompt(self):
		print("List Prompt Mode")

		while True:
			display_all = input("Display all records?(Y\\N):")

			if display_all.lower() in ["n", "no"]:
				# Ask for the filter parameters
				for ln in self.params_long_names:
					self.params_values.append(input("%s:" % ln.capitalize()))

				print("ListCommand >> Params complete")
				break
			elif display_all.lower() in ["y", "yes"]:
				self.params_values.append("*")
				print(">> About to display all records...")
				break

	def execute(self):
		try:
			assert len(self.params_values) == len(self.params_long_names)
		except AssertionError:
			raise RuntimeError("Arguments missing for command list")
		else:
			print(">> Records displayed")
