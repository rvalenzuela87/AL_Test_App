import os
import unittest

from AL_Test_App.src.utils import config_utils


class GetConfigTestCase(unittest.TestCase):
	def test_config_file_is_readable(self):
		"""
		Tests whether the configuration file (config.json) is accessible by calling the 'get_conf' funtion in the
		config_utils module
		"""

		try:
			config_utils.get_conf()
		except RuntimeError as exc:
			self.fail("The configuration file config.json is not accesible: {}".format(exc))

	def test_config_loaded_to_memory(self):
		"""
		Tests whether the configuration options are loaded to environment variables after a call to the
		'reload_config' function in the config_utils module
		"""

		config_utils.reload_config()

		env_keys = [
			"DEFAULT_SAVE_DIRECTORY", "DEFAULT_EXPORT_DIRECTORY", "SERIAL_TYPES", "EXPORT_TYPES"
		]

		for k in env_keys:
			try:
				os.environ[k]
			except KeyError:
				self.fail(
					"No environment variable set for \'{}\' after a call to the function reload_config.".format(k)
				)

	def test_get_serialization_types(self):
		"""
		Makes sure the supported serialization types are accessible by calling the 'get_serial_types' function in
		the config_utils module
		"""

		try:
			serial_types = config_utils.get_serial_types()
		except RuntimeError as exc:
			self.fail("Unable to read the app\'s supported serialization types: {}".format(exc))

		self.assertEqual(
			type(serial_types), list,
			"Expected the value returned by the function get_serial_types to be of type \'list\'. "
			"Got type \'{}\', instead".format(type(serial_types).__name__)
		)

	def test_get_serializers_directory(self):
		"""
		Tests whether the directory where the backup files are to be stored is accessible by calling the
		'get_serializers_dir' function in the config_utils module
		"""

		try:
			serial_dir = config_utils.get_serializers_dir(abs=True)
		except RuntimeError as exc:
			self.fail("Unable to read the app\'s serializers directory: {}".format(exc))

		self.assertTrue(
			type(serial_dir) in [str, 'unicode'],
			"Expected the value returned by the function get_serial_types to be of type \'list\'. "
			"Got type \'{}\', instead".format(type(serial_dir).__name__)
		)
