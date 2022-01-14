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


def extract_command_data_from_str(command_str):
	split_command_str = command_str.split()
	command_name = split_command_str[0]
	parameters = split_command_str[1:]
	args_keys = []

	for param in parameters:
		try:
			kwd, value = param.split("=")
		except ValueError:
			break
		else:
			args_keys.append((kwd, value))
	else:
		# All parameters are keyword-value pairs. Therefore, the function can end safely
		return command_name, tuple(), tuple(args_keys)

	# The for loop ended early. Therefore, not all arguments are key-value pairs. Make sure no key-value argument
	try:
		assert len(args_keys) == 0
	except AssertionError:
		# The parameters received are a mixed of positional and key-value arguments. Only one
		# type is supported at a time. Therefore, raise an exception
		raise RuntimeError("Mixed values received")
	else:
		# All arguments received are positional arguments for the command.
		return command_name, tuple(parameters), tuple()


def load_command_module(command_name):
	sys_path_changed = False

	# Assume the command module is already in memory
	for k in sys.modules.keys():
		if k.split(".").pop() == command_name:
			return sys.modules[k]

	# Try to import the module

	try:
		exec("from commands import %s" % command_name)
	except ImportError:
		raise ImportError("Unable to find the \"%s\" command module" % command_name)

	for k in sys.modules.keys():
		if k.split(".").pop() == command_name and type(sys.modules[k]).__name__ == "module":
			return sys.modules[k]


if __name__ == '__main__':
	print("# Options #")
	print("(N)ew | (O)pen | (S)ave | (L)ist | (A)dd | (D)elete | (E)xport | (H)elp | (Ex)it")
	print("#")
	abort = False

	while True:
		command = input("Your choice:")

		for sn, ln in commands_table:
			if command == sn or command == ln:
				print("Executing (%s|%s) command" % (sn, ln))

				if command == "ex" or command == "exit":
					abort = True
				else:
					try:
						command_module = load_command_module("_".join([ln, "command"]))
					except ImportError as exc:
						print("Error: {}".format(exc))
					else:
						print(">> Module {} imported correctly".format(command_module))
						command_module.__getattribute__(command_module.CLASS_NAME)(None)
				break
		else:
			print("Error: Unsupported command")

		if abort is True:
			break
