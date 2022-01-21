import os
import sys
import importlib
import re as regexp

ARGS_SEP = " "


def load_command_module(command_name):
	"""
	Loads and returns the module which corresponds to the command which long name matches the function's argument.

	:param command_name: The long name of the command which correspondent module is to be found
	:type command_name: str
	:return: The command's module
	:rtype: module
	"""

	command_name = "_".join([command_name, "command"])

	# Assume the command module is already in memory
	for k in sys.modules.keys():
		if k.split(".").pop() == command_name:
			# The module was found in memory. Therefore, return it
			return sys.modules[k]

	# The module wasn't found in memory, which means it hasn't being imported yet. Therefore, try to import it
	# from the 'commands' package
	try:
		return importlib.import_module(".{}".format(command_name), "AL_Test_App.src.commands")
	except ImportError:
		raise RuntimeError("Unable to import the correspondent module for command \'{}\'".format(command_name))


def get_commands_names():
	"""
	Finds the app's commands' long and short names. This function expects the commands modules files, names to
	conform to the pattern 'longname_command.py' and each of them to contain the public constants CMD_NAME and
	CMD_SHRT_NAME

	:return: List with 2 lists with the commands' long names in the first one and the commands' short names
	in the second
	:rtype: list
	"""

	commands_dir = os.path.dirname(os.path.dirname(__file__))
	command_mod_pattern = regexp.compile(r'^([a-zA-Z0-9]*)_command.py$')
	commands_names = []
	commands_short_names = []

	for fn in os.listdir(commands_dir):
		try:
			command_name = command_mod_pattern.match(fn).groups()[0]
		except AttributeError as exc:
			# The file doesn't correspond to a command module. Therefore, move on to the next
			# one
			continue

		try:
			command_mod = load_command_module(command_name)
		except RuntimeError as exc:
			# Unable to load the correspondant module. Therefore, move on to the next file
			continue

		commands_names.append(command_mod.CMD_NAME)
		commands_short_names.append(command_mod.CMD_SHRT_NAME)

	return [commands_names, commands_short_names]


