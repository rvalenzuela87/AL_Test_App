from .command import Command
from AL_Test_App.src.utils import commands_utils

CLASS_NAME = "HelpCommand"


class HelpCommand(Command):
	def __init__(self, receiver, *args, **kwargs):
		super(HelpCommand, self).__init__(receiver, *args, **kwargs)

		self.params_names = ["command"]
		self.params_short_names = ["cmd"]

		try:
			self.set_params(*args, **kwargs)
		except RuntimeError:
			pass

		self.execute()

	@staticmethod
	def help():
		return "Help for Help command"

	def execute(self):
		try:
			cmd_name = self.params_args["command"]
		except(TypeError, KeyError):
			print(self.help())
		else:
			cmds_long_names, cmds_short_names = commands_utils.get_commands_names()

			for ln, sn in zip(cmds_long_names, cmds_short_names):
				if cmd_name == sn:
					cmd_name = ln
				elif not cmd_name == ln:
					continue

				cmd_mod = commands_utils.load_command_module(cmd_name)
				print(cmd_mod.__getattribute__(cmd_mod.CLASS_NAME).help())
				print("\n")
				break
			else:
				print("[i] No help found for command \'{}\'\n".format(cmd_name))
