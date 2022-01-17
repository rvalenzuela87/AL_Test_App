import xml
from .serial import Serializer


class XMLSerial(Serializer):
	data_type = "xml"

	def __init__(self):
		super(XMLSerial, self).__init__()

	def load(self, data):
		print("Loading xml data to python object")

	def serial(self, data):
		print("Serializing python structure to XML")
