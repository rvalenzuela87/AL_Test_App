import os
import unittest
from ..src.utils import config_utils


class TxtExporterTestCase(unittest.TestCase):
	def setUp(self) -> None:
		config_utils.reload_config()

	def test_use_default_export_dir(self):
		exporter_mod = config_utils.get_exporter_module("txt")
		exporter = exporter_mod.__getattribute__(exporter_mod.CLASS_NAME)()
		export_default_dir = config_utils.get_default_directory(abs=True)

		self.assertEqual(
			exporter.directory(), export_default_dir,
			"When no argument is set for the directory parameter at instantiation, the text exporter is expected to"
			"use de default export directory set in the config file (config.json). Expected \'{}\'. Got \'{}\', "
			"instead".format(export_default_dir, exporter.directory())
		)

	def test_text_formatting(self):
		exporter_mod = config_utils.get_exporter_module("txt")
		exporter = exporter_mod.__getattribute__(exporter_mod.CLASS_NAME)()
		headers = ["name", "lastname", "phone"]
		rows = [["Rafael", "Valenzuela Ochoa", "2135680"], ["Adriana", "Ochoa Valenzuela", "7894563"]]

		expected_data_txt = "\n\n".join("\n".join(": ".join(pair) for pair in zip(headers, row)) for row in rows)
		data_txt = exporter.format_data(rows, headers)

		self.assertEqual(
			type(data_txt), str,
			"The returned value for the method \'format_data\' is expected to be a \'str\'. Got \'{}\', "
			"instead".format(type(data_txt).__name__)
		)

		self.assertEqual(
			data_txt, expected_data_txt,
			"String mal constructed:\n{}".format(data_txt)
		)

	def test_export_to_file(self):
		exporter_mod = config_utils.get_exporter_module("txt")
		exporter = exporter_mod.__getattribute__(exporter_mod.CLASS_NAME)()
		headers = ["name", "lastname", "phone"]
		rows = [["Rafael", "Valenzuela Ochoa", "2135680"], ["Adriana", "Ochoa Valenzuela", "7894563"]]

		data_txt = exporter.format_data(rows, headers)
		error_mssg = "An exporter instance is created with empty strings as the arguments for its two " \
		             "parameters: filename and directory. If no filename is set, then it is expected that a " \
		             "call to method export raises a RuntimeError exception"

		with self.assertRaises(RuntimeError, msg=error_mssg):
			exporter.export(data_txt)

		exporter.set_file_name("testFile.txt")
		exporter.export(data_txt)

		for filename in os.listdir(exporter.directory()):
			if filename == exporter.filename():
				# Delete the file
				os.remove(exporter.filepath())
				break
		else:
			self.fail(
				"No \'txt\' file was created"
			)

	def test_export_to_wrong_extension(self):
		exporter_mod = config_utils.get_exporter_module("txt")
		error_mssg = "When the argument for the \'filename\' parameter contains an extension " \
		             "different from \'.txt\', a RuntimeError exception is expected to occur"

		with self.assertRaises(ValueError, msg=error_mssg):
			exporter = exporter_mod.__getattribute__(exporter_mod.CLASS_NAME)(filename="testFile.csv")

		exporter = exporter_mod.__getattribute__(exporter_mod.CLASS_NAME)()
		headers = ["name", "lastname", "phone"]
		rows = [["Rafael", "Valenzuela Ochoa", "2135680"], ["Adriana", "Ochoa Valenzuela", "7894563"]]
		data_txt = exporter.format_data(rows, headers)

		# Set the file name using an unsupported extension
		with self.assertRaises(ValueError, msg=error_mssg):
			exporter.set_file_name("testFile.csv")

	def test_export_to_empty_string_filename(self):
		exporter_mod = config_utils.get_exporter_module("txt")
		error_mssg = "When the argument for the \'filename\' parameter contains an extension " \
		             "different from \'.txt\', a RuntimeError exception is expected to occur"

		exporter = exporter_mod.__getattribute__(exporter_mod.CLASS_NAME)(filename="")

		headers = ["name", "lastname", "phone"]
		rows = [["Rafael", "Valenzuela Ochoa", "2135680"], ["Adriana", "Ochoa Valenzuela", "7894563"]]
		data_txt = exporter.format_data(rows, headers)

		# Set the file name with an empty string as argument
		with self.assertRaises(ValueError, msg=error_mssg):
			exporter.set_file_name("")

	def test_export_to_file_wo_extension(self):
		exporter_mod = config_utils.get_exporter_module("txt")
		exporter = exporter_mod.__getattribute__(exporter_mod.CLASS_NAME)()
		headers = ["name", "lastname", "phone"]
		rows = [["Rafael", "Valenzuela Ochoa", "2135680"], ["Adriana", "Ochoa Valenzuela", "7894563"]]
		data_txt = exporter.format_data(rows, headers)

		exporter.set_file_name("testFile")

		self.assertEqual(
			exporter.filename(), "testFile.txt",
			"When the argument for the \'filename\' parameter contains no file extension it is expected "
			"to be changed to include the default \'txt\' extension"
		)
