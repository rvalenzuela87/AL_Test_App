import os
import sys
import json
import re as regexp


def get_conf():
	"""
	Returns the app's configuration values stored in the configuration file config.json

	:return: A dictionary containing the app's configuration
	:rtype: dict
	"""

	config_dir_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "config", "config.json")

	with open(config_dir_path, 'r') as fh:
		config = json.JSONDecoder().decode(fh.read())

	try:
		return config
	except(ValueError, RuntimeError):
		raise RuntimeError("Unable to read config file")


def reload_config():
	"""
	Reloads the configuration values to memory

	:return: Returns nothing
	:rtype: None
	"""

	config = get_conf()
	app_base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

	os.environ["DEFAULT_SAVE_DIRECTORY"] = os.path.join(app_base_dir, config["default_save_dir"])
	os.environ["DEFAULT_EXPORT_DIRECTORY"] = os.path.join(app_base_dir, config["default_export_dir"])
	os.environ["SERIAL_TYPES"] = "|".join(config["serial_types"])
	os.environ["EXPORT_TYPES"] = "|".join(config["export_types"])


def get_serial_types():
	"""
	Returns the app's supported serialization types as stated in the configuration file config.json

	:return: List with the extensions supported by the app for serialization
	:rtype: list
	"""

	try:
		return os.environ["SERIAL_TYPES"].split("|")
	except KeyError:
		reload_config()

		try:
			return os.environ["SERIAL_TYPES"].split("|")
		except KeyError:
			raise RuntimeError("Unable get the supported serialization types from the config file (config.json)")


def get_export_types():
	"""
	Returns the app's supported export types as stated in the configuration file config.json

	:return: List with the extensions supported by the app for exporting data
	:rtype: list
	"""

	try:
		return os.environ["EXPORT_TYPES"].split("|")
	except KeyError:
		reload_config()

		try:
			return os.environ["EXPORT_TYPES"].split("|")
		except KeyError:
			raise RuntimeError("Unable get the supported export extensions from the config file (config.json)")


def get_serializers_dir(abs=False):
	"""
	Returns the app's 'serializers' package directory

	:param abs: Weather the function should return the package's absoulte path or not
	:type abs: bool
	:return: Path to the app's serializers package
	:rtype: str
	"""

	try:
		dir = get_conf()["serials_dir"]
	except KeyError:
		raise RuntimeError("Unable to get the serializers directory from the configuration file config.json")

	if not abs:
		return dir
	else:
		return os.path.join(os.path.dirname(os.path.dirname(__file__)), dir)


def get_serializer_module(serial_type):
	serial_mod_pattern = regexp.compile(r'^(?:.*)\.([a-zA-Z]+)_serial$')

	# Firts, look for the serializer module in memory
	for k in sys.modules.keys():
		try:
			assert serial_mod_pattern.match(k).groups()[0] == serial_type
		except AssertionError:
			print("Serial module: %s" % k)
		except(AttributeError, IndexError):
			# The key may not belong to a serialization module or, if it does, it isn't the correspondant one.
			# Therefore, move on to the next module in memory
			continue
		else:
			# The current key belongs to a serialization module and it corresponds to the type received as argument
			return sys.modules[k]

	# At this point, the correct module was not found in memory. Therefore, import the serializers package
	# and look for the module again
	import AL_Test_App.src.serializers

	for k in sys.modules.keys():
		try:
			assert serial_mod_pattern.match(k).groups()[0] == serial_type
		except AssertionError:
			print("Serial module: %s" % k)
		except(AttributeError, IndexError):
			# The key may not belong to a serialization module or, if it does, it isn't the correspondant one.
			# Therefore, move on to the next module in memory
			continue
		else:
			# The current key belongs to a serialization module and it corresponds to the type received as argument
			return sys.modules[k]
	else:
		raise RuntimeError("No serializer module found for type \'{}\'".format(serial_type))


def get_serializers():
	# Retrieve the serializers folder from the configuration file
	serializers_dir = get_serializers_dir(abs=True)
	serial_pattern = regexp.compile(r'^(.*)_serial\.py$')
	serializers_files = [n for n in os.listdir(get_serializers_dir(abs=True)) if serial_pattern.match(n)]
	serializer_mods = []

	# Assume a serializer exist for every serialization type stored in the configuration file
	for serial_type in get_serial_types():
		for file_name in serializers_files:
			try:
				assert serial_pattern.match(file_name).groups()[0] == serial_type
			except(AssertionError, AttributeError, IndexError):
				continue
			else:
				serializer_mods.append((file_name, serializers_dir))
				break
		else:
			# No file found for the current serialization type
			continue

	return serializer_mods


def get_exporters_names():
	try:
		return get_conf()["exporters"]
	except KeyError:
		raise RuntimeError("Unable get the app\'s exporters names from the config file (config.json)")


def get_exporter_module(extension):
	exporter_mod_pattern = regexp.compile(r'^(?:.*)\.([a-zA-Z]+)_exporter$')

	# Firts, look for the exporter module in memory
	for k in sys.modules.keys():
		try:
			assert exporter_mod_pattern.match(k).groups()[0] == extension
		except AssertionError:
			pass
		except(AttributeError, IndexError):
			# The key may not belong to an exporter module or, if it does, it isn't the correspondant one.
			# Therefore, move on to the next module in memory
			continue
		else:
			# The current key belongs to an exporter module and it corresponds to the type received as argument
			return sys.modules[k]

	# At this point, the correct module was not found in memory. Therefore, import the exporters package
	# and look for the module again
	import AL_Test_App.src.exporters

	for k in sys.modules.keys():
		try:
			assert exporter_mod_pattern.match(k).groups()[0] == extension
		except AssertionError:
			pass
		except(AttributeError, IndexError):
			# The key may not belong to an exporter module or, if it does, it isn't the correspondant one.
			# Therefore, move on to the next module in memory
			continue
		else:
			# The current key belongs to an exporter module and it corresponds to the type received as argument
			return sys.modules[k]
	else:
		raise RuntimeError("No exporter module found for type \'{}\'".format(extension))


def get_save_directory(abs=False):
	"""
	Returns the directory where the backup files are stored by default.

	:param abs: Controls whether the function should return the directory's absolute path or just its name
	:type abs: bool
	:return: The directory where the save (backup) files are stored by default
	:rtype: str
	"""
	try:
		save_dir = os.environ["DEFAULT_SAVE_DIRECTORY"]
	except KeyError:
		reload_config()

		try:
			save_dir = os.environ["DEFAULT_SAVE_DIRECTORY"]
		except KeyError:
			raise RuntimeError("Unable to get the default backup directory from the configuration file (config.json)")

	if not abs:
		return os.path.split(save_dir)[1]
	else:
		return save_dir


def get_default_directory(abs=False):
	"""
	Returns the directory where the report files are stored by default.

	:param abs: Controls whether the function should return the directory's absolute path or just its name
	:type abs: bool
	:return: The directory where the report (export) files are stored by default
	:rtype: str
	"""

	try:
		export_dir = os.environ["DEFAULT_EXPORT_DIRECTORY"]
	except KeyError:
		reload_config()

		try:
			export_dir = os.environ["DEFAULT_EXPORT_DIRECTORY"]
		except KeyError:
			raise RuntimeError("Unable to get the default backup directory from the configuration file (config.json)")

	if not abs:
		return os.path.split(export_dir)[1]
	else:
		return export_dir


def get_menu_options_order():
	"""
	Returns the menu's option order as stored in the configuration file config.json

	:return: List with the commands' names in the order that should appear in the app's main menu
	:rtype: list
	"""

	return get_conf()["menu_order"]