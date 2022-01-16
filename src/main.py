from utils.commands_utils import *

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


if __name__ == '__main__':
	print("# Options #")
	print("(N)ew | (O)pen | (S)ave | (L)ist | (A)dd | (D)elete | (E)xport | (H)elp | (Ex)it")
	print("#")
	abort = False

	while True:
		try:
			command, args, kwargs = get_command_name_and_args_from_str(input("Your choice:"))
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
			# The loop ended and the command was not found in the commands table
			print("Error: Unsupported command")

		if abort is True:
			break
