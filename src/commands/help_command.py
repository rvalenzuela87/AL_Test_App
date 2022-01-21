from .command import Command
from .command_builder import CommandBuilder

CLASS_NAME = "HelpCommand"
CMD_NAME = "help"
CMD_SHRT_NAME = "h"


class HelpCommand(Command):
	def __init__(self, receiver, *args, **kwargs):
		super(HelpCommand, self).__init__(receiver, *args, **kwargs)

		self._cmd_builder = CommandBuilder()
		self.params_names = ["command"]
		self.params_short_names = ["cmd"]

		try:
			self.set_params(*args, **kwargs)
		except RuntimeError:
			pass

	@staticmethod
	def help():
		return "To access help for a specific command, simply provide the command's full name as argument for" \
		       "the help command, as such:\n\n\thelp 'command'\n\nSimply replace command by the desired " \
		       "command's full name."

	def execute(self):
		try:
			cmd_name = self.params_args["command"]
		except(TypeError, KeyError):
			print(self.help())
		else:
			try:
				cmd_mod = self._cmd_builder.get_command_module(cmd_name)
				print(cmd_mod.__getattribute__(cmd_mod.CLASS_NAME).help())
				print("\n")
			except RuntimeError:
				print("[i] No help found for command \'{}\'\n".format(cmd_name))
