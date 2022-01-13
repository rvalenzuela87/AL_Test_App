import xml
from abstract_serial import AbstractSerializer


class XMLSerial(AbstractSerializer):
	data_type = "xml"

	def __init__(self):
		super(XMLSerial, self).__init__()

	def load(self, data):
		print("Loading xml data to python object")

	def serial(self, data):
		print("Serializing python structure to XML")
