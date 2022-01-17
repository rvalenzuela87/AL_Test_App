import os
import sys
import re as regexp
import json


def get_conf():
	config_dir_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "config", "config.json")

	with open(config_dir_path, 'r') as fh:
		config = json.JSONDecoder().decode(fh.read())

	try:
		return config
	except(ValueError, RuntimeError):
		raise RuntimeError("Unable to read config file")


def get_serial_types():
	try:
		return get_conf()["serial_types"]
	except KeyError:
		raise RuntimeError("Unable get the supported serialization types from the config file (config.json)")


def get_serializers_dir(abs=False):
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


def get_save_directory(abs=False):
	try:
		dir = get_conf()["save_dir"]
	except KeyError:
		raise RuntimeError("Unable to get the serializers directory from the configuration file config.json")

	if not abs:
		return dir
	else:
		return os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), dir)


def get_default_directory(abs=False):
	return get_save_directory(abs=abs)