import os

from xml.etree import ElementTree
from .exporter import Exporter

CLASS_NAME = "HtmlExporter"


class HtmlExporter(Exporter):
	"""
	Implementaiont of the Exporter interface for exporting the records data to hml files
	"""

	data_type = "xml"

	def __init__(self, filename="", directory=""):
		super(HtmlExporter, self).__init__(filename=filename, directory=directory)

		if len(filename) > 0:
			self.set_file_name(filename)

	def set_file_name(self, filename):
		try:
			assert len(filename) > 0
			file_ext = os.path.splitext(filename)[1][1:].lower()
			assert len(file_ext) > 0 and file_ext == "html"
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
				filename = ".".join([filename, "html"])

		self._filename = filename

	def format_data(self, data, headers):
		html_element = ElementTree.Element("html")
		body_element = ElementTree.SubElement(html_element, "body")
		table_element = ElementTree.SubElement(body_element, "table")
		headers_row_element = ElementTree.SubElement(table_element, "tr")

		# Add the table headers
		for head in headers:
			head_element = ElementTree.SubElement(headers_row_element, "th")
			head_element.text = head

		for row in data:
			row_tag = ElementTree.SubElement(table_element, "tr")

			for tag_text in row:
				child_tag = ElementTree.SubElement(row_tag, "td")
				child_tag.text = tag_text

		# Convert the xml to a string
		return ElementTree.tostring(html_element, encoding="unicode", method="html", xml_declaration=True)

	def export(self, data):
		filepath = self.filepath()

		with open(filepath, 'w') as fh:
			fh.write(data)
