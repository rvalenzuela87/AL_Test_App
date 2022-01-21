from .command import Command

CLASS_NAME = "ListCommand"
CMD_NAME = "list"
CMD_SHRT_NAME = "l"


class ListCommand(Command):
	def __init__(self, receiver, *args, **kwargs):
		super(ListCommand, self).__init__(receiver, *args, **kwargs)

		try:
			self.params_names = kwargs.keys()
		except AttributeError:
			self.params_names = []

		self.params_short_names = [n for n in self.params_names]
		self.params_args = dict.fromkeys(self.params_names)

		for k in self.params_names:
			self.params_args[k] = kwargs[k]

	@staticmethod
	def help():
		help_msg = """
		The \"list (l)\" command offers a way of listing the records stored in memory. The list can be filtered or
		displayed in its entirety.
		
		This command supports the following arguments: name, lastname, city, address and phone. These arguments
		are shared with the \"add\" command, as well. If one of those arguments is specifed at calling time, the
		list displayed will be filtered accordingly.
		
		For instance, to display all records with names starting with 'J', one could do the following:
			
			list -name 'J*'
		
		Or in shor form:
			
			list -n 'J*'
			
		Next, a list with the command's keywords
		in both forms is provided:
		
			name (n)
			lastname (ln)
		    address (ad)
			city (c)
			phone (ph)
		"""

		return help_msg

	def prompt(self, missing_only=True):
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
		# Format the records for printing in the command line
		try:
			filter = self.params_args["filter"]

			assert len(filter) > 0
		except(TypeError, KeyError, AssertionError):
			# No filter was set. Then, use the 'all' option
			filter = "*"

		if len(self.params_args.keys()) == 0:
			print("[i] Listing all records\n")
			filter = "*"
		else:
			print(
				"[i] Listing all records matching {}\n".format(["=".join([k, self.params_args[k]]) for k in self.params_args.keys()])
			)

		try:
			records = self.receiver.filter_records(**self.params_args)
		except AttributeError:
			if self.receiver:
				# The receiver set has no method named records. Therefore, it is not compatible with this command
				raise RuntimeError(
					"The object set as receiver has no \'records\' method, therefore, it is incompatible "
					"with the \'list\' command"
				)
			else:
				raise RuntimeError(
					"No receiver set prior to executing the \'list\' command"
				)

		print("\n".join(" - ".join(row) for row in records))
		print("\n----- End -----\n")
