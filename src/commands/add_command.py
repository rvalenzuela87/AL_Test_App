from .command import Command


CLASS_NAME = "AddCommand"


class AddCommand(Command):
	def __init__(self, receiver, *args, **kwargs):
		super(AddCommand, self).__init__(receiver, *args, **kwargs)

		self.params_long_names = ["name", "lastname", "address", "city", "phone"]
		self.params_short_names = ["n", "ln", "ad", "c", "ph"]

		try:
			self.set_params(*args, **kwargs)
		except RuntimeError:
			print("Missing parameters values")
			self.prompt()
			self.execute()
		else:
			self.execute()

	def help(self):
		return "Help for Add command"

	def execute(self):
		print(">> Adding new record: {}".format(self.params_args))
