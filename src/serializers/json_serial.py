import json
from serial import Serializer


class JSONSerial(Serializer):
	data_type = "json"

	def __init__(self):
		super(JSONSerial, self).__init__()

	def load(self, data):
		print("loading json data to python object")

	def serial(self, data):
		print("Serializing python structure to JSON object")

	def write(self, data, file_handler):
		print("Dumping data to json file")
