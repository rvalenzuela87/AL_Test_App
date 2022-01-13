class AbstractSerializer(object):
	data_type = None

	def __init__(self, file):
		super(AbstractSerializer, self).__init__()

		self.data_type = ""
		self.file = file

	def load(self):
		"""
		Loads the information contained in the object received as argument to a python list of lists.

		:return: Python list of lists of size n x 3. Where n = records total
		:rtype: list
		"""
		pass

	def serial(self, data):
		"""

		:param data: Python list of lists of size n x 3, where n = records total
		:type data: list
		:return: Serialized data. The exact type depends on this method's definition in implementations
			of AbstractSerializer
		:rtype: *
		"""
		pass

	def write(self, data):
		"""

		:param data:
		:type data: list
		:return:
		:rtype: bool
		"""
		pass
