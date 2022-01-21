from .command import Command

CLASS_NAME = "DeleteCommand"
CMD_NAME = "delete"
CMD_SHRT_NAME = "d"


class DeleteCommand(Command):
	def __init__(self, receiver, *args, **kwargs):
		super(DeleteCommand, self).__init__(receiver, *args, **kwargs)

		self.params_names = ["index"]
		self.params_short_names = ["index"]

		self.set_params(*args, **kwargs)

	@staticmethod
	def help():
		help_msg = """
		The \"delete (d)\" command provides a way of deleting records. It takes one argument: index. In case no
		argument is provided at calling time, a prompt operation will be triggered asking for the index of the
		row that is to be deleted.
		
		The argument can be provided as positional, as such:
			
			delete '4'
		
		Or as keyword argument, as such:
		
			delete -index '4'
		
		And in short form, as such:
		
			delete -i '4'
		"""
		return help_msg

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

		print("\n[i] Record with index {}, deleted\n".format(self.params_args["index"]))