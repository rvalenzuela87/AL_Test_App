from xml.etree import ElementTree
from .serial import Serializer

CLASS_NAME = "XMLSerial"


class XMLSerial(Serializer):
	data_type = "xml"

	def __init__(self):
		super(XMLSerial, self).__init__()

	def load(self, filepath):
		xml_tree = ElementTree.parse(filepath)
		tree_root = xml_tree.getroot()
		data_dict = {}

		for row in tree_root.findall("row"):
			for child in row:
				try:
					data_dict[child.tag].append(child.text)
				except(AttributeError, KeyError):
					data_dict[child.tag] = [child.text]

		return data_dict

	def serial(self, data, headers):
		root_element = ElementTree.Element("records")

		for row in data:
			row_tag = ElementTree.SubElement(root_element, "row")

			for tag_name, tag_text in zip(headers, row):
				child_tag = ElementTree.SubElement(row_tag, tag_name)
				child_tag.text = tag_text

		# Convert the xml to a string
		return ElementTree.tostring(root_element, encoding="unicode", method="xml", xml_declaration=True)
