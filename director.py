from collections import namedtuple
from .file_manager import FileManager
from utils import validations

Record = namedtuple("Record", ["names", "last_name", "address", "city", "phone"])


class Director(object):
	__data = None

	def __init__(self):
		super(Director, self).__init__()

		self.__data = []

	def append(self, data):
		try:
			record = Record(*data)
		except RuntimeError:
			raise RuntimeError("Record data received as argument is not complete")

		assert validations.validate_name(record.name)
		assert validations.validate_name(record.last_name)
		assert validations.validate_address(record.address)
		assert validations.validate_city(record.city)
		assert validations.validate_phone(record.phone)

		self.__data.append(record)

	def delete(self, index):
		"""

		:param index:
		:type index: int
		:return: Returns 'true' if the operation completed successfully. Otherwise raises a RuntimeError exception
		:rtype: bool
		"""

		try:
			self.__data.pop(index)
		except IndexError:
			raise RuntimeError("Index %i not found" % index)
		except(TypeError, ValueError):
			raise RuntimeError("")
		else:
			return True

	def list(self, filter_exp=""):
		pass

	def save(self):
		FileManager().write(self.__data)

	def export(self, extension):
		pass
