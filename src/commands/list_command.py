from .command import Command

CLASS_NAME = "ListCommand"


class ListCommand(Command):
	def __init__(self, receiver, *args, **kwargs):
		super(ListCommand, self).__init__(receiver, *args, **kwargs)

		self.params_names = ["filter"]
		self.params_short_names = ["f"]

		if len(kwargs) == 0 and len(args) == 0:
			# Enter prompt mode
			self.prompt()
		else:
			self.set_params(*args, **kwargs)

		self.execute()

	def help(self):
		return "Help for List command"

	def prompt(self, missing_only=True):
		print("List Prompt Mode")

		while True:
			display_all = input("Display all records?(Y\\N):")

			if display_all.lower() in ["n", "no"]:
				# Ask for the filter parameters
				super(ListCommand, self).prompt(missing_only=False)
				print("ListCommand >> Params complete")
				break
			elif display_all.lower() in ["y", "yes"]:
				self.params_args = dict(zip(self.params_names, ["*"]))
				print(">> Set to display all records...")
				break
			else:
				# The user entered a non supported option. Therefore, continue with the loop
				print("Error: Option \'%s\' is not supported. Please, choose (y)es or (n)o, only.")
				continue

	def execute(self):
		try:
			assert len(self.params_args) == len(self.params_names)
		except AssertionError:
			raise RuntimeError("Arguments missing for command list")
		else:
			print(">> Records displayed")
