import re as regexp

from .utils import commands_utils


class CommandBuilder(object):
	CMD_FILE_PATTERN = regexp.compile(r'^([a-zA-Z0-9]*)_command\.py$')

	def __init__(self):
		super(CommandBuilder, self).__init__()

	@staticmethod
	def get_command_module(command_name):
		return commands_utils.load_command_module(command_name)

	@classmethod
	def get_command(cls, command_name, receiver, *args, **kwargs):
		# Look for the command's module
		cmd_mod = cls.get_command_module(command_name)

		# Return an instance of the command initialized with its receiver and positional and keywords arguments
		return cmd_mod.__getattribute__(cmd_mod.CLASS_NAME)(receiver, *args, **kwargs)
