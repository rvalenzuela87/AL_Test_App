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

		self.execute()

	@staticmethod
	def help():
		return "Help for Add command"

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
