import os
import sys
import re as regexp

ARGS_SEP = "|"


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
			r'^([a-zA-Z0-9_]+)\s?((?:(?:[a-zA-Z0-9_]+=)?\"[a-zA-Z0-9\s,\.\-\(\)+*]+\"\|?)*)$', command_str
		).groups()
	except(AttributeError, TypeError, ValueError):
		raise RuntimeError("Error: Command mal-constructed: %s" % command_str)

	arguments = arguments.split("|")
	kwd_pattern = regexp.compile(r'^([a-zA-Z0-9_]+)=\"([a-zA-Z0-9\s,\.\-\(\)+*]+)\"$')
	pos_pattern = regexp.compile(r'^\"([a-zA-Z0-9\s,\.\-\(\)+*]+)\"$')
	kwd_args = []
	pos_args = []

	for arg in arguments:
		# Assume the argument is a keyword-value pair
		try:
			kwd_args.append(kwd_pattern.match(arg).groups())
		except AttributeError:
			# Assume the argument is positional
			try:
				pos_args.append(pos_pattern.match(arg).groups()[0])
			except AttributeError:
				# The argument is not a valid argument or is an empty string
				continue

	if len(kwd_args) > 0:
		kwd_args_dict = dict(kwd_args)
	else:
		kwd_args_dict = {}

	print("Positional arguments: {}".format(pos_args))
	print("Keyword arguments: {}".format(kwd_args_dict))

	return command_name, tuple(pos_args), kwd_args_dict


def build_command_str(command_name, *args, **kwargs):
	try:
		pos_args_str = ARGS_SEP.join(args)
	except(ValueError, TypeError):
		pos_args_str = ""

	try:
		kwd_keys = kwargs.keys()
	except AttributeError:
		kwd_args_str = ""
	else:
		kwd_args_str = ARGS_SEP.join("=".join(pair) for pair in zip(kwd_keys, (kwargs[k] for k in kwd_keys)))

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