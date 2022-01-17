from .command import Command

CLASS_NAME = "DeleteCommand"


class DeleteCommand(Command):
	def __init__(self, receiver, *args, **kwargs):
		super(DeleteCommand, self).__init__(receiver, *args, **kwargs)

		self.params_names = ["index"]
		self.params_short_names = ["index"]

		self.set_params(*args, **kwargs)
		self.execute()

	@staticmethod
	def help():
		return "Help for delete command"

	def execute(self):
		try:
			index_value = self.params_args["index"]
		except(TypeError, KeyError):
			raise RuntimeError(
				"No value set for the \'index\' parameter"
			)

		try:
			self.receiver.delete_record(int(index_value))
		except KeyError:
			raise RuntimeError("No record index specified")
		except AttributeError:
			if self.receiver:
				# The receiver set has no method named records. Therefore, it is not compatible with this command
				raise RuntimeError(
					"The object set as receiver has no \'delete_record\' method, therefore, it is incompatible "
					"with the \'delete\' command"
				)
			else:
				raise RuntimeError(
					"No receiver set prior to executing the \'delete\' command"
				)

		print("[i] Record with index {}, deleted\n".format(self.params_args["index"]))