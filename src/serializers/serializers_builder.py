import sys
import importlib
import re as regexp


class SerializersBuilder(object):
	def __init__(self):
		super(SerializersBuilder, self).__init__()

	@staticmethod
	def get_serializer_module(extension):
		serial_mod_pattern = regexp.compile(r'^(?:.*)\.([a-zA-Z]+)_serial$')

		# Firts, look for the serializer module in memory
		for k in sys.modules.keys():
			try:
				assert serial_mod_pattern.match(k).groups()[0] == extension
			except AssertionError:
				continue
			except(AttributeError, IndexError):
				# The key may not belong to a serialization module or, if it does, it isn't the correspondant one.
				# Therefore, move on to the next module in memory
				continue
			else:
				# The current key belongs to a serialization module and it corresponds to the type received
				# as argument
				return sys.modules[k]

		try:
			return importlib.import_module(
				".{}".format("_".join([extension, "serial"])), "AL_Test_App.src.serializers"
			)
		except(ModuleNotFoundError, ImportError):
			raise RuntimeError("No serializer module found for type \'{}\'".format(extension))

	@classmethod
	def get_serializer(cls, extension):
		serial_mod = cls.get_serializer_module(extension)

		return serial_mod.__getattribute__(serial_mod.CLASS_NAME)()