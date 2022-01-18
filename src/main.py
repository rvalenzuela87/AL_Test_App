import sys
import os

import utils.config_utils as config_utils
import utils.commands_utils as commands_utils
from records_manager import RecordsManager as RecordsManager


def start():
	commands_names = ["new", "open", "exit"]
	commands_short_names = ["n", "o", "ex"]
	start_menu = " | ".join("%s (%s)" % (ln.capitalize(), sn) for ln, sn in zip(commands_names, commands_short_names))

	print("[i] Welcome. Please choose one of the following options to start:\n")
	print(start_menu)
	choice = input("\n>>:")

	while choice.lower() not in commands_names and choice.lower() not in commands_short_names:
		print("[E] Option \'{}\' is not supported. Please, choose one of the following options to start:\n".format(choice))
		print(start_menu)
		choice = input("\n>>:")

	if choice.lower() not in ["exit", "ex"]:
		# The user chose an option other than exit the application. Therefore, start the application's main loop
		print("\n")
		main_loop()

def main_loop():
	# The singleton records manager was supposed to be set during the main part of this script and may or may not
	# hold values, already. This depends on whether the script was called with a file name as argument or not
	rec_man = RecordsManager()

	commands_names, commands_short_names = commands_utils.get_commands_names()

	# Add new entries for the exit option
	commands_names.append("exit")
	commands_short_names.append("ex")

	command_mods = dict.fromkeys(commands_names)
	main_menu = " | ".join("%s (%s)" % (ln.capitalize(), sn) for ln, sn in zip(commands_names, commands_short_names))
	choice = ""

	while True:
		print(main_menu)
		choice = input("\n>>:")

		# Try to extract the command's name and arguments from the user input
		try:
			cmd_name, cmd_args, cmd_kwargs = commands_utils.get_command_name_and_args_from_str(choice)
		except RuntimeError as exc:
			# The command's name and arguments couldn't be extracted from the user input string. Therefore, print the
			# error and go back to the beginning of the loop
			print("[E] {}\n".format(exc))
			continue

		# The command's name and arguments were successfully extracted from the user input. Now, make sure the
		# command's name corresponds to an actual supported command in the application
		if cmd_name not in commands_names:
			# Look for the command's name in the list of commands short names. If found, replace the value
			# input by the user
			try:
				cmd_name = commands_names[commands_short_names.index(cmd_name)]
			except ValueError:
				# The command's name is not in either list. This means the command is not supported. Therefore,
				# print the error and go back to the beginning of the loop
				print(
					"[i] Unsupported option \'{}\'. Please choose one of options from the main "
					"menu\n".format(choice)
				)
				continue

		# The command name is a supported command
		print("\n[i] Executing \'{}\' with args {} and kwargs {}\n".format(cmd_name, cmd_args, cmd_kwargs))

		# If the user chose to exit the application, then break the endless loop
		if cmd_name == "exit":
			print("[i] Goodbye!...\n")
			break

		try:
			command_mods[cmd_name].__getattribute__(command_mods[cmd_name].CLASS_NAME)(
				rec_man, *cmd_args, **cmd_kwargs
			)
		except AttributeError:
			# The command module has not been stored yet. Therefore, initialize and add it to the list
			try:
				command_mods[cmd_name] = commands_utils.load_command_module(cmd_name)
			except RuntimeError as exc:
				print("[E] {}\n".format(exc))
				continue

			try:
				command_mods[cmd_name].__getattribute__(command_mods[cmd_name].CLASS_NAME)(
					rec_man, *cmd_args, **cmd_kwargs
				)
			except(RuntimeError, ValueError, TypeError) as exc:
				print("\n[E] {}\n".format(exc))
		except(RuntimeError, ValueError, TypeError) as exc:
			print("\n[E] {}\n".format(exc))


if __name__ == '__main__':
	# Load configuration
	config_utils.reload_config()

	print("\n")
	print("".join(["#" for __ in range(50)]))
	print("#")
	print("# Personal Records Database")
	print("#")
	print("".join(["#" for __ in range(50)]))
	print("\n")

	rec_man = RecordsManager()

	try:
		filename = sys.argv[1]

		assert len(filename) > 0
	except(AssertionError, IndexError):
		# No argument file was submitted. Therefore, initiate a completely new list
		print("[i] Initiating with a new list\n")
	else:
		print("[i] Working file: {}\n".format(filename))
		rec_man.load_from_file(filename)

	main_loop()