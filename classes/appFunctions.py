def hexToTuple(hexStr):
	"""
	берет строку в hex формате(цвет)
	и возвращает кортеж из 3-х чисел"""
	return (int(hexStr[0:2], 16), int(hexStr[2:4], 16), int(hexStr[4:6], 16))
