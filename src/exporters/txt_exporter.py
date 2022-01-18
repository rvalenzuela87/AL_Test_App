import os

from .exporter import Exporter

CLASS_NAME = "TxtExporter"


class TxtExporter(Exporter):
	def __init__(self, filename="", directory=""):
		super(TxtExporter, self).__init__(filename=filename, directory=directory)

		if len(filename) > 0:
			self.set_file_name(filename)

	def format_data(self, data, headers):
		format_rows = [
			"\n".join(": ".join(field_value_pair) for field_value_pair in zip(headers, row)) for row in data
		]

		return "\n\n".join(format_rows)

	def set_file_name(self, filename):
		try:
			assert len(filename) > 0
			file_ext = os.path.splitext(filename)[1][1:].lower()
			assert len(file_ext) > 0 and file_ext == "txt"
		except AssertionError:
			if len(filename) == 0:
				raise ValueError(
					"Empty string is not a valid file name"
				)
			elif len(file_ext) > 0:
				raise ValueError(
					"Unsupported extension \'{}\'".format(file_ext)
				)
			else:
				# The filename provided has no extension. Therefore, assume it's a txt file
				filename = ".".join([filename, "txt"])

		self._filename = filename

	def export(self, data):
		filepath = self.filepath()

		with open(filepath, 'w') as fh:
			fh.write(data)
