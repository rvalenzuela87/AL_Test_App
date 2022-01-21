import os

CLASS_NAME = "Exporter"


class Exporter(object):
	"""
	Interface for exporter objects. Implementations of this interface must provide definitions for the methods
	'set_file_name', 'format_data' and 'export'.
	"""

	def __init__(self, filename="", directory=""):
		super(Exporter, self).__init__()

		self._filename = filename

		if len(directory) > 0:
			self._directory = directory
		else:
			# Use the configuration's default directory
			try:
				self._directory = os.environ["DEFAULT_EXPORT_DIRECTORY"]
			except KeyError:
				self._directory = ""

	def filename(self):
		"""
		Returns the file name associated with this instance.

		:return: The file name associated with this instance
		:rtype: str
		"""

		return self._filename

	def directory(self):
		"""
		Returns the directory name associated with this instance, where the export files will be written.

		:return: The directory name where the export files will be written
		:rtype: str
		"""

		return self._directory

	def filepath(self):
		"""
		Returns the file path of the resulting export file.

		:return: The file path of the resulting export file
		:rtype: str
		"""

		if len(self._directory) > 0 and len(self._filename) > 0:
			return os.path.join(self._directory, self._filename)
		else:
			raise RuntimeError("No file and/or directory set, yet")

	def set_file_name(self, filename):
		"""
		Sets the file name where the data will be written. It is just the file name without its directory.
		This method needs to be defined by implementations of Exporter.

		:param filename: The file's name where the data will be written
		:type filename: str
		:return: Reference to self
		:rtype: str
		"""
		pass

	def set_directory(self, directory):
		"""
		Sets the directory where the export file will be written. By default, an instance of Exporter will use the
		directory set in the configuration file.

		:param directory: The directory where the export file(s) will be written
		:type directory: str
		:return: Reference to self
		:rtype: self
		"""

		self._directory = directory
		return self

	def format_data(self, data, headers):
		"""
		Formats the data received as argument so they can be written to the desired supported extension. This method
		needs to be defined by implementations of the Exporter interface.

		:param data: List of lists of records
		:type data: list
		:param headers: List with the records' column names
		:type headers: list
		:return: Reference to self
		:rtype: self
		"""
		pass

	def export(self, data):
		"""
		Writes the data string received as argument to the file and directory specified by the instance's file name and
		directory variables. This method needs to be defined by implementations of the Exporter interface.

		:param data: String of formated data to be written
		:type data: str
		:return: None
		:rtype: None
		"""
		pass