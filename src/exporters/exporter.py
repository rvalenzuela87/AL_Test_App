import os

CLASS_NAME = "Exporter"


class Exporter(object):
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
		return self._filename

	def directory(self):
		return self._directory

	def filepath(self):
		if len(self._directory) > 0 and len(self._filename) > 0:
			return os.path.join(self._directory, self._filename)
		else:
			raise RuntimeError("No file and/or directory set, yet")

	def set_file_name(self, filename):
		pass

	def set_directory(self, directory):
		self._directory = directory

	def format_data(self, data, headers):
		pass

	def export(self, data):
		pass