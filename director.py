import re as regexp
from collections import namedtuple
from file_manager import FileManager
import validations


RecordRow = namedtuple("Record", ["names", "last_name", "address", "city", "phone"])


class Director(object):
	__data = None

	def __init__(self, serializer=None, file_path=""):
		super(Director, self).__init__()

		self.__data = []

	def append_row(self, row_data):
		try:
			record_row = RecordRow(*row_data)
		except RuntimeError:
			raise RuntimeError("Record data received as argument is not complete")

		assert validations.validate_name(record_row.name)
		assert validations.validate_name(record_row.last_name)
		assert validations.validate_address(record_row.address)
		assert validations.validate_city(record_row.city)
		assert validations.validate_phone(record_row.phone)

	def delete_row(self, row_index):
		try:
			self.__data.pop(row_index)
		except IndexError:
			raise RuntimeError("Index %i not found" % row_index)
		else:
			return True

	def display(self, filter_exp=""):
		pass

	def save(self):
		FileManager().write(self.__data)

	def export(self, format_type):
		pass
