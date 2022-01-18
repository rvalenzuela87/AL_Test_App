import os
import sys
import re as regexp

ARGS_SEP = " "


def load_command_module(command_name):
	command_name = "_".join([command_name, "command"])
	# Assume the command module is already in memory
	for k in sys.modules.keys():
		if k.split(".").pop() == command_name:
			return sys.modules[k]

	# The module is not on memory. Therefore, try to import it
	try:
		exec("from commands import %s" % command_name)
	except ImportError:
		raise ImportError("Unable to find the \"%s\" command module" % command_name)

	# Find the module in memory and return it
	for k in sys.modules.keys():
		if k.split(".").pop() == command_name and type(sys.modules[k]).__name__ == "module":
			return sys.modules[k]


def get_commands_names():
	commands_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "commands")
	command_mod_pattern = regexp.compile(r'^([a-zA-Z0-9]*)_command.py$')
	commands_names = []
	commands_short_names = []

	for fn in os.listdir(commands_dir):
		try:
			command_name = command_mod_pattern.match(fn).groups()[0]
		except AttributeError:
			continue

		try:
			command_mod = load_command_module(command_name)
			assert command_mod is not None
		except(AssertionError, RuntimeError):
			continue

		commands_names.append(command_mod.CMD_NAME)
		commands_short_names.append(command_mod.CMD_SHRT_NAME)

	return commands_names, commands_short_names

	commands_names = ["new", "open", "save", "list", "add", "delete", "export", "help", "exit"]
	commands_short_names = ["n", "o", "s", "l", "a", "d", "e", "h", "ex"]

	return commands_names, commands_short_names


def get_command_name_and_args_from_str(command_str):
	try:
		command_name, arguments = regexp.match(
			r'^([a-zA-Z0-9_]+)\s?((?:(?:-[a-zA-Z0-9_]+\s?)?\'[a-zA-Z0-9\s,\.\-\(\)+*]+\'\s?)*)$', command_str
		).groups()
	except(AttributeError, TypeError, ValueError):
		raise RuntimeError("Error: Command mal-constructed: %s" % command_str)

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