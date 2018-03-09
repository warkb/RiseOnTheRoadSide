from collections import Iterable

class GVector():
	"""
	двумерный целочисленный вектор
	"""
	def __init__(self, x=0, y=0):
		if isinstance(x, Iterable):
			self.x, self.y = x
			return
		self.x = x
		self.y = y

	def __str__(self):
		"""переопределение функции print"""
		return 'Эт короче экзампляр GVector c координатами ({0},{1})'.format(self.x, self.y)

	def __add__(self, v2):
		"""переопределение оператора '+'"""
		return GVector(self.x + v2.x, self.y + v2.y)

	def __sub__(self, v2):
		"""Разность двух векторов"""
		return GVector(self.x-v2.x, self.y-v2.y)

	def __mul__(self, m):
		"""Умножение вектора на скаляр"""
		return GVector(self.x * m, self.y * m)

	def __getitem__(self, key):
		if key == 0:
			return self.x
		elif key == 1:
			return self.y
		else:
			raise BaseException('Нету больше ничего')

	def __iter__(self):
		return iter((self.x, self.y))

	def __setitem__(self, key, value):
		if key == 0:
			self.x = value
		elif key == 1:
			self.y = value
		else:
			raise BaseException('Нету больше ничего')

	def __len__(self):
		return 2

	def get(self):
		"""возвращает кортеж с координатами вектора в интовом виде"""
		return (round(self.x), round(self.y))

	def inRectangle(self, v1, v2):
		"""
		Возвращает True или False в зависимости от того,
		находятся ли координаты в прямоугольнике, ограниченном
		векторами v1 и 	v2
		"""
		if not v1.x < self.x < v2.x:
			return False
		if not v1.y < self.y < v2.y:
			return False
		return True
		