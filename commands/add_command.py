from commands.command import Command


class AddCommand(Command):
	def __init__(self, receiver, *args, **kwargs):
		super(AddCommand, self).__init__(receiver, *args, **kwargs)

		try:
			self.set_params(*args, *kwargs)
		except RuntimeError:
			print("Missing parameters values")
			self.prompt()
		else:
			self.execute()

	def help(self):
		return "Help for the Add command"

	def execute(self):
		print(">> Adding new record")
