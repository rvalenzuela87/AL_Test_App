import unittest
from AL_Test_App.src.commands.utils import commands_utils


class ExtractCommandInfoFromStringTestCase(unittest.TestCase):
	def test_build_command_str_wo_args(self):
		"""
		Test for building a command string with no arguments
		"""

		command_name = "cmnd"
		command_str = commands_utils.build_command_str(command_name)

		self.assertEqual(
			command_name,
			command_str,
			"A command string with no arguments must be equal to the command\'s name with no trailing spaces."
		)

	def test_build_command_str_w_pos_args(self):
		"""
		Test for building a command string with positional arguments only
		"""

		command_name = "cmnd"
		command_args = ["Rafael", "Valenzuela Ochoa", "2135680"]
		expected_command_str = " ".join([command_name, " ".join("\'%s\'" % c for c in command_args)])
		command_str = commands_utils.build_command_str(command_name, *command_args)

		self.assertEqual(
			command_str,
			expected_command_str,
			"The command string is non-complient with the expected form. Expected \'{}\'. Got \'{}\', "
			"instead.".format(expected_command_str, command_str)
		)

	def test_build_command_str_w_kwd_args(self):
		"""
		Test for building a command string with keyword arguments only
		"""

		command_name = "cmnd"
		command_kwd_args = [("name", "Rafael"), ("lastname", "Valenzuela Ochoa"), ("phone", "123456")]
		expected_command_str = " ".join(
			[command_name, " ".join("-%s \'%s\'" % (kwd, arg) for kwd, arg in command_kwd_args)]
		)
		command_str = commands_utils.build_command_str(command_name, **dict(command_kwd_args))

		self.assertEqual(
			command_str,
			expected_command_str,
			"The command string is non-complient with the expected form. Expected \'{}\'. Got \'{}\', "
			"instead.".format(expected_command_str, command_str)
		)

	def test_build_command_str_w_pos_and_kwd_args(self):
		"""
		Test for building a command string with positional and keyword arguments. It is important to note that,
		although this form can be constructed, it is not supported as a valid command string when trying to
		extract the command's name and arguments from it.
		"""

		command_name = "cmnd"
		command_args = ["Rafael", "Valenzuela Ochoa", "2135680"]
		command_kwd_args = [("name", "Rafael"), ("lastname", "Valenzuela Ochoa"), ("phone", "123456")]

		command_args_str = " ".join("\'%s\'" % c for c in command_args)
		command_kwd_args_str = " ".join("-%s \'%s\'" % (kwd, arg) for kwd, arg in command_kwd_args)

		expected_command_str = " ".join(
			[command_name, " ".join([command_args_str, command_kwd_args_str])]
		)
		command_str = commands_utils.build_command_str(command_name, *command_args, **dict(command_kwd_args))

		self.assertEqual(
			command_str,
			expected_command_str,
			"The command string is non-complient with the expected form. Expected \'{}\'. Got \'{}\', "
			"instead.".format(expected_command_str, command_str)
		)

	def test_extract_name_and_arguments(self):
		"""
		Extract the command's name and arguments from a command string with positional arguments only. This function
		only makes sure that the extracting operation returns a tuple with 3 elements: the command's name (str),
		positional arguments (list or tuple) and the keyword arguments (dict)
		"""

		command_name = "cmnd"
		command_args = ["Rafael", "Valenzuela Ochoa", "2135680"]
		command_kwd_args = [("address", "Mulholland Drv"), ("city", "Twin Peaks")]

		command_args_str = " ".join("\'%s\'" % c for c in command_args)
		command_kwd_args_str = " ".join("-%s \'%s\'" % (kwd, arg) for kwd, arg in command_kwd_args)
		command_kwd_args_dict = dict(command_kwd_args)

		command_str = " ".join([command_name, command_args_str, command_kwd_args_str])

		result = commands_utils.get_command_name_and_args_from_str(command_str)

		self.assertTrue(
			type(result) in (tuple, list),
			"Expected the value returned by the function get_command_name_and_args_from_str to be of type list "
			"or tuple. Got type {}, instead.".format(type(result).__name__)
		)

		self.assertEqual(
			len(result),
			3,
			"The function get_command_name_and_args_from_str is expected to return a tuple with 3 elements: "
			"command\'s name (str), positional arguments (tuple) and keyword arguments (dict). Got {} elements, "
			"instead.".format(len(result))
		)

		self.assertTrue(
			type(result[0]) is str,
			"Expected the first element of the tuple or list returned by get_command_name_and_args_from_str to be "
			"of type str and represent the command\'s name. Got type {}, instead.".format(type(result[0]).__name__)
		)

		self.assertTrue(
			type(result[1]) in (list, tuple),
			"Expected the second element of the tuple or list returned by get_command_name_and_args_from_str to be "
			"of type tuple and represent the command\'s positional arguments. "
			"Got type {}, instead.".format(type(result[1]).__name__)
		)

		self.assertTrue(
			type(result[2]) is dict,
			"Expected the third element of the tuple or list returned by get_command_name_and_args_from_str to be "
			"of type dict and represent the command\'s keyword arguments. "
			"Got type {}, instead.".format(type(result[2]).__name__)
		)

		self.assertListEqual(
			command_args,
			result[1],
			"The function failed to return the expected arguments from the command string. "
			"Expected {}. Got {}".format(command_args, result[1])
		)

		self.assertDictEqual(
			command_kwd_args_dict,
			result[2],
			"The function failed to return the expected keyword arguments from the command string. "
			"Expected {}. Got {}".format(command_kwd_args_dict, result[2])
		)

	def test_command_malconstructed(self):
		command_name = "cmnd"
		command_args = ["Rafael", "Valenzuela Ochoa", "123456"]
		command_str = " ".join([command_name, " ".join(command_args)])
		error_mssg = "Expected the call to function get_command_name_and_args_from_str with argument \"{}\" to " \
		             "raise a RuntimeError exception given that the argument string doesn\'t comply with the " \
		             "expected form of a command string."

		with self.assertRaises(RuntimeError, msg=error_mssg):
			commands_utils.get_command_name_and_args_from_str(command_str)
