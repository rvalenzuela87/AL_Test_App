import unittest
import pkgutil
import sys
import re as regexp

from ..src import commands


class LoadCommandModuleTestCase(unittest.TestCase):
	command_modules = None
	COMMANDS_MODS_PATTERN = regexp.compile(r'^(?:.*)commands\.([a-zA-Z]+_command)$')

	def setUp(self) -> None:
		# Read the commands package's files that represent a command module
		commands_dir_files = [name for __, name, __ in pkgutil.iter_modules(commands.__path__)]
		pattern = regexp.compile(r'^([a-zA-Z]+_command)$')

		self.command_modules = [m.groups()[0] for m in (pattern.match(fn) for fn in commands_dir_files) if m]

	def test_all_command_modules_loaded(self):
		"""
		Test that makes sure all command modules are loaded once the commands package has been imported
		"""

		loaded_mods = [m.groups()[0] for m in (self.COMMANDS_MODS_PATTERN.match(k) for k in sys.modules.keys()) if m]
		command_mods_not_loaded = list(set(loaded_mods).difference(self.command_modules))

		self.assertEqual(
			len(command_mods_not_loaded), 0, "Some command modules were not loaded: {}".format(command_mods_not_loaded)
		)

	def test_command_modules_have_class_name(self):
		"""
		Makes sure every command module has a public constant named CLASS_NAME which contains the name (str) of the
		command class
		"""

		loaded_mods = [sys.modules[k] for k in sys.modules.keys() if self.COMMANDS_MODS_PATTERN.match(k)]
		no_class_name_found = []

		for mod in loaded_mods:
			try:
				assert mod.CLASS_NAME is not None
			except(AttributeError, RuntimeError, Exception):
				no_class_name_found.append(mod.__name__)

		self.assertEqual(
			len(no_class_name_found), 0,
			"No CLASS_NAME constant found in the following modules: {}".format(",".join(no_class_name_found))
		)

	def test_command_modules_class_name_as_expected(self):
		"""
		Makes sure the CLASS_NAME constant in each command module has the expected value given the module's name
		"""

		loaded_mods_keys = sys.modules.keys()
		loaded_command_mods = [k for k in loaded_mods_keys if self.COMMANDS_MODS_PATTERN.match(k)]

		for mod_key in loaded_command_mods:
			try:
				class_name = sys.modules[mod_key].CLASS_NAME
			except AttributeError:
				continue

			try:
				mod_name = self.COMMANDS_MODS_PATTERN.match(mod_key).groups()[0]
			except(AttributeError, IndexError):
				continue
			else:
				cmd_name, suffix = mod_name.split("_")
				exp_class_name = "".join([cmd_name.capitalize(), suffix.capitalize()])

				self.assertEqual(
					class_name, exp_class_name,
					"Expected \"{}\" as the module {}'s CLASS_NAME constant. Got \"{}\", "
					"instead".format(exp_class_name, mod_key, class_name)
				)
