from sys import argv

from utils import commands_utils


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
	commands_names, commands_short_names = commands_utils.get_commands_names()
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
		else:
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
			print("\n[i] Executing \'{}\'\n".format(choice))

			# If the user chose to exit the application, then break the endless loop
			if cmd_name == "exit":
				print("[i] Goodbye!...\n")
				break

if __name__ == '__main__':
	print("\n")
	print("".join(["#" for __ in range(50)]))
	print("#")
	print("# Personal Records Database")
	print("#")
	print("".join(["#" for __ in range(50)]))
	print("\n")

	try:
		file_name = argv[1]

		assert len(file_name) > 0
	except(AssertionError, IndexError):
		# No argument file was submitted. Therefore, initiate a completely new list
		print("[i] Initiating with a new list\n")
	else:
		print("[i] Working file: {}\n".format(file_name))

	main_loop()