import sys

import AL_Test_App.src.utils.config_utils as config_utils
from AL_Test_App.src.commands.utils import commands_utils
from AL_Test_App.src.commands.command_builder import CommandBuilder
from AL_Test_App.src.records_manager import RecordsManager as RecordsManager


def build_main_menu():
	commands_names, commands_short_names = commands_utils.get_commands_names()
	menu_order = config_utils.get_menu_options_order()

	def _order_options_list(names):
		try:
			order = menu_order.index(names[0])
		except(IndexError, ValueError, AssertionError):
			return len(menu_order)
		else:
			return order

	menu_options_names = list(zip(commands_names, commands_short_names))
	menu_options_names.sort(key=_order_options_list)

	menu_options_names.append(("exit", "ex"))

	main_menu = " | ".join("%s (%s)" % (ln.capitalize(), sn) for ln, sn in menu_options_names)

	return main_menu

def main_loop():
	# The singleton records manager was supposed to be set during the main part of this script and may or may not
	# hold values, already. This depends on whether the script was called with a file name as argument or not
	rec_man = RecordsManager()
	cmds_builder = CommandBuilder()
	commands_names, commands_short_names = commands_utils.get_commands_names()
	commands_names.append("exit")
	commands_short_names.append("ex")
	main_menu = build_main_menu()
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

		# If the user chose to exit the application, then break the endless loop
		if cmd_name == "exit":
			print("[i] Goodbye!...\n")
			break

		# If the user chose a supported command different from 'exit' then try to instantiate and execute it
		try:
			cmds_builder.get_command(cmd_name, rec_man, *cmd_args, **cmd_kwargs).execute()
		except(RuntimeError, ValueError, TypeError) as exc:
			print("\n[E]{}\n".format(exc))


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