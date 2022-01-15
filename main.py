import msvcrt
import sys
import os
import re as regexp

commands_table = [
	("n", "new"),
	("o", "open"),
	("s", "save"),
	("l", "list"),
	("a", "add"),
	("d", "delete"),
	("e", "export"),
	("h", "help"),
	("ex", "exit")
]


def cmnd_name_args_from_str(command_str):
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

	for arg in arguments:
		try:
			kwd, value = arg.split("=")
		except ValueError:
			break
		else:
			kwd_args.append((kwd, value))
	else:
		# All parameters are keyword-value pairs. Therefore, the function can end safely
		return command_name, tuple(), dict(kwd_args)

	# The for loop ended early. Therefore, not all arguments are key-value pairs. Make sure no key-value argument
	try:
		assert len(kwd_args) == 0
	except AssertionError:
		# The parameters received are a mixed of positional and key-value arguments. Only one
		# type is supported at a time. Therefore, raise an exception
		raise RuntimeError("Mixed values received")
	else:
		# All arguments received are positional arguments for the command.
		return command_name, tuple(arguments), {}


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


if __name__ == '__main__':
	print("# Options #")
	print("(N)ew | (O)pen | (S)ave | (L)ist | (A)dd | (D)elete | (E)xport | (H)elp | (Ex)it")
	print("#")
	abort = False

	while True:
		try:
			command, args, kwargs = cmnd_name_args_from_str(input("Your choice:"))
		except RuntimeError as exc:
			print("Error >> {}".format(exc))
			continue

		for sn, ln in commands_table:
			if command == sn or command == ln:
				if command == "ex" or command == "exit":
					abort = True
				else:
					try:
						command_module = load_command_module("_".join([ln, "command"]))
					except ImportError as exc:
						print("Error: {}".format(exc))
					else:
						command_module.__getattribute__(command_module.CLASS_NAME)(None, *args, **kwargs)
				break
		else:
			# The loop ended
			print("Error: Unsupported command")

		if abort is True:
			break
