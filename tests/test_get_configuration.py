import os
import unittest

from ..src.utils import config_utils


class GetConfigTestCase(unittest.TestCase):
	def test_config_file_is_readable(self):
		try:
			config_utils.get_conf()
		except RuntimeError as exc:
			self.fail("The configuration file config.json is not accesible: {}".format(exc))

	def test_config_loaded_to_memory(self):
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
		try:
			serial_dir = config_utils.get_serializers_dir(abs=True)
		except RuntimeError as exc:
			self.fail("Unable to read the app\'s serializers directory: {}".format(exc))

		self.assertTrue(
			type(serial_dir) in [str, 'unicode'],
			"Expected the value returned by the function get_serial_types to be of type \'list\'. "
			"Got type \'{}\', instead".format(type(serial_dir).__name__)
		)

	def test_get_serializer_modules(self):
		serial_types = config_utils.get_serial_types()

		for st in serial_types:
			try:
				serial_module = config_utils.get_serializer_module(st)
			except RuntimeError as exc:
				self.fail("Unable to load or find module for serialization type \'{}\': {}".format(st, exc))
			else:
				self.assertTrue(
					type(serial_module).__name__ == "module",
					"A call to the function get_serializer_modules is expected to return a module. "
					"Got type \'{}\', instead".format(type(serial_module).__name__)
				)

	def test_get_exporters_modules(self):
		exporters_types = config_utils.get_export_types()

		for et in exporters_types:
			try:
				exporter_module = config_utils.get_exporter_module(et)
			except RuntimeError as exc:
				self.fail("Unable to load or find module to export \'{}\': {}".format(et, exc))
			else:
				self.assertTrue(
					type(exporter_module).__name__ == "module",
					"A call to the function get_exporter_module is expected to return a module. "
					"Got type \'{}\', instead".format(type(exporter_module).__name__)
				)
