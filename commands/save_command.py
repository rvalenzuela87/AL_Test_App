from commands.command import Command

CLASS_NAME = "SaveCommand"


class SaveCommand(Command):
	def __init__(self, receiver, *args, **kwargs):
		super(SaveCommand, self).__init__(receiver, *args, **kwargs)

		self.params_long_names = ["filename"]
		self.params_short_names = ["n"]

		try:
			self.set_params(*args, **kwargs)
		except RuntimeError:
			print("Missing parameters values")
			self.prompt()
			self.execute()
		else:
			self.execute()

	def help(self):
		return "Help for Save command"

	def execute(self):
		print("Saving file %s" % self.params_values[0])
