from .command import Command


CLASS_NAME = "AddCommand"
CMD_NAME = "add"
CMD_SHRT_NAME = "a"


class AddCommand(Command):
	def __init__(self, receiver, *args, **kwargs):
		super(AddCommand, self).__init__(receiver, *args, **kwargs)

		self.params_names = ["name", "lastname", "address", "city", "phone"]
		self.params_short_names = ["n", "ln", "ad", "c", "ph"]

		try:
			self.set_params(*args, **kwargs)
		except RuntimeError as exc:
			self.prompt()

	@staticmethod
	def help():
		help_msg = """
		The \"add (a)\" command provides a way of creating new records. It takes 5 arguments: name, last name, 
		address, city and phone. All of these arguments must be provided in order to create the new record.
		In case some or none of the required arguments are provided, a prompt operation will be triggered
		to ask for these values.
		
		The arguments can be provided as positional arguments as such:
		
			add 'John' 'Doe' '10 Mulholland Drv' 'Hollywood' '66254789'
		
		Notice how the arguments are written in the order they were stated in the last paragraph. This is important
		when passing arguments as positional.
		
		Another way of providing arguments for the add command is by using keywords, as such:
		
			add -name 'John' -lastname 'Doe' -address '10 Mullholland Drv' -city 'Hollywood' -phone '66254789'
			
		When using keyword arguments, the order in which they appear is not important.
		
		The keywords, as well as the command, have long and short forms. Next, a list with the command's keywords
		in both forms is provided:
		
			name (n)
			lastname (ln)
		    address (ad)
			city (c)
			phone (ph)
		"""
		return help_msg

	def execute(self):
		try:
			self.receiver.add_record([self.params_args[k] for k in self.params_names])
		except AttributeError:
			if self.receiver:
				# The receiver set has no method named records. Therefore, it is not compatible with this command
				raise RuntimeError(
					"The object set as receiver has no \'records\' method, therefore, it is incompatible "
					"with the \'add\' command"
				)
			else:
				raise RuntimeError(
					"No receiver set prior to executing the \'add\' command"
				)

		print("\n[i] New record added: {}\n".format(self.params_args))
