import os


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
		return cls.__file_name(file_path).split(".")[-1]

	@staticmethod
	def __file_name(file_path):
		try:
			return os.path.split(file_path)[-1]
		except(TypeError, ValueError):
			raise RuntimeError("No valid file path provided")

	def load_file(self, file_path):
		file_ext = self.__file_extension(file_path)

		if file_ext == "json":
			# Load a json serializer
			pass
		elif file_ext == "xml":
			# Load an xml serializer
			pass
		else:
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
