import sys
import re as regexp


def load_command_module(command_name):
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


def get_command_name_and_args_from_str(command_str):
	try:
		command_name, arguments = regexp.match(
			r'^([a-zA-Z0-9_]+)\s?((?:(?:[a-zA-Z0-9_]=)?[a-zA-Z0-9\s,\.\-\(\)+]+\|?)*)$', command_str
		).groups()
	except(TypeError, ValueError):
		print(
			regexp.match(
				r'^([a-zA-Z0-9_]+)\s?((?:(?:[a-zA-Z0-9_]=)?[a-zA-Z0-9\s,\.\-\(\)+]+\|?)*)$', command_str
			).groups()
		)
		raise RuntimeError("Error: Command mal-constructed")

	arguments = arguments.split("|")
	kwd_args = []
	pos_args = []

	for arg in arguments:
		# Assume the argument is a keyword-value pair
		try:
			kwd_args.append(tuple(arg.split("=")))
		except ValueError:
			# The argument is positional
			pos_args.append(arg)

	return command_name, tuple(pos_args), dict(kwd_args)