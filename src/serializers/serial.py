class Serializer(object):
	data_type = None

	def __init__(self):
		super(Serializer, self).__init__()

	def load(self, filepath):
		"""
		Loads the information contained in the object received as argument to a python list of lists.

		:return: Python list of lists of size n x 5. Where n = records total
		:rtype: list
		"""
		pass

	def serial(self, data, headers):
		"""

		:param data: Python list of lists of size n x 3, where n = records total
		:type data: list
		:return: Serialized data. The exact type depends on this method's definition in implementations
			of Serializer
		:rtype: *
		"""
		pass
