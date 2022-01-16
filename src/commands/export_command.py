from .command import Command

CLASS_NAME = "ExportCommand"


class ExportCommand(Command):
	def __init__(self, receiver, *args, **kwargs):
		super(ExportCommand, self).__init__(receiver, *args, **kwargs)

		self.params_names = ["filename"]
		self.params_short_names = ["n"]

		try:
			self.set_params(*args, **kwargs)
		except RuntimeError:
			print("Missing parameters values")
			self.prompt()

		self.execute()

	def help(self):
		return "Help for Export command"

	def execute(self):
		print("Exporting data to file %s" % self.params_args["filename"])
