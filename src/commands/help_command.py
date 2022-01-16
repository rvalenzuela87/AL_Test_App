from .command import Command


class HelpCommand(Command):
	def __init__(self, receiver, *args, **kwargs):
		super(HelpCommand, self).__init__(receiver, *args, **kwargs)

		self.params_names = ["command"]
		self.params_short_names = ["cmd"]

	def help(self):
		print("Help for Help command")

	def execute(self):
		pass