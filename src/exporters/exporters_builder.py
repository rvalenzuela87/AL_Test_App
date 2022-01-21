import sys
import re as regexp
import importlib


class ExportersBuilder(object):
	"""
	Class for building exporters instances
	"""

	def __init__(self):
		super(ExporterBuilder, self).__init__()

	@staticmethod
	def get_exporter_module(extension):
		"""
		Returns an exporter module correspondant to the extension received as argument. First, the module is looked
		in memory and, if it's not there, tries to import it. This method may raise a RuntimeError exception if it
		receives an unsupported extension as argument.

		:param extension: The extension supported by the exporter module
		:type extension: str
		:return: The exporter module correspondant with the extension received as argument
		:rtype: module
		"""

		exporter_mod_pattern = regexp.compile(r'^(?:.*)\.([a-zA-Z]+)_exporter$')

		# Firts, look for the exporter module in memory
		for k in sys.modules.keys():
			try:
				assert exporter_mod_pattern.match(k).groups()[0] == extension
			except AssertionError:
				pass
			except(AttributeError, IndexError):
				# The key may not belong to an exporter module or, if it does, it isn't the correspondant one.
				# Therefore, move on to the next module in memory
				continue
			else:
				# The current key belongs to an exporter module and it corresponds to the type received as argument
				return sys.modules[k]

		# The module wasn't found in memory, which means it hasn't being imported yet. Therefore, try to import it
		# from the 'exporters' package
		try:
			return importlib.import_module(
				".{}".format("_".join([extension, "exporter"])), "AL_Test_App.src.exporters"
			)
		except ImportError:
			raise RuntimeError(
				"Unable to import the correspondent module for export extension \'{}\'".format(extension)
			)

	@classmethod
	def get_exporter(cls, extension, *args, **kwargs):
		"""
		Returns an exporter instance correspondant with the extension received as its first argument. This method
		also supports unspecified number of positional and keyword arguments which are used as arguments when
		instantiating the exporter.

		:param extension: The type of extension supported by the exporter instance
		:type extension: str
		:param args: Positional arguments to use when instantiating the exporter
		:type args: list
		:param kwargs: Keyword arguments to use when instantiating the exporter
		:type kwargs: dict
		:return: An implementation of Exporter interface
		:rtype: Exporter
		"""

		exporter_mod = cls.get_exporter_module(extension)

		return exporter_mod.__getattribute__(exporter_mod.CLASS_NAME)(*args, **kwargs)
