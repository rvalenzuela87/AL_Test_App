import os

from utils import config_utils


class RecordsManager(object):
	_SINGLE = None
	_headers = []
	_records = None
	_serializer = None
	_working_file_path = None
	_save_directory = None

	def __new__(cls, *args, **kwargs):
		if cls._SINGLE:
			return cls._SINGLE
		else:
			cls._SINGLE = object.__new__(cls)
			cls._headers = ["name", "lastname", "address", "city", "phone"]
			cls._records = []
			cls._save_directory = config_utils.get_save_directory(abs=True)

			return cls._SINGLE

	@classmethod
	def __file_extension(cls, file_path):
		try:
			extension = os.path.splitext(file_path)[1][1:]

			assert len(extension) > 0
		except(IndexError, AssertionError):
			raise RuntimeError("Unable to retrieve the file extension from path \'{}\'".format(file_path))
		else:
			return extension

	def __force_load_serializer(self):
		serial_mod = config_utils.get_serializer_module(self.__file_extension(self._working_file_path).lower())
		self._serializer = serial_mod.__getattribute__(serial_mod.CLASS_NAME)()

	@staticmethod
	def __file_name(file_path):
		try:
			return os.path.split(file_path)[1]
		except(TypeError, ValueError, IndexError):
			raise RuntimeError("No valid file path provided")

	def load_from_file(self, filename):
		self.set_working_file_name(filename)
		data_dict = self._serializer.load(self._working_file_path)

		self._records = list(zip(*[data_dict[head] for head in self._headers]))

	def working_file_name(self):
		try:
			return self.__file_name(self._working_file_path)
		except RuntimeError:
			raise RuntimeError("No file loaded yet")

	def working_file_path(self):
		return self._working_file_path

	def set_working_file_name(self, filename):
		self._working_file_path = os.path.join(self._save_directory, filename)
		self.__force_load_serializer()

		os.environ["WORKING_FILE"] = filename
		os.environ["WORKING_FILE_PATH"] = self._working_file_path

	def working_file_directory(self):
		try:
			return os.path.dirname(self._working_file_path)
		except(TypeError, ValueError):
			raise RuntimeError("No file loaded yet")

	def working_file_extension(self):
		try:
			return self.__file_extension(self._working_file_path)
		except RuntimeError:
			raise RuntimeError("No file loaded yet")

	def headers(self):
		return self._headers

	def records(self):
		records = [[v for v in row] for row in self._records]

		for i, row in enumerate(records):
			row.insert(0, str(i))

		return records

	def add_record(self, record):
		try:
			assert len(record) == len(self._headers)
		except AssertionError:
			if len(self._headers) > len(record):
				raise ValueError(
					"The number of values for the record received as argument is less than the number "
					"of columns. Got {} values, expected {}".format(len(record), len(self._headers))
				)
			else:
				raise ValueError(
					"The number of values for the record received as argument is greater than the number "
					"of columns. Got {} values, expected {}".format(len(record), len(self._headers))
				)

		self._records.append(record)

	def filter_records(self, **kwargs):
		headers = self.headers()
		filtered_columns = []

		try:
			kwds = kwargs.keys()
		except AttributeError:
			kwds = []

		for k in kwds:
			try:
				filtered_columns.append((headers.index(k), kwargs[k]))
			except(ValueError, IndexError):
				# The keyword doesn't correspond to a header. Therefore, raise an exception
				raise ValueError(
					"There is no column header \'{}\'".format(k)
				)

		records = self.records()
		filtered_records = []

		for row in records:
			for col, filter_value in filtered_columns:
				# Split the filter value using the character * as the separator
				filter_parts = filter_value.split("*")

				# The column index must be increased by 1 given that the records used in the bucle contain the row's
				# index as the first element for each of the rows
				if len(filter_parts) > 1:
					# Make sure the column's value starts with the first filter split part and ends with the last
					# one
					try:
						assert row[col + 1].startswith(filter_parts[0])
						assert row[col + 1].endswith(filter_parts[-1])
					except AssertionError:
						# The column's value doesn't match the filter associated with the column. Therefore,
						# the current row has to be discarded and the bucle can be broken
						break
				else:
					# If the resulting list contains only one element, then, the column's value must be
					# exactly equal to that element
					try:
						assert row[col + 1] == filter_value
					except AssertionError:
						# The column's value doesn't match the filter associated with the column. Therefore,
						# the current row has to be discarded and the bucle can be broken
						break
			else:
				# The bucle reached its end without exiting prematurely. Therefore, it is safe to assume that
				# the current row's values matched all the filters received as arguments
				filtered_records.append(row)

		return filtered_records

	def delete_record(self, index):
		try:
			self._records.pop(index)
		except IndexError:
			raise RuntimeError(
				"Index {} is greater than the number of rows currently available. Indices are "
				"zero based.".format(index)
			)

	def delete_last_record(self):
		self._records.pop()

	def reset(self):
		self._records = []
		self._working_file_path = None
		self._serializer = None

	def empty_records(self):
		self._records = []

	def write(self, filename=""):
		if len(filename) > 0:
			self.set_working_file_name(filename)

		try:
			serial_data = self._serializer.serial(self._records, self._headers)
		except AttributeError:
			raise RuntimeError(
				"No serializer set, yet. Try setting a working file name or giving an argument "
				"for parameter \'filename\'"
			)
		except(RuntimeError, Exception) as exc:
			print("{}".format(exc))
		else:
			with open(self._working_file_path, 'w') as fh:
				fh.write(serial_data)

	def export(self, filename):
		extension = self.__file_extension(filename)
		exporter_mod = config_utils.get_exporter_module(extension)

		exporter = exporter_mod.__getattribute__(exporter_mod.CLASS_NAME)()
		exporter.set_file_name(filename)
		exporter.export(exporter.format_data(self._records, self._headers))
