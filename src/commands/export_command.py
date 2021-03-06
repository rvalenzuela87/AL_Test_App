import os
import re as regexp

from .command import Command

CLASS_NAME = "ExportCommand"
CMD_NAME = "export"
CMD_SHRT_NAME = "e"


class ExportCommand(Command):
	def __init__(self, receiver, *args, **kwargs):
		super(ExportCommand, self).__init__(receiver, *args, **kwargs)

		self.params_names = ["filename"]
		self.params_short_names = ["n"]

		try:
			self.set_params(*args, **kwargs)
		except RuntimeError:
			self.prompt()

	@staticmethod
	def help():
		help_msg = """
		The \"export (e)\" command provides a way for creating reports of the data in memory. It supports one 
		argument: filename. In case no argument is provided at calling time, a prompt operation will be triggered
		asking for the required argument. It is important that the filename provided contains only the name and 
		extension and not its directory. The exported files are stored in the directory specified in the 
		configuration file, by default.
		
		The command can be called with positional argument, as such:
		
			export 'report.txt'
			export 'report.html'
		
		Or with keyword argument, as such:
			
			export -filename 'report.txt'
			export -filename 'report.html'
		
		Or in short form, as such:
		
			export -fn 'report.txt'
			export -fn 'report.html'
			
		"""

		return help_msg

	def prompt(self, missing_only=False):
		supported_file_types = os.environ["EXPORT_TYPES"].split("|")
		filename_pattern = regexp.compile(r'^[a-zA-Z0-9_-]+\.([a-zA-Z0-9]+)$')

		while True:
			filename = input(
				"Provide a file name with supported extension ({}): ".format("|".join(supported_file_types))
			)

			try:
				extension = filename_pattern.match(filename).groups()[0]
			except(AttributeError, IndexError):
				print(
					"\n[E] Filename contains non supported characters or is missing the extension. Please, use "
					"alphanumeric characters and underscores, only.\n"
				)
			else:
				extension = extension.lower()

				try:
					assert extension in supported_file_types
				except AssertionError:
					print(
						"\n[E] File extension \'{}\' is not supported. Please, use one of the following supported "
						"extensions: {}\n".format(extension, ", ".join(supported_file_types))
					)
				else:
					print("\n")
					break

		self.params_args = dict.fromkeys(self.params_names)
		self.params_args["filename"] = filename

		return self

	def set_params(self, *args, **kwargs):
		# Makes sure the arguments received are all either positional or keyword arguments. Mixing the two is not
		# supported. An exception is raised if this condition is not met
		if len(args) > 0 and (kwargs and len(kwargs.keys()) > 0):
			# The method received a mix of positional and keyword arguments. This is not supported to avoid
			# confusion and to simplify the logic in the code.
			raise RuntimeError(
				"Mixing positional and keyword arguments is not supported. Please, refer to the command\'s help"
				"for more information on how the arguments should be delivered to the command."
			)

		supported_file_types = os.environ["EXPORT_TYPES"].split("|")
		self.params_args = dict.fromkeys(self.params_names)

		try:
			self.params_args["filename"] = args[0]
		except(AttributeError, IndexError):
			try:
				self.params_args["filename"] = kwargs["filename"]
			except TypeError:
				# No keyword argument containing the filename was provided. Therefore, ask the user for one
				self.prompt()
				return self
			except KeyError:
				try:
					self.params_args["filename"] = kwargs["n"]
				except KeyError:
					# No keyword argument containing the filename was provided. Therefore, ask the user for one
					self.prompt()
					return self

		# If the following code is reached, it means the filename was found within one of the method's arguments
		# and the user was not asked for it via a call to the prompt method. Therefore, make sure the filename
		# has a supported extension
		try:
			extension = os.path.splitext(self.params_args["filename"])[1][1:]

			assert extension in supported_file_types
		except AssertionError:
			self.params_args = None

			if len(extension) > 0:
				# The extension is not supported
				raise ValueError(
					"Extension \'{}\' is not supported. Please, choose from one of the following "
					"file extensions: ".format(extension, ", ".join(supported_file_types))
				)
			else:
				raise ValueError(
					"No extension found in the filename specified. Please, include one of the following "
					"file extensions in the file name: {}".format(", ".join(supported_file_types))
				)

		return self

	def execute(self):
		try:
			filename = self.params_args["filename"]
		except(TypeError, KeyError):
			self.prompt()
			filename = self.params_args["filename"]

		filepath = self.receiver.export(filename)
		print("\n[i] Records exported to \'{}\'\n".format(filepath))
