import re as regexp


def validate_name(name):
	try:
		assert regexp.fullmatch("^[a-zA-Z'\-\s]+$", name)
	except AssertionError:
		return False
	else:
		return True


def validate_address(address):
	try:
		assert regexp.fullmatch("^[0-9]+(\s[a-zA-Z'.\-])+$", address)
	except AssertionError:
		raise AssertionError(
			"Value \"{}\" doesn't comply with the expected address format. Ex. \"98 Mulholland Drv.\"".format(address)
		)
	else:
		return True


def validate_phone(phone):
	try:
		assert regexp.fullmatch("^[0-9]+$", phone)
	except AssertionError:
		raise AssertionError(
			"Value \"{}\" doesn't comply with the expected phone format. Ex. \"2-13-56-80\"".format(phone)
		)
	else:
		return True


def validate_city(city):
	try:
		assert regexp.fullmatch("^[a-zA-Z]+[,]?([a-zA-Z\s])?$", city)
	except AssertionError:
		raise AssertionError(
			"Value \"{}\" doesn't comply with the expected city format. Ex. \"Vancouver, BC\"".format(city)
		)
	else:
		return True
