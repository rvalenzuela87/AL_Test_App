import xml
from .serial import Serializer

CLASS_NAME = "XMLSerial"


class XMLSerial(Serializer):
	data_type = "xml"

	def __init__(self):
		super(XMLSerial, self).__init__()

	def load(self, filepath):
		print("Loading xml data to python object")

	def serial(self, data, headers):
		print("Serializing python structure to XML")

	def write(self, data, filepath):
		print("Dumpling data to XML file:\n{}".format(data))