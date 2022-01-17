from .command import Command

CLASS_NAME = "NewCommand"


class NewCommand(Command):
	def __init__(self, receiver, *args, **kwargs):
		super(NewCommand, self).__init__(receiver, *args, **kwargs)

		self.params_names = []
		self.params_short_names = []

		self.execute()

	@staticmethod
	def help():
		return "Help for the New command"

	def set_params(self, *args, **kwargs):
		pass

	def execute(self):
		while True:
			choice = input("About to empty the current records list. Continue?\n(y/n):")

			if choice.lower() not in ["y", "n", "yes", "no"]:
				print("\n[E] Please choose \'y\' for \'yes\' and \'n\' for \'no\', only\n")
			else:
				break

		if choice.lower() in ["n", "no"]:
			print("\n[i] Operation aborted. The current list remains intact\n")
		else:
			try:
				self.receiver.reset()
			except AttributeError:
				if self.receiver:
					# The receiver set has no method named empty_records. Therefore, it is not compatible with
					# this command
					raise RuntimeError(
						"The object set as receiver has no \'reset\' method, therefore, it is incompatible "
						"with the \'new\' command"
					)
				else:
					raise RuntimeError(
						"No receiver set prior to executing the \'new\' command"
					)

			print("\n[i] List of records emptied\n")