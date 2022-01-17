import os
import re as regexp

from .utils import config_utils


class FileManager(object):
	_SINGLE = None
	_serializer = None
	_working_file_path = None

	def __new__(cls):
		if cls._SINGLE:
			return cls._SINGLE
		else:
			cls._SINGLE = object.__new__(cls)
			return cls._SINGLE

	@classmethod
	def __file_extension(cls, file_path):
		try:
			extension = os.path.splitext(file_path)[1]

			assert len(extension) > 0
		except(IndexError, AssertionError):
			raise RuntimeError("Unable to retrieve the file extension from path \'{}\'".format(file_path))
		else:
			return extension

	@staticmethod
	def __file_name(file_path):
		try:
			return os.path.split(file_path)[-1]
		except(TypeError, ValueError):
			raise RuntimeError("No valid file path provided")

	def load_file(self, file_path):
		file_ext = self.__file_extension(file_path)
		supported_exts = config_utils.get_serial_types()
		serializers = dict(zip(supported_exts, (None for __ in range(len(supported_exts)))))

		try:
			serial = serializers[file_ext]
		except KeyError:
			raise RuntimeError("Unsupported file extension %s" % file_ext)

		self._working_file_path = file_path

	def working_file_name(self):
		try:
			return self.__file_name(self._working_file_path)
		except RuntimeError:
			raise RuntimeError("No file loaded yet")

	def working_file_directory(self):
		try:
			return os.path.dirname(self._working_file_path)
		except(TypeError, ValueError):
			raise RuntimeError("No file loaded yet")

	def working_file_extension(self):
		try:
			return self.__file_extension(self._working_file_path)
		except RuntimeError:
			raise RuntimeError("No file loaded yet")

	def write(self, data):
		pass
