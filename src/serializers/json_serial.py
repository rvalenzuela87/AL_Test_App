import json
from .serial import Serializer

CLASS_NAME = "JSONSerial"

class JSONSerial(Serializer):
	data_type = "json"

	def __init__(self):
		super(JSONSerial, self).__init__()

	def load(self, filepath):
		with open(filepath, 'r') as fh:
			data_dict = json.JSONDecoder().decode(fh.read())

		return data_dict

	def serial(self, data, headers):
		data_dict = dict(zip(headers, zip(*data)))

		return json.JSONEncoder().encode(data_dict)

	def write(self, data, headers, filepath):
		dict_data = dict(zip(headers, zip(*data)))

		with open(filepath, 'w') as fh:
			json.dump(dict_data, fh)
