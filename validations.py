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
			"Value \"%s\" doesn't comply with the expected address format. Ex. \"98 Mulholland Drv.\""
		)
	else:
		return True


def validate_phone(phone):
	try:
		assert regexp.fullmatch("^[0-9]+", phone)
	except AssertionError:
		return False
	else:
		return True


def validate_city(city):
	try:
		assert regexp.fullmatch("^[a-zA-Z]+[,]?([a-zA-Z\s])?", city)
	except AssertionError:
		return False
	else:
		return True