def get_command_name_and_args_from_str(command_str):
	"""
	Extracts the command's name and arguments (positional and keywords) from a command string. This function doesn't
	check whether the command name corresponds to a valid command within the app. Its only objective is to extract the
	information stated earlier. It expects a command string of the form:

	command 'posarg1' 'posarg2' 'posarg' -kwd1 'kwdarg1' -kwd 'kwdarg2'

	:param command_str:
	:type command_str:
	:return:
	:rtype:
	"""

	try:
		command_name, arguments = regexp.match(
			r'^([a-zA-Z0-9_]+)\s?((?:(?:-[a-zA-Z0-9_]+\s?)?\'[a-zA-Z0-9\s,\.\-\(\)+*]+\'\s?)*)$', command_str
		).groups()
	except(AttributeError, TypeError, ValueError):
		raise RuntimeError(
			"Error: Command mal-constructed: %s\n. Please, refer to the command\'s help for more "
			"information" % command_str
		)

	# Parse the arguments str and extract the positional and keyword arguments
	# Remove the trailing or leading whitespaces from the arguments string, if any
	arguments = arguments.strip()
	building_argument = False
	building_keyword = False
	arg_chars_list = []
	kwd_chars_list = []
	pos_args_list = []
	kwd_names_list = []
	kwd_args_list = []
	args_list_ = pos_args_list

	for i, char in enumerate(arguments):
		if char == "'":
			try:
				assert building_keyword is False
			except AssertionError:
				raise ValueError("Command malconstructed: Keywords can\'t contain \'")

			# A new argument is about to start. This may be a positional argument or the value of a keyword argument
			if building_argument:
				# The character may belong to an argument currently being parsed and doesn't mean a new argument is
				# about to start or it may signal the end of the argument currently being parsed. The only way to know
				# which one is the case is by looking at the next character.
				if i + 1 == len(arguments):
					# This is the last character in the string. Therefore, add the characters to the arguments list
					# and end the loop
					if len(arg_chars_list) > 0:
						args_list_.append("".join(arg_chars_list))

					break
				elif arguments[i + 1] == " ":
					# If the next character is a whitespace this means the current ' signals the end of the argument
					# being parsed. Therefore, DO NOT add it to the argument's list, turn off the flag and move on
					# to the next character
					building_argument = False

					if len(arg_chars_list) > 0:
						args_list_.append("".join(arg_chars_list))

					arg_chars_list = []

					# Set the arguments list to point to the positional arguments list as default
					args_list_ = pos_args_list
					continue
				else:
					# The ' belongs to the current argument. Therefore, add the character to the current argument's
					# list and move on to the next character
					arg_chars_list.append(char)
					continue
			else:
				# The building_argument flag is off. This means a new argument is about to start. Therefore,
				# create the new argument list, turn on the flag and move on to the next character.
				building_argument = True

				if len(arg_chars_list) > 0:
					args_list_.append("".join(arg_chars_list))

				arg_chars_list = []
				continue
		elif char == "-":
			try:
				assert building_keyword is False
			except AssertionError:
				raise ValueError("Command malconstructed: Keywords can\'t contain -")

			# This may signal the start of a keyword or it could mean a new character for the argument currently
			# being parsed, if any. The only way to know for sure is to look at the building_argument flag
			if building_argument:
				# The - character belongs to the argument's value. Therefore, add it to the list and move on to the
				# next character
				arg_chars_list.append(char)
				continue
			else:
				# A new keyword is about to start. Therefore, create a new list for the keyword and move on to the
				# next character
				building_keyword = True
				kwd_chars_list = []

				# The new arguments list now points to the keyword arguments list
				#args_list_ = kwd_args_list
				continue
		elif char == " ":
			if building_keyword:
				# This signals the end of the keyword. Therefore, ignore it, turn off the corresponding flag and
				# move on to the next character
				try:
					assert len(kwd_chars_list) > 0
				except AssertionError:
					raise ValueError("Command string malconstructed: Keyword names can't be empty")
				else:
					kwd_names_list.append("".join(kwd_chars_list))

				building_keyword = False

				# The new arguments list now points to the keyword arguments list
				args_list_ = kwd_args_list
				continue
			elif building_argument:
				# The current whitespace is part of the argument being parsed. Therfore, add it to the list and
				# move on to the next character
				arg_chars_list.append(char)
				continue
			else:
				# The flag is turned off. This means the current whitespace represents the space between arguments.
				# Therefore, ignore it and move on to the next character
				continue
		else:
			try:
				assert building_argument or building_keyword
			except AssertionError:
				raise ValueError("Command string malconstructed: Argument values must be enclosed with '")
			else:
				if building_argument:
					# Add the character to the current argument list and move on to the next character
					arg_chars_list.append(char)
					continue
				else:
					# Add the character to the current keyword list and move on to the next character
					kwd_chars_list.append(char)
					continue

	return command_name, pos_args_list, dict(zip(kwd_names_list, kwd_args_list))


def build_command_str(command_name, *args, **kwargs):
	"""
	Builds a string for calling a command. This string can be used as an input in the application. Building a command
	string doesn't execute the command. This function is not concerned if the command name received as argument
	corresponds to a valid command within the app. The string returned matches the following form:

	command 'posarg1' 'posarg2' 'posarg' -kwd1 'kwdarg1' -kwd 'kwdarg2'

	:param command_name: Command's name in either long or short version
	:type command_name: str
	:param args: (Optional) List of positional arguments for the command
	:type args: list
	:param kwargs: (Optional) List of keyword arguments for the command
	:type kwargs: dict
	:return: The command string
	:rtype: str
	"""

	try:
		pos_args_str = ARGS_SEP.join("\'%s\'" % a for a in args)
	except(ValueError, TypeError):
		pos_args_str = ""

	try:
		kwd_keys = kwargs.keys()
	except AttributeError:
		kwd_args_str = ""
	else:
		kwd_args_str = ARGS_SEP.join("-%s \'%s\'" % (kwd, arg) for kwd, arg in zip(kwd_keys, (kwargs[k] for k in kwd_keys)))

	args_str = ARGS_SEP.join([pos_args_str, kwd_args_str])

	if not args_str == ARGS_SEP:
		# Remove any leading or trailing ARGS_SEP
		if args_str.startswith(ARGS_SEP):
			args_str = args_str[1:]

		if args_str.endswith(ARGS_SEP):
			args_str = args_str[0:-1]
	else:
		args_str = ""

	if len(args_str) > 0:
		return " ".join([command_name, args_str])
	else:
		return command_name