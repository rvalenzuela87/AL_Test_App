import unittest

from AL_Test_App.src.utils import config_utils
from AL_Test_App.src.serializers.serializers_builder import SerializersBuilder


class TestSerializers(unittest.TestCase):
	def test_get_serializer_module(self):
		"""
		Makes sure all the types of serialization supported by the app as stated in its configuration file
		(config.json) have a correspondant module in the 'serializers' package and, also, that a call to the
		method 'get_serializer_module' returns a reference to a python module
		"""

		supported_extensions = config_utils.get_serial_types()
		serial_builder = SerializersBuilder()

		for st in supported_extensions:
			try:
				serial_mod = serial_builder.get_serializer_module(st)
			except RuntimeError as exc:
				self.fail("{}".format(exc))

			self.assertEqual(
				type(serial_mod).__name__, "module",
				"A call to the method get_serializer_module is expected to return a module. "
				"Got {}, instead".format(type(serial_mod).__name__)
			)

	def test_get_non_supported_serializer_module(self):
		"""
		Makes sure an exception is raised when the method 'get_serializer_module' is called with an unsupported
		extension as its argument
		"""

		serial_builder = SerializersBuilder()
		error_msg = "Expected a call to method get_serializer_module with an unsupported extension as argument " \
		            "to raise a RuntimeError exception"

		with self.assertRaises(RuntimeError, msg=error_msg):
			serial_builder.get_serializer_module("yaml")

	def test_get_serializer_module_with_empty_string(self):
		"""
		Makes sure an exception is raised when the method 'get_serializer_module' is called with an empty string as
		argument
		"""

		serial_builder = SerializersBuilder()
		error_msg = "Expected a call to method get_serializer_module with an empty string as argument " \
		            "to raise a RuntimeError exception"

		with self.assertRaises(RuntimeError, msg=error_msg):
			serial_builder.get_serializer_module("")
