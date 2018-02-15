from random import random

def generateRandomInJaggedArea(a, b, c, d):
	"""Генерирует рандомное число в области [a, b] U [c, d]"""
	randomNum = random() * ((b - a) + (d - c)) + a
	if randomNum > b and b != c:
		randomNum += (c - b)
	return randomNum

def hexToTuple(hexStr):
	"""
	берет строку в hex формате(цвет)
	и возвращает кортеж из 3-х чисел"""
	return (int(hexStr[0:2], 16), int(hexStr[2:4], 16), int(hexStr[4:6], 16))
