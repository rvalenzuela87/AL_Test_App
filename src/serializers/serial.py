class Serializer(object):
	data_type = None

	def __init__(self):
		super(Serializer, self).__init__()

	def load(self, filepath):
		"""
		Loads the information contained in the object received as argument to a python dictionary. This method needs
		to be defined by implementations of Serializer.

		:return: Python dictionary with 5 keys each with a list of size n, where n = recors total
		:rtype: dict
		"""
		pass

	def serial(self, data, headers):
		"""
		Serializes the data and headers received as argument to the supported extension. This method needs ot be
		defined by implementations of Serializer.

		:param data: Python list of lists of size n x 5, where n = records total
		:type data: list
		:return: Serialized data. The exact type depends on this method's definition in implementations of Serializer
		:rtype: *
		"""
		pass
