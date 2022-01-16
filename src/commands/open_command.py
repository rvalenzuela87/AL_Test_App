from .command import Command

CLASS_NAME = "OpenCommand"


class OpenCommand(Command):
	def __init__(self, receiver, *args, **kwargs):
		super(OpenCommand, self).__init__(receiver, *args, **kwargs)

		self.params_names = ["filename"]
		self.params_short_names = ["n"]

		try:
			self.set_params(*args, **kwargs)
		except RuntimeError:
			print("Missing parameters values")
			self.prompt()

		self.execute()

	def help(self):
		return "Help for Open command"

	def execute(self):
		print("Opening file %s" % self.params_args["filename"])
