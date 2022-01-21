import unittest
import os
import re as regexp

#from ..src import commands
from AL_Test_App.src.commands.utils import commands_utils


class LoadCommandModuleTestCase(unittest.TestCase):
	commands_names = None
	COMMANDS_MODS_PATTERN = regexp.compile(r'^(?:.*)commands\.([a-zA-Z]+_command)$')
	CMD_FILE_PATTERN = regexp.compile(r'^([a-zA-Z0-9]+)_command.py$')

	def setUp(self) -> None:
		# Read the commands package's files that represent a command module
		commands_dir_files = os.listdir(os.path.join(os.path.dirname(os.path.dirname(__file__)), "src", "commands"))
		pattern = self.CMD_FILE_PATTERN

		self.commands_names = [m.groups()[0] for m in (pattern.match(fn) for fn in commands_dir_files) if m]


	def test_all_command_modules_files_discoverable(self):
		"""
		Tests that all files inside the 'commands' package which match the expected pattern are discovered by the
		'get_commands_names' functions inside 'commands_utils'
		"""

		cmds_names, __ = commands_utils.get_commands_names()

		self.assertEqual(
			len(cmds_names), len(self.commands_names),
			"The number of discovered commands via the function get_commands_names is not the same as "
			"the files within the 'commands' package which match the expected "
			"form: {} vs {}".format(len(cmds_names), len(self.commands_names))
		)


	def test_all_command_modules_loaded(self):
		"""
		Test that makes sure all command modules are loaded once the commands package has been imported
		"""

		loaded_mods = []
		command_mods_not_loaded = []

		for cmd_name in self.commands_names:
			try:
				loaded_mods.append(commands_utils.load_command_module(cmd_name))
			except RuntimeError:
				command_mods_not_loaded.append(cmd_name)

		self.assertEqual(
			len(loaded_mods), len(self.commands_names),
			"Some command modules were not loaded: {}".format(command_mods_not_loaded)
		)

	def test_command_modules_have_class_name(self):
		"""
		Makes sure every command module has a public constant named CLASS_NAME which contains the name (str) of the
		command class
		"""

		loaded_mods = [commands_utils.load_command_module(cmd_name) for cmd_name in commands_utils.get_commands_names()[0]]
		no_class_name_found = []

		for mod in loaded_mods:
			try:
				assert mod.CLASS_NAME is not None
			except(AttributeError, RuntimeError, AssertionError):
				no_class_name_found.append(mod.__name__)

		self.assertEqual(
			len(no_class_name_found), 0,
			"No CLASS_NAME constant found in the following modules: {}".format(",".join(no_class_name_found))
		)

	def test_command_modules_class_name_as_expected(self):
		"""
		Makes sure the CLASS_NAME constant in each command module has the expected value given the module's name
		"""

		loaded_mods = [commands_utils.load_command_module(cmd_name) for cmd_name in commands_utils.get_commands_names()[0]]

		for cmd_mod in loaded_mods:
			try:
				class_name = cmd_mod.CLASS_NAME
			except AttributeError:
				# The command module doesn't have a CLASS_NAME public constant. Therefore, ignore it and move on
				# to the next module in the list
				continue

			try:
				mod_name = self.COMMANDS_MODS_PATTERN.match(cmd_mod.__name__).groups()[0]
			except(AttributeError, IndexError):
				# The command module's name doesn't comply with the expected name. Therefore, ignore it and move
				# on to the next module in the list
				continue
			else:
				cmd_name, suffix = mod_name.split("_")
				exp_class_name = "".join([cmd_name.capitalize(), suffix.capitalize()])

				self.assertEqual(
					class_name, exp_class_name,
					"Expected \"{}\" as the module {}'s CLASS_NAME constant. Got \"{}\", "
					"instead".format(exp_class_name, cmd_mod, class_name)
				)

	def test_command_modules_have_cmd_name(self):
		"""
		Makes sure every command module has a public constant named CMD_NAME which contains the string by which the
		command can be invoked
		"""

		loaded_mods = [commands_utils.load_command_module(cmd_name) for cmd_name in commands_utils.get_commands_names()[0]]
		no_cmd_name_found = []

		for mod in loaded_mods:
			try:
				assert mod.CMD_NAME is not None
			except(AttributeError, RuntimeError, Exception):
				no_cmd_name_found.append(mod.__name__)

		self.assertEqual(
			len(no_cmd_name_found), 0,
			"No CMD_NAME constant found in the following modules: {}".format(",".join(no_cmd_name_found))
		)

	def test_command_modules_have_cmd_short_name(self):
		"""
		Makes sure every command module has a public constant named CMD_SHORT_NAME which contains the alternative
		string by which the command can be invoked
		"""

		command_modules = [commands_utils.load_command_module(cmd_name) for cmd_name in commands_utils.get_commands_names()[0]]
		no_cmd_short_name_found = []

		for mod in command_modules:
			try:
				assert mod.CMD_SHRT_NAME is not None
			except(AttributeError, RuntimeError, Exception):
				no_cmd_short_name_found.append(mod.__name__)

		self.assertEqual(
			len(no_cmd_short_name_found), 0,
			"No CMD_SHORT_NAME constant found in the following modules: {}".format(",".join(no_cmd_short_name_found))
		)
